# 导入工具包
import pandas as pd
import json

# 读取csv表格 !!data.csv真路径
data = pd.read_csv(r"C:\Users\asus\git-test\week1-data-project\周任务数据\data.csv", encoding="utf-8")

# 把表格转成字典列表
data_list = data.to_dict("records")

# 创建并写入json文件
file = open("output.json", "w", encoding="utf-8")
json.dump(data_list, file, ensure_ascii=False, indent=2)
file.close()

# 提示完成
print("转换完成！")