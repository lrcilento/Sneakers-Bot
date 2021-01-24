import asyncio
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from config import *
from credentials import *

def run():
    initialTime = time.time()
    avaliable = True

    print("Carregando página...")
    driver.get(targetURL)
    print("Página carregada, tentando logar...")

    while(True):
        print("Checando já está disponível...")
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
        
        for size in range(0, len(sizeXPaths)):
            try:
                driver.find_element_by_xpath(sizeXPaths[size]).click()
                print("Número "+sizeXPaths[size]+" disponível, selecionando-o...")
                break
            except:
                time.sleep(0.5)
        
        print("Adicionando ao carrinho...")
        driver.find_element_by_id(buyButtonID).click()


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

dropped = False
while(True):
    now = datetime.datetime.now()
    now = str(now.hour)+":"+str(now.minute)
    if startTime == now and dropped == False:
        dropped = True
        binary = FirefoxBinary('/usr/lib/firefox/firefox')
        caps = DesiredCapabilities().FIREFOX
        caps["pageLoadStrategy"] = "eager"
        driver = webdriver.Firefox(capabilities=caps, firefox_binary=binary)
    else:
        time.sleep(1)
    if dropped:
        if run():
            break