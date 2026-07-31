# 双路视频帧差运动检测程序
## 项目简介
思路：
基于OpenCV，完成双视频同步读取————尺寸对齐、图像上下拼接自适应缩放、按键交互（空格截图、q退出）————Canny边缘提取————帧差法运动检测并更新状态日志、画面文字标注。
## 一、环境依赖安装
```bash
pip install opencv-python numpy -i https://pypi.tuna.tsinghua.edu.cn/simple
```
目录结构

week2-data-project
├── data
│   ├── 1.mp4              # 一号视频源
│   ├── 2.mp4              # 二号视频源
│   └── combine_screenshot.jpg  # 空格截图保存文件
├── img                    # 运行截图存放目录
├── README.md              # 本文档
└── weekly_log_W2.md       # 第二周日志
## 二、全局参数说明
所有可调参数统一放在代码最开头，修改效果不用改动业务逻辑。
| 变量名 | 含义说明 | 调节作用 |
| ---- | ---- | ---- |
| video_path_1 | 第一个视频文件路径 | 修改路径更换一号视频|
| video_path_2 | 第二个视频文件路径 | 修改路径更换二号视频 |
| screenshot_save_path | 截图保存路径 | 按下空格键，拼接画面保存至该地址 |
| canny_low | Canny 边缘检测低阈值 | 数值越小，细碎边缘越多；数值越大仅保留粗线条轮廓 |
| canny_high | Canny 边缘检测高阈值 | 和低阈值配合筛选有效边缘轮廓 |
| max_h | 拼接画面最大高度上限 | 画面总高度超出该值自动等比例缩小，避免窗口过大 |
| text_x, text_y | 左上角文字坐标 | 调整Cam编号、帧数文字的横竖位置 |
| status_text_offset | 右上角状态文字横向偏移 | 控制Active/Quiet距离画面右边缘远近 |
| font | OpenCV 内置文字字体 | 固定配置，一般无需改动 |
| text_color_green | 左上文字BGR颜色 | BGR格式绿色，用于标注摄像头名称、帧数 |
| text_color_red | 右上状态文字BGR颜色 | BGR格式红色，用于标注运动状态 |
| wait_delay | 帧间隔等待毫秒数 | 数值越大视频播放速度越慢、画面刷新越慢，常规取值25~30 |
| diff_threshold | 帧差运动判定阈值 | 差值均值大于阈值判定为Active；阈值越高检测越迟钝，越低越灵敏 |

路径存为相对路径：
```python
video_path_1 = r"./data/1.mp4"
video_path_2 = r"./data/2.mp4"
screenshot_save_path = r"./data/combine_screenshot.jpg"
```

## 三、核心函数详细说明
1. read_frame(vc, target_w=None, target_h=None)

读取单路视频帧，支持将画面强制缩放至指定宽高，用来统一两路视频尺寸。
  入参：
vc：cv2.VideoCapture视频读取对象
target_w、target_h：目标宽高；不传则保留原图尺寸
  返回值：
(ret, frame)
ret：布尔值，True 正常读帧，False 视频结束/读取失败
frame：图像数组，读取失败返回None
2. draw_overlay(img, cam_name, frame_id, width, state)

统一绘制两处文字，避免重复编写 putText 代码。
  入参：
img：待绘制画面
cam_name：摄像头标识 Cam1/Cam2
frame_id：当前帧数
width：画面整体宽度，用来定位右上角文字
state：运动状态字符串，仅支持 Active / Quiet
  绘制规则：
左上角：绿色文字=摄像头编号 + 当前帧数
画面右上角：红色文字=动静状态
  返回值：
绘制完成后的图像
3. detect_activity(current_frame, prev_frame, threshold)

帧差法检测画面是否存在运动，依靠前后帧像素差异判断动静。
实现逻辑：
当前帧与上一帧做像素绝对差值，计算差值图全部像素平均值，和阈值对比。
入参：
current_frame：当前最新画面帧
prev_frame：上一帧缓存画面
threshold：动静判定阈值 diff_threshold
返回值：
(status, has_prev)
status：Active / Quiet；has_prev：布尔值，标记是否存在历史帧

## 四、主程序main完整运行逻辑
### F1：初始化资源与缓存变量
1. 创建 cap1、cap2 两个视频读取对象，分别打开两路视频；
2. 初始化基础变量：
  frame_num：全局帧数计数器，初始值 0，每一帧 + 1；
  prev_frame1 /prev_frame2：缓存两路视频上一帧画面，用于帧差计算；
  state1_old /state2_old：缓存上一轮运动状态，捕捉状态切换。
### F2：视频合法性校验
调用 cap.isOpened()校验两路视频；任意一路打开失败，终端报错，统一执行资源释放并终止程序。
### F3：循环读取画面，对齐两路尺寸
读取Cam1画面，以1的宽高作为统一尺寸标准；任意一路读取完毕直接退出循环，保证两路播放时序同步；
Cam2调用read_frame自动缩放至1的尺寸，保障两张图像行列数完全一致。
### F4：Canny 边缘图像处理
BGR原图————灰度化————Canny边缘提取————转BGR三通道。
Canny 输出单通道灰度图，无法直接拼接；转回三通道保证数组维度匹配。
### F5：帧差运动检测 + 状态日志打印
1. 两路灰度图分别调用 detect_activity 获取实时状态
2. 对比当前状态和历史旧状态
新旧不一致则终端打印日志[CamX][帧xx] 状态切换：(旧)→(新)
3. 调用 draw_overlay，一次性完成左上帧号、右上状态绘制
### F6：更新缓存数据
循环结尾把当前灰度帧、最新运动状态赋值给prev_frame、state_old，为下一回合帧差比对留存数据。
### F7：画面竖直拼接 + 高度自适应缩放
np.vstack，Cam1上、Cam2下；
拼接后总高度超过 max_h，则整体等比例缩小画面，适配屏幕。
### F8：窗口展示 + 按键交互
imshow渲染拼接完成的画面；依靠waitKey捕获按键；
q键：退出主循环；空格键：调用imwrite保存画面至data目录，控制台提示保存成功。
### F9：帧数迭代与全场景资源回收
1. 单次循环结束，frame_num 自增；
2. 无论视频自然播完、手动按q退出、视频打开失败，全部执行标准化收尾：两路cap执行release释放流，调用destroyAllWindows关闭所有窗口，杜绝资源残留、视频文件被占用。

## 五、常见报错原因与解决办法
| 异常现象 | 根本原因 | 解决方式 |
| -------- | -------- | -------- |
| 一路/两路视频打开失败 | 文件路径写错、视频名不匹配、视频损坏 | 核对相对路径，确认data内视频文件名一致 |
| 图像拼接数组报错 | Canny单通道未转回BGR三通道 | 补充cvtColor灰度转BGR代码 |
| 第一帧无运动日志 | 首帧没有历史对比帧，规则默认静止 | 正常现象，第二帧开始生成状态日志 |
| 画面文字超出边界 | 文字坐标参数不合适 | 微调text_x、text_y、status_text_offset |
| 轻微走动无法触发检测 | 阈值过大 | 下调阈值，提升识别灵敏度 |
| 播放窗口黑屏无画面 | 缺少waitKey，画面无法刷新 | 保证代码存在waitKey等待语句 |