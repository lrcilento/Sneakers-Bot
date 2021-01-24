# CONFIGURAÇÕES
# URL do drop (utilizar a URL completa, com HTTPS://)
targetURL = 'https://www.nike.com.br/Snkrs/Produto/LeBron-18/153-169-211-280003'
# Lista de tamanhos que deseja comprar, ela segue uma ordem de prioridade da esquerda para direita
# Números quebrados, como 37.5, devem ser escritos sem o ponto, e.g.: 375
sizes = [36, 37, 38]
# Horário exato do drop no formato "HH:MM"
startTime = "18:12"

# NÃO MEXER DAQUI PARA BAIXO
test = False
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
sizeXPaths = []

for x in range(0, len(sizes)):
    sizeXPaths.append("//label[@for='tamanho__id"+str(sizes[x])+"']")