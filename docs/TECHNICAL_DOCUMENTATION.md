# SDN302 AI Assistant - Technical Documentation

## Overview

The SDN302 AI Assistant is a sophisticated Streamlit-based application that serves as an intelligent learning companion for the SDN302 NodeJS course. It combines Retrieval Augmented Generation (RAG) with GitHub Models API integration to provide contextual, educational responses based on uploaded course materials.

## Architecture

### Core Components

1. **Frontend**: Streamlit web interface
2. **Document Processing**: Multi-format file processing (PDF, TXT, DOCX)
3. **Vector Database**: FAISS/TF-IDF based semantic search
4. **Language Model**: GitHub Models API with mock fallback
5. **RAG Engine**: Retrieval Augmented Generation pipeline

### Technology Stack

- **Python 3.12+**
- **Streamlit**: Web application framework
- **FAISS**: Vector similarity search (with TF-IDF fallback)
- **SentenceTransformers**: Text embeddings (with scikit-learn fallback)
- **PyPDF2**: PDF document processing
- **python-docx**: Word document processing
- **GitHub Models API**: Large language model inference

## Features

### ✅ Implemented Features

1. **Multi-format Document Upload**
   - PDF files processing
   - TXT files processing  
   - DOCX files processing
   - Automatic text chunking and preprocessing

2. **Semantic Search**
   - FAISS vector database (when available)
   - TF-IDF fallback for offline operation
   - Similarity-based content retrieval

3. **RAG (Retrieval Augmented Generation)**
   - Context-aware responses
   - Combines uploaded course materials with AI knowledge
   - Intelligent content ranking and selection

4. **GitHub Models API Integration**
   - Full AI capabilities when token is provided
   - Mock responses for demo mode
   - Error handling and fallback mechanisms

5. **Interactive Chat Interface**
   - Real-time conversation
   - Chat history persistence
   - Code syntax highlighting
   - Markdown rendering

6. **Course Content Management**
   - Document upload tracking
   - Knowledge base management
   - Clear/reset functionality

### 🔄 Fallback Mechanisms

The application is designed to work in multiple modes:

1. **Full Mode**: With GitHub token and internet access
   - Uses GitHub Models API for responses
   - Downloads SentenceTransformer models
   - FAISS vector search

2. **Demo Mode**: Without GitHub token
   - Mock AI responses with educational content
   - Still supports document upload and search
   - TF-IDF based similarity search

3. **Offline Mode**: Without internet access
   - Local TF-IDF vectorization
   - Mock responses
   - Full document processing capabilities

## Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/phucpt10/SDN302-Assistant.git
cd SDN302-Assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your GitHub token
echo "GITHUB_TOKEN=your_github_token_here" > .env
```

### 4. Run Application
```bash
# Using the startup script
./start.sh

# Or directly with Streamlit
streamlit run app.py
```

## Usage Guide

### Getting Started

1. **Access the Application**
   - Open http://localhost:8501 in your browser
   - The interface loads with sidebar and main chat area

2. **Configure API Access** (Optional)
   - Enter GitHub Personal Access Token in sidebar
   - Without token: Demo mode with mock responses
   - With token: Full AI capabilities

3. **Upload Course Materials**
   - Use the file uploader in the sidebar
   - Supports PDF, TXT, and DOCX files
   - Files are automatically processed and indexed

4. **Start Asking Questions**
   - Type questions in the chat input
   - Get contextual responses based on uploaded content
   - Receive educational explanations with code examples

### Example Interactions

#### Without Uploaded Content
- **User**: "What is NodeJS?"
- **Assistant**: Provides general NodeJS explanation with code examples

#### With Uploaded Course Materials
- **User**: "How does the event loop work?"
- **Assistant**: Combines relevant course content with comprehensive explanation

## File Structure

```
SDN302-Assistant/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── start.sh                       # Startup script
├── .env.example                   # Environment variables template
├── utils/                         # Core utility modules
│   ├── __init__.py
│   ├── document_processor.py      # Document parsing and chunking
│   ├── vector_store.py           # FAISS vector database with fallback
│   ├── github_client.py          # GitHub Models API client with mock
│   ├── rag_engine.py             # RAG pipeline implementation
│   ├── vector_store_fallback.py  # TF-IDF fallback implementation
│   └── github_client_fallback.py # Mock client implementation
├── sample_content/               # Example course materials
│   ├── nodejs_fundamentals.txt
│   └── lab1_express.txt
├── docs/                        # Documentation
│   └── screenshots/            # Application screenshots
├── test_functionality.py       # Integration tests
├── test_fallback.py           # Fallback implementation tests
└── README.md                  # Project documentation
```

## Technical Implementation Details

### Document Processing Pipeline

1. **File Upload**: Streamlit file uploader accepts multiple formats
2. **Format Detection**: Based on file extension (.pdf, .txt, .docx)
3. **Text Extraction**: Format-specific parsers extract raw text
4. **Text Cleaning**: Remove excess whitespace, normalize encoding
5. **Chunking**: Split into overlapping chunks (1000 chars, 200 char overlap)
6. **Indexing**: Add to vector store for similarity search

### RAG Implementation

1. **Query Processing**: User input is processed and normalized
2. **Retrieval**: Similarity search finds relevant document chunks
3. **Context Selection**: Top-k results filtered by similarity threshold
4. **Prompt Construction**: Combine query + context for LLM
5. **Generation**: LLM generates response using context
6. **Response Formatting**: Markdown rendering with code highlighting

### Vector Search Strategy

**Primary (FAISS)**:
- Uses SentenceTransformer embeddings
- Cosine similarity search
- High accuracy semantic matching

**Fallback (TF-IDF)**:
- Scikit-learn TfidfVectorizer
- Works offline without external models
- Good performance for keyword matching

## API Integration

### GitHub Models API

The application integrates with GitHub's AI models service:

```python
# Configuration
BASE_URL = "https://models.inference.ai.azure.com"
MODEL = "gpt-4o-mini"

# Authentication
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}
```

### Mock Implementation

For demo mode, the application provides educational mock responses:

- NodeJS concepts and explanations
- Code examples and best practices  
- Course-relevant information
- Clear indication of mock mode

## Testing

### Test Coverage

1. **Document Processing Tests**
   - PDF, TXT, DOCX file parsing
   - Text chunking and cleaning
   - Error handling for corrupted files

2. **Vector Store Tests**
   - FAISS index creation and search
   - TF-IDF fallback functionality
   - Similarity scoring accuracy

3. **API Client Tests**
   - GitHub Models API integration
   - Mock client responses
   - Error handling and fallbacks

4. **RAG Pipeline Tests**
   - End-to-end query processing
   - Context retrieval accuracy
   - Response generation quality

### Running Tests

```bash
# Full functionality test (requires internet)
python test_functionality.py

# Fallback implementation test (offline)
python test_fallback.py
```

## Deployment

### Local Development
```bash
streamlit run app.py --server.headless false
```

### Production Deployment
```bash
streamlit run app.py --server.headless true --server.port 8501
```

### Docker Deployment (Optional)
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py", "--server.headless", "true"]
```

## Performance Considerations

### Memory Usage
- Vector embeddings stored in memory
- Large documents may require chunking limits
- Session state management for multiple users

### Response Time
- FAISS search: ~10-50ms for moderate datasets
- TF-IDF search: ~5-20ms for small datasets  
- LLM inference: ~1-5 seconds via API

### Scalability
- Stateless design supports horizontal scaling
- Vector index can be persisted to disk
- API rate limiting considerations

## Security & Privacy

### Data Handling
- Uploaded documents processed locally
- No persistent storage of sensitive content
- Session-based data management

### API Security
- GitHub token validation
- Request timeout and retry logic
- Error message sanitization

### Input Validation
- File type restrictions
- File size limits (200MB default)
- Input sanitization for chat queries

## Future Enhancements

### Planned Features
1. **Enhanced Document Support**
   - PowerPoint presentations (PPTX)
   - Markdown files
   - Code file analysis

2. **Advanced Search**
   - Semantic filters
   - Date-based queries
   - Multi-document search

3. **User Experience**
   - Dark/light theme toggle
   - Export chat history
   - Bookmark important responses

4. **Analytics**
   - Usage statistics
   - Query performance metrics
   - User engagement tracking

### Technical Improvements
- Persistent vector storage
- Incremental indexing
- Batch document processing
- Advanced chunking strategies

## Troubleshooting

### Common Issues

1. **Module Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **GitHub API Authentication**
   - Verify token validity
   - Check API rate limits
   - Ensure proper permissions

3. **Document Upload Failures**
   - Check file format support
   - Verify file size limits
   - Test with sample documents

4. **Vector Search Issues**
   - Monitor memory usage
   - Check embedding model availability
   - Verify TF-IDF fallback

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Submit pull request

### Code Standards
- PEP 8 compliance
- Type hints for public APIs
- Comprehensive docstrings
- Unit test coverage

---

**Built for SDN302 NodeJS Course**  
*AI-powered learning companion with RAG capabilities*