"""
运行方式：
  pip install streamlit
  streamlit run app.py
"""

import streamlit as st
from agent_core import chat

# ============================================================
# 页面基础配置（只能出现一次，必须放在最顶部）
# ============================================================
st.set_page_config(page_title="电商智能客服", page_icon="🛒")
st.title("🛒 电商智能客服")
st.caption("基于 DeepSeek + RAG 的电商客服 Agent")

# ============================================================
# 初始化对话状态
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是电商客服助手。可查商品、订单、退换货、发货、售后等。用中文简洁回答。"}
    ]
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
# 存放侧边按钮点击待提问内容
if "pending_question" not in st.session_state:
    st.session_state.pending_question = None

# ============================================================
# 渲染历史对话
# ============================================================
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ============================================================
# 处理侧边栏点击提问
# ============================================================
if st.session_state.pending_question is not None:
    prompt = st.session_state.pending_question
    st.session_state.pending_question = None

    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                reply, st.session_state.messages = chat(prompt, st.session_state.messages)
                st.markdown(reply)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
            except Exception as e:
                error_msg = f"出错了: {e}"
                st.error(error_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})

# ============================================================
# 唯一用户输入框（增加唯一key，杜绝ID冲突）
# ============================================================
if prompt := st.chat_input("请输入你的问题...", key="main_chat_input"):
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                reply, st.session_state.messages = chat(prompt, st.session_state.messages)
                st.markdown(reply)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
            except Exception as e:
                error_msg = f"出错了: {e}"
                st.error(error_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})

# ============================================================
# 侧边栏（只渲染一组按钮，无重复）
# ============================================================
with st.sidebar:
    st.markdown("### 💡 试试问")
    examples = [
        "iPhone 15 多少钱？",
        "查订单 ORD001",
        "苹果15有货吗？",
        "能开发票吗？",
        "保修期多久？",
        "怎么查物流？",
    ]
    for idx, q in enumerate(examples):
        # 每个按钮绑定唯一key
        if st.button(q, use_container_width=True, key=f"example_btn_{idx}"):
            st.session_state.pending_question = q
            st.rerun()

    st.divider()
    if st.button("🗑️ 清空对话", use_container_width=True, key="clear_chat_btn"):
        st.session_state.messages = [
            {"role": "system", "content": "你是电商客服助手。可查商品、订单、退换货、发货、售后等。用中文简洁回答。"}
        ]
        st.session_state.chat_history = []
        st.rerun()