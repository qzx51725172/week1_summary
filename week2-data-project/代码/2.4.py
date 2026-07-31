import cv2
import numpy as np

# 全局固定参数
video_path_1 = r"C:\Users\asus\git-test\week2-data-project\data\1.mp4"
video_path_2 = r"C:\Users\asus\git-test\week2-data-project\data\2.mp4"
screenshot_save_path = r"C:\Users\asus\git-test\week2-data-project\data\combine_screenshot.jpg"
canny_low = 50
canny_high = 150
max_h = 800
text_x = 20
text_y = 40
font = cv2.FONT_HERSHEY_SIMPLEX
text_color = (0, 255, 0)
wait_delay = 25

# 读取单路帧+尺寸适配
def read_frame(vc, target_w=None, target_h=None):
    ret, frame = vc.read()
    if not ret:
        return False, None
    if target_w is not None and target_h is not None:
        frame = cv2.resize(frame, (target_w, target_h))
    return ret, frame

# 统一绘制左上角cam+帧号文字
def draw_overlay(img, cam_name, frame_id):
    cv2.putText(img, f"{cam_name} Frame:{frame_id}", (text_x, text_y), font, 1, text_color, 2)
    return img

# 帧差活动检测
def detect_activity(cur_frame, prev_frame, threshold):
    if prev_frame is None:
        return "Quiet"
    diff_img = cv2.absdiff(cur_frame, prev_frame)
    mean_diff = np.mean(diff_img)
    return "Active" if mean_diff > threshold else "Quiet"
# 主体程序
def main():
    cap1 = cv2.VideoCapture(video_path_1)
    cap2 = cv2.VideoCapture(video_path_2)
    # 定义全局帧计数器
    frame_num = 0

    if not cap1.isOpened() or not cap2.isOpened():
        print("至少一路视频打开失败，请检查文件路径")
        cap1.release()
        cap2.release()
        return
    else:
        print("双路视频加载成功，按 q 退出，按空格键保存当前拼接画面")
        while True:
            ret1, frame1 = read_frame(cap1)
            if not ret1:
                print("某一路视频播放结束")
                break
            h, w = frame1.shape[:2]
            ret2, frame2 = read_frame(cap2, w, h)
            if not ret2:
                print("某一路视频播放结束")
                break

            # 新增部分：图像处理
            # 边缘检测Canny
            gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            edge1 = cv2.Canny(gray1, canny_low, canny_high)
            frame1 = cv2.cvtColor(edge1, cv2.COLOR_GRAY2BGR)

            gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            edge2 = cv2.Canny(gray2, canny_low, canny_high)
            frame2 = cv2.cvtColor(edge2, cv2.COLOR_GRAY2BGR)

            # 新增部分：文字叠加putText
            frame1 = draw_overlay(frame1, "Cam1", frame_num)
            frame2 = draw_overlay(frame2, "Cam2", frame_num)

            # 拼接、缩放
            combine_frame = np.vstack([frame1, frame2])
            total_h, total_w = combine_frame.shape[:2]
            if total_h > max_h:
                scale = max_h / total_h
                new_w = int(total_w * scale)
                new_h = int(total_h * scale)
                combine_frame = cv2.resize(combine_frame, (new_w, new_h))

            cv2.imshow("Dual Video", combine_frame)
            key = cv2.waitKey(wait_delay) & 0xFF
            if key == ord("q"):
                break
            elif key == ord(' '):
                cv2.imwrite(screenshot_save_path, combine_frame)
                print("截图保存成功，文件名为 combine_screenshot.jpg")

            # 每循环一次，帧号+1
            frame_num = frame_num + 1

        cap1.release()
        cap2.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()