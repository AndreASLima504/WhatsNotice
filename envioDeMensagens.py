from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import *
from threading import Thread
import time
import os

class WhatsAppBot:
    def __init__(self, mensagem, delay=3, status_callback=None):
        self.mensagem = mensagem
        self.delay = delay
        self.status_callback = status_callback
        self.driver = None
        
        self.arquivo_contatados = "clientes_contatados.txt"
        self.mensagens_enviadas = set()
        
        self.arquivo_contatos = "lista_contatos.txt"
        self.contatos = set()
        
        self.contatos_pendentes = list()

        if not os.path.exists(self.arquivo_contatados):
            open(self.arquivo_contatados, "w", encoding="utf-8").close()

        with open(self.arquivo_contatados, "r", encoding="utf-8") as f:
            self.mensagens_enviadas = set(f.read().splitlines())
            
        if not os.path.exists(self.arquivo_contatos):
            open(self.arquivo_contatos, "w", encoding="utf-8").close()
        
        with open(self.arquivo_contatos, "r", encoding="utf-8") as f:
            self.contatos = set(f.read().splitlines())
            



    def registrar_mensagem_enviada(self, nome):
        with open(self.arquivo_contatados, "a", encoding="utf-8") as arquivo:
            arquivo.write(f"{nome}\n")
        self.mensagens_enviadas.add(nome)
        
        
    def registrar_novo_contato(self, nome):
        if nome not in self.contatos:
            self.contatos.add(nome)
            with open(self.arquivo_contatos, "a", encoding="utf-8") as arquivo:
                arquivo.write(f"{nome}\n")
        
        if nome not in self.mensagens_enviadas:
            self.contatos_pendentes.append(nome)
            
            
        
    def rolar_lista_para_baixo(self, destino):
            print("Rolando lista para baixo...")
            self.driver.execute_script("arguments[0].scrollIntoView();", destino)
            time.sleep(1.5)
            


    def iniciar_driver(self):
        self.driver = webdriver.Firefox()
        self.driver.get("https://web.whatsapp.com")
        if self.status_callback:
            self.status_callback("Escaneie o QR Code do WhatsApp Web e clique em 'Iniciar envio' quando estiver logado.")

    
    def scroll_forcar_atualizacao(self):
        try:
            chats_atualizados = self.driver.find_elements(By.XPATH, "//div[@role='row']")
            if chats_atualizados:
                self.rolar_lista_para_baixo(chats_atualizados[-1])
                time.sleep(1)
                print("Rolando lista para baixo")
        except Exception as e:
            print("Erro ao rolar lista no final ->", e)


    def enviar_mensagens(self):
        for contato in self.contatos:
            if contato not in self.mensagens_enviadas:
                self.contatos_pendentes.append(contato)
        
        for nome_contato in self.contatos_pendentes:
            tentativas = 0
            while tentativas < 3:
                try:
                    self.garantir_conexao()
                    self.enviar_mensagem_para_contato(nome_contato)
                    self.registrar_mensagem_enviada(nome_contato)
                    break
                except Exception as e:
                    self.status_callback(f"❌ Erro ao enviar mensagem para {nome_contato}: {e}" + f"Tentativa {tentativas}/3")
                    tentativas += 1
                    print(f"Erro em {nome_contato}: {e}")
            else:
                self.status_callback(f"⚠️ Falha ao enviar mensagem para {nome_contato} após 3 tentativas. Pulando contato e atualizando a página.")
                print(f"⚠️ Falha ao enviar mensagem para {nome_contato} após 3 tentativas. Pulando contato e atualizando a página.")
                self.driver.get("https://web.whatsapp.com")
                

            time.sleep(5)
        
        self.status_callback("✅ Envio de mensagens concluído para todos os contatos.")
            
            
    def garantir_conexao(self):
        try:
            self.driver.find_element(By.ID, "pane-side")
            return True
        except:
            self.status_callback(f"WhatsApp perdeu sessão/recarregou. Tentando recuperar...")
            
            try:
                time.sleep(10)

                self.driver.find_element(By.ID, "pane-side")
                self.status_callback("Sessão restaurada.")
                return True

            except Exception as e:
                self.status_callback(f"❌ Falha ao restaurar sessão: {e}")
                return False
        
    def enviar_mensagem_para_contato(self, nome_contato):
        caixa_pesquisa = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@role='textbox']")
                )
        )
        
        self.status_callback(f"Enviando mensagem para {nome_contato}...")
        caixa_pesquisa.click()
                
        for char in nome_contato:
            caixa_pesquisa.send_keys(char)
        time.sleep(1)
        
        conversa = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, f".//span[@title]")
            )
        )
        conversa.click()
                
        caixa_pesquisa.clear()
        time.sleep(1)
        
        try:
                print("Localizando caixa de mensagem para", nome_contato)
                caixa_mensagem = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located(
                        (By.XPATH,
                            "//div[@data-testid='conversation-compose-box-input']"
                        )
                    )
                )

                # Envio da mensagem
                print("Enviando mensagem para", nome_contato)
                for char in self.mensagem:
                    caixa_mensagem.send_keys(char)
                caixa_mensagem.send_keys(Keys.ENTER)
        except Exception as e:
            print("Erro ao localizar caixa de mensagem ->", e)
            if self.status_callback:
                self.status_callback(f"⚠️ Não foi possível encontrar a caixa de mensagem para {nome_contato}.")
            
            
    def buscar_contatos(self):
        # Encontra o elemento primeiro (opcional, mas recomendado para clareza)
        pane_side = self.driver.find_element(By.ID, "pane-side")
        
        self.status_callback("Buscando contatos...")

        while True:
            chats_visiveis = self.driver.find_elements(By.XPATH, "//div[@role='row']")
            
            if not chats_visiveis:
                time.sleep(1)
                continue
            
            for chat in chats_visiveis:
                nome = chat.find_element(By.XPATH, ".//span[@title]")
                self.registrar_novo_contato(nome.get_attribute("title"))
                
            
            is_at_bottom = self.driver.execute_script(
                """
                var el = arguments[0];
                return (el.scrollTop + el.clientHeight) >= (el.scrollHeight - 1);
                """, 
                pane_side
            )
            
            if is_at_bottom:
                print("Chegou ao final da lista de conversas.")
                actions = ActionChains(self.driver)
                actions.send_keys(Keys.ESCAPE).perform()
                self.status_callback("✅ Lista de contatos atualizada. Pronto para enviar mensagens.")
                break
            
            self.rolar_lista_para_baixo(chats_visiveis[-1])
        
            
        
