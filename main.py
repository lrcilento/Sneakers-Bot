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
    print("Verificando se já está disponível...")

    while(True):
        try:
            driver.find_element_by_xpath(sizeXPaths[0])
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
            time.sleep(0.1)

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
                driver.find_element_by_xpath(sizeXPaths[0])
                print("Achei!")
                break
            except:
                time.sleep(0.1)
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

        if avaliableSize == None:
            print("Nenhum tamanho disponível, verifique a lista e tente novamente.")

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
                            smsCode = input("Número inserido, por favor insira o código de verificação (seis dígitos):")
                            for x in range(0, len(smsCode)):
                                driver.find_element_by_xpath("//input[@name='Code{0}']".format(x+1)).send_keys(smsCode[x])
                            driver.find_element_by_xpath(confirmSMSButtonXPath).click()
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
                    print("Abriu!")
                    break
                except:
                    time.sleep(0.1)

            print("Procurando botão de confirmação de endereço...")
            while(True):
                try:
                    driver.find_element_by_xpath(confirmAddressXPath).click()
                except:
                    time.sleep(0.1)
                try:
                    driver.find_element_by_xpath(confirmAddressXPath)
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

binary = FirefoxBinary('/usr/lib/firefox/firefox')
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
    if test:
        print("Modo teste ativado, ignorando horário...")
        driver = webdriver.Firefox(firefox_options=opts, capabilities=caps, firefox_binary=binary)
        driver.maximize_window()
    else:
        nowHour = datetime.datetime.now().hour
        nowMinute = datetime.datetime.now().minute
        now = str(nowHour)+":"+str(nowMinute)
        if startTime == now and dropped == False:
            dropped = True
            driver = webdriver.Firefox(firefox_options=opts, capabilities=caps, firefox_binary=binary)
            driver.maximize_window()
        else:
            time.sleep(1)
            if lastMinute != nowMinute:
                lastMinute = nowMinute
                remainingMinutes = ((int(startHour)*60)+int(startMinute))-((int(nowHour)*60)+int(nowMinute))
                if remainingMinutes > 0:
                    print(str(remainingMinutes)+" minutos restantes...")
                else:
                    print("Parace que o drop já foi... Verifique o horário e tente novamente.")
                    break
    if dropped:
        if run():
            break