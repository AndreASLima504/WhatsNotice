
---

# 📩 WhatsNotice

WhatsNotice é uma ferramenta de automação para envio de mensagens no **WhatsApp Web** utilizando **Python + Selenium**.  
O objetivo do projeto é facilitar o contato em escala, enviando mensagens personalizadas para múltiplos chats não lidos de forma estável e contínua.

---

## 🚀 Funcionalidades

- Detecta automaticamente conversas **não lidas** no WhatsApp Web  
- Envia mensagens personalizadas para cada chat  
- Evita contatos repetidos (registro automático em arquivo.txt)  
- Sistema robusto contra erros como `StaleElementReferenceException`  
- Rolagem inteligente para encontrar novos chats  
- Interface simples com Tkinter  
- Logs em tempo real

---

## 📦 Tecnologias Utilizadas

- **Python 3**
- **Selenium WebDriver**
- **Firefox + Geckodriver**
- **Tkinter**
- **WhatsApp Web**

---

## 🛠️ Instalação e Configuração

1. Clone o repositório:

```sh
git clone https://github.com/AndreASLima504/WhatsNotice
cd WhatsNotice
````

2. Instale as dependências:

```sh
pip install -r requirements.txt
```

3. Certifique-se de ter instalado:

* **Firefox**
* **Geckodriver** (compatível com sua versão do navegador)

4. Execute o programa:

```sh
python interface.py
```

---

## ▶️ Como Usar

1. Abra o programa (interface Tkinter)
2. Escreva a mensagem que deseja enviar para os contatos
3. Clique em **Iniciar Driver**
4. No navegador que abrir, faça login no **WhatsApp Web**
5. Clique em **Atualizar lista de contatos**
6. O bot começará a varrer a lista de conversas e registrar os nomes dos contatos na lista de contatos
7. Clique em **Iniciar envio**
8. O bot comecará a enviar a mensagem automaticamente para os contatos da lista de contatos que não estão em "clientes_contatados"

---

## 📁 Armazenamento de Contatos

Contatos são registrados em:

```
lista_contatos.txt
```

Contatos já atendidos são registrados em:
```
lista_contatos.txt
```

Isso impede que o bot envie mensagens duplicadas quando for necessário parar no meio do processo e continuar mais tarde. 

**IMPORTANTE:** Os arquivos .txt devem estar no mesmo diretório que a aplicação

---

## ⚠️ Aviso Legal

Este projeto tem finalidade **educacional**.
Automatizar o WhatsApp Web pode violar seus termos de serviço.
Use por sua conta e risco.

---

