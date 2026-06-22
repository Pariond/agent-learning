from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 1. 读取文档
loader = TextLoader("knowledge_base.txt", encoding="utf-8")
docs = loader.load()
print(f"读取了 {len(docs)} 个文档")

# 2. 切分成小块（每 150 字一段，重叠 20 字）
splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=20,
)
chunks = splitter.split_documents(docs)
print(f"切分成 {len(chunks)} 块")

for i, c in enumerate(chunks):
    print(f"  块 {i+1}: {c.page_content[:40]}...")

# 3. 向量化并存入 ChromaDB
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db", 
)
vectorstore.persist()
print("\n知识库导入完成！存储在 chroma_db/ 文件夹")
