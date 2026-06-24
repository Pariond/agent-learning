"""
Agent 核心逻辑
供 Streamlit 前端调用，也保留原来的黑窗口入口
"""
# -*- coding: utf-8 -*-
import json
from openai import OpenAI
from dotenv import load_dotenv
import os
# 配置（部署时改成环境变量）
# 加载 .env 文件里的环境变量
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")                #自己导入环境变量 放入key
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# 加载向量知识库
try:
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_chroma import Chroma

    print("正在加载知识库...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"local_files_only": True}
    )
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings,
    )
    print("知识库加载完成")
except Exception as e:
    print(f"知识库加载失败（首次运行请先执行 ingest.py）: {e}")
    vectorstore = None

# 商品和订单数据
PRODUCTS = [
    {"id": 1001, "name": "iPhone 15",     "price": 5999,  "stock": 100},
    {"id": 1002, "name": "MacBook Pro",   "price": 14999, "stock": 50},
    {"id": 1003, "name": "AirPods Pro",   "price": 1999,  "stock": 200},
    {"id": 1004, "name": "iPad Air",      "price": 4999,  "stock": 80},
    {"id": 1005, "name": "Apple Watch",   "price": 3299,  "stock": 60},
]

ORDERS = [
    {"id": "ORD001", "product": "iPhone 15",   "status": "已发货", "address": "北京"},
    {"id": "ORD002", "product": "MacBook Pro", "status": "待发货", "address": "上海"},
    {"id": "ORD003", "product": "AirPods Pro", "status": "已签收", "address": "广州"},
]

ALIASES = {
    "苹果15": "iPhone 15", "苹果手机": "iPhone 15",
    "mac": "MacBook Pro", "macbook": "MacBook Pro",
    "耳机": "AirPods Pro", "平板": "iPad Air", "手表": "Apple Watch",
}

# 工具函数
def search_product(keyword):
    if keyword in ALIASES:
        keyword = ALIASES[keyword]
    for p in PRODUCTS:
        if keyword in p["name"]:
            return json.dumps(p, ensure_ascii=False)
    return "没有找到相关商品"

def check_order(order_id):
    for o in ORDERS:
        if o["id"] == order_id.upper():
            return json.dumps(o, ensure_ascii=False)
    return "订单不存在"

def cancel_order(order_id):
    for o in ORDERS:
        if o["id"] == order_id.upper():
            if o["status"] == "待发货":
                o["status"] = "已取消"
                return "订单已取消"
            else:
                return f"订单状态为{o['status']}，无法取消"
    return "订单不存在"

def search_knowledge(question):
    if vectorstore is None:
        return "知识库未加载"
    docs = vectorstore.similarity_search(question, k=3)
    return "\n---\n".join([d.page_content for d in docs]) if docs else "知识库中未找到相关信息"

TOOLS = [
    {"type":"function","function":{"name":"search_product","description":"按关键词搜索商品信息","parameters":{"type":"object","properties":{"keyword":{"type":"string","description":"商品关键词"}},"required":["keyword"]}}},
    {"type":"function","function":{"name":"check_order","description":"查询订单状态","parameters":{"type":"object","properties":{"order_id":{"type":"string","description":"订单号"}},"required":["order_id"]}}},
    {"type":"function","function":{"name":"cancel_order","description":"取消待发货的订单","parameters":{"type":"object","properties":{"order_id":{"type":"string","description":"要取消的订单号"}},"required":["order_id"]}}},
    {"type":"function","function":{"name":"search_knowledge","description":"从知识库搜索发货、售后、发票等信息","parameters":{"type":"object","properties":{"question":{"type":"string","description":"用户问题"}},"required":["question"]}}},
]

def execute_tool_call(tc):
    name, args = tc.function.name, json.loads(tc.function.arguments)
    print(f"  [调用工具] {name}".encode("utf-8", errors="replace").decode("utf-8"))
    if name == "search_product": return search_product(**args)
    if name == "check_order": return check_order(**args)
    if name == "cancel_order": return cancel_order(**args)
    if name == "search_knowledge": return search_knowledge(**args)
    return "未知工具"

# 核心函数：处理单条消息，返回回复文本
def chat(user_input: str, messages: list) -> tuple:
    """
    处理用户输入，返回（回复文本, 更新后的消息列表）
    messages 需要以 [{"role":"system","content":"..."}] 开头
    """
    messages.append({"role": "user", "content": user_input})
    r = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS, tool_choice="auto")
    c, m = r.choices[0], r.choices[0].message

    if c.finish_reason == "tool_calls":
        messages.append(m)
        for t in m.tool_calls:
            messages.append({"role": "tool", "tool_call_id": t.id, "content": execute_tool_call(t)})
        final = client.chat.completions.create(model=MODEL, messages=messages)
        reply = final.choices[0].message.content
        messages.append(final.choices[0].message)
    else:
        reply = m.content
        messages.append(m)

    return reply, messages

# CLI 入口（保留原先的黑窗口模式）
if __name__ == "__main__":
    if "你的" in API_KEY:
        print("错误：还没填 API Key")
        exit()
    msgs = [{"role":"system","content":"你是电商客服助手。用中文回答。"}]
    print("客服 Agent 已启动")
    while True:
        u = input("\n你: ")
        if u.lower() == "q": break
        reply, msgs = chat(u, msgs)
        print(f"\n客服: {reply}")
