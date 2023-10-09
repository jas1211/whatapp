from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import argparse
import datetime
import re


# Константы для Selenium
# Constants for Selenium
url = f"https://web.whatsapp.com/"
#xpath = "//button[@aria-label='compose-btn-send']"
xpath = "//button[@aria-label='Отправить']"
xpathAttach = "//div[@data-testid='conversation-clip']"
cssIdOfDocument = "[aria-label='Документ']"
cssIdOfSendButton = "[aria-label='Отправить']"
#xpathSearchField = "//div[@data-testid='chat-list-search']"
xpathSearchField = "//div[@title='Текстовое поле поиска']"
xpathFoundItem = "//span[contains(@class,'matched-text')]"
#xpathInputLineForText = "//div[@data-testid='conversation-compose-box-input']"
xpathInputLineForText = "//div[@title='Введите сообщение']"
#xpathMessage = "//div[@role = 'row']"
xpathMessage = "//div[@role='application']//div[@role = 'row' or contains(@class,'focusable-list-item')]"
xpathAuthorTime = "span[contains(@class,'_3FuDI')]"
xpathText1 = "span[contains(@class,'selectable-text')]"
xpathText2 = "span[contains(@class,'copyable-text')]"

commandEnableOrDisableJavaScript = "Emulation.setScriptExecutionDisabled"

# Константы для обработки сообщений
# Constants for message process
messageIsOutgoing = "message-out"
messageIsText = "data-pre-plain-text"
messageClassOfBody = "selectable-text copyable-text"
messageBodyStart = "<span>"
messageBodyStop = "</span>"
messageIsPicture = "img"
messageWarrningAboutPicture = "Смайлики не обрабатываю!  I don't process emoticons !"
finishDate = "finishdate.txt"
keys = ["Hello everyone! we play tennis on", "Who’s going to play", "мы играем в теннис в", "в теннисном центре НТЦ 2", "Кто будет играть?"]

class whatapp():
    """ Это класс бота для Whatsapp
       This class is bot for Whatsapp"""


    def startBrowser(self):
        options = webdriver.ChromeOptions()
# если у вас другой браузер, например FireFox, мы просто пишем options = webdriver.FirefoxOptions() .
# if you have the Mozilla Fifefox just write                   options = webdriver.FirefoxOptions()
        options.add_argument('--allow-profiles-outside-user-dir')
        options.add_argument('--enable-profile-shortcut-manager')
# УКАЖИТЕ ПУТЬ ГДЕ ЛЕЖИТ ВАШ python ФАЙЛ. Советую создать отдельную папку для него
# Specify the path to where your python file is located. I suggest you create a separate folder for it
        options.add_argument('user-data-dir=D:\\Projects\\python\\whatapp')
        options.add_argument('--profile-directory=Profile 1')
        options.add_argument('--profiling-flush=n')
        options.add_argument('--enable-aggressive-domstorage-flushing')

# эти опции нужны чтобы подавить любые сообщения об ошибках  SSL, сертификатов и т.п. Но работает только последняя :(
# these options need to disabled any messages about bad ssl, certification & etc
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument('log-level=3')

        options.add_argument('--profile-directory=Default')
        options.add_argument('--user-data-dir=C:/Temp/ChromeProfile')

# INFO = 0,
# WARNING = 1,
# LOG_ERROR = 2,
# LOG_FATAL = 3.
# default is 0.
# Мы запускаем браузер
# We are starting a browser
        #self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.driver = webdriver.Chrome(service=Service(), options=options)
# ждём его загрузки
# it takes some time to load it
        wait = WebDriverWait(self.driver, 30)
# идём туда
# go to there
        self.driver.get(url)
# ждём загрузки страницы Whatsapp
# we are waiting for Whatsapp page to load
        wait.until(EC.element_to_be_clickable((By.XPATH, xpathSearchField)))


    def finish(self):
# закрыть все
# close all
        self.driver.quit()

    def searchGroup(self, group_name):
# Найти группу для обработки
# В поле поиска вводим название группы и нажимаем на кнопку "Искать"
# Find a group to process
# In the search field, enter the name of the group and click "Search".
        self.driver.find_element(By.XPATH, xpathSearchField).send_keys(group_name)
        sleep(1)
        self.driver.find_element(By.XPATH, xpathFoundItem).click()
        sleep(5)


    def sendMessage(self, message):
# Разрешаем JavaSctipt
# Enable JavaSctipt
        self.driver.execute_cdp_cmd(commandEnableOrDisableJavaScript, {'value': False})
# Ищем строку ввода и отправляем туда текст сообщения
# Find the input line and send the message text there
        self.driver.find_element(By.XPATH, xpathInputLineForText).send_keys(message)
# теперь ищем кнопку "Отправить" и нажимаем на нее
# now we look for the Send Button and click on it
        self.driver.find_element(By.XPATH, xpath).click()
        sleep(5)


    def searchLastMessageAndProcessMessages(self):
# проверям дату
        file = open(finishDate, 'r')
        date = file.read()
        if (not date is None and date == str(datetime.date.today())):
            return True

# скролим
        for i in [1, 2, 3, 4, 5]:
            self.driver.find_element(By.XPATH, "//div[@role='application']").send_keys(Keys.CONTROL + Keys.HOME)
            sleep(1)

# Запрещаем JavaSctipt
# Disable   JavaSctipt
        self.driver.execute_cdp_cmd(commandEnableOrDisableJavaScript, {'value': True})
# Выберем все сообщения
# Select all messages
        messages = self.driver.find_elements(By.XPATH, xpathMessage)
        print('Found %s messages' % len(messages))
# просмотрим все сообщения
# review all messages
        today = False
        finish = False
        author = ''
        for item in messages:
# получим тело сообщения
# get body of the message
            line = str(item.text)
            line = line.replace("\n\n", " ")
            words = line.split('\n')
            
            if (not today):
                if (words[0] == "СЕГОДНЯ"):
                    today = True
                else:
                    continue
            
            if (len(words) == 3):
                author = words[0]
                mes = words[1]
                time = words[2]
            elif (len(words) == 2):
                mes = words[0]
                time = words[1]
            else:
                continue
            


            if (not author == "Тимур Теннис По Группам"):
                continue
            
        #     if (not author == "Аселя"):
        #         continue
            
            for key in keys:
                result = re.search(key, mes)
                if (result != None):
                    finish = True

                    self.sendMessage('in')
                    
                    file = open(finishDate, 'w')
                    file.write(str(datetime.date.today()))

                    break

            if finish:
                print(mes)
                break
             
        return finish 


def main():
# основной бесконечный цикл. Прервать его - Ctrl+C
# the main infinite loop. interrupt it with Ctrl+C
    try:
        while True:
            wa = whatapp()
            wa.startBrowser()
            wa.searchGroup("InterNations Tennis Group")
            #wa.searchGroup("Тест")            
            result = wa.searchLastMessageAndProcessMessages()
            wa.finish()
            print(str(datetime.datetime.now()) + ' ' + str(result))
            if (result):
                break
            sleep(15)
    except KeyboardInterrupt:
        wa.finish()
    return


if __name__ == '__main__':
# мы разбираем параметры командной строки
# we are parsing command line parameters
    parser = argparse.ArgumentParser(description='Process messages by Whatsapp')
    #parser.add_argument('--group', help='Text for send', required=True)
    #args = parser.parse_args()
# начать обработку
# start  processing
    #main(args)
    main()