"""
Streamlit 前端 — 电商客服（Mysql对话记录保存,Rag文档）
"""

import streamlit as st
from datetime import datetime
from agent_core import chat
from db_manager import save_message, get_all_sessions, get_history, delete_session

st.set_page_config(page_title="电商智能客服", page_icon="🛒")
st.title("🛒 电商智能客服")

# ============================================================
# 初始化
# ============================================================
if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("session_%m%d_%H%M%S")
if "msgs" not in st.session_state:
    st.session_state.msgs = [{"role":"system","content":"你是电商客服助手，可查商品、订单、退换货、售后等。用中文回答。"}]
if "history" not in st.session_state:
    st.session_state.history = []

# ============================================================
# 显示对话
# ============================================================
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ============================================================
# 用户输入
# ============================================================
if prompt := st.chat_input("请输入你的问题..."):
    # 显示用户消息
    st.chat_message("user").markdown(prompt)
    st.session_state.history.append({"role":"user","content":prompt})
    save_message(st.session_state.session_id, "user", prompt)

    # 调用 agent
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                reply, st.session_state.msgs = chat(prompt, st.session_state.msgs)
                st.markdown(reply)
                st.session_state.history.append({"role":"assistant","content":reply})
                save_message(st.session_state.session_id, "assistant", reply)
            except Exception as e:
                st.error(f"出错了: {e}")
                st.session_state.history.append({"role":"assistant","content":f"出错了，请检查 API Key 和网络"})

# ============================================================
# 侧边栏
# ============================================================
with st.sidebar:
    st.markdown("### 💬 当前会话")
    st.caption(st.session_state.session_id)

    st.divider()
    st.markdown("### 📋 历史会话")
    sessions = get_all_sessions()
    if sessions:
        for s in sessions[:10]:  # 只显示最近 10 个
            label = f"{s['time'][:16]} ({s['id']})"
            if st.button(label, use_container_width=True, key=s["id"]):
                st.session_state["target_session"] = s["id"]
    else:
        st.caption("暂无历史记录")

    if "target_session" in st.session_state and st.session_state["target_session"]:
        sid = st.session_state["target_session"]
        st.divider()
        st.markdown(f"**会话: {sid}**")
        records = get_history(sid)
        for r in records:
            with st.chat_message(r["role"]):
                st.markdown(r["content"][:100] + "..." if len(r["content"])>100 else r["content"])
        if st.button("关闭预览", use_container_width=True):
            st.session_state["target_session"] = ""
            st.rerun()

    st.divider()
    st.markdown("### 🧹")
    if st.button("🗑️ 清空当前对话", use_container_width=True):
        st.session_state.msgs = [{"role":"system","content":"你是电商客服助手。用中文回答。"}]
        st.session_state.history = []
        st.session_state.session_id = datetime.now().strftime("session_%m%d_%H%M%S")
        st.rerun()

    st.markdown("### 💡 试试问")
    for q in ["iPhone 15 多少钱？","查订单 ORD001","能开发票吗？","保修期多久？","怎么查物流？"]:
        if st.button(q, use_container_width=True, key="q_"+q):
            st.session_state.history.append({"role":"user","content":q})
            save_message(st.session_state.session_id, "user", q)
            reply, st.session_state.msgs = chat(q, st.session_state.msgs)
            st.session_state.history.append({"role":"assistant","content":reply})
            save_message(st.session_state.session_id, "assistant", reply)
            st.rerun()
