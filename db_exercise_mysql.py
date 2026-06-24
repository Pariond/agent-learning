#数据库内容操作
import mysql.connector
from datetime import datetime

# 连接 MySQL
conn = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="123456",
    database="ecommerce_agent"
)
cursor = conn.cursor()
print("✅ MySQL 连接成功")

# 建表
# id 自增，会自动从 1 开始编号
cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INT AUTO_INCREMENT PRIMARY KEY,
        session_id VARCHAR(50),
        role VARCHAR(20),
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
""")
conn.commit()
print("✅ 表 chat_history 创建成功")

# 第 3 步：插入数据
sql = "INSERT INTO chat_history (session_id, role, content) VALUES (%s, %s, %s)"
cursor.execute(sql, ("session_001", "user", "iPhone 15 多少钱？"))
cursor.execute(sql, ("session_001", "assistant", "iPhone 15 售价 5999 元"))
cursor.execute(sql, ("session_002", "user", "能开发票吗？"))
cursor.execute(sql, ("session_002", "assistant", "下单时勾选需要发票即可，电子发票发到邮箱"))
conn.commit()
print("✅ 插入 4 条记录成功，最后插入的 ID:", cursor.lastrowid)

# 第 4 步：查询数据
cursor.execute(
    "SELECT id, session_id, role, content, timestamp FROM chat_history WHERE session_id = %s ORDER BY id",
    ("session_001",)
)
records = cursor.fetchall()
print(f"\n📋 session_001 的对话：")
for r in records:
    print(f"  [{r[4]}] [{r[1]}] {r[2]}: {r[3]}")

# 第 5 步：查所有 session
cursor.execute("SELECT DISTINCT session_id FROM chat_history")
sessions = cursor.fetchall()
print(f"\n📋 共有 {len(sessions)} 个会话:")
for s in sessions:
    print(f"  - {s[0]}")

# 清理：关闭连接
cursor.close()
conn.close()
print("\n连接已关闭")


