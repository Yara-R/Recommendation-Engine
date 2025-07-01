import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Usuario } from './initial/usuario/usuario';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Usuario],
  templateUrl: './app.html',
  styleUrl: './app.css'
})

export class App {
  protected nome = 'Yara';

  contador = signal(0);

  AddContador(){
    this.contador.update(x => x + 1);
  }
}
