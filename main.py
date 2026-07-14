import pandas as pd
import json

df = pd.read_csv("./data/dataplus.csv", encoding="utf-8", usecols=["姓名", "分数"])
score_col = df["分数"]

stat_info = {
    "平均分": float(score_col.mean()),
    "最高分": int(score_col.max()),
    "最低分": int(score_col.min())
}

pass_data = df[df["分数"] >= 60].to_dict("records")

result = {
    "基础分数统计": stat_info,
    "及格人员数据": pass_data
}

with open("./result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("结果输出至result.json")