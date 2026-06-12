git push -u origin main"""
第一个 Agent 脚本
模型：DeepSeek（兼容 OpenAI SDK）
"""
import json
from openai import OpenAI
API_KEY = "sk-82ed228c9f1344ca97c06950c88b26c8"
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
def get_weather(city):
    mock = {"北京":"25C晴","上海":"28C多云","广州":"32C阵雨"}
    return mock.get(city, f"没有{city}的数据")
def send_notification(msg):
    print(f"\n[通知]: {msg}\n")
    return "通知成功"
TOOLS = [
    {"type":"function","function":{"name":"get_weather","description":"查询天气","parameters":{"type":"object","properties":{"city":{"type":"string","description":"城市名"}},"required":["city"]}}},
    {"type":"function","function":{"name":"send_notification","description":"发通知","parameters":{"type":"object","properties":{"message":{"type":"string","description":"通知内容"}},"required":["message"]}}}
]
def execute(tc):
    n = tc.function.name; a = json.loads(tc.function.arguments)
    print(f"  -> 调工具: {n} {a}")
    if n=="get_weather": return json.dumps({"r":get_weather(**a)})
    if n=="send_notification": return json.dumps({"r":send_notification(**a)})
    return json.dumps({"e":"未知工具"})
def run():
    msgs=[{"role":"system","content":"你是一个智能助手，可以查天气和发通知"}]
    print("Agent启动！输入 q 退出")
    while True:
        u = input("\n你: ")
        if u.lower()=="q": break
        msgs.append({"role":"user","content":u})
        r = client.chat.completions.create(model=MODEL,messages=msgs,tools=TOOLS,tool_choice="auto")
        c = r.choices[0]; m = c.message
        if c.finish_reason=="tool_calls":
            msgs.append(m)
            for t in m.tool_calls:
                msgs.append({"role":"tool","tool_call_id":t.id,"content":execute(t)})
            final = client.chat.completions.create(model=MODEL,messages=msgs).choices[0].message.content
        else:
            final = m.content
        print(f"\n助手: {final}")
        msgs.append({"role":"assistant","content":final})
if __name__=="__main__":
    run()
