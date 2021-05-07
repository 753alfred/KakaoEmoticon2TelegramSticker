from telegram.ext import CommandHandler, Dispatcher, Filters, MessageHandler, Updater
import telegram

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup
import requests

apiKeyFile = open("/home/server/KakaoEmoticon2TelegramSticker_KEY", 'r')
TOKEN = apiKeyFile.read().rstrip('\n')
apiKeyFile.close()

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def createEmoticon(update, context):
    emoticonURL = context.args[0]
    soupHeader = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(executable_path='/home/server/KakaoEmoticon2TelegramSticker/chromedriver', chrome_options=options)
    url = 'https://e.kakao.com/t/uh-uh-uh-ver-2'
    driver.get(url) 

    pageResource = driver.page_source
    soup = BeautifulSoup(pageResource, features="html.parser")

    divRoot = soup.find("div", id="root")
    divWrap = divRoot.find("div", id="kakaoWrap")
    divContent = divWrap.find("div", id="kakaoContent")
    divInfo = divContent.find("div", class_="area_product")
    divTitle = divInfo.find("div", class_="info_product")
    strTitle = divTitle.find("h3", class_="tit_product")
    context.bot.send_message(chat_id=update.effective_chat.id, text=strTitle.text)

    divEmoticons = divContent.find("div", class_="area_emoticon")
    listEmoticons = divEmoticons.find("ul")
    itemEmoticons = listEmoticons.find_all("li")

    context.bot.send_message(chat_id=update.effective_chat.id, text=strTitle)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot Started!")

create_handler = CommandHandler("create", createEmoticon)
start_handler = CommandHandler("start", start)

dispatcher.add_handler(create_handler)
dispatcher.add_handler(start_handler)

updater.start_polling()