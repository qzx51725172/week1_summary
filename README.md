# week1-data-project
## 功能
读取本地CSV成绩表格
1. 计算分数均值、最大/最小值，筛选及格人员
2. 分布统计：单个分数出现频次、成绩区间人数分布（不及格 / 中等 / 优秀）；
将全部统计结果导出为JSON文件。

## 运行环境
Python 3.10
依赖库：pandas

## 数据源准备
1. 在项目根目录新建 `data` 文件夹；
2. 将成绩CSV文件命名为 `dataplus.csv`，放入 `data/` 文件夹内；
3. CSV表头固定为「姓名,分数」，否则代码读取字段会报错。
项目标准目录结构
week1-data-project/       # 项目根目录
├─ main.py                # 主处理脚本
├─ result.json            # 程序运行后自动生成的输出文件
├─ README.md              # 本说明文档
└─ data/                  # 数据源文件夹
   └─ dataplus.csv        # 成绩原始CSV表格

## 切换项目根目录
打开 Git Bash ，cd C:\Users\asus\git-test\week1-data-project，所有命令均在此目录执行。

## 依赖安装与脚本运行命令
激活 py310 虚拟环境后，执行命令安装依赖：
```bash
pip install pandas
```
在项目根目录执行以下命令运行数据处理程序：
```bash
python main.py
```
(其余解析已基本写在py文件具体位置了)
## 导出JSON文件部分代码解析
```python
with open("./result.json", "w", encoding="utf-8") as f:
```
"./result.json"：文件路径，代表项目根目录下的 result.json
"w"：打开模式 write 写入模式
文件不存在 → 自动新建文件
文件已存在 → 清空原有全部内容，从头写入新内容
encoding="utf-8"：指定文件编码为 UTF-8，防止中文乱码

with 是 Python 安全文件读写语法，自动关闭文件，不用手动写f.close()，避免忘记关文件导致数据丢失、占用资源。
as f：给打开的文件对象起别名 f，后面操作文件直接用 f
```python
json.dump(res, f, ensure_ascii=False, indent=2)
```
json.dump(要保存的数据, 文件对象, 参数1, 参数2)，作用：把 Python 字典 / 列表写入 JSON 文件
indent=2 格式化排版
给 JSON 自动换行、缩进 2 空格，文件内容分层清晰可读；
如果删掉这个参数，所有内容会挤成一行，不方便查看
ensure_ascii=False :保证 JSON 正常显示中文，不会转义成 Unicode 编码

## 问题描述
运行代码时提示 FileNotFoundError，程序无法读取 CSV 文件。
## 解决思路
一、确认终端工作目录切换至项目根文件夹 week1-data-project；
二、严格按规范将 CSV 文件放入 data 子文件夹，代码使用相对路径./data/dataplus.csv读取，保证路径匹配。
三、本项目源码直接放在根目录，运行命令为python main.py，无需 src 路径前缀。