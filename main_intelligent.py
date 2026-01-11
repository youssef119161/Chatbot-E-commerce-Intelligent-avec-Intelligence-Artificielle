"""
FastAPI Backend for Intelligent E-commerce Chatbot v2.0
Upgraded with intent scoring, conversation memory, and learning capabilities
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import uvicorn
import logging

# Import the new intelligent chatbot system
from intelligent_chatbot import intelligent_chatbot
from conversation_memory import conversation_memory
from intent_scorer import intent_scorer
from database import product_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Intelligent E-commerce Chatbot API",
    description="Advanced chatbot with intent scoring and conversation memory",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = "anonymous"

class ChatResponse(BaseModel):
    response: str
    products: List[Dict[str, Any]]
    confidence: float
    detected_intents: List[str]
    context_used: Dict[str, Any]
    needs_clarification: bool
    suggested_questions: List[str]
    timestamp: datetime = datetime.now()

class ProductSearchRequest(BaseModel):
    category: Optional[str] = None
    color: Optional[str] = None
    max_price: Optional[float] = None
    gender: Optional[str] = None
    age_group: Optional[str] = None
    tags: Optional[List[str]] = None

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Intelligent E-commerce Chatbot API v2.0",
        "status": "operational",
        "features": [
            "Intent scoring with keyword weighting",
            "Conversation memory per user",
            "Learning through unknown query logging",
            "SQLite persistence",
            "Context-aware responses"
        ],
        "endpoints": {
            "chat": "/chat - Main chatbot interaction",
            "products": "/products - Product search",
            "stats": "/stats - System statistics",
            "memory": "/memory/{user_id} - User conversation history",
            "intents": "/intents/test - Test intent detection"
        },
        "documentation": "/docs"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """
    Main chatbot endpoint using intelligent intent scoring
    """
    try:
        logger.info(f"Processing message from user {chat_message.user_id}: {chat_message.message}")
        
        # Validate message
        if not chat_message.message or not chat_message.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Process message through intelligent chatbot
        response = intelligent_chatbot.process_message(
            user_id=chat_message.user_id,
            message=chat_message.message
        )
        
        logger.info(f"Generated response with confidence {response.confidence:.2f}")
        
        return ChatResponse(
            response=response.message,
            products=response.products,
            confidence=response.confidence,
            detected_intents=response.detected_intents,
            context_used=response.context_used,
            needs_clarification=response.needs_clarification,
            suggested_questions=response.suggested_questions,
            timestamp=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chatbot error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")

@app.get("/products")
async def get_all_products():
    """Get all available products"""
    try:
        products = product_db.get_all_products()
        return {"products": products, "total": len(products)}
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/products/search")
async def search_products(search_request: ProductSearchRequest):
    """Advanced product search with multiple criteria"""
    try:
        # Convert request to search criteria
        criteria = {}
        
        if search_request.category:
            criteria["category"] = search_request.category
        if search_request.color:
            criteria["color"] = search_request.color
        if search_request.max_price:
            criteria["max_price"] = search_request.max_price
        if search_request.gender:
            criteria["gender"] = search_request.gender
        if search_request.age_group:
            criteria["age_group"] = search_request.age_group
        if search_request.tags:
            criteria["tags"] = search_request.tags
        
        # Perform search
        if criteria:
            products = product_db.complex_search(**criteria)
        else:
            products = product_db.get_all_products()
        
        return {
            "products": products,
            "total": len(products),
            "criteria_used": criteria
        }
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@app.get("/memory/{user_id}")
async def get_user_memory(user_id: str, limit: Optional[int] = 10):
    """Get conversation history for a specific user"""
    try:
        history = conversation_memory.get_conversation_history(user_id, limit=limit)
        context = conversation_memory.get_conversation_context(user_id)
        preferences = conversation_memory.get_user_preferences(user_id)
        
        return {
            "user_id": user_id,
            "conversation_history": [turn.to_dict() for turn in history],
            "current_context": context,
            "user_preferences": preferences,
            "total_conversations": len(history)
        }
        
    except Exception as e:
        logger.error(f"Memory error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Memory error: {str(e)}")

@app.delete("/memory/{user_id}")
async def clear_user_memory(user_id: str):
    """Clear all data for a specific user (GDPR compliance)"""
    try:
        conversation_memory.clear_user_data(user_id)
        logger.info(f"Cleared all data for user {user_id}")
        return {"message": f"All data for user {user_id} has been cleared"}
        
    except Exception as e:
        logger.error(f"Clear memory error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Clear memory error: {str(e)}")

@app.get("/stats")
async def get_system_stats():
    """Get comprehensive system statistics"""
    try:
        stats = intelligent_chatbot.get_system_stats()
        unknown_queries = conversation_memory.get_unknown_queries(limit=20)
        
        return {
            "system_stats": stats,
            "unknown_queries": unknown_queries,
            "database_stats": {
                "total_products": len(product_db.get_all_products()),
                "categories": list(set(p["category"] for p in product_db.get_all_products()))
            },
            "api_version": "2.0.0",
            "features": ["intent_scoring", "conversation_memory", "learning"]
        }
        
    except Exception as e:
        logger.error(f"Stats error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Stats error: {str(e)}")

@app.get("/intents/test")
async def test_intent_detection(message: str):
    """Test intent detection for a specific message"""
    try:
        primary_intent = intent_scorer.get_primary_intent(message)
        all_intents = intent_scorer.detect_intents(message, top_k=5)
        
        return {
            "message": message,
            "primary_intent": {
                "intent": primary_intent.intent,
                "confidence": primary_intent.confidence,
                "matched_keywords": primary_intent.matched_keywords,
                "context_data": primary_intent.context_data
            },
            "all_intents": [
                {
                    "intent": intent.intent,
                    "confidence": intent.confidence,
                    "matched_keywords": intent.matched_keywords
                }
                for intent in all_intents
            ]
        }
        
    except Exception as e:
        logger.error(f"Intent test error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Intent test error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        products_count = len(product_db.get_all_products())
        
        # Test memory system
        memory_stats = conversation_memory.get_conversation_stats()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now(),
            "chatbot": "operational",
            "database": f"connected ({products_count} products)",
            "memory": f"active ({memory_stats['total_users']} users)",
            "version": "2.0.0"
        }
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now()
        }

# Legacy compatibility endpoint (for existing frontend)
@app.post("/chatbot")
async def legacy_chatbot_endpoint(chat_message: ChatMessage):
    """
    Legacy endpoint for backward compatibility
    Redirects to new intelligent chatbot
    """
    logger.info("Legacy endpoint called, redirecting to new system")
    return await chat_endpoint(chat_message)

@app.get("/categories")
async def get_categories():
    """Get available categories, colors, etc."""
    try:
        products = product_db.get_all_products()
        categories = list(set(p["category"] for p in products))
        colors = list(set(p["color"] for p in products))
        
        return {
            "categories": sorted(categories),
            "colors": sorted(colors)
        }
    except Exception as e:
        logger.error(f"Categories error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Categories error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Intelligent E-commerce Chatbot API v2.0")
    print("📊 Features: Intent Scoring + Conversation Memory + Learning")
    print("🔗 API Documentation: http://localhost:8000/docs")
    print("💾 SQLite Database: backend/chatbot_memory.db")
    print("🤖 Ready to serve intelligent conversations!")
    
    uvicorn.run(
        "main_intelligent:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )