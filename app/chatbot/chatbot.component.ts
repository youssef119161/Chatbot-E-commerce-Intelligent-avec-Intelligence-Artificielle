/**
 * Composant principal du chatbot e-commerce
 * Gère l'interface utilisateur et les interactions avec le service
 */

import { AfterViewChecked, Component, ElementRef, EventEmitter, Input, OnInit, Output, ViewChild } from '@angular/core';
import { CartService } from '../services/cart.service';
import { ChatResponse, ChatService, Product } from '../services/chat.service';

// Interface pour représenter un message dans la conversation
export interface Message {
  content: string;
  isUser: boolean;
  timestamp: Date;
  isError?: boolean;
  products?: Product[];
}

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css']
})
export class ChatbotComponent implements OnInit, AfterViewChecked {
  // Référence au conteneur de messages pour le scroll automatique
  @ViewChild('messagesContainer') private messagesContainer!: ElementRef;

  // Propriétés pour contrôler l'affichage
  @Input() isVisible: boolean = true;
  @Output() close = new EventEmitter<void>();

  // Propriétés du composant
  messages: Message[] = [];
  currentMessage: string = '';
  isLoading: boolean = false;
  isApiConnected: boolean = false;
  apiStatus: string = 'Vérification...';

  constructor(private chatService: ChatService, private cartService: CartService) { }

  ngOnInit(): void {
    this.initializeChat();
  }

  ngAfterViewChecked(): void {
    this.scrollToBottom();
  }

  /**
   * Initialise le chat en vérifiant la connexion API
   */
  private initializeChat(): void {
    console.log('🚀 Initialisation du chatbot e-commerce...');

    // Vérification de la connexion API
    this.chatService.checkApiHealth().subscribe({
      next: (response) => {
        this.isApiConnected = true;
        this.apiStatus = 'Connecté';

        // Message de bienvenue e-commerce
        this.addMessage(
          '🛍️ Bonjour ! Je suis votre assistant shopping IA. Je peux vous aider à trouver des produits selon vos critères !\n\n' +
          '💡 Exemples de recherches :\n' +
          '• "Je veux une casquette rouge"\n' +
          '• "Un cadeau pour ma fille qui aime le bleu, budget 40 DT"\n' +
          '• "Montrez-moi des bijoux"\n\n' +
          'Que recherchez-vous aujourd\'hui ?',
          false
        );
      },
      error: (error) => {
        this.isApiConnected = false;
        this.apiStatus = 'Déconnecté';
        this.addMessage(
          'Erreur : Impossible de se connecter au serveur. Vérifiez que l\'API FastAPI est démarrée sur le port 8000.',
          false,
          true
        );
      }
    });
  }

  /**
   * Envoie un message au chatbot e-commerce
   */
  sendMessage(): void {
    const message = this.currentMessage.trim();

    // Validation du message
    if (!message) {
      return;
    }

    if (!this.isApiConnected) {
      this.addMessage('Erreur : Pas de connexion au serveur', false, true);
      return;
    }

    // Ajout du message utilisateur
    this.addMessage(message, true);
    this.currentMessage = '';
    this.isLoading = true;

    // Appel à l'API e-commerce
    this.chatService.sendMessage(message).subscribe({
      next: (response: ChatResponse) => {
        // Ajout de la réponse du bot avec les produits
        this.addMessage(response.response, false, false, response.products);
        console.log('✅ Réponse reçue avec produits:', response);
        this.isLoading = false;
      },
      error: (error: any) => {
        // Gestion des erreurs
        this.addMessage(
          `Erreur : ${error.message}`,
          false,
          true
        );
        console.error('❌ Erreur lors de l\'envoi:', error);
        this.isLoading = false;
      }
    });
  }

  /**
   * Ajoute un message à la conversation
   */
  private addMessage(content: string, isUser: boolean, isError: boolean = false, products?: Product[]): void {
    const message: Message = {
      content,
      isUser,
      timestamp: new Date(),
      isError,
      products: products || []
    };

    this.messages.push(message);
    console.log('💬 Message ajouté:', message);
  }

  /**
   * Gère l'appui sur la touche Entrée
   */
  onKeyPress(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }

  /**
   * Efface la conversation
   */
  clearChat(): void {
    this.messages = [];
    this.addMessage(
      '🛍️ Conversation effacée. Comment puis-je vous aider à trouver des produits ?',
      false
    );
  }

  /**
   * Ferme le chatbot
   */
  closeChatbot(): void {
    this.close.emit();
  }

  /**
   * Teste la connexion API manuellement
   */
  testConnection(): void {
    this.apiStatus = 'Test en cours...';

    this.chatService.checkApiHealth().subscribe({
      next: (response) => {
        this.isApiConnected = true;
        this.apiStatus = 'Connecté';
        this.addMessage('Connexion API réussie !', false);
      },
      error: (error) => {
        this.isApiConnected = false;
        this.apiStatus = 'Déconnecté';
        this.addMessage('Échec de connexion API', false, true);
      }
    });
  }

  /**
   * Ajoute un produit au panier (simulation)
   */
  addToCart(product: Product): void {
    this.cartService.addToCart(product, 1);
    console.log('🛒 Ajout au panier depuis chatbot:', product.name);

    // Message de confirmation
    this.addMessage(
      `✅ ${product.name} ajouté au panier ! 🛒\n\n💡 Vous pouvez continuer vos achats ou voir votre panier dans la navbar.`,
      false
    );
  }

  /**
   * Fait défiler automatiquement vers le bas
   */
  private scrollToBottom(): void {
    try {
      if (this.messagesContainer) {
        this.messagesContainer.nativeElement.scrollTop =
          this.messagesContainer.nativeElement.scrollHeight;
      }
    } catch (err) {
      console.warn('Erreur lors du scroll:', err);
    }
  }

  /**
   * Formate l'heure d'un message
   */
  formatTime(timestamp: Date): string {
    return timestamp.toLocaleTimeString('fr-FR', {
      hour: '2-digit',
      minute: '2-digit'
    });
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