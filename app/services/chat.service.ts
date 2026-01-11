/**
 * Service Angular pour la communication avec l'API FastAPI
 * Gère les requêtes HTTP vers le backend du chatbot
 */

import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, timeout } from 'rxjs/operators';

// Interfaces TypeScript pour typer les données
export interface ChatRequest {
  message: string;
  user_id?: string;
}

export interface Product {
  id: number;
  name: string;
  category: string;
  subcategory: string;
  color: string;
  price: number;
  currency: string;
  description: string;
  tags: string[];
  age_group: string;
  gender: string;
  image: string;
  stock: number;
  imageError?: boolean; // Pour gérer les erreurs de chargement d'images
}

export interface ChatResponse {
  response: string;
  timestamp: string;
  user_message: string;
  products: Product[];
  criteria: any;
  questions?: string[];
}

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  // URL de base de l'API FastAPI
  private readonly API_BASE_URL = 'http://localhost:8000';

  // Configuration des headers HTTP
  private readonly httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    })
  };

  constructor(private http: HttpClient) {
    console.log('🔧 ChatService initialisé avec URL:', this.API_BASE_URL);
  }

  /**
   * Envoie un message au chatbot via l'API FastAPI
   */
  sendMessage(message: string, userId: string = 'angular-user'): Observable<ChatResponse> {
    const chatRequest: ChatRequest = {
      message: message.trim(),
      user_id: userId
    };

    console.log('📤 Envoi du message:', chatRequest);

    return this.http.post<ChatResponse>(
      `${this.API_BASE_URL}/chat`,
      chatRequest,
      this.httpOptions
    ).pipe(
      timeout(10000), // Timeout de 10 secondes
      catchError(this.handleError)
    );
  }

  /**
   * Vérifie la santé de l'API
   */
  checkApiHealth(): Observable<any> {
    return this.http.get(`${this.API_BASE_URL}/health`).pipe(
      timeout(5000),
      catchError(this.handleError)
    );
  }

  /**
   * Gestion centralisée des erreurs HTTP
   */
  private handleError(error: any): Observable<never> {
    let errorMessage = 'Une erreur inattendue s\'est produite';

    if (error.error instanceof ErrorEvent) {
      // Erreur côté client
      errorMessage = `Erreur client: ${error.error.message}`;
    } else {
      // Erreur côté serveur
      switch (error.status) {
        case 0:
          errorMessage = 'Impossible de contacter le serveur. Vérifiez que l\'API FastAPI est démarrée.';
          break;
        case 400:
          errorMessage = error.error?.detail || 'Requête invalide';
          break;
        case 404:
          errorMessage = 'Endpoint non trouvé';
          break;
        case 500:
          errorMessage = error.error?.detail || 'Erreur interne du serveur';
          break;
        default:
          errorMessage = `Erreur ${error.status}: ${error.error?.detail || error.message}`;
      }
    }

    console.error('❌ Erreur ChatService:', errorMessage, error);
    return throwError(() => new Error(errorMessage));
  }
}