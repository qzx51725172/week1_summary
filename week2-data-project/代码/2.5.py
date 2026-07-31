import cv2
import numpy as np

# 全局统一参数
video_path_1 = r"C:\Users\asus\git-test\week2-data-project\data\1.mp4"
video_path_2 = r"C:\Users\asus\git-test\week2-data-project\data\2.mp4"
screenshot_save_path = r"C:\Users\asus\git-test\week2-data-project\data\combine_screenshot.jpg"
canny_low = 50
canny_high = 150
max_h = 800
text_x, text_y = 20, 40
status_text_offset = 120
font = cv2.FONT_HERSHEY_SIMPLEX
text_color_green = (0, 255, 0)
text_color_red = (0, 0, 255)
wait_delay = 25
diff_threshold = 8

# ===================== 三个核心函数 =====================
def read_frame(vc, target_w=None, target_h=None):
    """读取单路视频帧，支持统一缩放尺寸"""
    ret, frame = vc.read()
    if not ret:
        return False, None
    if target_w is not None and target_h is not None:
        frame = cv2.resize(frame, (target_w, target_h))
    return ret, frame


def draw_overlay(img, cam_name, frame_id, width, state):
    """统一绘制左上角摄像头帧号、右上角动静状态文字"""
    # 左上：Cam编号+帧号
    cv2.putText(img, f"{cam_name} Frame:{frame_id}", (text_x, text_y), font, 1, text_color_green, 2)
    # 右上：Active/Quiet状态
    cv2.putText(img, state, (width - status_text_offset, text_y), font, 1, text_color_red, 2)
    return img


def detect_activity(current_frame, prev_frame, threshold):
    """简易帧差活动检测，返回状态字符串"""
    if prev_frame is None:
        return "Quiet", False
    diff_img = cv2.absdiff(current_frame, prev_frame)
    mean_diff = np.mean(diff_img)
    current_state = "Active" if mean_diff > threshold else "Quiet"
    return current_state, True

# ===================== 主程序逻辑（完全保留原版流程与注释） =====================
def main():
    cap1 = cv2.VideoCapture(video_path_1)
    cap2 = cv2.VideoCapture(video_path_2)

    # 基础变量
    frame_num = 0
    # 【2.5新增】存储两路前一帧
    prev_frame1 = None
    prev_frame2 = None
    # 【2.5新增】记录上一轮状态，用来判断是否切换
    state1_old = None
    state2_old = None

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

            # 原有：边缘检测图像处理
            gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            edge1 = cv2.Canny(gray1, canny_low, canny_high)
            frame1 = cv2.cvtColor(edge1, cv2.COLOR_GRAY2BGR)

            gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            edge2 = cv2.Canny(gray2, canny_low, canny_high)
            frame2 = cv2.cvtColor(edge2, cv2.COLOR_GRAY2BGR)

            # 2.5新增 活动检测开始
            state1, _ = detect_activity(frame1, prev_frame1, diff_threshold)
            state2, _ = detect_activity(frame2, prev_frame2, diff_threshold)

            # Cam1状态切换日志打印
            if prev_frame1 is not None and state1_old is not None and state1 != state1_old:
                print(f"【帧{frame_num}】Cam1 状态切换：{state1_old} → {state1}")
            # Cam2状态切换日志打印
            if prev_frame2 is not None and state2_old is not None and state2 != state2_old:
                print(f"【帧{frame_num}】Cam2 状态切换：{state2_old} → {state2}")

            # 绘制左上角帧号+右上角状态文字
            frame1 = draw_overlay(frame1, "Cam1", frame_num, w, state1)
            frame2 = draw_overlay(frame2, "Cam2", frame_num, w, state2)

            # 更新前帧、旧状态
            prev_frame1 = frame1.copy()
            prev_frame2 = frame2.copy()
            state1_old = state1
            state2_old = state2
            # 2.5新增结束

            # 原有拼接、适配屏幕全部保留
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

            frame_num = frame_num + 1

        cap1.release()
        cap2.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()