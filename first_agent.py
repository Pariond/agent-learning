import json
from openai import OpenAI
from dotenv import load_dotenv
import os

# 加载 .env 文件里的环境变量
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


def get_weather(city):
    if not city or city.strip=="":
        return f"输入不能为空"
    mock = {
        "北京": "25C晴",
        "上海": "28C多云",
        "广州": "32C阵雨"
    }
    result=mock.get(city)
    if result is None:
        return f"抱歉，未获取到{city}的数据"
    return result


def send_notification(msg):
    print(f"\n[通知]: {msg}\n")
    return "通知成功"


def get_time(city):
    return f"{city}当前的时间是14:30"
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_notification",
            "description": "发通知",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "通知内容"
                    }
                },
                "required": ["message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "查询某个城市当前的时间",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "城市名"
                    }
                },
                "required": ["city"]
            }
        }
    }
]


def execute(tc):
    n = tc.function.name
    a = json.loads(tc.function.arguments)
    print(f"  -> 调工具: {n} {a}")

    if n == "get_weather":
        return json.dumps({"r": get_weather(**a)})
    if n == "send_notification":
        return json.dumps({"r": send_notification(**a)})
    if n == "get_time":
        return json.dumps({"r": get_time(**a)})
    return json.dumps({"e": "未知工具"})


def run():
    msgs = [
        {
            "role": "system",
            "content": "你是一个专业的电商客服。回答要礼貌、简洁、耐心。如果用户问的问题你查不到，就说'抱歉我查不到这个信息，请提供更详细的信息'。"
        }
    ]
    print("Agent启动！输入 q 退出")

    while True:
        u = input("\n你: ")
        if u.lower() == "q":
            break

        msgs.append({"role": "user", "content": u})
        r = client.chat.completions.create(
            model=MODEL,
            messages=msgs,
            tools=TOOLS,
            tool_choice="auto"
        )

        c = r.choices[0]
        m = c.message

        if c.finish_reason == "tool_calls":
            msgs.append(m)
            for t in m.tool_calls:
                msgs.append({
                    "role": "tool",
                    "tool_call_id": t.id,
                    "content": execute(t)
                })

            final = client.chat.completions.create(
                model=MODEL,
                messages=msgs
            ).choices[0].message.content
        else:
            final = m.content

        print(f"\n助手: {final}")
        msgs.append({"role": "assistant", "content": final})


if __name__ == "__main__":
    run()
