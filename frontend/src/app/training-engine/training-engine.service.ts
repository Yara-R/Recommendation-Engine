import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class UsuarioService {
  private apiUrl = 'http://localhost:8000'; // ou sua URL real do FastAPI

  constructor(private http: HttpClient) {}

  enviarDados(usuario: { idade: number; genero: string }): Observable<any> {
    return this.http.post(`${this.apiUrl}/usuarios/`, usuario);
  }
}
