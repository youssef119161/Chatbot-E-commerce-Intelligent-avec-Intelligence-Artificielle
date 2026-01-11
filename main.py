"""
API FastAPI pour le Chatbot E-commerce Intelligent
Point d'entrée principal du backend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

# Imports locaux
from models import ChatRequest, ChatResponse, ProductSearchRequest, ProductListResponse, Product
from chatbot_logic import ecommerce_chatbot
from database import product_db

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title="Chatbot E-commerce Intelligent API",
    description="API REST pour un chatbot de recherche de produits - Boutique en ligne",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS pour permettre les requêtes depuis Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Endpoint racine - Point d'entrée de l'API
    """
    return {
        "message": "Chatbot E-commerce Intelligent API",
        "version": "2.0.0",
        "status": "active",
        "description": "Assistant IA pour recherche de produits",
        "documentation": "/docs",
        "endpoints": {
            "chat": "/chat",
            "products": "/products",
            "search": "/products/search",
            "health": "/health",
            "stats": "/stats"
        }
    }


@app.get("/health")
async def health_check():
    """
    Endpoint de santé
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "service": "chatbot-ecommerce-api",
        "products_count": len(product_db.get_all_products())
    }


@app.get("/stats")
async def get_stats():
    """
    Endpoint statistiques - Informations sur le chatbot et la boutique
    """
    try:
        chatbot_stats = ecommerce_chatbot.get_stats()
        return {
            "chatbot_stats": chatbot_stats,
            "api_info": {
                "framework": "FastAPI",
                "version": "2.0.0",
                "type": "E-commerce Chatbot",
                "cors_enabled": True
            }
        }
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des stats: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint principal du chat e-commerce
    Analyse la demande et retourne les produits correspondants
    """
    try:
        logger.info(f"Nouveau message reçu: {request.message} (user: {request.user_id})")
        
        # Validation du message
        if not request.message or request.message.strip() == "":
            raise HTTPException(
                status_code=400, 
                detail="Le message ne peut pas être vide"
            )
        
        # Génération de la réponse par le chatbot e-commerce intelligent
        bot_result = ecommerce_chatbot.generate_smart_response(request.message)
        
        # Conversion des produits en modèles Pydantic
        products = [Product(**product) for product in bot_result["products"]]
        
        # Création de la réponse structurée
        response = ChatResponse(
            response=bot_result["response"],
            timestamp=datetime.now(),
            user_message=request.message,
            products=products,
            criteria=bot_result["criteria"]
        )
        
        logger.info(f"Réponse générée avec {len(products)} produits")
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors du traitement du chat: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Erreur interne lors de la génération de la réponse"
        )


@app.get("/products", response_model=ProductListResponse)
async def get_all_products():
    """
    Endpoint pour récupérer tous les produits
    """
    try:
        products = product_db.get_all_products()
        products_models = [Product(**product) for product in products]
        
        return ProductListResponse(
            products=products_models,
            total=len(products_models)
        )
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des produits: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


@app.post("/products/search", response_model=ProductListResponse)
async def search_products(search_request: ProductSearchRequest):
    """
    Endpoint pour recherche avancée de produits
    """
    try:
        # Conversion en dictionnaire pour la recherche
        criteria = {k: v for k, v in search_request.dict().items() if v is not None}
        
        # Recherche dans la base de données
        products = product_db.complex_search(**criteria)
        products_models = [Product(**product) for product in products]
        
        return ProductListResponse(
            products=products_models,
            total=len(products_models),
            filters_applied=criteria
        )
    except Exception as e:
        logger.error(f"Erreur lors de la recherche de produits: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


@app.get("/products/categories")
async def get_categories():
    """
    Endpoint pour récupérer les catégories disponibles
    """
    try:
        products = product_db.get_all_products()
        categories = list(set(p["category"] for p in products))
        subcategories = list(set(p["subcategory"] for p in products))
        colors = list(set(p["color"] for p in products))
        
        return {
            "categories": sorted(categories),
            "subcategories": sorted(subcategories),
            "colors": sorted(colors)
        }
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des catégories: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")


# Point d'entrée pour le développement
if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Démarrage du serveur Chatbot E-commerce API...")
    print("📚 Documentation disponible sur: http://localhost:8000/docs")
    print("🔗 API accessible sur: http://localhost:8000")
    print("🛍️ Boutique e-commerce avec IA intégrée")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )