import time
import datetime
import os
import logging
import requests
import threading
from sys import platform
from selenium import webdriver
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.keys import Keys
from config import *
from env import *

def get_sms():
    try:
        smsList = requests.get(smsAPIURL).json()
        lastSMS = smsList[len(smsList) - 1]["SMS_CONTENT"]
        return lastSMS
    except:
        return ""

login = False
def run(threadName, driver):
    print("{} Iniciado!".format(threadName))
    initialTime = time.time()
    avaliable, brokenPage, brokenLogin, loaded = False, False, False, False
    driver.get(targetURL)
    oldSMS = get_sms()
    if len(threads) > 1:
        global login

    while 1:
        if driver.execute_script("return document.readyState") == "complete":
            loaded = True
            break
        else:
            try:
                driver.find_element_by_xpath("//button[@id='{0}']".format(loginElementID))
                avaliable = True
                break
            except:
                try:
                    driver.find_element_by_id(remindMeButtonID)
                    break
                except:
                    driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
                    time.sleep(delay)
                    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                    time.sleep(delay)
                    try:
                        driver.find_element_by_xpath("//button[@id='{0}']".format(loginElementID))
                        avaliable = True
                        break
                    except:
                        try:
                            driver.find_element_by_id(remindMeButtonID)
                            break
                        except:
                            driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                            time.sleep(delay)

    if loaded and not avaliable:
        try:
            driver.find_element_by_xpath("//button[@id='{0}']".format(loginElementID))
            avaliable = True
        except:
            driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            time.sleep(delay)
            try:
                driver.find_element_by_xpath("//button[@id='{0}']".format(loginElementID))
                avaliable = True
            except:
                driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                time.sleep(delay)
                try:
                    driver.find_element_by_xpath("//button[@id='{0}']".format(loginElementID))
                    avaliable = True
                except:
                    brokenPage = True

    if avaliable:
        while 1:
            try:
                driver.find_element_by_id(loginElementID).click()
                break
            except:
                continue

        driver.switch_to_frame(loginFrameID)

        if not login:
            while 1:
                try:
                    driver.find_element_by_name('emailAddress').send_keys(email)
                    driver.find_element_by_name('password').send_keys(password)
                    driver.find_element_by_name('password').send_keys(Keys.ENTER)
                    break
                except:
                    continue
        
        else:
            print("{} Encerrado, outro Thread já conseguiu logar!".format(threadName))
            return True

        while 1:
            try:
                try:
                    driver.find_element_by_id(buyButtonID)
                    break
                except:
                    driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
                    time.sleep(delay)
                    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                    try:
                        driver.find_element_by_id(buyButtonID)
                        break
                    except:
                        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                        try:
                            driver.switch_to_frame(loginFrameID)
                            driver.find_element_by_xpath(loginFrameErrorXPath)
                            print("{} Erro ocorrido ao tentar realizar login...".format(threadName))
                            brokenLogin = True
                            break
                        except:
                            try:
                                driver.switch_to_default_content()
                            except:
                                continue
            except:
                continue

        if not brokenLogin:
            if len(threads) > 1:
                print("{} Login realizado com sucesso!".format(threadName))
                login = True
            avaliableSize = None
            for x in range(0, len(sizeXPaths)):
                try:
                    if driver.find_element_by_xpath(sizeXPaths[x]).find_element_by_xpath('..').get_attribute('class') != "tamanho-desabilitado":
                        avaliableSize = sizeXPaths[x]
                        break
                except:
                    continue

            if avaliableSize == None:
                print("{} Nenhum tamanho disponível, verifique a lista e tente novamente.".format(threadName))
                return True

            else:
                while 1:
                    try:
                        driver.find_element_by_xpath(avaliableSize).click()
                        driver.find_element_by_id(buyButtonID).click()
                        break
                    except:
                        try:
                            driver.find_element_by_tag_name('body').send_keys(Keys.HOME)
                            time.sleep(delay)
                            driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                            time.sleep(delay)
                            try:
                                driver.find_element_by_xpath(avaliableSize).click()
                                driver.find_element_by_id(buyButtonID).click()
                                break
                            except:
                                try:
                                    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                                    time.sleep(delay)
                                except:
                                    continue
                        except:
                            continue
                
                while 1:
                    try:
                        driver.find_element_by_xpath(checkoutButtonXPath).click()
                        break
                    except:
                        try:
                            driver.find_element_by_xpath("//input[@name='CelularCliente']")
                            try:
                                for number in phoneNumber:
                                    time.sleep(0.1)
                                    driver.find_element_by_xpath("//input[@name='CelularCliente']").send_keys(number)
                                driver.find_element_by_xpath("//input[@name='CelularCliente']").send_keys(Keys.ENTER)
                                smsCode = oldSMS
                                while smsCode == oldSMS:
                                    smsCode = get_sms()
                                for x in range(0, len(smsCode)):
                                    time.sleep(0.1)
                                    driver.find_element_by_xpath("//input[@name='Code{0}']".format(x+1)).send_keys(smsCode[x])
                                while 1:
                                    try:
                                        driver.find_element_by_xpath(confirmSMSButtonXPath).click()
                                        break
                                    except:
                                        continue
                            except:
                                continue
                        except:
                            continue

                while 1:
                    try:
                        driver.find_element_by_id(buyButtonID)
                        try:
                            driver.find_element_by_id(buyButtonID).click()
                        except:
                            continue
                    except:
                        break

                while 1:
                    try:
                        driver.find_element_by_tag_name('body').send_keys(Keys.END)
                        driver.find_element_by_xpath(paymentButtonXPath).click()
                    except:                       
                        try:
                            driver.find_element_by_xpath(confirmAddressXPath)
                            viableXPath = confirmAddressXPath
                            break
                        except:
                            try:
                                driver.find_element_by_xpath(alternativeConfirmAddressXPath)
                                viableXPath = alternativeConfirmAddressXPath
                                break
                            except:
                                continue

                while 1:
                    try:
                        driver.find_element_by_xpath(viableXPath).click()
                    except:
                        try:
                            driver.find_element_by_xpath(viableXPath)
                        except:
                            break
                
                while 1:
                    try:
                        driver.find_element_by_id(cardsDivID).click()
                        break
                    except:
                        continue

                while 1:
                    try:
                        driver.find_element_by_class_name(cardClassName).click()
                        break
                    except:
                        continue

                while 1:
                    try:
                        driver.find_element_by_xpath(termsCheckboxXPath).click()
                        break
                    except:
                        try:
                            driver.find_element_by_xpath(termsDivXPath).click()
                            break
                        except:
                            continue
                        continue

                if test == False:
                    while 1:
                        try:
                            driver.find_element_by_id(finalButtonID).click()
                            print("{} Compra realizada com sucesso!".format(threadName))
                            break
                        except:
                            continue
                else:
                    print("{} Encerrando o fluxo de teste...".format(threadName))

                finalTime = time.time()
                print("{} Tempo decorrido: %4.1fs".format(threadName) % (finalTime - initialTime))
                return True
    
    else:
        print("{} Algo deu errado, recarregando a página...".format(threadName))
        time.sleep(1)

def retrieveProxies():
    print("Colentando lista de proxies...")
    proxies = []
    if len(proxies) + 1 < threadNumber:
        rawProxies = RequestProxy(log_level=logging.ERROR).get_proxy_list()
        for proxy in rawProxies:
            if proxy.country == "Brazil":
                proxies.append(proxy.get_address())
    return proxies

def prepareDriver(threadName, first = False):
    caps = DesiredCapabilities().FIREFOX
    caps["pageLoadStrategy"] = "eager"
    opts = FirefoxOptions()
    if headless:
        opts.set_headless()
        os.environ['MOZ_HEADLESS_WIDTH'] = '1920'
        os.environ['MOZ_HEADLESS_HEIGHT'] = '1080'
    if not first and proxy:
        if len(proxies) > 0:
            caps['proxy'] = {
                "httpProxy":proxies[0],
                "ftpProxy":proxies[0],
                "sslProxy":proxies[0],
                "proxyType":"MANUAL"
            }
            proxies.pop(0)
    driver = webdriver.Firefox(firefox_options=opts, capabilities=caps, firefox_binary=binary, executable_path=path)
    driver.maximize_window()
    while 1:
        if run(threadName, driver):
            break

if platform == 'linux':
    binary = FirefoxBinary('/usr/lib/firefox/firefox')
    path = '/usr/local/bin/geckodriver'
else:
    binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
    path = "C:\\Program Files\\Mozilla Firefox\\geckodriver.exe"

if test:
    dropped = True
else:
    dropped = False
    print("Horário do drop: "+startTime)
    startHour = startTime[:2]
    startMinute = startTime[-2:]
lastMinute = None
setup = False
threads = []

while 1:
    if threadNumber > 1 and proxy:
        proxies = retrieveProxies()
    if setup == False:
        if test:
            print("Modo teste ativado, ignorando horário...")
            setup = True
        else:
            nowHour = datetime.datetime.now().hour
            nowMinute = datetime.datetime.now().minute
            remainingMinutes = ((int(startHour)*60)+int(startMinute))-((int(nowHour)*60)+int(nowMinute))
            if remainingMinutes < 2 and dropped == False:
                nowSeconds = datetime.datetime.now().second
                if nowSeconds > 55:
                    dropped = True
                    setup = True
            else:
                time.sleep(1)
                if lastMinute != remainingMinutes:
                    print(str(remainingMinutes)+" minutos restantes...")
                lastMinute = remainingMinutes

    if dropped:
        for x in range(0, threadNumber):
            if x == 0:
                main = threading.Thread(target=prepareDriver, args=("[Main]", True))
                main.start()
                threads.append(main)
            else:
                slave = threading.Thread(target=prepareDriver, args=("[Slave-{}]".format(x), False))
                slave.start()
                threads.append(slave)
        break