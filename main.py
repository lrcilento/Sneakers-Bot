import time
import datetime
import requests
from sys import platform
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.keys import Keys
from config import *
from env import *

def get_sms():
    return requests.get(smsAPIURL).json()["sms"]

def run():
    print("Verificando SMS anterior...")
    oldSMS = get_sms()
    initialTime = time.time()
    avaliable = True
    print("Carregando página...")
    driver.get(targetURL)
    print("Página carregada.")
    print("Verificando se já está disponível...")

    while(True):
        try:
            driver.find_element_by_xpath("//button[@id='{0}']".format(loginElementID))
            print("Está!")
            break
        except:
            try:
                driver.find_element_by_id(remindMeButtonID)
                print("Não está disponível ainda...")
                avaliable = False
                time.sleep(2)
                break
            except:
                driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
                time.sleep(0.1)
                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                time.sleep(0.1)
                try:
                    driver.find_element_by_xpath("//button[@id='{0}']".format(loginElementID))
                    print("Está!")
                    break
                except:
                    try:
                        driver.find_element_by_id(remindMeButtonID)
                        print("Não está disponível ainda...")
                        avaliable = False
                        time.sleep(2)
                        break
                    except:
                        time.sleep(0.1)
                        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

    if avaliable:
        print("Procurando botão de login...")
        while(True):
            try:
                driver.find_element_by_id(loginElementID).click()
                print("Achei!")
                break
            except:
                time.sleep(0.1)

        driver.switch_to_frame(loginFrameID)

        print("Procurando formulário de login...")
        while(True):
            try:
                driver.find_element_by_name('emailAddress').send_keys(email)
                driver.find_element_by_name('password').send_keys(password)
                driver.find_element_by_name('password').send_keys(Keys.ENTER)
                print("Submetendo formulário...")
                break
            except:
                time.sleep(0.1)

        driver.switch_to_default_content()

        print("Procurando tabela de números...")
        while(True):
            try:
                try:
                    driver.find_element_by_id(buyButtonID)
                    print("Achei!")
                    break
                except:
                    time.sleep(0.1)
                    driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
                    time.sleep(0.1)
                    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                    try:
                        driver.find_element_by_id(buyButtonID)
                        print("Achei!")
                        break
                    except:
                        time.sleep(0.1)
                        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            except:
                time.sleep(0.1)

        avaliableSize = None
        for x in range(0, len(sizeXPaths)):
            try:
                if driver.find_element_by_xpath(sizeXPaths[x]).find_element_by_xpath('..').get_attribute('class') != "tamanho-desabilitado":
                    print("Número "+sizeXPaths[x][-4:-2]+" disponível, selecionando-o...")
                    avaliableSize = sizeXPaths[x]
                    break
                else:
                    print("Número "+sizeXPaths[x][-4:-2]+" indisponível...")
            except:
                print("Número "+sizeXPaths[x][-4:-2]+" inexistente...")
                time.sleep(0.1)

        if avaliableSize == None:
            print("Nenhum tamanho disponível, verifique a lista e tente novamente.")
            return True

        else:
            print("Adicionando número "+avaliableSize[-4:-2]+" ao carrinho...")
            while(True):
                try:
                    driver.find_element_by_xpath(avaliableSize).click()
                    driver.find_element_by_id(buyButtonID).click()
                    print("Adicionado!")
                    break
                except:
                    time.sleep(0.1)
                    try:
                        driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
                        time.sleep(0.1)
                        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                        try:
                            driver.find_element_by_xpath(avaliableSize).click()
                            driver.find_element_by_id(buyButtonID).click()
                            print("Adicionado!")
                            break
                        except:
                            try:
                                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                                time.sleep(0.1)
                            except:
                                time.sleep(0.1)
                    except:
                        time.sleep(0.1)
            
            print("Procurando botão de check-out...")
            while(True):
                try:
                    driver.find_element_by_xpath(checkoutButtonXPath).click()
                    print("Botão de check-out disponível!")
                    break
                except:
                    try:
                        driver.find_element_by_xpath("//input[@name='CelularCliente']")
                        try:
                            for number in phoneNumber:
                                time.sleep(0.1)
                                driver.find_element_by_xpath("//input[@name='CelularCliente']").send_keys(number)
                            print("Precisa do SMS! Inserindo o número de telefone...")
                            driver.find_element_by_xpath("//input[@name='CelularCliente']").send_keys(Keys.ENTER)
                            smsCode = oldSMS
                            while smsCode == oldSMS:
                                smsCode = get_sms()
                            for x in range(0, len(smsCode)):
                                driver.find_element_by_xpath("//input[@name='Code{0}']".format(x+1)).send_keys(smsCode[x])
                                time.sleep(0.1)
                            while(True):
                                try:
                                    driver.find_element_by_xpath(confirmSMSButtonXPath).click()
                                    print("Finalizado")
                                    break
                                except:
                                    time.sleep(0.1)
                        except:
                            time.sleep(0.1)
                    except:
                        time.sleep(0.1)
                    time.sleep(0.1)

            print("Procurando botão de seguir para o pagamento...")
            while(True):
                try:
                    driver.find_element_by_tag_name('body').send_keys(Keys.END)
                    driver.find_element_by_xpath(paymentButtonXPath).click()
                except:
                    time.sleep(0.1)
                try:
                    driver.find_element_by_xpath(confirmAddressXPath)
                    viableXPath = confirmAddressXPath
                    print("Abriu!")
                    break
                except:
                    time.sleep(0.1)
                try:
                    driver.find_element_by_xpath(alternativeConfirmAddressXPath)
                    print("Abriu!")
                    viableXPath = alternativeConfirmAddressXPath
                    break
                except:
                    time.sleep(0.1)


            print("Procurando botão de confirmação de endereço...")
            # AQUI
            while(True):
                try:
                    driver.find_element_by_xpath(viableXPath).click()
                except:
                    time.sleep(0.1)
                try:
                    driver.find_element_by_xpath(viableXPath)
                    time.sleep(0.1)
                except:
                    print("Achei!")
                    break
            
            print("Procurando painel de cartões salvos...")
            while(True):
                try:
                    driver.find_element_by_id(cardsDivID).click()
                    print("Achei!")
                    break
                except:
                    time.sleep(0.1)

            print("Tentando selecionar cartão...")
            while(True):
                try:
                    driver.find_element_by_class_name(cardClassName).click()
                    print("Consegui!")
                    break
                except:
                    time.sleep(0.1)

            print("Procurando onde aceitar os termos...")
            while(True):
                try:
                    driver.find_element_by_xpath(termsCheckboxXPath).click()
                    print("Achei o checkbox!")
                    break
                except:
                    try:
                        driver.find_element_by_xpath(termsDivXPath).click()
                        print("Achei o div inteiro!")
                        break
                    except:
                        time.sleep(0.1)
                    time.sleep(0.1)

            if test == False:
                print("Tentando finalizar compra...")
                while(True):
                    try:
                        driver.find_element_by_id(finalButtonID).click()
                        print("Consegui!")
                        break
                    except:
                        time.sleep(0.1)
            else:
                print("Modo teste ativado, encerrando o fluxo sem finalizar compra...")

            finalTime = time.time()
            print("Tempo decorrido: "+str(finalTime - initialTime)+"s")
            return True

if platform == 'linux':
    binary = FirefoxBinary('/usr/lib/firefox/firefox')
    path = '/usr/local/bin/geckodriver'
else:
    binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
    path = "C:\\Program Files\\Mozilla Firefox\\geckodriver.exe"
caps = DesiredCapabilities().FIREFOX
caps["pageLoadStrategy"] = "eager"
opts = FirefoxOptions()
if headless:
    opts.set_headless()
    opts.add_argument("--width=2560");
    opts.add_argument("--height=1440");

if test:
    dropped = True
else:
    dropped = False
    print("Horário do drop: "+startTime)
    startHour = startTime[:2]
    startMinute = startTime[-2:]
lastMinute = None
while(True):
    get_sms()
    if test:
        print("Modo teste ativado, ignorando horário...")
        driver = webdriver.Firefox(firefox_options=opts, capabilities=caps, firefox_binary=binary, executable_path=path)
        driver.maximize_window()
    else:
        nowHour = datetime.datetime.now().hour
        nowMinute = datetime.datetime.now().minute
        remainingMinutes = ((int(startHour)*60)+int(startMinute))-((int(nowHour)*60)+int(nowMinute))
        if remainingMinutes < 1 and dropped == False:
            dropped = True
            driver = webdriver.Firefox(firefox_options=opts, capabilities=caps, firefox_binary=binary, executable_path=path)
            driver.maximize_window()
        else:
            time.sleep(1)
            print(str(remainingMinutes)+" minutos restantes...")
    if dropped:
        if run():
            break