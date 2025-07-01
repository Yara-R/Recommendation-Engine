# Recommendation Engine

<p align="center">

  <a href="https://github.com/Yara-R/Recommendation-Engine/commits/main/">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/Yara-R/Recommendation-Engine">
  </a>

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/Yara-R/Recommendation-Engine">

  <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/Yara-R/Recommendation-Engine">

  <a href="https://www.linkedin.com/in/yara-rodrigues-b14203236/">
    <img alt="Made by Yara Rodrigues" src="https://img.shields.io/badge/made_by-Yara_Rodrigues-353949">
  </a>

  <img alt="License" src="https://img.shields.io/badge/license-MIT-brightgreen">

</p>

## 📌 Descrição

Este projeto implementa um sistema de recomendação inteligente de filmes baseado em preferências do usuário, utilizando Machine Learning e aprendizado colaborativo. A aplicação é composta por:

- 🔙 **Backend** em **Flask**
- 🌐 **Frontend** em **Angular**
- 🧠 Módulo de **recomendação automática**
- 🗃️ Banco de dados **PostgreSQL**
- 🐳 Integração total via **Docker**

---

## 📁 Estrutura do Projeto

## ⚙️ Como Executar

### 🔧 Requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Make (opcional)

### ▶️ Instruções

```bash
# 1. Clone o repositório
git clone https://github.com/Yara-R/Recommendation-Engine.git
cd Recommendation-Engine

# 2. Execute os containers
docker-compose up --build
```

---

## 🧠 Como Funciona o Motor de Recomendação

O sistema utiliza dados de interações dos usuários com filmes para sugerir novos títulos com base em:

* Similaridade de conteúdo

* Filtragem colaborativa

* Respostas dos usuários sobre os filmes assistidos (curtiu/não curtiu)

O modelo é continuamente atualizado conforme novos feedbacks são registrados.

---

## 📊 Visualização e Análise
A análise dos dados e desempenho do modelo pode ser feita por meio de dashboards conectados ao banco de dados, como com o Power BI.

---

## 📝 Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🙋‍♀️ Autora
Desenvolvido por [Yara Rodrigues](https://www.linkedin.com/in/yara-rodrigues-inacio/)
