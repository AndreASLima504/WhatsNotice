
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
2. Clique em **Iniciar Driver**
3. No navegador que abrir, faça login no **WhatsApp Web**
4. Clique em **Iniciar envio**
5. O bot começará a varrer a lista de conversas e enviar mensagens automáticas para contatos não lidos

---

## 📁 Armazenamento de Contatos

Contatos já atendidos são registrados em:

```
clientes_contatados.txt
```

Isso impede que o bot envie mensagens duplicadas. 

**IMPORTANTE:** O arquivo .txtdeve estar no mesmo diretório que a aplicação

---

## ⚠️ Aviso Legal

Este projeto tem finalidade **educacional**.
Automatizar o WhatsApp Web pode violar seus termos de serviço.
Use por sua conta e risco.

---

