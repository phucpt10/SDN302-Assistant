import streamlit as st
import os
from dotenv import load_dotenv
import tempfile
import shutil
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="SDN302 AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = None
if "documents" not in st.session_state:
    st.session_state.documents = []

# Import custom modules
try:
    from utils.vector_store import VectorStore
    from utils.github_client import GitHubModelsClient
except ImportError:
    print("⚠️ Using fallback implementations due to missing dependencies")
    from utils.vector_store_fallback import VectorStore
    from utils.github_client_fallback import GitHubModelsClient

from utils.document_processor import DocumentProcessor
from utils.rag_engine import RAGEngine

def main():
    st.title("🤖 SDN302 AI Assistant")
    st.markdown("*Trợ lý AI thông minh cho môn học SDN302 NodeJS*")
    
    # Sidebar for file upload and configuration
    with st.sidebar:
        st.header("📚 Knowledge Base")
        
        # GitHub token configuration
        github_token = st.text_input(
            "GitHub Token", 
            value=os.getenv("GITHUB_TOKEN", ""),
            type="password",
            help="Enter your GitHub Personal Access Token for API access"
        )
        
        if github_token:
            os.environ["GITHUB_TOKEN"] = github_token
            st.success("✅ Token provided")
        else:
            st.info("💡 No token provided - using demo mode with mock responses")
        
        st.divider()
        
        # File upload section
        st.subheader("Upload Course Materials")
        uploaded_files = st.file_uploader(
            "Upload documents (PDF, TXT, DOCX)",
            type=["pdf", "txt", "docx"],
            accept_multiple_files=True,
            help="Upload course materials, slides, or lab instructions"
        )
        
        # Process uploaded files
        if uploaded_files:
            process_uploaded_files(uploaded_files)
        
        # Display current documents
        if st.session_state.documents:
            st.subheader("📄 Uploaded Documents")
            for doc in st.session_state.documents:
                st.text(f"• {doc}")
        
        # Clear knowledge base button
        if st.button("🗑️ Clear Knowledge Base"):
            clear_knowledge_base()
    
    # Main chat interface
    display_chat_interface()

def process_uploaded_files(uploaded_files):
    """Process and add uploaded files to knowledge base"""
    if not uploaded_files:
        return
    
    with st.spinner("Processing uploaded documents..."):
        try:
            # Initialize document processor
            doc_processor = DocumentProcessor()
            
            # Process each file
            new_texts = []
            for uploaded_file in uploaded_files:
                if uploaded_file.name not in st.session_state.documents:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(
                        delete=False, 
                        suffix=Path(uploaded_file.name).suffix
                    ) as tmp_file:
                        shutil.copyfileobj(uploaded_file, tmp_file)
                        tmp_path = tmp_file.name
                    
                    # Process the document
                    texts = doc_processor.process_document(tmp_path)
                    new_texts.extend(texts)
                    
                    # Add to documents list
                    st.session_state.documents.append(uploaded_file.name)
                    
                    # Clean up temporary file
                    os.unlink(tmp_path)
            
            # Update vector store if new texts were processed
            if new_texts:
                if st.session_state.knowledge_base is None:
                    st.session_state.knowledge_base = VectorStore()
                
                st.session_state.knowledge_base.add_texts(new_texts)
                st.success(f"Successfully processed {len(uploaded_files)} document(s)!")
            
        except Exception as e:
            st.error(f"Error processing documents: {str(e)}")

def clear_knowledge_base():
    """Clear the knowledge base and uploaded documents"""
    st.session_state.knowledge_base = None
    st.session_state.documents = []
    st.success("Knowledge base cleared!")

def display_chat_interface():
    """Display the main chat interface"""
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about NodeJS or your course materials..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

def generate_response(user_input):
    """Generate response using RAG if knowledge base exists, otherwise direct LLM"""
    try:
        # Initialize GitHub Models client (will use mock if no token)
        github_client = GitHubModelsClient()
        
        # Use RAG if knowledge base exists
        if st.session_state.knowledge_base is not None:
            rag_engine = RAGEngine(
                vector_store=st.session_state.knowledge_base,
                llm_client=github_client
            )
            response = rag_engine.query(user_input)
        else:
            # Direct LLM response for general NodeJS questions
            system_prompt = """You are an AI assistant specialized in NodeJS and web development. 
            You help students with the SDN302 NodeJS course by answering questions about:
            - NodeJS fundamentals and advanced concepts
            - Express.js framework
            - Database integration (MongoDB, SQL)
            - API development and RESTful services
            - Authentication and security
            - Testing and debugging
            - Best practices and design patterns
            
            Always provide clear, educational explanations with code examples when appropriate.
            Focus on practical knowledge that helps with coursework and lab assignments."""
            
            response = github_client.generate_response(user_input, system_prompt)
        
        return response
        
    except Exception as e:
        return f"❌ Error generating response: {str(e)}"

if __name__ == "__main__":
    main()