import numpy as np
from typing import List, Tuple, Optional
import pickle
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimpleTfIdfVectorStore:
    """Simple TF-IDF based vector store for semantic search (fallback when sentence-transformers unavailable)"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            max_df=0.8,
            min_df=1  # Allow single occurrence words
        )
        self.texts = []
        self.vectors = None
        self.is_fitted = False
    
    def add_texts(self, texts: List[str], metadatas: Optional[List[dict]] = None):
        """Add texts to the vector store"""
        if not texts:
            return
        
        self.texts.extend(texts)
        
        # Fit and transform all texts
        try:
            all_texts = self.texts
            self.vectors = self.vectorizer.fit_transform(all_texts)
            self.is_fitted = True
            print(f"✅ TF-IDF vectorizer fitted with {len(all_texts)} documents")
        except Exception as e:
            print(f"❌ Error fitting TF-IDF vectorizer: {e}")
    
    def similarity_search(self, query: str, k: int = 4) -> List[Tuple[str, float]]:
        """Search for similar texts using TF-IDF cosine similarity"""
        if not self.is_fitted or not self.texts:
            return []
        
        try:
            # Transform query
            query_vector = self.vectorizer.transform([query])
            
            # Calculate similarities
            similarities = cosine_similarity(query_vector, self.vectors).flatten()
            
            # Get top k results
            top_indices = similarities.argsort()[-k:][::-1]
            
            results = []
            for idx in top_indices:
                if idx < len(self.texts) and similarities[idx] > 0.01:  # Minimum similarity threshold
                    results.append((self.texts[idx], float(similarities[idx])))
            
            return results
            
        except Exception as e:
            print(f"❌ Error in similarity search: {e}")
            return []
    
    def get_relevant_context(self, query: str, max_context_length: int = 2000) -> str:
        """Get relevant context for RAG"""
        results = self.similarity_search(query, k=6)
        
        if not results:
            return ""
        
        # Combine relevant texts
        context_parts = []
        current_length = 0
        
        for text, score in results:
            # Only include if similarity score is reasonable
            if score > 0.1:  # Lower threshold for TF-IDF
                if current_length + len(text) <= max_context_length:
                    context_parts.append(text)
                    current_length += len(text)
                else:
                    # Add partial text if it fits
                    remaining_space = max_context_length - current_length
                    if remaining_space > 100:
                        context_parts.append(text[:remaining_space])
                    break
        
        return "\n\n".join(context_parts)

try:
    from sentence_transformers import SentenceTransformer
    import faiss
    
    class VectorStore:
        """FAISS-based vector store for semantic search"""
        
        def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
            self.model_name = model_name
            try:
                self.encoder = SentenceTransformer(model_name)
                self.dimension = self.encoder.get_sentence_embedding_dimension()
                
                # Initialize FAISS index
                self.index = faiss.IndexFlatIP(self.dimension)
                self.texts = []
                self.metadata = []
                self.use_faiss = True
                print(f"✅ Using FAISS vector store with model: {model_name}")
                
            except Exception as e:
                print(f"⚠️ Could not initialize sentence-transformers: {e}")
                print("🔄 Falling back to TF-IDF vector store")
                self.fallback_store = SimpleTfIdfVectorStore()
                self.use_faiss = False
        
        def add_texts(self, texts: List[str], metadatas: Optional[List[dict]] = None):
            """Add texts to the vector store"""
            if not texts:
                return
            
            if not self.use_faiss:
                return self.fallback_store.add_texts(texts, metadatas)
            
            # Generate embeddings
            embeddings = self.encoder.encode(texts, convert_to_tensor=False)
            
            # Normalize for cosine similarity
            embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
            
            # Add to FAISS index
            self.index.add(embeddings.astype('float32'))
            
            # Store texts and metadata
            self.texts.extend(texts)
            if metadatas:
                self.metadata.extend(metadatas)
            else:
                self.metadata.extend([{} for _ in texts])
        
        def similarity_search(self, query: str, k: int = 4) -> List[Tuple[str, float]]:
            """Search for similar texts"""
            if not self.use_faiss:
                return self.fallback_store.similarity_search(query, k)
            
            if self.index.ntotal == 0:
                return []
            
            # Encode query
            query_embedding = self.encoder.encode([query], convert_to_tensor=False)
            query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
            
            # Search
            scores, indices = self.index.search(query_embedding.astype('float32'), k)
            
            # Return results
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < len(self.texts):
                    results.append((self.texts[idx], float(score)))
            
            return results
        
        def get_relevant_context(self, query: str, max_context_length: int = 2000) -> str:
            """Get relevant context for RAG"""
            if not self.use_faiss:
                return self.fallback_store.get_relevant_context(query, max_context_length)
            
            results = self.similarity_search(query, k=6)
            
            if not results:
                return ""
            
            # Combine relevant texts
            context_parts = []
            current_length = 0
            
            for text, score in results:
                # Only include if similarity score is reasonable
                threshold = 0.3 if self.use_faiss else 0.1
                if score > threshold:
                    if current_length + len(text) <= max_context_length:
                        context_parts.append(text)
                        current_length += len(text)
                    else:
                        # Add partial text if it fits
                        remaining_space = max_context_length - current_length
                        if remaining_space > 100:
                            context_parts.append(text[:remaining_space])
                        break
            
            return "\n\n".join(context_parts)

except ImportError:
    print("⚠️ sentence-transformers or faiss-cpu not available, using TF-IDF fallback")
    
    # Use simple TF-IDF store as main VectorStore
    VectorStore = SimpleTfIdfVectorStore