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
    try:
        smsList = requests.get(smsAPIURL).json()
        lastSMS = smsList[len(smsList) - 1]["SMS_CONTENT"]
        return lastSMS
    except:
        return ""

def run():
    initialTime = time.time()
    avaliable = False
    brokenPage = False
    brokenLogin = False
    loaded = False
    driver.get(targetURL)
    oldSMS = get_sms()

    while(True):
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
        while(True):
            try:
                driver.find_element_by_id(loginElementID).click()
                break
            except:
                continue

        driver.switch_to_frame(loginFrameID)

        while(True):
            try:
                driver.find_element_by_name('emailAddress').send_keys(email)
                driver.find_element_by_name('password').send_keys(password)
                driver.find_element_by_name('password').send_keys(Keys.ENTER)
                break
            except:
                continue

        while(True):
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
                            print("Erro ocorrido ao tentar realizar login...")
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
            avaliableSize = None
            for x in range(0, len(sizeXPaths)):
                try:
                    if driver.find_element_by_xpath(sizeXPaths[x]).find_element_by_xpath('..').get_attribute('class') != "tamanho-desabilitado":
                        avaliableSize = sizeXPaths[x]
                        break
                except:
                    continue

            if avaliableSize == None:
                print("Nenhum tamanho disponível, verifique a lista e tente novamente.")
                return True

            else:
                while(True):
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
                                    try:
                                        driver.find_element_by_xpath(avaliableSize).click()
                                        driver.find_element_by_id(buyButtonID).click()
                                        break
                                    except:
                                        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
                                        time.sleep(delay)
                                except:
                                    continue
                        except:
                            continue
                
                while(True):
                    try:
                        driver.find_element_by_xpath(checkoutButtonXPath).click()
                        break
                    except:
                        try:
                            driver.find_element_by_xpath("//input[@name='CelularCliente']")
                            print("Precisa do SMS! Inserindo o número de telefone...")
                            try:
                                for number in phoneNumber:
                                    time.sleep(delay)
                                    driver.find_element_by_xpath("//input[@name='CelularCliente']").send_keys(number)
                                driver.find_element_by_xpath("//input[@name='CelularCliente']").send_keys(Keys.ENTER)
                                smsCode = oldSMS
                                while smsCode == oldSMS:
                                    smsCode = get_sms()
                                for x in range(0, len(smsCode)):
                                    time.sleep(delay)
                                    driver.find_element_by_xpath("//input[@name='Code{0}']".format(x+1)).send_keys(smsCode[x])
                                while(True):
                                    try:
                                        driver.find_element_by_xpath(confirmSMSButtonXPath).click()
                                        break
                                    except:
                                        continue
                            except:
                                continue
                        except:
                            continue
                        continue

                while(True):
                    try:
                        driver.find_element_by_id(buyButtonID)
                        try:
                            driver.find_element_by_id(buyButtonID).click()
                        except:
                            continue
                    except:
                        break

                while(True):
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

                while(True):
                    try:
                        driver.find_element_by_xpath(viableXPath).click()
                    except:
                        try:
                            driver.find_element_by_xpath(viableXPath)
                        except:
                            break
                
                while(True):
                    try:
                        driver.find_element_by_id(cardsDivID).click()
                        break
                    except:
                        continue

                while(True):
                    try:
                        driver.find_element_by_class_name(cardClassName).click()
                        break
                    except:
                        continue

                while(True):
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
                    while(True):
                        try:
                            driver.find_element_by_id(finalButtonID).click()
                            print("Compra realizada com sucesso!")
                            break
                        except:
                            continue
                else:
                    print("Encerrando o fluxo de teste...")

                finalTime = time.time()
                print("Tempo decorrido: %4.1fs" % (finalTime - initialTime))
                return True
    
    else:
        print("Algo deu errado, recarregando a página...")
        time.sleep(1)

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
    opts.add_argument("--width=1920");
    opts.add_argument("--height=1080");

if test:
    dropped = True
else:
    dropped = False
    print("Credenciais: "+email+" ("+phoneNumber+")")
    print("Horário do drop: "+startTime)
    startHour = startTime[:2]
    startMinute = startTime[-2:]
lastMinute = None
setup = False

while(True):
    if setup == False:
        if test:
            print("Modo teste ativado, ignorando horário...")
            driver = webdriver.Firefox(firefox_options=opts, capabilities=caps, firefox_binary=binary, executable_path=path)
            driver.maximize_window()
            setup = True
        else:
            nowHour = datetime.datetime.now().hour
            nowMinute = datetime.datetime.now().minute
            remainingMinutes = ((int(startHour)*60)+int(startMinute))-((int(nowHour)*60)+int(nowMinute))
            if remainingMinutes < 1 and dropped == False:
                dropped = True
                driver = webdriver.Firefox(firefox_options=opts, capabilities=caps, firefox_binary=binary, executable_path=path)
                driver.maximize_window()
                setup = True
            else:
                time.sleep(1)
                if lastMinute != remainingMinutes:
                    print(str(remainingMinutes)+" minutos restantes...")
                lastMinute = remainingMinutes
    if dropped:
        if run():
            break