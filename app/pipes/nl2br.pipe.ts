/**
 * Pipe pour convertir les sauts de ligne en balises HTML <br>
 */

import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'nl2br'
})
export class Nl2brPipe implements PipeTransform {
  transform(value: string): string {
    if (!value) return value;
    
    return value
      .replace(/\n/g, '<br>')
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Support du gras **texte**
      .replace(/💡/g, '<span style="color: #ff9800;">💡</span>') // Coloration des icônes
      .replace(/🛍️/g, '<span style="color: #e91e63;">🛍️</span>')
      .replace(/🎨/g, '<span style="color: #9c27b0;">🎨</span>');
  }
}