#!/usr/bin/env python3
"""
Script de test pour vérifier le bon fonctionnement du projet
Chatbot E-commerce FastAPI + Angular
"""

import requests
import json
import time
import sys
from typing import Dict, Any

class ProjectTester:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:4200"
        self.tests_passed = 0
        self.tests_failed = 0

    def print_header(self, title: str):
        """Affiche un en-tête de section"""
        print(f"\n{'='*50}")
        print(f"🧪 {title}")
        print(f"{'='*50}")

    def print_test(self, test_name: str, success: bool, details: str = ""):
        """Affiche le résultat d'un test"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
        
        if success:
            self.tests_passed += 1
        else:
            self.tests_failed += 1

    def test_backend_health(self) -> bool:
        """Test de santé du backend"""
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.print_test("Backend Health Check", True, f"Status: {data.get('status')}")
                return True
            else:
                self.print_test("Backend Health Check", False, f"Status Code: {response.status_code}")
                return False
        except Exception as e:
            self.print_test("Backend Health Check", False, f"Erreur: {str(e)}")
            return False

    def test_backend_root(self) -> bool:
        """Test de l'endpoint racine"""
        try:
            response = requests.get(f"{self.backend_url}/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.print_test("Backend Root Endpoint", True, f"Version: {data.get('version')}")
                return True
            else:
                self.print_test("Backend Root Endpoint", False, f"Status Code: {response.status_code}")
                return False
        except Exception as e:
            self.print_test("Backend Root Endpoint", False, f"Erreur: {str(e)}")
            return False

    def test_chatbot_endpoint(self) -> bool:
        """Test de l'endpoint du chatbot"""
        try:
            payload = {
                "message": "Bonjour, je veux une casquette rouge",
                "user_id": "test_user"
            }
            response = requests.post(
                f"{self.backend_url}/chat", 
                json=payload, 
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                products_count = len(data.get('products', []))
                self.print_test(
                    "Chatbot Endpoint", 
                    True, 
                    f"Réponse reçue, {products_count} produits trouvés"
                )
                return True
            else:
                self.print_test("Chatbot Endpoint", False, f"Status Code: {response.status_code}")
                return False
        except Exception as e:
            self.print_test("Chatbot Endpoint", False, f"Erreur: {str(e)}")
            return False

    def test_products_endpoint(self) -> bool:
        """Test de l'endpoint des produits"""
        try:
            response = requests.get(f"{self.backend_url}/products", timeout=5)
            if response.status_code == 200:
                data = response.json()
                products_count = data.get('total', 0)
                self.print_test(
                    "Products Endpoint", 
                    True, 
                    f"{products_count} produits disponibles"
                )
                return True
            else:
                self.print_test("Products Endpoint", False, f"Status Code: {response.status_code}")
                return False
        except Exception as e:
            self.print_test("Products Endpoint", False, f"Erreur: {str(e)}")
            return False

    def test_search_endpoint(self) -> bool:
        """Test de l'endpoint de recherche"""
        try:
            payload = {
                "color": "rouge",
                "category": "accessoires"
            }
            response = requests.post(
                f"{self.backend_url}/products/search", 
                json=payload, 
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                products_count = data.get('total', 0)
                self.print_test(
                    "Search Endpoint", 
                    True, 
                    f"{products_count} produits trouvés pour 'rouge + accessoires'"
                )
                return True
            else:
                self.print_test("Search Endpoint", False, f"Status Code: {response.status_code}")
                return False
        except Exception as e:
            self.print_test("Search Endpoint", False, f"Erreur: {str(e)}")
            return False

    def test_categories_endpoint(self) -> bool:
        """Test de l'endpoint des catégories"""
        try:
            response = requests.get(f"{self.backend_url}/products/categories", timeout=5)
            if response.status_code == 200:
                data = response.json()
                categories_count = len(data.get('categories', []))
                self.print_test(
                    "Categories Endpoint", 
                    True, 
                    f"{categories_count} catégories disponibles"
                )
                return True
            else:
                self.print_test("Categories Endpoint", False, f"Status Code: {response.status_code}")
                return False
        except Exception as e:
            self.print_test("Categories Endpoint", False, f"Erreur: {str(e)}")
            return False

    def test_frontend_accessibility(self) -> bool:
        """Test d'accessibilité du frontend"""
        try:
            response = requests.get(self.frontend_url, timeout=5)
            if response.status_code == 200:
                self.print_test("Frontend Accessibility", True, "Page Angular accessible")
                return True
            else:
                self.print_test("Frontend Accessibility", False, f"Status Code: {response.status_code}")
                return False
        except Exception as e:
            self.print_test("Frontend Accessibility", False, f"Erreur: {str(e)}")
            return False

    def test_chatbot_intelligence(self) -> bool:
        """Test de l'intelligence du chatbot avec différents messages"""
        test_messages = [
            "Bonjour",
            "Je veux une casquette rouge",
            "Un cadeau pour ma fille qui aime le bleu, budget 40 DT",
            "Montrez-moi des bijoux",
            "Au revoir"
        ]
        
        success_count = 0
        for message in test_messages:
            try:
                payload = {"message": message, "user_id": "test_user"}
                response = requests.post(
                    f"{self.backend_url}/chat", 
                    json=payload, 
                    timeout=10
                )
                
                if response.status_code == 200:
                    success_count += 1
                    
            except Exception:
                pass
        
        success_rate = (success_count / len(test_messages)) * 100
        is_success = success_rate >= 80
        
        self.print_test(
            "Chatbot Intelligence", 
            is_success, 
            f"{success_count}/{len(test_messages)} messages traités ({success_rate:.1f}%)"
        )
        return is_success

    def run_all_tests(self):
        """Exécute tous les tests"""
        print("🚀 Démarrage des tests du projet Chatbot E-commerce")
        print("📋 Vérification de tous les composants...")

        # Tests Backend
        self.print_header("Tests Backend FastAPI")
        self.test_backend_health()
        self.test_backend_root()
        self.test_chatbot_endpoint()
        self.test_products_endpoint()
        self.test_search_endpoint()
        self.test_categories_endpoint()

        # Tests Intelligence
        self.print_header("Tests Intelligence Chatbot")
        self.test_chatbot_intelligence()

        # Tests Frontend
        self.print_header("Tests Frontend Angular")
        self.test_frontend_accessibility()

        # Résumé
        self.print_header("Résumé des Tests")
        total_tests = self.tests_passed + self.tests_failed
        success_rate = (self.tests_passed / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"✅ Tests réussis: {self.tests_passed}")
        print(f"❌ Tests échoués: {self.tests_failed}")
        print(f"📊 Taux de réussite: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("\n🎉 Projet fonctionnel ! Prêt pour la démonstration.")
        else:
            print("\n⚠️  Certains composants nécessitent une attention.")
            print("💡 Vérifiez que les serveurs sont démarrés :")
            print("   - Backend: uvicorn main:app --reload")
            print("   - Frontend: ng serve")

        return success_rate >= 80

if __name__ == "__main__":
    tester = ProjectTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)