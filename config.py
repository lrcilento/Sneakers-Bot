#Variáveis
targetURL = 'https://www.nike.com.br/Snkrs/Produto/Zoom-Freak-2/153-169-211-305438'
size = 36
startTime = "17:28"

# Constantes
buyButtonID = "btn-comprar"
checkoutButtonXPath = '/html/body/main/div[4]/div/div[4]/a'
loginElementID = "anchor-acessar-unite-oauth2"
loginFrameID = "nike-unite-oauth2-iframe"
sizeXPath = "//label[@for='tamanho__id"+str(size)+"']"
paymentButtonXPath = "//*[@id='seguir-pagamento']"
confirmAddressXPath = "/html/body/div[15]/div/div/div[3]/button[1]"
cardsDivID = "cartoes-salvos"
cardClassName = "select-cta-option"
termsCheckboxXPath = "/html/body/main/div/div[3]/div[8]/div[2]/div[3]/div/input"
termsDivXPath = "/html/body/main/div/div[3]/div[8]/div[2]/div[3]/div"
finalButtonID = "confirmar-pagamento"
remindMeButtonID = "btn-avisar"