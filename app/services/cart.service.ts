/**
 * Service Angular pour la gestion du panier d'achat
 */

import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { Product } from './chat.service';

export interface CartItem {
    product: Product;
    quantity: number;
    addedAt: Date;
}

export interface Cart {
    items: CartItem[];
    totalItems: number;
    totalPrice: number;
}

@Injectable({
    providedIn: 'root'
})
export class CartService {
    private cartSubject = new BehaviorSubject<Cart>({
        items: [],
        totalItems: 0,
        totalPrice: 0
    });

    public cart$ = this.cartSubject.asObservable();

    constructor() {
        // Charger le panier depuis le localStorage au démarrage
        this.loadCartFromStorage();
    }

    /**
     * Ajouter un produit au panier
     */
    addToCart(product: Product, quantity: number = 1): void {
        const currentCart = this.cartSubject.value;
        const existingItemIndex = currentCart.items.findIndex(
            item => item.product.id === product.id
        );

        if (existingItemIndex >= 0) {
            // Produit déjà dans le panier, augmenter la quantité
            currentCart.items[existingItemIndex].quantity += quantity;
        } else {
            // Nouveau produit
            const newItem: CartItem = {
                product,
                quantity,
                addedAt: new Date()
            };
            currentCart.items.push(newItem);
        }

        this.updateCart(currentCart);
        console.log(`🛒 ${product.name} ajouté au panier (quantité: ${quantity})`);
    }

    /**
     * Retirer un produit du panier
     */
    removeFromCart(productId: number): void {
        const currentCart = this.cartSubject.value;
        currentCart.items = currentCart.items.filter(
            item => item.product.id !== productId
        );

        this.updateCart(currentCart);
        console.log(`🗑️ Produit ${productId} retiré du panier`);
    }

    /**
     * Modifier la quantité d'un produit
     */
    updateQuantity(productId: number, quantity: number): void {
        if (quantity <= 0) {
            this.removeFromCart(productId);
            return;
        }

        const currentCart = this.cartSubject.value;
        const itemIndex = currentCart.items.findIndex(
            item => item.product.id === productId
        );

        if (itemIndex >= 0) {
            currentCart.items[itemIndex].quantity = quantity;
            this.updateCart(currentCart);
        }
    }

    /**
     * Vider le panier
     */
    clearCart(): void {
        const emptyCart: Cart = {
            items: [],
            totalItems: 0,
            totalPrice: 0
        };

        this.updateCart(emptyCart);
        console.log('🗑️ Panier vidé');
    }

    /**
     * Obtenir le panier actuel
     */
    getCurrentCart(): Cart {
        return this.cartSubject.value;
    }

    /**
     * Vérifier si un produit est dans le panier
     */
    isInCart(productId: number): boolean {
        return this.cartSubject.value.items.some(
            item => item.product.id === productId
        );
    }

    /**
     * Obtenir la quantité d'un produit dans le panier
     */
    getProductQuantity(productId: number): number {
        const item = this.cartSubject.value.items.find(
            item => item.product.id === productId
        );
        return item ? item.quantity : 0;
    }

    /**
     * Mettre à jour le panier et recalculer les totaux
     */
    private updateCart(cart: Cart): void {
        // Recalculer les totaux
        cart.totalItems = cart.items.reduce((total, item) => total + item.quantity, 0);
        cart.totalPrice = cart.items.reduce(
            (total, item) => total + (item.product.price * item.quantity),
            0
        );

        // Mettre à jour le BehaviorSubject
        this.cartSubject.next(cart);

        // Sauvegarder dans le localStorage
        this.saveCartToStorage(cart);
    }

    /**
     * Sauvegarder le panier dans le localStorage
     */
    private saveCartToStorage(cart: Cart): void {
        try {
            localStorage.setItem('ecommerce_cart', JSON.stringify(cart));
        } catch (error) {
            console.warn('Impossible de sauvegarder le panier:', error);
        }
    }

    /**
     * Charger le panier depuis le localStorage
     */
    private loadCartFromStorage(): void {
        try {
            const savedCart = localStorage.getItem('ecommerce_cart');
            if (savedCart) {
                const cart: Cart = JSON.parse(savedCart);
                // Reconvertir les dates
                cart.items.forEach(item => {
                    item.addedAt = new Date(item.addedAt);
                });
                this.cartSubject.next(cart);
            }
        } catch (error) {
            console.warn('Impossible de charger le panier:', error);
        }
    }

    /**
     * Obtenir le nombre total d'articles
     */
    getTotalItems(): Observable<number> {
        return new Observable(observer => {
            this.cart$.subscribe(cart => {
                observer.next(cart.totalItems);
            });
        });
    }

    /**
     * Obtenir le prix total
     */
    getTotalPrice(): Observable<number> {
        return new Observable(observer => {
            this.cart$.subscribe(cart => {
                observer.next(cart.totalPrice);
            });
        });
    }
}