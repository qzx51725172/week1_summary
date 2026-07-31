import cv2
import numpy as np

# 全局配置常量
# 视频文件路径
video_path_1 = r"C:\Users\asus\git-test\week2-data-project\data\1.mp4"
video_path_2 = r"C:\Users\asus\git-test\week2-data-project\data\2.mp4"
# 截图保存路径
screenshot_save_path = r"C:\Users\asus\git-test\week2-data-project\data\combine_screenshot.jpg"
# 画面限制最大高度
max_display_height = 800
# 帧刷新等待毫秒数
frame_wait_delay = 25
# 窗口名称
window_name = "Dual Video"

# 读取函数read_frame
def read_frame(vc, target_width = None, target_height = None):
    """
    读取单路视频帧，支持统一缩放尺寸
    vc: VideoCapture 视频捕获对象
    target_width: 目标宽度，None则不缩放
    target_height: 目标高度，None则不缩放
    return: (读取成功标记, 处理后图像帧)
    """
    ret, frame = vc.read()
    if not ret:
        return False, None
    # 指定尺寸则统一缩放
    if target_width is not None and target_height is not None:
        frame = cv2.resize(frame, (target_width, target_height))
    return True, frame

# 主程序入口
def main():
    # 初始化两路视频捕获器
    cap1 = cv2.VideoCapture(video_path_1)
    cap2 = cv2.VideoCapture(video_path_2)

    # 校验视频是否打开成功
    if not cap1.isOpened() or not cap2.isOpened():
        print("至少一路视频打开失败，请检查文件路径")
        # 打开失败也要释放资源，避免泄漏
        cap1.release()
        cap2.release()
        return

    print("双路视频加载成功，按 q 退出，按空格键保存当前拼接画面")

    while True:
        # 读取第一路，获取基准宽高
        ret1, frame1 = read_frame(cap1)
        if not ret1:
            print("某一路视频播放结束")
            break
        h, w = frame1.shape[:2]

        # 读取第二路，统一缩放至和第一路相同尺寸
        ret2, frame2 = read_frame(cap2, w, h)
        if not ret2:
            print("某一路视频播放结束")
            break

        # 纵向上下拼接两路画面
        combine_frame = np.vstack([frame1, frame2])

        # 等比例缩放，限制画面最大高度，防止超出显示器可视范围
        total_h, total_w = combine_frame.shape[:2]
        if total_h > max_display_height:
            scale = max_display_height / total_h
            new_w = int(total_w * scale)
            new_h = int(total_h * scale)
            combine_frame = cv2.resize(combine_frame, (new_w, new_h))

        # 窗口展示拼接画面
        cv2.imshow(window_name, combine_frame)
        key = cv2.waitKey(frame_wait_delay) & 0xFF

        # q键退出程序
        if key == ord("q"):
            break
        # 空格保存截图
        elif key == ord(' '):
            cv2.imwrite(screenshot_save_path, combine_frame)
            print("截图保存成功，文件名为 combine_screenshot.jpg")

    # 循环结束统一释放所有资源
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

# Python标准程序执行入口
if __name__ == "__main__":
    main()