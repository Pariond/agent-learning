import streamlit as st
from datetime import datetime
from agent_core import chat
import db_manager

st.set_page_config(page_title="电商智能客服", page_icon="🛒")
st.title("🛒 电商智能客服")

if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("session_%m%d_%H%M%S")
if "msgs" not in st.session_state:
    st.session_state.msgs = [{"role":"system","content":"你是电商客服助手，可查商品、订单、退换货、售后等。用中文回答。"}]
if "history" not in st.session_state:
    st.session_state.history = []

# 显示历史消息
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 用户输入
if prompt := st.chat_input("请输入你的问题...", key="chat_main"):
    st.chat_message("user").markdown(prompt)
    st.session_state.history.append({"role":"user","content":prompt})
    try: db_manager.save_message(st.session_state.session_id, "user", prompt)
    except: pass
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                reply, st.session_state.msgs = chat(prompt, st.session_state.msgs)
                st.markdown(reply)
                st.session_state.history.append({"role":"assistant","content":reply})
                try: db_manager.save_message(st.session_state.session_id, "assistant", reply)
                except: pass
            except Exception as e:
                st.error(f"出错了: {e}")

# 侧边栏
with st.sidebar:
    st.markdown("### 💬 当前会话")
    st.caption(st.session_state.session_id)
    st.divider()

    # 历史会话列表
    st.markdown("### 📋 历史会话")
    try:
        sessions = db_manager.get_all_sessions()
        if sessions:
            for i, s in enumerate(sessions[:10]):
                label = f"{s['time'][:16]} ({s['id']})"
                if st.button(label, use_container_width=True, key=f"session_{i}_{s['id']}"):
                    st.session_state["target_session"] = s["id"]
        else:
            st.caption("暂无历史记录")
    except:
        st.caption("数据库不可用")
    st.divider()

    # 历史会话预览
    if "target_session" in st.session_state and st.session_state["target_session"]:
        sid = st.session_state["target_session"]
        st.markdown(f"**会话: {sid}**")
        records = db_manager.get_history(sid)
        for r in records:
            with st.chat_message(r["role"]):
                content = r["content"][:100] + "..." if len(r["content"]) > 100 else r["content"]
                st.markdown(content)
        if st.button("关闭预览", use_container_width=True, key="close_preview"):
            st.session_state["target_session"] = ""
            st.rerun()

    # 清空按钮
    if st.button("🗑️ 清空对话", use_container_width=True, key="btn_clear"):
        st.session_state.msgs = [{"role":"system","content":"你是电商客服助手。用中文回答。"}]
        st.session_state.history = []
        st.session_state.session_id = datetime.now().strftime("session_%m%d_%H%M%S")
        st.rerun()


    # 建议问题（用索引防key重复，彻底解决报错）
    st.markdown("### 💡 试试问")
    questions = ["iPhone 15 多少钱？","查订单 ORD001","能开发票吗？","保修期多久？","怎么查物流？"]
    for i, q in enumerate(questions):
        if st.button(q, use_container_width=True, key=f"q_btn_{i}"):
            st.session_state.history.append({"role":"user","content":q})
            try: db_manager.save_message(st.session_state.session_id, "user", q)
            except: pass
            reply, st.session_state.msgs = chat(q, st.session_state.msgs)
            st.session_state.history.append({"role":"assistant","content":reply})
            try: db_manager.save_message(st.session_state.session_id, "assistant", reply)
            except: pass
            st.rerun()