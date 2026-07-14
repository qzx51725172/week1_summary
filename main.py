#库导入
import pandas as pd
import json

# 从相对路径读取csv，指定UTF-8 编码，仅保留姓名、分数
data = pd.read_csv("./data/dataplus.csv", encoding="utf-8", usecols=["姓名", "分数"])
score = data["分数"]

# 单个分数出现次数统计，将 pandas 统计表格转为普通 Python 字典，适配 JSON 导出格式。
count = data["分数"].value_counts().to_dict()
# 成绩分段，将连续分数划分为离散档位，在原表格新增一列，存储每条数据对应的成绩档位；统计每个档位的总人数，转为字典
bins = [0, 59, 79, 100]
lab = ["不及格(0-59)", "中等(60-79)", "优秀(80-100)"]
data["段"] = pd.cut(score, bins=bins, labels=lab, right=True)
level = data["段"].value_counts().to_dict()
#基础数值统计汇总
stats = {
    "平均分": float(score.mean()),
    "最高分": int(score.max()),
    "最低分": int(score.min()),
    "分数次数": count,
    "分段人数": level
}

#筛选及格人员
pass_data = data[data["分数"] >= 60].to_dict("records")
result = {
    "基础统计": stats,
    "及格名单": pass_data
}

#JSON 文件写入导出
with open("./result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("结果输出至result.json")