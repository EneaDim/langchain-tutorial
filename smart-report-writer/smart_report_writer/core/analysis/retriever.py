# Minimal placeholder retriever; can expand with FAISS/PGVector later
class NullRetriever:
    def search(self, query: str):
        return []
