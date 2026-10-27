# Chatbot Desktop em Python com CustomTkinter

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-blueviolet?style=for-the-badge)
![NVIDIA NIM](https://img.shields.io/badge/AI-NVIDIA_NIM-76B900?style=for-the-badge&logo=nvidia)


Aplicação desktop em Python que simula um chatbot de TI. O projeto inclui login local, troca entre modo claro e escuro, respostas locais para temas básicos e integração com modelos de IA da plataforma NVIDIA NIM.

---

## Funcionalidades

- **Tela de login:** autenticação local com credenciais pré-definidas.
- **Interface gráfica:** construída com CustomTkinter, com troca de tema (escuro/claro) em tempo real.
- **Gerenciamento de conversa:** caixa de texto com rolagem automática, histórico de contexto e botão para limpar a conversa.
- **Respostas com IA e fallback local:** integração com modelos da NVIDIA NIM. Se a API falhar, o chatbot responde com textos locais sobre Python, HTML, CSS e SQL.
- **Processamento em segundo plano:** o módulo `threading` envia as requisições à API sem travar a interface.

---

## Tecnologias

- **Linguagem:** Python 3.x
- **Interface gráfica:** CustomTkinter
- **Integração com IA:** OpenAI SDK (`openai`), apontando para a API da NVIDIA NIM
- **Variáveis de ambiente:** `python-dotenv`
- **Concorrência:** módulo nativo `threading`

---

## Instalação e Execução

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/chatBotIA.git
cd chatBotIA
```

### 2. Instalar as dependências

Com o Python 3.x instalado, execute no terminal:

```bash
pip install customtkinter openai python-dotenv
```

### 3. Obter a chave da API

1. Crie uma conta em [build.nvidia.com](https://build.nvidia.com).
2. Gere uma chave de API no painel. Ela começa com `nvapi-`.

### 4. Configurar o arquivo `.env`

Crie um arquivo chamado `.env` na raiz do projeto, na mesma pasta do `main.py`, com o conteúdo:

```
NVIDIA_API_KEY=nvapi-sua-chave-aqui
```

> **Importante:** o arquivo `.env` contém sua chave pessoal. Ele já deve estar listado no `.gitignore` para não ser enviado ao GitHub. Nunca escreva a chave diretamente no código.

### 5. Executar a aplicação

```bash
python main.py
```

---

## Modelo utilizado

O modelo está definido na constante `MODELO_IA` no início do `main.py`. Atualmente:

```python
MODELO_IA = "openai/gpt-oss-20b"
```

Os modelos disponíveis na NVIDIA NIM mudam com o tempo. Se a aplicação passar a retornar erros `404` ou `410`, o modelo pode ter sido removido do catálogo. Para ver os modelos disponíveis para a sua chave, rode:

```python
from openai import OpenAI
import os

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY"),
)

for m in client.models.list().data:
    print(m.id)
```

---

## Acesso de teste

Para entrar na aplicação, use as credenciais padrão:

- **Usuário:** `admin`
- **Senha:** `1234`

---

## Estrutura do projeto

```
chatBotIA/
├── main.py       # Código principal da aplicação
├── .env          # Chave da API (não versionar)
├── .gitignore    # Deve conter ao menos: .env
└── README.md
```

---