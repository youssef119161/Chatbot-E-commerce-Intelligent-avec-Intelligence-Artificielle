/**
 * Composant Catalogue de Produits
 * Affiche la liste des produits de la boutique
 */

import { Component, OnInit } from '@angular/core';
import { CartService } from '../services/cart.service';
import { Product, ProductListResponse, ProductService } from '../services/product.service';

@Component({
  selector: 'app-product-catalog',
  templateUrl: './product-catalog.component.html',
  styleUrls: ['./product-catalog.component.css']
})
export class ProductCatalogComponent implements OnInit {
  products: Product[] = [];
  loading: boolean = false;
  error: string = '';
  categories: string[] = [];
  colors: string[] = [];

  constructor(private productService: ProductService, private cartService: CartService) { }

  ngOnInit(): void {
    this.loadProducts();
    this.loadCategories();
  }

  /**
   * Charge tous les produits
   */
  loadProducts(): void {
    this.loading = true;
    this.error = '';

    this.productService.getAllProducts().subscribe({
      next: (response: ProductListResponse) => {
        this.products = response.products;
        this.loading = false;
        console.log('✅ Produits chargés:', this.products.length);
      },
      error: (error) => {
        this.error = error.message;
        this.loading = false;
        console.error('❌ Erreur chargement produits:', error);
      }
    });
  }

  /**
   * Charge les catégories disponibles
   */
  loadCategories(): void {
    this.productService.getCategories().subscribe({
      next: (response) => {
        this.categories = response.categories || [];
        this.colors = response.colors || [];
        console.log('✅ Catégories chargées:', this.categories);
      },
      error: (error) => {
        console.error('❌ Erreur chargement catégories:', error);
      }
    });
  }

  /**
   * Filtre les produits par catégorie
   */
  filterByCategory(category: string): void {
    this.loading = true;

    this.productService.searchProducts({ category }).subscribe({
      next: (response: ProductListResponse) => {
        this.products = response.products;
        this.loading = false;
        console.log(`✅ Produits filtrés par ${category}:`, this.products.length);
      },
      error: (error) => {
        this.error = error.message;
        this.loading = false;
      }
    });
  }

  /**
   * Filtre les produits par couleur
   */
  filterByColor(color: string): void {
    this.loading = true;

    this.productService.searchProducts({ color }).subscribe({
      next: (response: ProductListResponse) => {
        this.products = response.products;
        this.loading = false;
        console.log(`✅ Produits filtrés par ${color}:`, this.products.length);
      },
      error: (error) => {
        this.error = error.message;
        this.loading = false;
      }
    });
  }

  /**
   * Remet à zéro les filtres
   */
  clearFilters(): void {
    this.loadProducts();
  }

  /**
   * Ajoute un produit au panier
   */
  addToCart(product: Product): void {
    this.cartService.addToCart(product, 1);
    console.log('🛒 Ajout au panier:', product.name);
  }

  /**
   * Vérifie si un produit est dans le panier
   */
  isInCart(productId: number): boolean {
    return this.cartService.isInCart(productId);
  }

  /**
   * Obtient la quantité d'un produit dans le panier
   */
  getCartQuantity(productId: number): number {
    return this.cartService.getProductQuantity(productId);
  }

  /**
   * Gère les erreurs de chargement d'images
   */
  onImageError(event: any, product: Product): void {
    console.warn('❌ Erreur de chargement d\'image pour:', product.name);
    product.imageError = true;
    event.target.style.display = 'none';
  }
}