"""
Startup script for the Intelligent E-commerce Chatbot System
"""

import uvicorn
import sys
import os

sys.path.append(os.path.dirname(__file__))

def main():
    """Start the intelligent chatbot API server"""
    
    print("🚀 Starting Intelligent E-commerce Chatbot API v2.0")
    print("=" * 60)
    print("📊 Features:")
    print("  • Intent scoring with keyword weighting")
    print("  • Conversation memory per user")
    print("  • Learning through unknown query logging")
    print("  • SQLite persistence")
    print("  • Context-aware responses")
    print("=" * 60)
    print("🔗 API Documentation: http://localhost:8000/docs")
    print("💾 Database: backend/chatbot_memory.db")
    print("🤖 Ready to serve intelligent conversations!")
    print("=" * 60)
    
    uvicorn.run(
        "main_intelligent:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()