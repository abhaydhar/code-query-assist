import os

class Config:
    CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_db")
    MODEL_CACHE = os.getenv("MODEL_CACHE", "./models")
    MAX_CONTEXT_LENGTH = 4096