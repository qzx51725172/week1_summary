from zhipuai import ZhipuAI

# 填入你本地保存的完整API Key
client = ZhipuAI(api_key="个人API Key")

response = client.chat.completions.create(
    model="glm-4-flash",
    messages=[{"role": "user", "content": "简单介绍PyTorch是什么"}]
)
print("大模型返回回答：")
print(response.choices[0].message.content)