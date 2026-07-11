from dotenv import load_dotenv
import os
load_dotenv()

UPLOAD_DIR = "app/data/uploads"
INDEX_PATH = "app/data/faiss.index"
TEXT_PATH = "app/data/texts.pkl"
API_KEY = os.getenv("DASHSCOPE_API_KEY")
EMBEDDING_MODEL = "shibing624/text2vec-base-chinese"
LLM_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
RERANK_MODEL_PATH = "./models/rerank"
DEVICE = "cpu"
SEARCH_TOP_K = 10
RERANK_TOP_K = 3
