
# 💸 Seu Banco: Inteligência Financeira ao Seu Alcance

Este projeto utiliza conceitos de ETL - Extract, Transform and Load + um agente inteligente da Google ADK para gerar **dicas financeiras personalizadas** com base nos dados bancários de clientes (fornecidos por um arquivo CSV). A aplicação analisa padrões de gastos e comportamento financeiro, oferecendo orientações práticas para ajudar os clientes a organizar melhor seu orçamento e tomar decisões mais conscientes.

---

## 📸 Layout da Aplicação

![Interface da Aplicação](assets/aplicacao.png)


---

## 🚀 Como Usar

1. **Clone o repositório:**

```bash
git clone https://github.com/Bernardinense/seu-banco.git
cd seu-banco
```

2. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

3. **Adicione o arquivo CSV com seus dados bancários.**

> O CSV deve conter colunas como: `Data`, `Descrição`, `Valor`, `Categoria` (ou similar).

4. **Execute a aplicação:**

```bash
streamlit run main.py
```

---

## 🧠 Tecnologias Utilizadas

- **Python 3.10+**
- **Streamlit** – Para a interface web interativa
- **Google ADK (Agent Development Kit)** – Para criação e orquestração dos agentes de IA
- **Pandas** – Manipulação e análise de dados

---

## 📂 Estrutura do Projeto

```
📦 projeto/
├── .streamlit/                  # Configurações do Streamlit (ex: tema, layout)
├── assets/                      # Imagens
├── core.py                      # Lógica central do projeto (análise, IA, fluxo)
├── utils.py                     # Função para ler e tratar o CSV
├── dados_bancarios_com_UserID.xlsx  # Exemplo de dados de entrada
├── main.py                      # Ponto de entrada principal com a interface Streamlit
├── requirements.txt             # Dependências do projeto
├── LICENSE                      # Licença do projeto
├── .env                         # Variáveis de ambiente (chaves, tokens)
├── .gitignore                   # Arquivos a serem ignorados pelo Git
└── README.md                    # Documentação do projeto
```

---

## ✨ Funcionalidades

- Leitura e análise automática de dados bancários: Saldo em conta, Limites.
- Geração de **dicas personalizadas** com base no comportamento financeiro.
- Interface intuitiva para visualização dos resultados.
- Arquitetura modular com agente especializado em cada tipo de perfil de Cliente.

---

## 📌 Observações

- Atualiza o banco de dados da aplicação (arquivo CSV) disponibizando futuras implementações: histórico, geração de graficos, envio de sugestões em massa, etc.
- As sugestões são geradas com base em regras gerais e **NÃO** substituem orientação financeira profissional.

---

## ✉️ Contato

Para dúvidas, sugestões ou contribuições, entre em contato.

- Email:    bfpc7@icloud.com
- GitHub:   https://github.com/Bernardinense
- LinkedIn: https://www.linkedin.com/in/bfpc7/

---

## 📄 Licença

Apache 2.0
