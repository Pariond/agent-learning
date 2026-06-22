import json
from openai import OpenAI
from dotenv import load_dotenv
import os
# 加载 .env 文件里的环境变量
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")                #自己导入环境变量 放入key
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

os.environ["HF_HUB_ENABLE_HF_SYMLINKS"] = "0"
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
# HuggingFace 国内镜像
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
print("正在加载知识库...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
)
print("知识库加载完成\n")

ALIASES = {                               #做别名
    "苹果15": "iPhone 15",
    "苹果手机": "iPhone 15",
    "mac": "MacBook Pro",
    "macbook": "MacBook Pro",
    "耳机": "AirPods Pro",
    "平板": "iPad Air",
    "手表": "Apple Watch",
}
PRODUCTS = [                   #数据
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

# ============================================================
# 工具函数（多了一个 search_knowledge）
# ============================================================
def search_product(keyword):
    # 先查别名表
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

def get_return_policy():
    return "收货后7天可无理由退换，质量问题商家承担运费。"

def cancel_order(order_id):
    for o in ORDERS:
        if o["id"] == order_id.upper():
            if o["status"] == "待发货":
                o["status"] = "已取消"
                return "订单已取消"
            else:
                return f"订单状态为{o['status']}，无法取消"
    return "订单不存在"

#Rag文档
def search_knowledge(question):
#先切片文档 再找数据 然后返回
    docs = vectorstore.similarity_search(question, k=3)
    if not docs:
        return "知识库中没有找到相关信息"

    # 把检索到的片段拼在一起返回
    result = "\n---\n".join([d.page_content for d in docs])
    return result


#工具
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_product",
            "description": "按关键词搜索商品信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "搜索关键词"}
                },
                "required": ["keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_order",
            "description": "查询订单状态",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "订单号"}
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_return_policy",
            "description": "获取退换货政策",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_order",
            "description": "取消待发货的订单",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "要取消的订单号"}
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "从公司知识库中搜索信息，用于解答发货政策、售后规则、常见问题等",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "用户的问题"}
                },
                "required": ["question"]
            }
        }
    },
]


def run():
    if "你的" in API_KEY:
        print("错误：你还没填 API Key")
        print("请打开文件，把第 13 行的 sk-你的DeepSeek密钥 替换成真正的 key")
        return

    messages = [{"role": "system",
        "content": "你是电商客服助手。可查商品、订单、退换货。对于发货、售后、发票等问题，使用 search_knowledge 工具从知识库中查找答案。用中文回答。"}]

    print("=" * 50)
    print("电商客服 Agent（带RAG版）已启动")
    print("=" * 50)
    print("试试问：")
    print("  'iPhone 15 多少钱？'")
    print("  '查订单 ORD001'")
    print("  '怎么查物流？'      ← 这个会从知识库检索")
    print("  '能开发票吗？'      ← 这个也会从知识库检索")
    print("  '保修期多久？'      ← 这个也会")
    print("=" * 50)

    while True:
        try:
            user = input("\n你: ")
            if user.lower() == "q":
                break
            if not user.strip():
                continue

            messages.append({"role": "user", "content": user})
            r = client.chat.completions.create(
                model=MODEL, messages=messages,
                tools=TOOLS, tool_choice="auto"
            )
            c = r.choices[0]
            m = c.message

            if c.finish_reason == "tool_calls":
                messages.append(m)
                for t in m.tool_calls:
                    name = t.function.name
                    args = json.loads(t.function.arguments)
                    print(f"  [调用工具] {name}")

                    if name == "search_product":
                        result = search_product(**args)
                    elif name == "check_order":
                        result = check_order(**args)
                    elif name == "get_return_policy":
                        result = get_return_policy(**args)
                    elif name == "cancel_order":
                        result = cancel_order(**args)
                    elif name == "search_knowledge":
                        # ★ RAG 查询：从知识库检索
                        result = search_knowledge(**args)
                    else:
                        result = "未知工具"

                    messages.append({"role": "tool", "tool_call_id": t.id, "content": result})

                final = client.chat.completions.create(model=MODEL, messages=messages)
                print(f"\n客服: {final.choices[0].message.content}")
                messages.append(final.choices[0].message)
            else:
                print(f"\n客服: {m.content}")
                messages.append(m)

        except Exception as e:
            print(f"\n出错了: {e}")
            print("检查：1.API Key  2.pip install 装了没  3.先运行了 ingest.py 没")


if __name__ == "__main__":
    run()
