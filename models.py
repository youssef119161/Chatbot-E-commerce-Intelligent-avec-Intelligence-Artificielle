"""
Modèles Pydantic pour l'API Chatbot E-commerce
Définit les structures de données pour les requêtes et réponses
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatRequest(BaseModel):
    """
    Modèle pour les requêtes de chat
    """
    message: str
    user_id: Optional[str] = "anonymous"
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Salut je veux une casquette rouge",
                "user_id": "user123"
            }
        }


class Product(BaseModel):
    """
    Modèle pour un produit
    """
    id: int
    name: str
    category: str
    subcategory: str
    color: str
    price: float
    currency: str
    description: str
    tags: List[str]
    age_group: str
    gender: str
    image: str
    stock: int


class ChatResponse(BaseModel):
    """
    Modèle pour les réponses du chatbot e-commerce
    """
    response: str
    timestamp: datetime
    user_message: str
    products: List[Product] = []
    criteria: Dict[str, Any] = {}
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": "🛍️ J'ai trouvé 2 produit(s) pour vous !",
                "timestamp": "2024-01-15T10:30:00",
                "user_message": "casquette rouge",
                "products": [
                    {
                        "id": 1,
                        "name": "Casquette Rouge Classique",
                        "category": "accessoires",
                        "subcategory": "casquettes",
                        "color": "rouge",
                        "price": 25.0,
                        "currency": "DT",
                        "description": "Casquette rouge en coton",
                        "tags": ["sport", "casual"],
                        "age_group": "adulte",
                        "gender": "unisexe",
                        "image": "casquette_rouge_1.jpg",
                        "stock": 15
                    }
                ],
                "criteria": {
                    "color": "rouge",
                    "category": "casquette"
                }
            }
        }


class ProductSearchRequest(BaseModel):
    """
    Modèle pour les recherches directes de produits
    """
    color: Optional[str] = None
    category: Optional[str] = None
    max_price: Optional[float] = None
    min_price: Optional[float] = None
    tags: Optional[List[str]] = None
    gender: Optional[str] = None
    age_group: Optional[str] = None


class ProductListResponse(BaseModel):
    """
    Modèle pour la liste des produits
    """
    products: List[Product]
    total: int
    filters_applied: Dict[str, Any] = {}