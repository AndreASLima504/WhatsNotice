from tkinter import *
from threading import Thread
import time
import os
from envioDeMensagens import WhatsAppBot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Application:
    def __init__(self, master=None):
        self.master = master
        self.master.title("Envio Automático WhatsApp")
        self.master.geometry("480x300")

        # Mensagem inicial padrão
        self.mensagem = StringVar(value="Olá! Esta é uma mensagem automática de teste.")

        # Widgets principais
        self.frame = Frame(master)
        self.frame.pack(pady=15)

        Label(self.frame, text="Mensagem a enviar:", font=("Calibri", 10, "bold")).pack()

        self.text_input = Text(self.frame, width=50, height=4, font=("Calibri", 10))
        self.text_input.insert("1.0", self.mensagem.get())
        self.text_input.pack(pady=5)

        # Botões
        self.botao_whatsapp = Button(
            self.frame,
            text="Abrir WhatsApp Web",
            font=("Calibri", 10),
            width=20,
            command=self.iniciar_driver
        )
        self.botao_whatsapp.pack(pady=5)

        self.botao_enviar = Button(
            self.frame,
            text="Iniciar envio",
            font=("Calibri", 10),
            width=20,
            state=DISABLED,
            command=self.iniciar_envio
        )
        self.botao_enviar.pack(pady=5)

        # Status
        self.status_label = Label(self.frame, text="", font=("Calibri", 9), fg="green", wraplength=400, justify="center")
        self.status_label.pack(pady=10)

        # Bot é inicializado apenas quando o driver for aberto
        self.bot = None

    def atualizar_status(self, texto):
        self.status_label.config(text=texto)
        self.master.update_idletasks()

    def iniciar_driver(self):
        mensagem_usuario = self.text_input.get("1.0", END).strip()
        if not mensagem_usuario:
            self.atualizar_status("⚠️ Digite uma mensagem antes de iniciar o envio.")
            return

        self.mensagem.set(mensagem_usuario)
        self.atualizar_status("Abrindo WhatsApp Web...")

        def run_driver():
            self.bot = WhatsAppBot(
                mensagem=self.mensagem.get(),
                delay=3,
                status_callback=self.atualizar_status
            )
            self.bot.iniciar_driver()
            self.atualizar_status("✅ WhatsApp Web aberto. Escaneie o QR Code e clique em 'Iniciar envio'.")
            self.botao_enviar.config(state=NORMAL)

        Thread(target=run_driver).start()

    def iniciar_envio(self):
        if not self.bot:
            self.atualizar_status("⚠️ Abra o WhatsApp Web primeiro.")
            return

        self.atualizar_status("🚀 Iniciando envio de mensagens...")
        Thread(target=self.bot.enviar_mensagens).start()


# ==============================
# EXECUÇÃO
# ==============================
if __name__ == "__main__":
    root = Tk()
    app = Application(root)
    root.mainloop()