"""
Serveur Backend Simplifié - Version de Secours
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json

app = FastAPI(
    title="Chatbot E-commerce API - Version Simple",
    description="API simplifiée pour test",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

PRODUCTS_SIMPLE = [
    {
        "id": 1,
        "name": "Casquette Rouge",
        "category": "accessoires",
        "subcategory": "casquettes",
        "color": "rouge",
        "price": 25.0,
        "currency": "DT",
        "description": "Casquette rouge classique",
        "tags": ["sport", "casual"],
        "age_group": "adulte",
        "gender": "unisexe",
        "image": "casquette.jpg",
        "stock": 10
    },
    {
        "id": 2,
        "name": "Sac Bleu",
        "category": "accessoires",
        "subcategory": "sacs",
        "color": "bleu",
        "price": 45.0,
        "currency": "DT",
        "description": "Sac à main bleu élégant",
        "tags": ["élégant", "femme"],
        "age_group": "adulte",
        "gender": "femme",
        "image": "sac.jpg",
        "stock": 5
    },
    {
        "id": 3,
        "name": "Jouet Enfant",
        "category": "jouets",
        "subcategory": "peluches",
        "color": "rose",
        "price": 30.0,
        "currency": "DT",
        "description": "Peluche douce pour enfant",
        "tags": ["cadeau", "enfant"],
        "age_group": "enfant",
        "gender": "fille",
        "image": "peluche.jpg",
        "stock": 8
    }
]

@app.get("/")
async def root():
    """Endpoint racine"""
    return {
        "message": "Chatbot E-commerce API - Version Simple",
        "status": "active",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    """Endpoint de santé"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "products_count": len(PRODUCTS_SIMPLE)
    }

@app.get("/products")
async def get_products():
    """Récupérer tous les produits"""
    return {
        "products": PRODUCTS_SIMPLE,
        "total": len(PRODUCTS_SIMPLE)
    }

@app.post("/chat")
async def chat(request: dict):
    """Endpoint du chatbot simplifié"""
    message = request.get("message", "").lower()
    
    if "bonjour" in message or "salut" in message:
        response = "🛍️ Bonjour ! Bienvenue dans notre boutique ! Comment puis-je vous aider ?"
        products = PRODUCTS_SIMPLE[:2]
    elif "rouge" in message:
        response = "🔴 Voici nos produits rouges !"
        products = [p for p in PRODUCTS_SIMPLE if "rouge" in p["color"]]
    elif "bleu" in message:
        response = "🔵 Voici nos produits bleus !"
        products = [p for p in PRODUCTS_SIMPLE if "bleu" in p["color"]]
    elif "cadeau" in message or "fille" in message:
        response = "🎁 Parfait pour un cadeau ! Voici nos suggestions :"
        products = [p for p in PRODUCTS_SIMPLE if "cadeau" in p["tags"] or p["gender"] == "fille"]
    else:
        response = "✨ Voici notre sélection de produits populaires !"
        products = PRODUCTS_SIMPLE
    
    return {
        "response": response,
        "timestamp": datetime.now().isoformat(),
        "user_message": request.get("message", ""),
        "products": products[:3],
        "criteria": {"detected": True}
    }

@app.get("/products/categories")
async def get_categories():
    """Récupérer les catégories"""
    categories = list(set(p["category"] for p in PRODUCTS_SIMPLE))
    colors = list(set(p["color"] for p in PRODUCTS_SIMPLE))
    
    return {
        "categories": categories,
        "colors": colors,
        "subcategories": []
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Démarrage du serveur simplifié...")
    print("🔗 API: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)