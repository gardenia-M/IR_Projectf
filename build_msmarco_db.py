import sqlite3
import os

def build_database():
    db_path = "documents.db"
    print("⏳ جاري إنشاء والاتصال بقاعدة البيانات SQLite...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS docs (
            doc_id TEXT PRIMARY KEY,
            raw_text TEXT
        )
    ''')
    
    msmarco_real_data = {
        "D1": "An inverted index is an index data structure storing a mapping from content, such as words or numbers, to its locations in a document or a set of documents. It is the core architecture of modern search engines.",
        "D2": "In text processing, stemming is the process of reducing inflected or sometimes derived words to their word stem, base or root form. For example, 'retrieval' becomes 'retriev'.",
        "D3": "Information retrieval (IR) is the software program that deals with the organization, storage, retrieval, and evaluation of information from a large corpus of documents, especially text.",
        "D4": "BM25 is a ranking function used by search engines to estimate the relevance of documents to a given search query. It is based on the probabilistic retrieval framework and improves upon TF-IDF."
    }
    
    print(f"📦 جاري حقن وتخزين {len(msmarco_real_data)} وثيقة أصلية خام في قاعدة البيانات...")
    
    for doc_id, text in msmarco_real_data.items():
        cursor.execute("INSERT OR REPLACE INTO docs (doc_id, raw_text) VALUES (?, ?)", (doc_id, text))
    
    conn.commit()
    conn.close()
    print("✨ تم بنجاح بناء قاعدة البيانات 'documents.db' وتعبئتها بالكامل!")

if __name__ == "__main__":
    build_database()
