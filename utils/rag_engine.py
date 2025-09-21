from typing import Optional
from .vector_store import VectorStore
from .github_client import GitHubModelsClient

class RAGEngine:
    """Retrieval Augmented Generation engine combining vector search with LLM"""
    
    def __init__(self, vector_store: VectorStore, llm_client: GitHubModelsClient):
        self.vector_store = vector_store
        self.llm_client = llm_client
    
    def query(self, user_question: str, max_context_length: int = 2000) -> str:
        """Process a query using RAG approach"""
        
        # Step 1: Retrieve relevant context
        context = self.vector_store.get_relevant_context(
            user_question, 
            max_context_length
        )
        
        # Step 2: Generate response with context
        if context.strip():
            # Use context-aware generation
            response = self.llm_client.generate_with_context(
                user_message=user_question,
                context=context
            )
        else:
            # Fallback to general NodeJS knowledge
            system_prompt = """You are an AI assistant specialized in NodeJS and web development for the SDN302 course.
            The user doesn't have uploaded course materials, so answer based on your general NodeJS knowledge.
            Provide clear, educational explanations with practical examples.
            Focus on helping students understand NodeJS concepts and complete their assignments.
            
            Cover topics like:
            - NodeJS fundamentals (modules, event loop, async programming)
            - Express.js framework and middleware
            - Database integration (MongoDB, SQL)
            - RESTful APIs and web services
            - Authentication and security
            - Testing and debugging
            - NPM and package management
            - Error handling and best practices"""
            
            response = self.llm_client.generate_response(
                user_message=user_question,
                system_message=system_prompt
            )
        
        return response
    
    def get_context_preview(self, user_question: str, num_chunks: int = 3) -> list:
        """Get a preview of the context that would be used for a query"""
        results = self.vector_store.similarity_search(user_question, k=num_chunks)
        
        preview = []
        for text, score in results:
            preview.append({
                'text': text[:200] + "..." if len(text) > 200 else text,
                'similarity_score': round(score, 3),
                'length': len(text)
            })
        
        return preview
    
    def suggest_questions(self) -> list:
        """Suggest relevant questions based on uploaded content"""
        if not self.vector_store.texts:
            return [
                "What is NodeJS and how does it work?",
                "How do I create a simple Express.js server?",
                "What are the differences between synchronous and asynchronous programming in NodeJS?",
                "How do I connect NodeJS to a MongoDB database?",
                "What are middleware functions in Express.js?",
                "How do I handle errors in NodeJS applications?",
                "What is npm and how do I manage packages?",
                "How do I implement authentication in a NodeJS app?"
            ]
        
        # For now, return general questions - could be enhanced to analyze content
        return [
            "Summarize the main concepts from the uploaded materials",
            "What are the key learning objectives covered?",
            "Explain the practical examples in the course content",
            "What are the important NodeJS patterns mentioned?",
            "How do the lab exercises relate to the theory?"
        ]