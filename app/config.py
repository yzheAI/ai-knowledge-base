from dotenv import load_dotenv
import os
load_dotenv()

UPLOAD_DIR = "app/data/uploads"
INDEX_PATH = "app/data/faiss.index"
TEXT_PATH = "app/data/texts.pkl"
API_KEY = os.getenv("DASHSCOPE_API_KEY")
