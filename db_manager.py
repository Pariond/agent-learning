"""
数据库管理模块
封装了所有 MySQL 操作，供 agent_core.py 和 app.py 调用。
"""

import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()   #导入环境变量Mysql_password
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": "ecommerce_agent"
}


def save_message(session_id: str, role: str, content: str):
    """保存一条对话记录到 MySQL"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_history (session_id, role, content) VALUES (%s, %s, %s)",
        (session_id, role, content)
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_history(session_id: str) -> list:
    """读取某个会话的全部对话记录"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT role, content, timestamp FROM chat_history WHERE session_id = %s ORDER BY id",
        (session_id,)
    )
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records


def get_all_sessions() -> list:
    """获取所有会话 ID（按时间倒序）"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT session_id, MIN(timestamp) as t FROM chat_history GROUP BY session_id ORDER BY t DESC"
    )
    sessions = [{"id": r[0], "time": str(r[1])} for r in cursor.fetchall()]
    cursor.close()
    conn.close()
    return sessions


def delete_session(session_id: str):
    """删除某个会话的全部记录"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history WHERE session_id = %s", (session_id,))
    conn.commit()
    cursor.close()
    conn.close()


def clear_all():
    """清空全部对话记录"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history")
    conn.commit()
    cursor.close()
    conn.close()
