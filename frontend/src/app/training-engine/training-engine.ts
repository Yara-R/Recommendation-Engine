import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-training-engine',
  imports: [CommonModule, FormsModule],
  templateUrl: './training-engine.html',
  styleUrl: './training-engine.css'
})
export class TrainingEngine {

  idade: number | null = null;
  genero: string = '';
  iniciouPesquisa = false;

  filmes = [
    'Clube da Luta',
    'Matrix',
    'O Poderoso Chefão',
    'Interestelar',
    'Forrest Gump',
    'A Origem',
    'O Senhor dos Anéis: A Sociedade do Anel',
    'Pulp Fiction',
    'O Silêncio dos Inocentes',
    'A Lista de Schindler',
    'O Rei Leão',
    'Gladiador',
    'A Vida é Bela',
    'Cidadão Kane',
    'O Grande Lebowski',
    'A Rede Social',
    'O Exorcista',
    'O Labirinto do Fauno',
    'A Forma da Água',
  ];
  filmeAtualIndex = 0;

  contadorAssistidosOuQuer = 0;

  iniciarPesquisa() {
    if (this.idade && this.genero) {
      this.iniciouPesquisa = true;
    }
  }

  responder(resposta: string) {
    if (resposta === 'sim' || resposta === 'nao_mas_quero') {
      this.contadorAssistidosOuQuer++;
    }
  

    if (this.filmeAtualIndex < this.filmes.length - 1) {
      this.filmeAtualIndex++;
    } else {
      alert('Não temos mais filmes para recomendar.');
      this.iniciouPesquisa = false;
      this.filmeAtualIndex = 0;
      this.contadorAssistidosOuQuer = 0;
    }
  }

  encerrar() {
    alert('Pesquisa encerrada! Obrigado por participar!');
    this.iniciouPesquisa = false;
    this.filmeAtualIndex = 0;
    this.contadorAssistidosOuQuer = 0;
  }

  get filmeAtual() {
    return this.filmes[this.filmeAtualIndex];
  }
}
