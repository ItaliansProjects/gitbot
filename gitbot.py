import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

DOWNLOAD_FOLDER = 'downloads'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Benvenuto! Puoi utilizzare il comando /search seguito dalla query per cercare repository su GitHub.')

def search(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    
    if not query:
        update.message.reply_text('Per favore, fornisci una query di ricerca.')
        return

    github_api_url = f'https://api.github.com/search/repositories?q={query}'
    response = requests.get(github_api_url)

    if response.status_code == 200:
        results = response.json().get('items', [])
        if results:
            for result in results[:25]:  
                repo_name = result.get('full_name', 'N/A')
                repo_url = result.get('html_url', 'N/A')
                update.message.reply_text(f'Repository: {repo_name}\nURL: {repo_url}')
        else:
            update.message.reply_text('Nessun risultato trovato.')
    else:
        update.message.reply_text('Si è verificato un problema durante la ricerca.')

def main() -> None:
    
    TOKEN = input("Inserisci il token del tuo bot Telegram: ")

    updater = Updater(TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("search", search))

    updater.start_polling()

    updater.idle()

if name == 'main':
     main()
