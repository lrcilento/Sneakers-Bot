from env import *

buyButtonID = "btn-comprar"
checkoutButtonXPath = '/html/body/main/div[4]/div/div[4]/a'
loginElementID = "anchor-acessar-unite-oauth2"
loginFrameID = "nike-unite-oauth2-iframe"
paymentButtonXPath = "//*[@id='seguir-pagamento']"
confirmAddressXPath = "/html/body/div[15]/div/div/div[3]/button[1]"
cardsDivID = "cartoes-salvos"
cardClassName = "select-cta-option"
termsCheckboxXPath = "/html/body/main/div/div[3]/div[8]/div[2]/div[3]/div/input"
termsDivXPath = "/html/body/main/div/div[3]/div[8]/div[2]/div[3]/div"
finalButtonID = "confirmar-pagamento"
remindMeButtonID = "btn-avisar"
smsAPIURL = "https://sms-handler-api.herokuapp.com/sms"
confirmSMSButtonXPath = "/html/body/div[22]/div/div/div[2]/form[2]/div[2]/button[1]"
sizeXPaths = []

for x in range(0, len(sizes)):
    sizeXPaths.append("//label[@for='tamanho__id"+str(sizes[x])+"']")