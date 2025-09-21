import os
from typing import Optional, Dict, Any

class MockGitHubModelsClient:
    """Mock client for GitHub Models API when token is not available"""
    
    def __init__(self):
        self.model = "mock-gpt-4o-mini"
        print("⚠️ Using mock GitHub Models client (no token provided)")
    
    def generate_response(
        self, 
        user_message: str, 
        system_message: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """Generate a mock response"""
        
        # Simple keyword-based responses for demonstration
        user_lower = user_message.lower()
        
        if "nodejs" in user_lower or "node.js" in user_lower:
            return """NodeJS is a JavaScript runtime built on Chrome's V8 JavaScript engine that allows you to run JavaScript on the server side. 

Key features include:
- Event-driven, non-blocking I/O model
- Single-threaded with event loop
- Large ecosystem (npm)
- Cross-platform compatibility

Example of a simple HTTP server:
```javascript
const http = require('http');
const server = http.createServer((req, res) => {
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.end('Hello World!');
});
server.listen(3000);
```

💡 This is a mock response. Please provide a GitHub token for full AI functionality."""

        elif "express" in user_lower:
            return """Express.js is a minimal and flexible NodeJS web framework that provides robust features for web and mobile applications.

Basic Express server:
```javascript
const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.send('Hello Express!');
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
```

Key concepts:
- Routing
- Middleware
- Template engines
- Error handling

💡 This is a mock response. Please provide a GitHub token for full AI functionality."""

        elif "module" in user_lower:
            return """NodeJS uses the CommonJS module system for organizing code.

Exporting modules:
```javascript
// math.js
exports.add = (a, b) => a + b;
// or
module.exports = { add: (a, b) => a + b };
```

Importing modules:
```javascript
const { add } = require('./math');
const math = require('./math');
```

ES6 modules are also supported with .mjs files or "type": "module" in package.json.

💡 This is a mock response. Please provide a GitHub token for full AI functionality."""

        elif "lab" in user_lower or "assignment" in user_lower:
            return """For lab assignments in SDN302, focus on:

1. **Basic Setup**: Create project structure with npm init
2. **Express Routes**: Implement GET, POST, PUT, DELETE endpoints
3. **Middleware**: Add logging, parsing, error handling
4. **Database**: Connect to MongoDB or SQL database
5. **Testing**: Use tools like Postman or curl

Common lab topics:
- Building REST APIs
- Authentication implementation
- Database integration
- Error handling
- Input validation

💡 This is a mock response. Please provide a GitHub token for full AI functionality."""

        else:
            return f"""I understand you're asking about: "{user_message}"

For SDN302 NodeJS course, I can help with:
- NodeJS fundamentals and core concepts
- Express.js framework development
- Database integration techniques
- API development best practices
- Lab assignments and exercises

💡 This is a mock response. Please provide a GitHub token in the sidebar for full AI functionality with contextual responses."""
    
    def generate_with_context(
        self,
        user_message: str,
        context: str,
        system_message: Optional[str] = None
    ) -> str:
        """Generate response with additional context for RAG"""
        
        if context.strip():
            response = f"""Based on your uploaded course materials, here's the answer to: "{user_message}"

**📚 Relevant Context from Course Materials:**
{context[:400]}{'...' if len(context) > 400 else ''}

**💡 Answer:**
{self.generate_response(user_message, system_message)}

This response combines your uploaded content with educational explanations. Provide a GitHub token for enhanced AI capabilities."""
        else:
            response = self.generate_response(user_message, system_message)
        
        return response
    
    def test_connection(self) -> Dict[str, Any]:
        """Test the connection (always returns success for mock)"""
        return {
            "success": True,
            "status_code": 200,
            "message": "Mock connection successful"
        }

class GitHubModelsClient:
    """Client for GitHub Models API with fallback to mock"""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.token = os.getenv("GITHUB_TOKEN")
        
        # Check if we have a valid token
        if not self.token or self.token == "your_github_token_here" or self.token.strip() == "":
            self.mock_client = MockGitHubModelsClient()
            self.use_mock = True
            return
        
        # Try to use real GitHub Models API
        try:
            import requests
            
            self.base_url = "https://models.inference.ai.azure.com"
            self.headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            self.use_mock = False
            print(f"✅ Using GitHub Models API with model: {model}")
        except ImportError:
            print("⚠️ requests module not available, using mock client")
            self.mock_client = MockGitHubModelsClient()
            self.use_mock = True
    
    def generate_response(
        self, 
        user_message: str, 
        system_message: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> str:
        """Generate a response using GitHub Models API or mock"""
        
        if self.use_mock:
            return self.mock_client.generate_response(user_message, system_message, max_tokens, temperature)
        
        import requests
        
        messages = []
        
        if system_message:
            messages.append({
                "role": "system",
                "content": system_message
            })
        
        messages.append({
            "role": "user", 
            "content": user_message
        })
        
        payload = {
            "messages": messages,
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                error_msg = f"API Error {response.status_code}: {response.text}"
                
                # Handle specific error cases
                if response.status_code == 401:
                    return "❌ Authentication failed. Please check your GitHub token."
                elif response.status_code == 429:
                    return "⏳ Rate limit exceeded. Please try again in a moment."
                elif response.status_code == 500:
                    return "🔧 GitHub Models API is experiencing issues. Please try again later."
                else:
                    return f"❌ Error: {error_msg}"
                    
        except requests.exceptions.Timeout:
            return "⏰ Request timed out. Please try again."
        except requests.exceptions.ConnectionError:
            return "🌐 Connection error. Please check your internet connection."
        except Exception as e:
            return f"❌ Unexpected error: {str(e)}"
    
    def generate_with_context(
        self,
        user_message: str,
        context: str,
        system_message: Optional[str] = None
    ) -> str:
        """Generate response with additional context for RAG"""
        
        if self.use_mock:
            return self.mock_client.generate_with_context(user_message, context, system_message)
        
        enhanced_message = f"""Context from course materials:
{context}

Question: {user_message}

Please answer the question based on the provided context and your knowledge of NodeJS. If the context doesn't contain relevant information, use your general knowledge but mention that you're drawing from general NodeJS knowledge."""
        
        if not system_message:
            system_message = """You are an AI assistant specialized in NodeJS and web development for the SDN302 course. 
            Use the provided context from course materials when relevant, and supplement with your general NodeJS knowledge.
            Always provide clear, educational explanations with practical examples.
            Focus on helping students understand concepts and complete their assignments."""
        
        return self.generate_response(
            enhanced_message, 
            system_message,
            max_tokens=1500,
            temperature=0.6
        )
    
    def test_connection(self) -> Dict[str, Any]:
        """Test the connection to GitHub Models API"""
        if self.use_mock:
            return self.mock_client.test_connection()
        
        import requests
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "messages": [{"role": "user", "content": "Hello"}],
                    "model": self.model,
                    "max_tokens": 10
                },
                timeout=10
            )
            
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "message": "Connection successful" if response.status_code == 200 else response.text
            }
            
        except Exception as e:
            return {
                "success": False,
                "status_code": None,
                "message": str(e)
            }