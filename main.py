import os
import time
import threading
import customtkinter as ctk
from tkinter import messagebox
from google import genai

# Configuração do visual do CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# Credenciais pré-definidas para a Tela de Login
USUARIO_CORRETO = "admin"
SENHA_CORRETA = "1234"


class AppChatbot(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Chatbot IA - SENAI")
        self.geometry("500x650")
        self.resizable(False, False)

        # Configuração do Cliente Gemini
        api_key = os.environ.get("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)
        
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
        # Barra Superior de Controles
        self.frame_topo = ctk.CTkFrame(self, height=40)
        self.frame_topo.pack(fill="x", padx=10, pady=(10, 0))

        lbl_usuario = ctk.CTkLabel(self.frame_topo, text="Usuário: Admin", font=("Arial", 12, "bold"))
        lbl_usuario.pack(side="left", padx=10)

        self.btn_tema = ctk.CTkButton(self.frame_topo, text="Alternar Tema", command=self.alternar_tema, width=120)
        self.btn_tema.pack(side="right", padx=10, pady=5)

        self.btn_limpar = ctk.CTkButton(self.frame_topo, text="Limpar", command=self.limpar_conversa, fg_color="red", hover_color="darkred", width=80)
        self.btn_limpar.pack(side="right", padx=5, pady=5)

        # Caixa de Texto com Scroll para exibir a conversa
        self.txt_conversa = ctk.CTkTextbox(self, state="disabled", wrap="word", font=("Arial", 13))
        self.txt_conversa.pack(padx=10, pady=10, fill="both", expand=True)

        # Área de Input e Envio
        self.frame_input = ctk.CTkFrame(self)
        self.frame_input.pack(fill="x", padx=10, pady=(0, 10))

        self.ent_mensagem = ctk.CTkEntry(self.frame_input, placeholder_text="Digite sua mensagem...", font=("Arial", 13))
        self.ent_mensagem.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        self.ent_mensagem.bind("<Return>", lambda event: self.enviar_mensagem())

        self.btn_enviar = ctk.CTkButton(self.frame_input, text="Enviar", command=self.enviar_mensagem, width=90)
        self.btn_enviar.pack(side="right", padx=(5, 10), pady=10)

        # Mensagem Inicial
        self.exibir_mensagem("IA Chatbot", "Olá! Sou o assistente de TI. Como posso te ajudar hoje?")

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

    # ==========================================
    # 4. LÓGICA DE RESPOSTA E IA
    # ==========================================
    def enviar_mensagem(self):
        texto_usuario = self.ent_mensagem.get().strip()
        if not texto_usuario:
            return

        # Limpa o campo de entrada e exibe a mensagem do usuário
        self.ent_mensagem.delete(0, "end")
        self.exibir_mensagem("Você", texto_usuario)

        # Usa uma Thread separada para não travar a interface gráfica durante a resposta
        threading.Thread(target=self.processar_resposta, args=(texto_usuario,), daemon=True).start()

    def processar_resposta(self, pergunta):
        # Simula um pequeno atraso (raciocínio da IA)
        time.sleep(1)

        # Respostas locais de backup sobre TI
        respostas_locais = {
            "python": "Python é uma linguagem de programação de alto nível, amplamente usada em Data Science, IA e Web.",
            "html": "HTML é a linguagem de marcação padrão para criar páginas web.",
            "css": "CSS é usado para estilizar e estruturar o visual de páginas HTML.",
            "sql": "SQL é a linguagem padrão para gerenciar e consultar bancos de dados relacionais."
        }

        resposta_final = ""

        # Tenta obter resposta da API do Gemini
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=pergunta
            )
            resposta_final = response.text
        except Exception:
            # Caso a API falhe ou não haja internet, recorre à resposta condicional local sobre TI
            pergunta_lower = pergunta.lower()
            for chave, resposta in respostas_locais.items():
                if chave in pergunta_lower:
                    resposta_final = resposta
                    break

            if not resposta_final:
                resposta_final = "Desculpe, estou temporariamente sem conexão com a IA principal e não encontrei este assunto na minha base local de TI."

        # Atualiza a interface gráfica com a resposta da IA
        self.after(0, self.exibir_mensagem, "IA Chatbot", resposta_final)


# ESSAS LINHAS NO FINAL SÃO OBLIGATÓRIAS PARA ABRIR A JANELA
if __name__ == "__main__":
    app = AppChatbot()
    app.mainloop()