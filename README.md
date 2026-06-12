<<<<<<< HEAD
 # Agent 开发工程师学习与实习计划
 
 目标：2026 年暑假找到 agent 开发实习，大四秋招找到好工作。
 
 ## 技术栈（已决定）
 - 模型：DeepSeek（OpenAI 兼容接口）
 - Agent 框架：LangChain
 - 向量库：ChromaDB
 - 后端：FastAPI
 - 前端：Streamlit
 
 ## 阶段一：地基冲刺（6月12日 - 6月30日）
 
 ### 第 1 步（今天）
 1. 注册 DeepSeek：https://platform.deepseek.com → API Keys → 创建
 2. 注册 GitHub，创建仓库 agent-learning（Public）
 3. 安装 pip install openai，替换 first_agent.py 里的 API key，运行
 4. git add / commit / push 到 GitHub
 
 ### 第 2 步（6月13日 - 6月15日）
 读懂 first_agent.py 每一行，理解 API 调用、function calling、ReAct 循环
 
 ### 第 3 步（6月16日 - 6月20日）
 修改 first_agent.py：新增 get_time 工具、改系统提示词、加错误处理
 
 ### 第 4 步（6月21日 - 6月28日）
 学习 RAG，完成 rag_bot 项目
 pip install langchain langchain-community chromadb
 
 ## 阶段二：电商智能客服 Agent（7月1日 - 7月15日）
 
 两周完成：
 - P0：商品查询 + 订单查询 + 退换货 + 取消订单（四个工具）
 - P0：多轮对话记忆
 - P1：RAG 知识库
 - P1：Streamlit 前端
 - P2：部署上线
 
 ## 阶段三：资产沉淀 + 面试冲刺（7月15日 - 8月31日）
 
 每周：刷八股 3 天 + 投简历 2 天 + 写博客 1 天 + 复盘 1 天
 
 必写三篇文章：
 1. 《从零实现一个带 RAG 和工具调用的 Agent》
 2. 《电商智能客服 Agent 完整实践》
 3. （拿到 offer 后写经历）
 
 ## 投递策略
 
 平台：BOSS 直聘 > 实习僧 > 拉勾 > 牛客网
 关键词：AI实习生 / LLM实习生 / 大模型应用开发 / Agent开发
 数量：6月每天 5 家，7月每天 5 家，8月每天 10 家
 
 ## 面试重点
 
 Python 基础：装饰器、生成器、*args/**kwargs、GIL、浅拷贝深拷贝
 LangChain：AgentExecutor 原理、Tool/Memory/Chain 区别
 RAG：chunk/embed/retrieve/generate 五步流程、chunk 策略、hybrid search
 Agent 场景：工具超时处理、无限循环预防、幻觉控制、冲突处理
 
 ## 每天模板
 早上 30 分钟：投 5 家
 晚上 2-3 小时：写代码
 睡前 15 分钟：背 3 个面试题
=======
# agent-learning
Agent development learning project
>>>>>>> 48a4388d312b1b93e380daa7f551d86c173e6606
