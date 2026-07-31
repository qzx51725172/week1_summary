import requests

# 智谱配置区
ZHIPU_API_KEY = "API Key"
url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
model = "glm-4-flash"

# 1. 读取question.txt里的问题
with open("question.txt", "r", encoding="utf-8") as f:
    user_question = f.read()
if not user_question:
    print("错误：question.txt 为空，请写入提问内容")
    exit()
# 2. 调用智谱AI接口
headers = {
    "Authorization": f"Bearer {ZHIPU_API_KEY}",
    "Content-Type": "application/json"
}
payload = {
    "model": model,
    "messages": [{"role": "user", "content": user_question}]
}
response = requests.post(url, headers=headers, json=payload)
result = response.json()
answer_text = result["choices"][0]["message"]["content"]

# 3. 把回答写入answer.txt
with open("answer.txt", "w", encoding="utf-8") as f:
    f.write(answer_text)

# 控制台打印方便查看
print("AI回答：")
print(answer_text)
print("\n已自动保存到 answer.txt")
