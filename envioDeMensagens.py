from selenium import webdriver
# import selenium.webdriver
# import selenium.webdriver.firefox
# import selenium.webdriver.common
# import selenium.webdriver.support
# import selenium.webdriver.remote
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from tkinter import *
from threading import Thread
import time
import os


# ==============================
# SERVIÇO DE AUTOMAÇÃO
# ==============================
class WhatsAppBot:
    def __init__(self, mensagem, delay=3, status_callback=None):
        self.mensagem = mensagem
        self.delay = delay
        self.status_callback = status_callback
        self.nomes_vistos = set()
        self.driver = None
        self.arquivo_contatados = "clientes_contatados.txt"

        if not os.path.exists(self.arquivo_contatados):
            open(self.arquivo_contatados, "w", encoding="utf-8").close()

        with open(self.arquivo_contatados, "r", encoding="utf-8") as f:
            self.nomes_vistos = set(f.read().splitlines())

    def registrar_mensagem_enviada(self, nome):
        with open(self.arquivo_contatados, "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{nome}\n")
        self.nomes_vistos.add(nome)
        
    def rolar_lista_para_baixo(self, destino):
            print("Rolando lista para baixo...")
            self.driver.execute_script("arguments[0].scrollIntoView();", destino)
            # destino.click()
            time.sleep(1.5)
            


    def iniciar_driver(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://web.whatsapp.com")
        if self.status_callback:
            self.status_callback("Escaneie o QR Code do WhatsApp Web e clique em 'Iniciar envio' quando estiver logado.")

    def filtrar_chats_novos(self, chats):
        novos_chats = []
        for chat in chats:
            try:
                nome_elem = chat.find_element(By.XPATH, ".//span[@title]")
                nome = nome_elem.get_attribute("title")
                if nome not in self.nomes_vistos:
                    novos_chats.append((chat, nome))
            except:
                continue
        return novos_chats

    def enviar_mensagens(self):
        if not self.driver:
            raise RuntimeError("Driver não iniciado. Chame iniciar_driver() antes de enviar mensagens.")

        time.sleep(3)

        while True:

            chats = self.driver.find_elements(By.XPATH, "//div[@role='row']")
            print("Atualizando conversas. Total encontrado:", len(chats))

            novos_chats = self.filtrar_chats_novos(chats)
            print("Não lidas:", len(novos_chats))
            
            while not novos_chats:
                try:
                    self.rolar_lista_para_baixo(chats[-1])
                except Exception as e:
                    print("Erro ao rolar lista ->", e)
                    if self.status_callback:
                        self.status_callback("⚠️ Erro ao rolar a lista.")
                    break

                # Recarregar a lista após rolar
                chats = self.driver.find_elements(By.XPATH, "//div[@role='row']")
                novos_chats = self.filtrar_chats_novos(chats)

                print("Após scroll → Total:", len(chats), "| Não lidas:", len(novos_chats))

            for chat, nome in novos_chats:
                try:
                    if self.status_callback:
                        self.status_callback(f"💬 Enviando mensagem para {nome}...")

                    # Scroll até o chat
                    self.driver.execute_script("arguments[0].scrollIntoView();", chat)
                    chat.click()
                    time.sleep(2)

                    # Input da mensagem
                    try:
                        text_box = self.driver.find_element(
                            By.XPATH,
                            "//div[contains(@class, '_ak1r')]"
                            "//div[contains(@class, 'lexical-rich-text-input')]"
                            "//div[@role='textbox' and @contenteditable='true']"
                        )
                    except Exception as e:
                        print("Erro ao localizar caixa de mensagem ->", e)
                        if self.status_callback:
                            self.status_callback(f"⚠️ Não foi possível encontrar a caixa de mensagem para {nome}.")
                            self.registrar_mensagem_enviada(nome)
                        continue

                    # Enviar de fato (se quiser ativar)
                    # for char in self.mensagem:
                    #     text_box.send_keys(char)
                    # text_box.send_keys(Keys.ENTER)

                    # Registrar contato
                    self.registrar_mensagem_enviada(nome)
                    if self.status_callback:
                        self.status_callback(f"✅ Mensagem enviada para {nome}")

                    time.sleep(self.delay)

                except Exception as e:
                    print("Erro ao enviar mensagem para", nome, "->", e)
                    if self.status_callback:
                        self.status_callback(f"⚠️ Erro ao enviar para {nome}.")
                    continue  # NÃO PARA O LOOP → continua com os próximos


            try:
                chats_atualizados = self.driver.find_elements(By.XPATH, "//div[@role='row']")
                if chats_atualizados:
                    self.driver.execute_script("arguments[0].scrollIntoView();", chats_atualizados[-1])
                    time.sleep(2)
            except Exception as e:
                print("Erro ao rolar lista no final ->", e)
