import os
import time
import threading
import customtkinter as ctk
from tkinter import messagebox
from dotenv import load_dotenv
from openai import OpenAI

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configuração do visual do CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Credenciais pré-definidas para a Tela de Login
USUARIO_CORRETO = "admin"
SENHA_CORRETA = "1234"

# Modelo testado e disponível para a conta gratuita
MODELO_IA = "openai/gpt-oss-20b"
PROMPT_SISTEMA = "Você é um assistente de TI prestativo e educado do SENAI."


class AppChatbot(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Chatbot IA - SENAI (NVIDIA NIM)")
        self.geometry("500x650")
        self.resizable(False, False)

        # Cliente NVIDIA NIM (padrão OpenAI). A chave vem do arquivo .env
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv("NVIDIA_API_KEY"),
        )

        # Histórico de mensagens para manter o contexto da conversa
        self.historico_mensagens = [
            {"role": "system", "content": PROMPT_SISTEMA}
        ]

        # Iniciar na Tela de Login
        self.criar_tela_login()

    # ==========================================
    # 1. TELA DE LOGIN
    # ==========================================
    def criar_tela_login(self):
        self.frame_login = ctk.CTkFrame(self)
        self.frame_login.pack(padx=20, pady=20, fill="both", expand=True)

        lbl_titulo = ctk.CTkLabel(self.frame_login, text="Login do Sistema", font=("Arial", 22, "bold"))
        lbl_titulo.pack(pady=(40, 20))

        self.ent_usuario = ctk.CTkEntry(self.frame_login, placeholder_text="Usuário", width=250)
        self.ent_usuario.pack(pady=10)

        self.ent_senha = ctk.CTkEntry(self.frame_login, placeholder_text="Senha", show="*", width=250)
        self.ent_senha.pack(pady=10)

        btn_entrar = ctk.CTkButton(self.frame_login, text="Entrar", command=self.validar_login, width=250)
        btn_entrar.pack(pady=20)

    def validar_login(self):
        usuario = self.ent_usuario.get()
        senha = self.ent_senha.get()

        if usuario == USUARIO_CORRETO and senha == SENHA_CORRETA:
            self.frame_login.destroy()
            self.criar_tela_chat()
        else:
            messagebox.showerror("Erro de Autenticação", "Usuário ou senha inválidos!")

    # ==========================================
    # 2. TELA PRINCIPAL DO CHAT
    # ==========================================
    def criar_tela_chat(self):
        # Barra superior de controles
        self.frame_topo = ctk.CTkFrame(self, height=40)
        self.frame_topo.pack(fill="x", padx=10, pady=(10, 0))

        lbl_usuario = ctk.CTkLabel(self.frame_topo, text="Usuário: Admin", font=("Arial", 12, "bold"))
        lbl_usuario.pack(side="left", padx=10)

        self.btn_tema = ctk.CTkButton(self.frame_topo, text="Alternar Tema", command=self.alternar_tema, width=120)
        self.btn_tema.pack(side="right", padx=10, pady=5)

        self.btn_limpar = ctk.CTkButton(
            self.frame_topo, text="Limpar", command=self.limpar_conversa,
            fg_color="red", hover_color="darkred", width=80
        )
        self.btn_limpar.pack(side="right", padx=5, pady=5)

        # Caixa de texto com scroll para exibir a conversa
        self.txt_conversa = ctk.CTkTextbox(self, state="disabled", wrap="word", font=("Arial", 13))
        self.txt_conversa.pack(padx=10, pady=10, fill="both", expand=True)

        # Área de input e envio
        self.frame_input = ctk.CTkFrame(self)
        self.frame_input.pack(fill="x", padx=10, pady=(0, 10))

        self.ent_mensagem = ctk.CTkEntry(self.frame_input, placeholder_text="Digite sua mensagem...", font=("Arial", 13))
        self.ent_mensagem.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        self.ent_mensagem.bind("<Return>", lambda event: self.enviar_mensagem())

        self.btn_enviar = ctk.CTkButton(self.frame_input, text="Enviar", command=self.enviar_mensagem, width=90)
        self.btn_enviar.pack(side="right", padx=(5, 10), pady=10)

        # Mensagem inicial
        self.exibir_mensagem("IA Chatbot", "Olá! Sou o assistente de TI via NVIDIA NIM. Como posso te ajudar hoje?")

    # ==========================================
    # 3. EXIBIÇÃO E MANIPULAÇÃO DE MENSAGENS
    # ==========================================
    def exibir_mensagem(self, remetente, mensagem):
        self.txt_conversa.configure(state="normal")
        self.txt_conversa.insert("end", f"{remetente}:\n{mensagem}\n\n")
        self.txt_conversa.configure(state="disabled")
        self.txt_conversa.see("end")

    def alternar_tema(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")

    def limpar_conversa(self):
        self.txt_conversa.configure(state="normal")
        self.txt_conversa.delete("1.0", "end")
        self.txt_conversa.configure(state="disabled")
        # Reinicia o histórico, mantendo apenas a instrução do sistema
        self.historico_mensagens = [
            {"role": "system", "content": PROMPT_SISTEMA}
        ]

    # ==========================================
    # 4. LÓGICA DE RESPOSTA E IA (NVIDIA)
    # ==========================================
    def enviar_mensagem(self):
        texto_usuario = self.ent_mensagem.get().strip()
        if not texto_usuario:
            return

        self.ent_mensagem.delete(0, "end")
        self.exibir_mensagem("Você", texto_usuario)

        threading.Thread(target=self.processar_resposta, args=(texto_usuario,), daemon=True).start()

    def processar_resposta(self, pergunta):
        time.sleep(0.5)

        respostas_locais = {
            "python": "Python é uma linguagem de programação de alto nível, amplamente usada em Data Science, IA e Web.",
            "html": "HTML é a linguagem de marcação padrão para criar páginas web.",
            "css": "CSS é usado para estilizar e estruturar o visual de páginas HTML.",
            "sql": "SQL é a linguagem padrão para gerenciar e consultar bancos de dados relacionais."
        }

        resposta_final = ""

        # Adiciona a mensagem do usuário ao histórico
        self.historico_mensagens.append({"role": "user", "content": pergunta})

        try:
            response = self.client.chat.completions.create(
                model=MODELO_IA,
                messages=self.historico_mensagens,
                temperature=0.2,
                top_p=0.7,
                max_tokens=2048
            )
            resposta_final = response.choices[0].message.content or ""

            if not resposta_final:
                raise ValueError("A API retornou uma resposta vazia.")

            # Adiciona a resposta da IA ao histórico
            self.historico_mensagens.append({"role": "assistant", "content": resposta_final})

        except Exception as e:
            print(f"\n[ERRO DETALHADO DA API NVIDIA]: {e}\n")

            # Remove a pergunta que falhou, para não contaminar o histórico
            self.historico_mensagens.pop()

            pergunta_lower = pergunta.lower()
            for chave, resposta in respostas_locais.items():
                if chave in pergunta_lower:
                    resposta_final = resposta
                    break

            if not resposta_final:
                resposta_final = "Desculpe, ocorreu um erro ao conectar com a API da NVIDIA."

        self.after(0, self.exibir_mensagem, "IA Chatbot", resposta_final)


if __name__ == "__main__":
    app = AppChatbot()
    app.mainloop()