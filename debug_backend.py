#!/usr/bin/env python3
"""
Script de diagnostic pour le backend FastAPI
"""

import sys
import traceback

def test_imports():
    """Test des imports"""
    print("🔍 Test des imports...")
    
    try:
        import fastapi
        print(f"✅ FastAPI: {fastapi.__version__}")
    except Exception as e:
        print(f"❌ FastAPI: {e}")
        return False
    
    try:
        import uvicorn
        print(f"✅ Uvicorn: {uvicorn.__version__}")
    except Exception as e:
        print(f"❌ Uvicorn: {e}")
        return False
    
    try:
        import pydantic
        print(f"✅ Pydantic: {pydantic.__version__}")
    except Exception as e:
        print(f"❌ Pydantic: {e}")
        return False
    
    return True

def test_app_creation():
    """Test de création de l'app"""
    print("\n🔍 Test de création de l'app...")
    
    try:
        from main import app
        print("✅ App créée avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur de création de l'app: {e}")
        traceback.print_exc()
        return False

def test_modules():
    """Test des modules locaux"""
    print("\n🔍 Test des modules locaux...")
    
    try:
        import models
        print("✅ Models importé")
    except Exception as e:
        print(f"❌ Models: {e}")
    
    try:
        import database
        print("✅ Database importé")
    except Exception as e:
        print(f"❌ Database: {e}")
    
    try:
        import chatbot_logic
        print("✅ Chatbot_logic importé")
    except Exception as e:
        print(f"❌ Chatbot_logic: {e}")

def main():
    """Fonction principale de diagnostic"""
    print("🚀 Diagnostic Backend FastAPI")
    print("=" * 40)
    
    # Test des imports
    if not test_imports():
        print("\n❌ Problème avec les dépendances de base")
        print("💡 Exécutez: pip install -r requirements.txt")
        return
    
    # Test des modules locaux
    test_modules()
    
    # Test de création de l'app
    if not test_app_creation():
        print("\n❌ Problème avec la création de l'app")
        return
    
    print("\n🎉 Diagnostic terminé !")
    print("💡 Si tout est OK, le problème vient peut-être du port ou de la configuration réseau")

if __name__ == "__main__":
    main()