 # 完整操作步骤
 
 本文件把 README 里的计划拆成每一步怎么操作。照着做就行，不需要自己决定。
 
 ---
 
 ## 第 1 步：注册 DeepSeek（5 分钟）
 
 1. 打开浏览器，输入网址：https://platform.deepseek.com
 2. 点击右上角"登录 / 注册"
 3. 用手机号注册，接收验证码
 4. 登录成功后，在左侧菜单点击"API Keys"
 5. 点击"创建 API Key"
 6. 取个名字比如"agent-learning"，点确定
 7. 弹出的一串密钥（格式是 sk-xxx...），点"复制"，粘贴到记事本里存好
    - 注意：这个页面关了就看不到了，一定要先复制
 8. 再点一下"充值"→ 输入 10 元（DeepSeek 很便宜，10 元够你用半年）
 
 ---
 
 ## 第 2 步：注册 GitHub 并创建仓库（10 分钟）
 
 1. 打开 https://github.com
 2. 点右上角 Sign up，用邮箱注册
    - 用户名建议：你的英文名或拼音
    - 邮箱用 QQ 邮箱或 Gmail 都行
 3. 注册完登录，点右上角 + → New repository
 4. 填写：
    - Repository name: agent-learning
    - 描述（Description）: Agent development learning project
    - Public（公开）不要选 Private
    - 勾选 Add a README file
 5. 点最下面的 Create repository
 6. 创建好后，点右上角你的头像 → Your repositories → 找到 agent-learning
 
 ---
 
 ## 第 3 步：安装 Python 环境（如果还没装的话，15 分钟）
 
 1. 打开浏览器，输入：https://www.python.org/downloads/
 2. 下载最新的 Python 3.x（比如 Python 3.12 或 3.13）
 3. 双击安装包，安装时**一定要勾选"Add Python to PATH"**
 4. 一直点 Next 直到安装完成
 5. 验证：按 Win+R → 输入 cmd → 回车 → 输入 `python --version`
    - 如果显示 Python 3.xx 说明装好了
 
 ---
 
 ## 第 4 步：运行 first_agent.py（30 分钟）
 
 ### 4.1 找到文件位置
 
 first_agent.py 在我刚创建的文件夹里：
 ```
 D:\agent-learning\first_agent.py
 ```
 
 ### 4.2 打开文件，填入 API Key
 
 1. 右键 first_agent.py → 打开方式 → 选择"记事本"
 2. 找到这一行（大概在第 5 行）：
    ```python
    API_KEY = "sk-你的DeepSeek密钥"
    ```
 3. 把 `sk-你的DeepSeek密钥` 替换成你第 1 步复制的 key
    改完之后应该是这样的（举例）：
    ```python
    API_KEY = "sk-a1b2c3d4e5f6..."
    ```
 4. 保存文件（Ctrl+S）
 
 ### 4.3 安装依赖
 
 1. 按 Win+R → 输入 cmd → 回车
 2. 在黑窗口里输入：
    ```
    pip install openai
    ```
 3. 等它跑完，看到 Successfully installed 说明安装成功
 
 ### 4.4 运行脚本
 
 1. 在同一个黑窗口里，输入：
    ```
    cd D:\agent-learning
    python first_agent.py
    ```
 2. 看到屏幕显示"Agent启动！输入 q 退出"说明成功了
 3. 测试一下，输入：
    ```
    北京天气怎么样？
    ```
 4. 如果它回复了天气信息，说明 agent 跑通了
 5. 再测试：
    ```
    查一下广州天气，然后通知我
    ```
 6. 输入 `q` 退出
 
 ### 4.5 如果报错了怎么办
 
 常见错误及解决方法：
 
 | 报错信息 | 原因 | 解决方法 |
 |----------|------|----------|
 | `ModuleNotFoundError: No module named 'openai'` | 没安装 openai 包 | 执行 `pip install openai` |
 | `AuthenticationError` | API Key 填错了 | 重新复制 key 粘贴 |
 | `'python' 不是内部或外部命令` | Python 没加到 PATH | 重新安装 Python，勾选 Add to PATH |
 | `ConnectionError` | 网络连不上 DeepSeek | 检查网络，或者切换手机热点试试 |
 
 ---
 
 ## 第 5 步：推送到 GitHub（15 分钟）
 
 1. 打开 cmd 黑窗口
 2. 进入文件夹：
    ```
    cd D:\agent-learning
    ```
 3. 初始化 Git 仓库：
    ```
    git init
    ```
 4. 添加所有文件：
    ```
    git add .
    ```
 5. 提交：
    ```
    git commit -m "first agent: weather + notification"
    ```
 6. 设置分支名：
    ```
    git branch -M main
    ```
 7. 关联远程仓库（把下面的用户名改成你的 GitHub 用户名）：
    ```
    git remote add origin https://github.com/你的用户名/agent-learning.git
    ```
 8. 推送：
    ```
    git push -u origin main
    ```
 9. 如果提示要登录，在弹出的 GitHub 登录窗口登录
 10. 完成后打开 https://github.com/你的用户名/agent-learning 确认文件已经上传
 
 ---
 
 ## 第 6 步：理解 first_agent.py 的每一部分（3 天）
 
 ### Day 1（6月13日）：理解第 1-25 行
 
 用 VS Code 打开 first_agent.py（推荐装 VS Code，比记事本好用）。
 
 先看前三行：
 ```python
 import json
 from openai import OpenAI
 ```
 - `import json`：导入 Python 自带的 json 工具包，之后用来解析模型返回的数据
 - `from openai import OpenAI`：从 openai 库中导入 OpenAI 这个类
 
 再看变量区：
 ```python
 API_KEY = "sk-..."     # 你的 DeepSeek 密钥
 BASE_URL = "https://api.deepseek.com"  # DeepSeek 的服务器地址
 MODEL = "deepseek-chat"  # 用的模型名字
 client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
 ```
 - `client` 就是你和 DeepSeek 之间的"电话线"。你发消息、收回复都通过它。
 
 **作业：** 搜一下"什么是 API？API Key 是用来干什么的？"看 3 分钟视频
 
 ### Day 2（6月14日）：理解第 27-60 行
 
 ```python
 def get_weather(city):
     mock = {"北京":"25C晴", "上海":"28C多云", "广州":"32C阵雨"}
     return mock.get(city, f"没有{city}的数据")
 ```
 - 这是一个函数，`city` 是参数（城市名）
 - 函数体里是一个字典（你学过的），根据城市名返回天气
 - `mock.get(city, ...)` 意思是：如果字典里有这个城市就返回天气，没有就返回"没有数据"
 
 ```python
 TOOLS = [...]
 ```
 - 这个列表描述了两个工具的名字、功能、参数
 - 它会被发给 DeepSeek，让模型知道："你可以用这些工具"
 - 注意这里的 JSON 嵌套结构
 
 **作业：** 搜一下"什么是 function calling？"看 10 分钟视频
 
 ### Day 3（6月15日）：理解第 62 行到结尾
 
 ```python
 def run():
 ```
 - 这个函数是 agent 的核心，包含一个 while 循环
 - while True 的意思是"无限循环"，除非用户输入 q 退出
 
 每次循环做的事情：
 1. 获取你的输入 → 存入 messages 列表（对话历史）
 2. 把 messages 发给 DeepSeek → 模型决定要不要调工具
 3. 如果模型说"要调工具"（finish_reason == "tool_calls"）：
    - 执行对应的 Python 函数（get_weather 或 send_notification）
    - 把工具结果发回给模型 → 模型生成最终回复
 4. 打印回复
 5. 把回复加入 messages → 进入下一次循环
 
 **检查标准：** 关掉文件，你能用大白话讲清楚"从你输入到看到回复，中间经历了哪几步？"
 
 ---
 
 ## 第 7 步：自己动手改代码（6月16日 - 6月20日）
 
 ### 7.1 新增一个工具：get_time（6月16日）
 
 打开 first_agent.py，按顺序修改：
 
 **① 加函数（在 send_notification 后面加）：**
 ```python
 def get_time(city):
     # 模拟：返回一个固定时间
     return f"{city}当前时间是 14:30"
 ```
 
 **② 加工具描述（在 TOOLS 列表里加）：**
 找到 TOOLS 列表的结尾，在最后一个 `},` 的后面加上：
 ```python
     {
         "type": "function",
         "function": {
             "name": "get_time",
             "description": "查询某个城市的当前时间",
             "parameters": {
                 "type": "object",
                 "properties": {
                     "city": {
                         "type": "string",
                         "description": "城市名称",
                     }
                 },
                 "required": ["city"],
             },
         },
     },
 ```
 注意：最后一项后面不要加逗号了。
 
 **③ 加调度逻辑（在 execute 函数里加）：**
 找到：
 ```python
     if n=="send_notification": return json.dumps({"r":send_notification(**a)})
 ```
 这行下面加一行：
 ```python
     if n=="get_time": return json.dumps({"r":get_time(**a)})
 ```
 
 **④ 测试：** 运行脚本，输入"现在北京几点了？"
 
 **⑤ 提交到 GitHub：**
 ```
 git add .
 git commit -m "add get_time tool"
 git push
 ```
 
 ### 7.2 改系统提示词（6月17日）
 
 找到这行：
 ```python
 msgs=[{"role":"system","content":"你是一个智能助手，可以查天气和发通知"}]
 ```
 改成：
 ```python
 msgs=[{"role":"system","content":"你是一个专业的电商客服。回答要礼貌、简洁、耐心。如果用户问的问题你查不到，就说'抱歉我查不到这个信息，请提供更详细的信息'。"}]
 ```
 
 跑起来试试，语气是不是变了？
 
 ### 7.3 加错误处理（6月18日）
 
 把 get_weather 函数改成：
 ```python
 def get_weather(city):
     if not city or city.strip() == "":
         return "城市名不能为空"
     mock = {"北京":"25C晴", "上海":"28C多云", "广州":"32C阵雨"}
     result = mock.get(city)
     if result is None:
         return f"抱歉，没有{city}的天气数据"
     return result
 ```
 
 ### 7.4 提交最终版（6月19日）
 
 ```
 git add .
 git commit -m "add error handling + system prompt update"
 git push
 ```
 
 6月20日休息或补之前落下的进度。
 
 ---
 
 ## 第 8 步：做 RAG 文档问答 bot（6月21日 - 6月28日）
 
 ### 8.1 安装依赖（6月21日）
 
 打开 cmd，输入：
 ```
 pip install langchain langchain-community chromadb sentence-transformers
 ```
 
 ### 8.2 创建项目结构（6月21日）
 
 在 D:\agent-learning 下新建文件夹 rag_bot，里面建这些文件：
 
 ```
 D:\agent-learning\rag_bot\
 ├── ingest.py        # 导入文档
 ├── query.py         # 问问题
 ├── docs\            # 放文档
 │   ├── product_manual.txt
 │   └── return_policy.txt
 ```
 
 怎么建文件夹：
 ```
 cd D:\agent-learning
 mkdir rag_bot
 mkdir rag_bot\docs
 ```
 
 ### 8.3 准备文档（6月21日）
 
 新建一个文本文件 `D:\agent-learning\rag_bot\docs\product_manual.txt`
 在里面写几段产品说明，比如：
 ```
 产品名称：智能手表 X1
 价格：299 元
 功能：心率监测、步数统计、消息提醒
 电池续航：7 天
 防水等级：IP68
 
 产品名称：蓝牙耳机 Pro
 价格：159 元
 功能：主动降噪、无线充电、IPX5 防水
 续航：单次 8 小时，配合充电仓 36 小时
 
 退换货政策：
 1. 收货后 7 天内可无理由退换
 2. 退换商品需保持原包装完整
 3. 质量问题由商家承担运费
 4. 非质量问题退货运费由买家承担
 ```
 
 ### 8.4 写 ingest.py（6月22日）
 
 打开记事本，输入以下内容，保存为 `D:\agent-learning\rag_bot\ingest.py`：
 
 ```python
 from langchain_community.document_loaders import TextLoader
 from langchain.text_splitter import RecursiveCharacterTextSplitter
 from langchain_community.embeddings import HuggingFaceEmbeddings
 from langchain_community.vectorstores import Chroma
 
 # 1. 读取文档
 loader = TextLoader("docs/product_manual.txt", encoding="utf-8")
 documents = loader.load()
 
 # 2. 分块：每 200 字一段，重叠 20 字
 text_splitter = RecursiveCharacterTextSplitter(
     chunk_size=200,
     chunk_overlap=20,
 )
 chunks = text_splitter.split_documents(documents)
 print(f"共切分成 {len(chunks)} 块")
 
 # 3. 向量化并存入 ChromaDB
 embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
 vectorstore = Chroma.from_documents(
     documents=chunks,
     embedding=embeddings,
     persist_directory="./chroma_db",  # 存到本地
 )
 vectorstore.persist()
 print("导入完成！")
 ```
 
 运行：
 ```
 cd D:\agent-learning\rag_bot
 python ingest.py
 ```
 
 ### 8.5 写 query.py（6月23日）
 
 新建 `D:\agent-learning\rag_bot\query.py`：
 
 ```python
 from langchain_community.embeddings import HuggingFaceEmbeddings
 from langchain_community.vectorstores import Chroma
 from openai import OpenAI
 import os
 
 # 配置 DeepSeek
 client = OpenAI(
     api_key="sk-你的DeepSeek密钥",  # 换成你的 key
     base_url="https://api.deepseek.com"
 )
 
 # 加载向量库
 embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
 vectorstore = Chroma(
     persist_directory="./chroma_db",
     embedding_function=embeddings,
 )
 
 def answer_question(question):
     # 1. 从向量库检索相关片段
     docs = vectorstore.similarity_search(question, k=3)
     context = "\n".join([doc.page_content for doc in docs])
     
     # 2. 拼 prompt：把检索到的内容作为上下文
     prompt = f"""基于以下信息回答问题。如果信息不足以回答，就说"根据现有信息无法回答"。
 
 参考信息：
 {context}
 
 问题：{question}
 回答："""
 
     # 3. 调 DeepSeek 生成回答
     response = client.chat.completions.create(
         model="deepseek-chat",
         messages=[{"role": "user", "content": prompt}],
     )
     return response.choices[0].message.content
 
 # 主循环
 if __name__ == "__main__":
     print("RAG 问答系统已启动！输入 q 退出")
     while True:
         q = input("\n问题：")
         if q.lower() == "q":
             break
         a = answer_question(q)
         print(f"\n回答：{a}")
 ```
 
 运行：
 ```
 python query.py
 ```
 
 测试问题：
 - "智能手表多少钱？"
 - "耳机续航多长时间？"
 - "退换货政策是什么？"
 - "手表能防水吗？"
 
 ### 8.6 提交代码（6月25日）
 
 ```
 cd D:\agent-learning
 git add .
 git commit -m "rag bot with chromadb"
 git push
 ```
 
 剩下的时间（6月26日-28日）把前面没做好的地方补上，或者补投简历。
 
 ---
 
 ## 第 9 步：做电商客服 Agent 项目（7月1日 - 7月15日）
 
 （注意：以下步骤以 first_agent.py 为基础扩展，不需要从零写）
 
 ### 9.1 准备数据文件（7月1日）
 
 在 `D:\agent-learning` 下新建 `ecommerce_agent` 文件夹：
 ```
 cd D:\agent-learning
 mkdir ecommerce_agent
 ```
 
 新建 `D:\agent-learning\ecommerce_agent\products.json`：
 ```json
 [
     {"id":1001, "name":"iPhone 15", "price":5999, "stock":100, "category":"手机"},
     {"id":1002, "name":"MacBook Pro", "price":14999, "stock":50, "category":"笔记本"},
     {"id":1003, "name":"AirPods Pro", "price":1999, "stock":200, "category":"耳机"},
     {"id":1004, "name":"iPad Air", "price":4999, "stock":80, "category":"平板"},
     {"id":1005, "name":"Apple Watch", "price":3299, "stock":60, "category":"手表"}
 ]
 ```
 
 新建 `D:\agent-learning\ecommerce_agent\orders.json`：
 ```json
 [
     {"order_id":"ORD001", "product":"iPhone 15", "status":"已发货", "address":"北京市海淀区...", "date":"2026-07-01"},
     {"order_id":"ORD002", "product":"MacBook Pro", "status":"待发货", "address":"上海市浦东区...", "date":"2026-07-02"},
     {"order_id":"ORD003", "product":"AirPods Pro", "status":"已签收", "address":"广州市天河区...", "date":"2026-06-28"}
 ]
 ```
 
 ### 9.2 创建客服 agent（7月2日-3日）
 
 新建 `D:\agent-learning\ecommerce_agent\customer_service.py`
 
 核心代码结构：
 ```python
 import json
 from openai import OpenAI
 
 client = OpenAI(api_key="sk-...", base_url="https://api.deepseek.com")
 
 # 加载数据
 with open("products.json", encoding="utf-8") as f:
     products = json.load(f)
 with open("orders.json", encoding="utf-8") as f:
     orders = json.load(f)
 
 # 工具函数
 def search_product(keyword):
     """按关键词搜索商品"""
     results = [p for p in products if keyword in p["name"]]
     return json.dumps(results, ensure_ascii=False)
 
 def check_order(order_id):
     """查询订单状态"""
     for o in orders:
         if o["order_id"] == order_id:
             return json.dumps(o, ensure_ascii=False)
     return json.dumps({"error": "订单不存在"})
 
 def get_return_policy():
     """获取退换货政策"""
     return "收货后7天内可无理由退换，质量问题商家承担运费，非质量问题买家承担运费。"
 
 # 后面就是和 first_agent.py 一样的结构
 # 把上面的三个函数注册到 TOOLS 里
 # 把 execute 函数改成能调度这三个工具
 # run_agent 函数照抄
 ```
 
 ### 9.3 完整结构
 
 最终的 `ecommerce_agent` 结构：
 ```
 D:\agent-learning\ecommerce_agent\
 ├── customer_service.py   # 主 agent 脚本
 ├── products.json         # 商品数据
 ├── orders.json           # 订单数据
 └── knowledge_base\       # 如果有更多文档放这里
 ```
 
 不需要太多文件。等 7月7日之后再加前端和部署。
 
 ---
 
 ## 第 10 步：每天投简历（贯穿全程）
 
 ### 每天早上的动作（15 分钟）
 
 1. 打开 BOSS 直聘 App 或网页版
 2. 搜以下关键词（每天换着搜）：
    - "AI 实习生"
    - "大模型 实习生"
    - "Agent 开发"
    - "LLM 实习生"
    - "Python AI 实习生"
 3. 点"在线"筛选（在线的人回复快）
 4. 发打招呼消息：直接用 BOSS 的模板，改成这样可以提高回复率：
    ```
    您好，我有 agent 开发项目经验，做过带工具调用和 RAG 的智能客服系统，
    GitHub 项目在这里：https://github.com/你的用户名/agent-learning
    方便发简历给您看看吗？
    ```
 5. 每天投够 5 家再停
 
 ### 被拒绝了怎么办
 
 不要停。投 10 家被拒 → 继续投 10 家。这是概率问题。
 
 把 BOSS 直聘的对话当成练习。每次被拒，回一句"谢谢，如果以后有相关机会希望还能联系您"，留下好印象。
 
 ---
 
 ## 常用命令速查
 
 ```powershell
 # 终端操作
 cd D:\agent-learning          # 进入文件夹
 dir                            # 查看当前文件夹内容（Windows）
 python xxx.py                  # 运行 Python 脚本
 pip install xxx                # 安装 Python 包
 
 # Git 操作
 git status                     # 查看哪些文件改过了
 git add .                      # 添加所有改动
 git commit -m "说明"           # 提交
 git push                       # 推送到 GitHub
 git pull                       # 从 GitHub 拉取最新代码
 ```
 
 ---
 
 ## 遇到问题怎么办
 
 1. **看报错信息的最后一行** — 那行通常会告诉你问题是什么
 2. **把报错复制到百度搜一下** — 95% 的问题别人已经遇到过
 3. **如果还搞不定** — 截图发给我，带着你的文件路径和报错信息
 
 现在就开始：打开 https://platform.deepseek.com 注册拿 key。
