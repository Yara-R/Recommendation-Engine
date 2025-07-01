import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { TrainingEngine } from './training-engine/training-engine';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, TrainingEngine],
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