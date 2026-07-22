from dotenv import load_dotenv
from pathlib import Path
import os
load_dotenv()

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 数据目录
DATA_DIR = BASE_DIR / "data"

# 模型目录
MODEL_DIR = BASE_DIR / "models"

API_KEY = os.getenv("DASHSCOPE_API_KEY")

EMBEDDING_MODEL = "shibing624/text2vec-base-chinese"

LLM_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

RERANK_MODEL_PATH = MODEL_DIR / "models/BAAI--bge-reranker-base/snapshots/master"

DEVICE = "cpu"
SEARCH_TOP_K = 10
RERANK_TOP_K = 3
EMBEDDING_DIM = 768

JSON_PATH = BASE_DIR / "app/data/dataset.json"
KNOWLEDGE_BASE_PATH = DATA_DIR / "knowledge_bases"
SAVE_JSON_PATH = BASE_DIR / "app/evaluation/results/retrieval_result.json"
