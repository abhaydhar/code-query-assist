import chromadb
from sentence_transformers import SentenceTransformer
from typing import List


class VectorIndexer:
    def __init__(self, persist_dir: str = "./chroma_db"):
        self.embedding_model = SentenceTransformer('codebert-base')
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection("code_vectors")

    def index_code(self, code_chunks: List[str], metadata: List[dict]):
        """Index code chunks with metadata"""
        embeddings = self.embedding_model.encode(code_chunks).tolist()
        ids = [str(hash(chunk)) for chunk in code_chunks]

        self.collection.add(
            embeddings=embeddings,
            documents=code_chunks,
            metadatas=metadata,
            ids=ids
        )

    def search(self, query: str, top_k: int = 5):
        """Semantic search over codebase"""
        query_embedding = self.embedding_model.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        return results['documents'][0]