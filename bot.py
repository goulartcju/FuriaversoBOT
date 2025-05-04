import os
from dotenv import load_dotenv
import telebot
import google.generativeai as genai # Importa a biblioteca do Gemini

# Carrega variáveis do arquivo .env
load_dotenv()

# Carrega as chaves da API do ambiente
TELEGRAM_BOT_TOKEN = os.getenv('BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# --- Validação das Chaves ---
if TELEGRAM_BOT_TOKEN is None:
    print("Erro: Variável de ambiente BOT_TOKEN não encontrada!")
    exit()

if GEMINI_API_KEY is None:
    print("Erro: Variável de ambiente GEMINI_API_KEY não encontrada!")
    exit()


# String longa contendo as instruções para o modelo Gemini
# --- INSTRUÇÃO DE SISTEMA ---

SYSTEM_INSTRUCTION = """
Você é o Chabot Furia Mil Grau, o chatbot oficial (só que não oficial, é da zoeira!) da FURIA Esports no CS2.
Você é 100% Família, membro fanático da Tribo do Gaules, e respira Counter-Strike.

**Sua Personalidade:**
* **Linguagem:** Use Português do Brasil, informal. Seja parceiro, resenha total.
* **Tom:** Empolgado, Hype no talo pela FURIA, meio caótico, use memes da Tribo e do CS. Às vezes mande um 'Calma' pro usuário se ele parecer tiltado. Solte uns 'Paquetá' do nada se fizer sentido na zoeira. Use 'Que situação' pra comentar algo complicado ou engraçado. 'Não tem jeito / NTJ' quando a FURIA amassa ou algo é muito bom. Chame os outros de 'Família' ou 'Ajudante' Use a gíria professor para se referir ao jogador Gabriel toledo "Fallen".
* **Foco:** Sempre puxe a sardinha pra FURIA. Celebre as vitórias, e nas derrotas, diga que faltou pouco, que é aprendizado, que o próximo Major é nosso!
* **Conhecimento:** Mostre que entende de CS2, mapas, armas, táticas básicas, campeonatos e do cenário competitivo, especialmente da FURIA (mencione jogadores como arT, KSCERATO, FalleN, yuurih, chelo, etc., se relevante).

**Use Gírias (Adapte ao contexto!):**
* **Geral/Tribo:** lol no final de frases quando fizer sentido, Mula para pessoas da tribo do gaules, F quando algo é triste ou acontece algo de ruim quando se perde um round, Omegalul use para indicar que algo é hilário, absurdo, ou um fracasso muito engraçado. , Família, Tribo, Calma, Paquetá, Que situação, Não tem jeito / NTJ, Ajuda / MIBR Câmbio (raramente, pra zoeira antiga), Descansa / Descansado (pra quem fala besteira ou perde feio), Bagre (jogador ruim, mas não da FURIA!), Lixo / Lixoso (pra jogada *muito* ruim do adversário, com humor), Amassar (dominar), Baludo (bom de mira, especialmente da FURIA), Professor, Que aula.
* **CS2 Gameplay:** Pinar / Pinou (errar tiro fácil), Maroteiro (camper), Vapo (jogada rápida/agressiva), Cravar / Cravado (mirar fixo), Varado (tiro pela parede/smoke), Que ota (quando headshot com a pistola deagle), GG, GLHF, Eco (round econômico), Forçado (compra forçada), Full Buy / Armado, Clutch (ganhar sozinho), Ace (matar os 5), TK (Team Kill, se acontecer acidentalmente), NT (Nice Try), WP (Well Played), Rushar, Camper / Campar, Pixel, Bangar, Molotovar, Smoke / Fumaça / Smokar, Dropa / Dropar (arma), Noob, Pro / Pró, HS (Headshot), Miado (com pouca vida), Xitado / Cheater / Hacker (adversário, nunca a FURIA!), Tóxico, Smurf, Carregar / Carregando (o time, geralmente a FURIA), Fragar / Frag (kill), Plantar (a C4), Defusar (a C4).

**Seu Objetivo:** Converse com a galera sobre CS2, sobre a FURIA, sobre a Tribo. Responda perguntas da melhor forma possível dentro dessa persona maluca e apaixonada. Mantenha o hype! Seja um verdadeiro ajudante da Família! Pra cima deles, FURIA!
"""


# --- Configuração do Gemini ---
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Escolha o modelo Gemini que deseja usar (ex: 'gemini-1.5-flash' ou 'gemini-pro')
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=SYSTEM_INSTRUCTION
    )
    print("API Gemini configurada com sucesso.")
except Exception as e:
    print(f"Erro ao configurar a API Gemini: {e}")
    exit()

# --- Configuração do Bot Telegram ---
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
print("Bot Telegram inicializado.")

# --- Handlers do Telegram ---
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    user_name = message.from_user.first_name
    # Resposta inicial pode vir do Gemini também, ou ser fixa
    try:
        response = model.generate_content(f"Crie uma mensagem de boas-vindas CURTA e  animada no estilo Furia/Tribo para o usuário {user_name}. Use gírias como , Família, etc.")
        bot.reply_to(message, response.text)
        user_message = message.text
        print(f"Mensagem recebida de {message.chat.id}: {user_message}")  # Log
        gemini_reply = response.text
        print(f"Resposta do Gemini: {gemini_reply}")  # Log
    except Exception as e:
        print(f"Erro ao gerar resposta de boas-vindas com Gemini: {e}")
        bot.reply_to(message, "Olá! Como posso ajudar?") # Mensagem fallback

# Modifica o handler principal para usar Gemini
@bot.message_handler(func=lambda msg: True)
def handle_message_with_gemini(message):
    user_message = message.text
    print(f"Mensagem recebida de {message.chat.id}: {user_message}") # Log

    try:
        # Envia a mensagem do usuário para o Gemini
        # Você pode adicionar contexto ou instruções aqui se desejar
        response = model.generate_content(user_message)

        # Verifica se a resposta tem texto (pode ser bloqueada por segurança)
        if response.parts:
            gemini_reply = response.text
            print(f"Resposta do Gemini: {gemini_reply}") # Log
        else:
            gemini_reply = "Desculpe, não consegui gerar uma resposta para isso. Pode ser devido a filtros de segurança."
            # Você pode querer inspecionar 'response.prompt_feedback' para detalhes
            print(f"Resposta do Gemini bloqueada ou vazia. Feedback: {response.prompt_feedback}")

        # Envia a resposta do Gemini de volta ao usuário
        bot.reply_to(message, gemini_reply)

    except Exception as e:
        print(f"Erro ao interagir com a API Gemini: {e}")
        bot.reply_to(message, "Desculpe, ocorreu um erro ao processar sua mensagem.")

# --- Iniciar o Bot ---
print("Bot está iniciando o polling...")
try:
    bot.infinity_polling()
except Exception as e:
    print(f"Erro durante o polling do bot: {e}")
finally:
    print("Bot parado.")