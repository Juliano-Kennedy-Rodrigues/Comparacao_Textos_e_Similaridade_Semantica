# Sistema de Comparação Semântica de Textos (TCC)

Aplicação web desenvolvida em Django para avaliação de similaridade semântica entre documentos textuais (com suporte a ficheiros PDF e TXT) utilizando modelos de Processamento de Linguagem Natural (PLN) baseados no Transformer `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`.

---

## 🚀 Funcionalidades

* **Processamento Local:** Executa o modelo de embeddings diretamente no hardware local, garantindo privacidade e independência de APIs externas pagas.
* **Leitura de Múltiplos Formatos:** Extração automatizada de texto a partir de ficheiros PDF (`pypdf`) e texto bruto (`.txt`).
* **Métricas de Similaridade:** Cálculo de similaridade de cosseno (`scikit-learn`) entre documentos âncora e comparados.
* **Interface Web Dinâmica:** Design responsivo adaptado para apresentações académicas.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python, Django
* **Processamento de Linguagem Natural:** `sentence-transformers`, PyTorch
* **Computação Científica:** `NumPy`, `scikit-learn`
* **Manipulação de Ficheiros:** `pypdf`
* **Túnel de Rede:** Ngrok (para acesso remoto, alternativa a sites de host como PythonAnywhere e Railway)

---

## 📦 Pré-requisitos

Certifique-se de ter o **Python 3.10+** instalado no seu sistema.

---

## ⚙️ Instalação e Execução Local

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU-UTILIZADOR/NOME-DO-REPOSITORIO.git](https://github.com/SEU-UTILIZADOR/NOME-DO-REPOSITORIO.git)
   cd NOME-DO-REPOSITORIO

2. **Crie e ative um ambiente virtual:**

python -m venv venv

   1. No Windows:
venv\Scripts\activate

   2. No macOS/Linux:
source venv/bin/activate

4. **Instale as dependências:**

pip install -r requirements.txt

5. **Execute as migrações da base de dados:**

python manage.py migrate

6. **Inicie o servidor de desenvolvimento:**

python manage.py runserver

7. **Acesse a aplicação pelo seu navegador:**

http://127.0.0.1:8000/
ou use ngrokcom:  ngrok http 8000



## LICENÇA:

Este projeto foi desenvolvido como Trabalho de Conclusão de Curso (TCC). Sinta-se livre para utilizar o código para fins académicos ou educacionais.