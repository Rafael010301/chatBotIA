# Chatbot Desktop em Python com CustomTkinter

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-blueviolet?style=for-the-badge)
![Google Gemini](https://img.shields.io/badge/AI-Google_Gemini-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Aplicação desktop em Python que simula um chatbot inteligente. O projeto inclui login local, troca entre modo claro e escuro, respostas locais para temas de TI e integração com a API do Google Gemini.

---

## Funcionalidades

- **Tela de login:** autenticação local com credenciais pré-definidas.
- **Interface gráfica:** construída com CustomTkinter, com troca de tema (escuro/claro) em tempo real.
- **Gerenciamento de conversa:** caixa de texto com rolagem automática e botão para limpar o histórico.
- **Respostas com IA e fallback local:** integração com o modelo Gemini e respostas locais estruturadas para temas de TI quando não há conexão ou a API não está disponível.
- **Processamento assíncrono:** o módulo `threading` simula o tempo de resposta da IA sem travar a interface.

---

## Tecnologias

- **Linguagem:** Python 3.x
- **Interface gráfica:** CustomTkinter
- **Integração com IA:** Google GenAI SDK (`google-genai`)
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
pip install customtkinter google-genai
```

### 3. Configurar a chave da API (opcional)

A chave do Gemini é lida da variável de ambiente `GEMINI_API_KEY`. Sem ela, o chatbot continua funcionando com as respostas locais para temas de TI.

No PowerShell (Windows):

```powershell
$env:GEMINI_API_KEY="SUA_CHAVE_AQUI"
```

No Linux ou macOS:

```bash
export GEMINI_API_KEY="SUA_CHAVE_AQUI"
```

### 4. Executar a aplicação

```bash
python main.py
```

---

## Acesso de teste

Para entrar na aplicação, use as credenciais padrão:

- **Usuário:** `admin`
- **Senha:** `1234`

---
