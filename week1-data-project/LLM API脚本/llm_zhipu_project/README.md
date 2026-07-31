## 设计思路
1. 读本地文件：读取 question.txt 里面的问题
2. 网络请求：调用智谱 AI 接口，把问题发过去，拿到 AI 回复
3. 写本地文件：把 AI 返回的回答，存进 answer.txt

## 按功能写程序
## F1 读取 txt 文件(单独测试本地文本读取功能)
```python
# 仅测试读文件
with open("question.txt", "r", encoding="utf-8") as f:
    q = f.read()
print(q)
```
## F2 智谱 AI 接口调用(固定测试问题，隔离文件操作，单独验证接口连通性)
前置环境准备
调用接口需要网络请求库 requests，先在终端执行安装：
```bash
pip install requests
```
完整测试代码：
```python
# 1. 导入网络请求工具，用来向智谱服务器发送数据
import requests

# ========== 配置区，只需要修改这里 ==========
# 替换成你自己后台复制的密钥
ZHIPU_KEY = "API Key"
# 智谱官方接口地址，固定不用改
api_url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
# 选用的大模型
model_name = "glm-4-flash"
# 固定测试问题，不用读取文件，纯测试接口
test_question = "简单介绍Python是什么"
# ===========================================

# 2. 请求头headers：身份验证 + 数据格式声明
# Authorization：带上密钥，服务器识别你是合法用户
# Content-Type：告诉服务器我们发送的是json格式数据
headers = {
    "Authorization": f"Bearer {ZHIPU_KEY}",
    "Content-Type": "application/json"
}

# 3. 请求体data：智谱规定的标准格式，固定结构不能乱改
data = {
    # 指定使用哪个模型
    "model": model_name,
    # 对话列表，数组格式，role代表角色
    # user = 用户提问，assistant = AI回复，system = 系统设定
    "messages": [
        {
            "role": "user",
            "content": test_question
        }
    ]
}

# 4. 发送POST网络请求，把headers和data一起发给智谱服务器
# json=data 会自动把字典转换成标准json字符串
response = requests.post(url=api_url, headers=headers, json=data)

# 5. 将服务器返回的json字符串，转为Python字典，方便读取内容
response_data = response.json()

# 6. 提取AI回答核心内容（固定取值路径）
# choices：模型生成的回复列表，一般只有1条回复，取下标0
# message：单条回复对象，content就是AI输出的文字
ai_reply = response_data["choices"][0]["message"]["content"]

# 7. 在控制台打印AI回复，验证接口调用成功
print("AI回答：")
print(ai_reply)
```

## F3 写入 txt 文件(单独测试文本保存功能)
目的：随便一段文字，代码能自动生成 answer.txt 并保存文字
```python
ans = "这是AI的回答"
with open("answer.txt","w",encoding="utf-8") as f:
    f.write(ans)
print("写入完成，请查看answer.txt")
```

## 合并功能，实现自动读取、调用、回答
```python
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
```

## 正确操作步骤
1. 依赖安装 
```bash
pip install requests
```
2. 在项目根目录 question.txt 写入提问内容
3. 将代码中 ZHIPU_API_KEY 替换为个人智谱平台密钥
4. 终端执行脚本 
```bash
python test.py
```
5. 运行完成后查看answer.txt 获取 AI 回复
## 说明：
本项目调用 智谱 AI 开放平台 GLM 系列大模型接口
接口地址：https://open.bigmodel.cn/api/paas/v4/chat/completions
使用模型：glm-4-flash