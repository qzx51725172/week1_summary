import cv2

# 全局配置参数
video_path = r"C:\Users\asus\git-test\week2-data-project\data\1.mp4"
window_name = "Video Player"
wait_delay = 25
exit_char = 'q'

# 封装read_frame读取函数
def read_frame(vc):
    """
    读取单路视频帧，封装read逻辑，供双路视频复用
    参数:
        vc: VideoCapture视频捕获对象
    返回:
        ret: 布尔值，True读到有效帧，False读到视频末尾/读取失败
        frame: numpy数组，当前帧图像
    """
    # 2. 循环逐帧读取,一次读取一帧画面，返回两个值：
    ret, frame = vc.read()
    return ret, frame

# 主程序入口
def main():
    # 1. 创建视频捕获对象
    cap = cv2.VideoCapture(video_path)
    #实例化视频捕获器，底层打开视频流。
    #参数两种形式：
    #传入字符串路径：读取本地视频文件；
    #传入数字 0 / 1：调用电脑摄像头（实时流）。

    # 检查视频是否成功打开
    if not cap.isOpened():
        print("视频打开失败！检查文件路径是否正常")
        cap.release()
        cv2.destroyAllWindows()
        return
    print("视频读取成功，按 q 键退出播放")

    while True:
        ret, frame = read_frame(cap)

        # ret=False 代表视频读取完毕，跳出循环
        if not ret:
            print("视频播放结束")
            break

        # 3. 显示当前帧
        cv2.imshow(window_name, frame)
        #cv2.imshow(窗口名, frame)

        # 4. 等待按键，按 q 退出
        key = cv2.waitKey(wait_delay) & 0xFF
        if key == ord(exit_char):  #获取字符q对应的 ASCII 编码。
            break

    #cv2.waitKey(delay)  delay：等待毫秒时长；25 ≈ 40 帧（1000/25=40fps），waitKey 延时不自动同步视频原生帧率，只是人为控制画面刷新间隔
    #作用两件事：
    #刷新图像窗口（imshow 必须配合 waitKey 才会正常显示画面！缺少会黑屏不显示）
    #监听键盘输入
    #如果等待时间内没有按键，返回 -1

    # 5. 释放资源、销毁窗口
    cap.release() #关闭视频文件，释放底层解码器、文件句柄。
    cv2.destroyAllWindows() #关闭所有 OpenCV 创建的图像窗口，释放 GUI 资源。

if __name__ == "__main__":
    main()