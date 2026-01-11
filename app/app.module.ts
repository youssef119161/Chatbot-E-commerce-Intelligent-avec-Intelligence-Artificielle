import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ChatbotComponent } from './chatbot/chatbot.component';
import { NavbarComponent } from './navbar/navbar.component';
import { ProductCatalogComponent } from './product-catalog/product-catalog.component';
import { Nl2brPipe } from './pipes/nl2br.pipe';

@NgModule({
  declarations: [
    AppComponent,
    ChatbotComponent,
    NavbarComponent,
    ProductCatalogComponent,
    Nl2brPipe
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
