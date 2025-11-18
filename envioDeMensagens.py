from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from tkinter import *
from threading import Thread
import time
import os

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

            while True:
                actions = ActionChains(self.driver)
                actions.send_keys(Keys.ESCAPE).perform()
                chats = self.driver.find_elements(By.XPATH, "//div[@role='row']")
                novos_chats = self.filtrar_chats_novos(chats)

                print(f"Atualizando conversas → Total: {len(chats)} | Não lidas: {len(novos_chats)}")

                if novos_chats:  # SE TEM NÃO LIDOS → SAI
                    break

                if not chats:
                    print("⚠️ Nenhum chat visível. Aguardando reconstrução...")
                    time.sleep(1)
                    continue

                try:
                    
                    self.rolar_lista_para_baixo(chats[-1])
                except Exception as e:
                    print("Erro ao rolar lista ->", e)
                    time.sleep(1)
                    continue

                time.sleep(1)

        
            for _chat_element, nome in novos_chats:

                try:
                    if self.status_callback:
                        self.status_callback(f"💬 Enviando mensagem para {nome}...")

                    chat_fresco = None
                    actions = ActionChains(self.driver)
                    actions.send_keys(Keys.ESCAPE).perform()
                    chats_visiveis = self.driver.find_elements(By.XPATH, "//div[@role='row']")

                    for c in chats_visiveis:
                        try:
                            span = c.find_element(By.XPATH, ".//span[@title]")
                            if span.get_attribute("title") == nome:
                                chat_fresco = c
                                break
                        except:
                            continue

                    if not chat_fresco:
                        print(f"❌ Chat de {nome} não encontrado após stale refresh.")
                        continue

                    self.driver.execute_script("arguments[0].scrollIntoView();", chat_fresco)
                    time.sleep(0.5)
                    chat_fresco.click()
                    time.sleep(1.5)

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
                    
                    # Envio da mensagem
                    for char in self.mensagem:
                        text_box.send_keys(char)
                    text_box.send_keys(Keys.ENTER)

                    self.registrar_mensagem_enviada(nome)

                    if self.status_callback:
                        self.status_callback(f"✅ Mensagem enviada para {nome}")

                    time.sleep(self.delay)

                except Exception as e:
                    print(f"Erro ao enviar mensagem para {nome} -> {e}")
                    if self.status_callback:
                        self.status_callback(f"⚠️ Erro ao enviar para {nome}.")
                    continue

            # =====================================================
            # 3. SCROLL FINAL PARA FORÇAR O WHATSAPP A ATUALIZAR
            # =====================================================
            try:
                actions = ActionChains(self.driver)
                actions.send_keys(Keys.ESCAPE).perform()
                chats_atualizados = self.driver.find_elements(By.XPATH, "//div[@role='row']")
                if chats_atualizados:
                    self.rolar_lista_para_baixo(chats_atualizados[-1])
                    time.sleep(1)
            except Exception as e:
                print("Erro ao rolar lista no final ->", e)
