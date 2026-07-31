import cv2  #导入 OpenCV 计算机视觉库，用于图像读写、绘图、图像处理。
import numpy as np #导入数值计算库，OpenCV 的图像本质就是NumPy 多维数组
# 全局常量配置
# 画布尺寸
CANVAS_HEIGHT = 200
CANVAS_WIDTH = 200
CHANNELS = 3

# 圆形参数
CIRCLE_CENTER = (100, 100)
CIRCLE_RADIUS = 50
CIRCLE_COLOR = (0, 0, 255)  # BGR格式：红色
CIRCLE_THICKNESS = 2

# 保存路径
SAVE_IMG_PATH = r"C:\Users\asus\git-test\week2-data-project\data\imgtest_result.png"

# 快速验证 OpenCV 是否正常导入，用于环境测试。
print("OpenCV 版本：", cv2.__version__)
print("Python + OpenCV 环境验证成功")

# 基础绘图功能测试
# 创建全0数组黑色画布：高、宽、3彩色通道，像素0~255，uint8图像标准类型
img = np.zeros((CANVAS_HEIGHT, CANVAS_WIDTH, CHANNELS), dtype=np.uint8)
# cv2.circle(图像, 圆心坐标, 半径, 颜色, 线条粗细)
# (0, 0, 255)：OpenCV 默认色彩顺序 BGR → (蓝，绿，红)，所以(0,0,255)= 红色
# 2：轮廓线条宽度；如果设为-1代表填充圆形
cv2.circle(img, CIRCLE_CENTER, CIRCLE_RADIUS, CIRCLE_COLOR, CIRCLE_THICKNESS)

# 自动生成图片保存到本地
cv2.imwrite(SAVE_IMG_PATH, img)
print("图像已保存为 imgtest_result.png")