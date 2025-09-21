# SDN302 AI Assistant

A Streamlit-based AI Assistant for the SDN302 NodeJS course that provides intelligent support through Retrieval Augmented Generation (RAG), integrates with GitHub Models API, and allows uploading course content for semantic search.

## Features

- 🤖 **AI-Powered Chat Interface**: Interactive chat with course-specific AI assistant
- 📚 **RAG (Retrieval Augmented Generation)**: Upload and query course materials intelligently
- 🔍 **Semantic Search**: Find relevant information from uploaded course content
- 🌐 **GitHub Models API Integration**: Leverages advanced language models
- 📄 **Multi-format Support**: Upload PDF, TXT, and DOCX files
- 💾 **Persistent Knowledge Base**: Maintains uploaded content across sessions

## Installation

1. Clone the repository:
```bash
git clone https://github.com/phucpt10/SDN302-Assistant.git
cd SDN302-Assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your GitHub token
```

4. Run the application:
```bash
streamlit run app.py
```

## Configuration

Create a `.env` file with the following variables:
- `GITHUB_TOKEN`: Your GitHub Personal Access Token for GitHub Models API

## Usage

1. **Upload Course Content**: Use the sidebar to upload PDF, TXT, or DOCX files containing course materials
2. **Ask Questions**: Type questions about NodeJS, the course content, or request help with labs
3. **Get Contextual Answers**: The AI will provide answers based on uploaded course materials and general knowledge

## Technology Stack

- **Frontend**: Streamlit
- **LLM**: GitHub Models API
- **Vector Database**: FAISS
- **Embeddings**: SentenceTransformers
- **Document Processing**: PyPDF2, python-docx
- **Framework**: LangChain

## Course Support

This assistant is specifically designed to help with:
- NodeJS fundamentals and advanced concepts
- Laboratory exercises and assignments
- Course material explanations
- Code examples and debugging
- Best practices and patterns

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is for educational purposes as part of the SDN302 course.
