/**
 * Composant principal de l'application e-commerce
 */

import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Boutique E-commerce avec IA';
  isChatbotVisible = false;

  /**
   * Affiche le chatbot
   */
  showChatbot(): void {
    console.log('🤖 Ouverture du chatbot IA');
    this.isChatbotVisible = true;
  }

  /**
   * Cache le chatbot
   */
  hideChatbot(): void {
    console.log('🤖 Fermeture du chatbot IA');
    this.isChatbotVisible = false;
  }
}
