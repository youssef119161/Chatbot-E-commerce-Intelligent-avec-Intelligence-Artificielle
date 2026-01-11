/**
 * Composant Navbar pour la boutique e-commerce
 * Contient le bouton pour ouvrir le chatbot IA
 */

import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { CartService } from '../services/cart.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  @Output() openChatbot = new EventEmitter<void>();

  cartItemCount = 0;
  showCartDropdown = false;

  constructor(public cartService: CartService) { }

  ngOnInit(): void {
    // S'abonner aux changements du panier
    this.cartService.cart$.subscribe(cart => {
      this.cartItemCount = cart.totalItems;
    });

    // Fermer le dropdown en cliquant ailleurs
    document.addEventListener('click', (event) => {
      const target = event.target as HTMLElement;
      if (!target.closest('.cart-container')) {
        this.showCartDropdown = false;
      }
    });
  }

  /**
   * Ouvre le chatbot IA
   */
  onOpenChatbot(): void {
    console.log('🤖 Ouverture du chatbot IA');
    this.openChatbot.emit();
  }

  /**
   * Affiche/cache le dropdown du panier
   */
  toggleCartDropdown(): void {
    this.showCartDropdown = !this.showCartDropdown;
  }

  /**
   * Vide le panier
   */
  clearCart(): void {
    this.cartService.clearCart();
    this.showCartDropdown = false;
  }
}