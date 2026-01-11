#!/usr/bin/env python3
"""
Démarrage sécurisé du backend FastAPI
"""

import uvicorn
import sys
import os

def main():
    """Démarrage sécurisé"""
    print("🚀 Démarrage Sécurisé du Backend FastAPI")
    print("=" * 45)
    
    try:
        # Vérifier que nous sommes dans le bon dossier
        if not os.path.exists("main.py"):
            print("❌ Fichier main.py non trouvé !")
            print("💡 Assurez-vous d'être dans le dossier backend")
            return
        
        print("📍 Dossier backend détecté")
        print("🔧 Configuration du serveur...")
        
        # Configuration du serveur
        config = {
            "app": "main:app",
            "host": "127.0.0.1",
            "port": 8000,
            "reload": True,
            "log_level": "info",
            "access_log": True
        }
        
        print(f"🌐 Serveur configuré sur http://{config['host']}:{config['port']}")
        print("📚 Documentation disponible sur http://127.0.0.1:8000/docs")
        print("⏹️  Appuyez sur Ctrl+C pour arrêter")
        print()
        
        # Démarrer le serveur
        uvicorn.run(**config)
        
    except KeyboardInterrupt:
        print("\n⏹️  Serveur arrêté par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur de démarrage: {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 Essayez: python debug_backend.py pour diagnostiquer")

if __name__ == "__main__":
    main()