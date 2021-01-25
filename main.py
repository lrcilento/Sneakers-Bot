import asyncio
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.keys import Keys
from config import *
from credentials import *

def run():
    initialTime = time.time()
    avaliable = True

    print("Carregando página...")
    driver.get(targetURL)
    print("Página carregada.")

    while(True):
        print("Verificando se já está disponível...")
        try:
            driver.find_element_by_xpath(sizeXPaths[0])
            print("Está!")
            break
        except:
            try:
                print("Não achei a tabela de números, procurando o botão de aviso...")
                driver.find_element_by_id(remindMeButtonID)
                print("Achei, não está disponível ainda...")
                avaliable = False
                time.sleep(2)
                break
            except:
                print("Não achei o botão de aviso também, aguardando...")
                driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
                time.sleep(0.1)
                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                time.sleep(0.5)
            time.sleep(0.5)

    if avaliable:

        while(True):
            print("Procurando botão de login...")
            try:
                driver.find_element_by_id(loginElementID).click()
                print("Achei!")
                break
            except:
                time.sleep(0.5)

        driver.switch_to_frame(loginFrameID)

        while(True):
            print("Procurando formulário de login...")
            try:
                driver.find_element_by_name('emailAddress').send_keys(email)
                print("Email inserido!")
                break
            except:
                time.sleep(0.5)

        driver.find_element_by_name('password').send_keys(password)
        print("Senha inserida!")
        driver.find_element_by_name('password').send_keys(Keys.RETURN)
        print("Submetendo formulário...")

        driver.switch_to_default_content()

        while(True):
            print("Procurando tabela de números...")
            try:
                driver.find_element_by_xpath(sizeXPaths[0])
                print("Achei!")
                break
            except:
                time.sleep(0.5)
                driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
                time.sleep(0.1)
                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        
        for x in range(0, len(sizeXPaths)):
            try:
                if driver.find_element_by_xpath(sizeXPaths[x]).find_element_by_xpath('..').get_attribute('class') != "tamanho-desabilitado":
                    print("Número "+sizeXPaths[x][-4:-2]+" disponível, selecionando-o...")
                    avaliableSize = sizeXPaths[x]
                    break
                else:
                    print("Número "+sizeXPaths[x][-4:-2]+" indisponível...")
            except:
                time.sleep(0.1)

        while(True):
            try:
                driver.find_element_by_xpath(avaliableSize).click()
                print("Adicionando ao carrinho...")
                driver.find_element_by_id(buyButtonID).click()
                break
            except:
                time.sleep(0.5)
                try:
                    driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
                    time.sleep(0.1)
                    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                except:
                    time.sleep(0.5)

        while(True):
            print("Procurando botão de check-out...")
            try:
                driver.find_element_by_xpath(checkoutButtonXPath).click()
                print("Achei!")
                break
            except:
                time.sleep(0.5)

        while(True):
            print("Procurando botão de seguir para o pagamento...")
            try:
                driver.find_element_by_tag_name('body').send_keys(Keys.END)
                driver.find_element_by_xpath(paymentButtonXPath).click()
                print("Achei!")
            except:
                time.sleep(0.5)
            print("Chechando se o modal abriu mesmo...")
            try:
                driver.find_element_by_xpath(confirmAddressXPath)
                print("Abriu!")
                break
            except:
                time.sleep(0.5)
            print("Procurando botão de confirmação de endereço, quem sabe...")
            try:
                driver.find_element_by_xpath(confirmAddressXPath)
                print("Achei!")
                break
            except:
                time.sleep(0.5)

        while(True):
            print("Procurando botão de confirmação de endereço...")
            try:
                driver.find_element_by_xpath(confirmAddressXPath).click()
                print("Achei!")
            except:
                time.sleep(0.5)
            try:
                print("Checando se o modal fechou mesmo...")
                driver.find_element_by_xpath(confirmAddressXPath)
                time.sleep(0.5)
            except:
                break

        while(True):
            print("Procurando painel de cartões salvos...")
            try:
                driver.find_element_by_id(cardsDivID).click()
                print("Achei!")
                break
            except:
                time.sleep(0.5)

        while(True):
            print("Tentando selecionar cartão...")
            try:
                driver.find_element_by_class_name(cardClassName).click()
                print("Consegui!")
                break
            except:
                time.sleep(0.5)

        while(True):
            print("Procurando onde aceitar os termos...")
            try:
                driver.find_element_by_xpath(termsCheckboxXPath).click()
                print("Achei o checkbox!")
                break
            except:
                print("Tetando procurar o div inteiro...")
                try:
                    driver.find_element_by_xpath(termsDivXPath).click()
                    print("Achei!")
                    break
                except:
                    time.sleep(0.5)
                time.sleep(0.5)

        if test == False:
            while(True):
                print("Tentando finalizar compra...")
                try:
                    driver.find_element_by_id(finalButtonID).click()
                    print("Consegui!")
                    break
                except:
                    time.sleep(0.5)

        finalTime = time.time()
        print("Tempo decorrido: "+str(finalTime - initialTime)+"s")
        return True

binary = FirefoxBinary('/usr/lib/firefox/firefox')
caps = DesiredCapabilities().FIREFOX
caps["pageLoadStrategy"] = "eager"

if test:
    dropped = True
else:
    dropped = False
print("Horário do drop: "+startTime)
startHour = startTime[:2]
startMinute = startTime[-2:]
lastMinute = None
while(True):
    if test:
        print("Modo teste ativado, ignorando horário...")
        driver = webdriver.Firefox(capabilities=caps, firefox_binary=binary)
        driver.maximize_window()
    else:
        nowHour = datetime.datetime.now().hour
        nowMinute = datetime.datetime.now().minute
        now = str(nowHour)+":"+str(nowMinute)
        if startTime == now and dropped == False:
            dropped = True
            driver = webdriver.Firefox(capabilities=caps, firefox_binary=binary)
            driver.maximize_window()
        else:
            time.sleep(1)
            if lastMinute != nowMinute:
                lastMinute = nowMinute
                print(str(((int(startHour)*60)+int(startMinute))-((int(nowHour)*60)+int(nowMinute)))+" minutos restantes...")
    if dropped:
        if run():
            break