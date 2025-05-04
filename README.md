# Chatbot FURIA Mil Grau - Telegram + Gemini 🖤💛🤖

Este repositório contém o código para o **Chatbot FURIA Mil Grau**, um bot de Telegram desenvolvido em Python que utiliza a API do Google Gemini para interagir com usuários.

O bot é configurado com uma **persona específica**: um fã fanático da FURIA Esports no cenário de CS2, membro da "Tribo" do Gaules, utilizando gírias e um tom de voz característico da comunidade.

## ✨ Funcionalidades Principais

* **Integração com Telegram:** Responde a mensagens e comandos básicos (`/start`) na plataforma Telegram.
* **Inteligência Artificial com Gemini:** Utiliza o modelo `gemini-1.5-flash` (configurável) para gerar respostas contextuais e criativas.
* **Persona Customizada:** Possui uma `SYSTEM_INSTRUCTION` detalhada que define seu comportamento, tom de voz e uso de gírias (ex: "Calma", "Paquetá", "NTJ", "Família", "Professor").
* **Foco Temático:** Conversa sobre CS2, a FURIA, campeonatos e a cultura da Tribo.

## 🚀 Tecnologias Utilizadas

* Python 3
* `pyTelegramBotAPI` (para a API do Telegram)
* `google-generativeai` (para a API do Gemini)
* `python-dotenv` (para gerenciamento de chaves de API)

## 🔧 Configuração

1.  Clone o repositório.
2.  Instale as dependências: `pip install pyTelegramBotAPI google-generativeai python-dotenv`
3.  Crie um arquivo `.env` na raiz do projeto.
4.  Adicione suas chaves de API ao `.env`:
    ```
    BOT_TOKEN=SUA_CHAVE_TELEGRAM_AQUI
    GEMINI_API_KEY=SUA_CHAVE_GEMINI_AQUI
    ```
5.  Execute o script Python: `python seu_script.py`

## ⚠️ Aviso

Este é um projeto **não oficial**, criado para fins de entretenimento e aprendizado. Não possui afiliação direta com a FURIA Esports ou o Gaules.
