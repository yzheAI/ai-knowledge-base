AI Knowledge Base Architecture Notes


## 为什么需要 VectorStore？
如果没有封装，faiss_index,texts,metadata,bm25 将会分散在不同的地方，
会导致：数据管理困难、多知识库无法隔离、代码复用困难。
因此设计 VectorStore，并且一个 VectorStore 对应一个知识库

## 为什么需要 Manager？
对于单知识库，无需使用 Manager 对实例进行管理，
但是多知识库：copper_base,medical,legal，这些都需要Faiss，BM25，metadata。
如果不使用 Manager，会出现: 数据混合、index 覆盖、查询错误
因此使用 VectorStoreManager 对多个知识库进行管理，通过 kb_name 找到对应的实例

## 为什么 BM25 放在 VectorStore 内？
因为 BM25 和 FAISS 属于同一个知识库的数据，
必须保证它们之间的对应一致，如果使用 BM25 独立管理，容易出现数据错位

## 一次查询经过哪些模块？
User Query
    ↓
FastAPI
    ↓
Retriever
    ↓
KnowledgeManager
    ↓
VectorStore
    ↓
Faiss semantic search
    +
BM25 keyword search
    ↓
Deduplication
    ↓
CrossEncoder Rerank
    ↓
Prompt Builder
    ↓
Qwen
    ↓
Answer + Source


## 数据生命周期
### 上传
PDF/TXT
↓
Parser
↓
Chunk
↓
Embedding
↓
VectorStore.add()
↓
Faiss 保存
↓
BM25 保存
↓
texts.pkl 保存


### 查询
query
↓
加载对应 kb
↓
retrieve
↓
生成答案


