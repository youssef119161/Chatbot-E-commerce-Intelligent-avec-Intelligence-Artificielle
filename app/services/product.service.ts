/**
 * Service Angular pour la gestion des produits
 * Communique avec l'API FastAPI pour récupérer les produits
 */

import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, timeout } from 'rxjs/operators';

// Interfaces TypeScript pour les produits
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

export interface ProductListResponse {
  products: Product[];
  total: number;
  filters_applied?: any;
}

export interface ProductSearchRequest {
  color?: string;
  category?: string;
  max_price?: number;
  min_price?: number;
  tags?: string[];
  gender?: string;
  age_group?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  private readonly API_BASE_URL = 'http://localhost:8000';

  private readonly httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    })
  };

  constructor(private http: HttpClient) {
    console.log('🛍️ ProductService initialisé');
  }

  /**
   * Récupère tous les produits
   */
  getAllProducts(): Observable<ProductListResponse> {
    return this.http.get<ProductListResponse>(
      `${this.API_BASE_URL}/products`,
      this.httpOptions
    ).pipe(
      timeout(10000),
      catchError(this.handleError)
    );
  }

  /**
   * Recherche avancée de produits
   */
  searchProducts(criteria: ProductSearchRequest): Observable<ProductListResponse> {
    return this.http.post<ProductListResponse>(
      `${this.API_BASE_URL}/products/search`,
      criteria,
      this.httpOptions
    ).pipe(
      timeout(10000),
      catchError(this.handleError)
    );
  }

  /**
   * Récupère les catégories disponibles
   */
  getCategories(): Observable<any> {
    return this.http.get(`${this.API_BASE_URL}/products/categories`).pipe(
      timeout(5000),
      catchError(this.handleError)
    );
  }

  /**
   * Gestion des erreurs
   */
  private handleError(error: any): Observable<never> {
    let errorMessage = 'Une erreur s\'est produite';

    if (error.error instanceof ErrorEvent) {
      errorMessage = `Erreur client: ${error.error.message}`;
    } else {
      switch (error.status) {
        case 0:
          errorMessage = 'Impossible de contacter le serveur';
          break;
        case 404:
          errorMessage = 'Produits non trouvés';
          break;
        case 500:
          errorMessage = 'Erreur interne du serveur';
          break;
        default:
          errorMessage = `Erreur ${error.status}: ${error.message}`;
      }
    }

    console.error('❌ Erreur ProductService:', errorMessage, error);
    return throwError(() => new Error(errorMessage));
  }
}