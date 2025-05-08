import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule], 
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css']
})
export class ChatbotComponent {
  mensaje: string = '';
  mensajes: { rol: string, texto: string }[] = [];

  constructor(private http: HttpClient) {}

  enviar() {
    const texto = this.mensaje.trim();
    if (!texto) return;

    this.mensajes.push({ rol: 'Usuario', texto });

    this.http.post<{ sentimiento: string }>('/analizar', {
      mensaje: texto
    }).subscribe({
      next: res => {
        this.mensajes.push({ rol: 'Bot', texto: `Sentimiento: ${res.sentimiento}` });
        this.mensaje = '';
      },
      error: () => {
        this.mensajes.push({ rol: 'Bot', texto: 'Error al conectar con el backend.' });
      }
    });
  }
}
