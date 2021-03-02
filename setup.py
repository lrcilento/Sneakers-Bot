import os

try:
    os.remove("env.py")
    print("Removendo configurações antigas...")
except:
    print("Nenhuma configuração passada encontrada.")
envFile = open("env.py", "w+")
envFile.write("email = '"+input("Insira seu e-mail de login do site da Nike: ")+"'\n")
envFile.write("password = '"+input("Insira sua senha do site da Nike: ")+"'\n")
envFile.write("phoneNumber = '"+input("Insira o número de celula que deseja receber o SMS no formato '11987654321': ")+"'\n")
envFile.write("targetURL = '"+input("Insira a URL completa do Sneaker que deseja comprar (com 'https://'): ")+"'\n")
tamanhos = input("Insira os tamanhos que deseja comprar, em ordem de preferencia e seperados por espaço (e. g.: 39 40 42): ").split(" ")
for x in range(0, len(tamanhos)):
    tamanhos[x] = int(tamanhos[x])
envFile.write("sizes = "+str(tamanhos)+"\n")
print("O modo teste ignora a necessiade de horário de início e não chega e finalizar a compra, use-o para testar o fluxo")
enableTest = input("Deseja habilitar o modo teste? (y/n) ")
if enableTest.lower() == 'y':
    envFile.write("test = True\n")
    envFile.write("startTime = None\n")
else:
    envFile.write("test = False\n")
    envFile.write("startTime = '"+input("Insira o horário do drop no formato 'HH:MM': ")+"'\n")
print("O modo headless faz com que não seja necessário que o bot abra uma aba física do navegador, é o ideal para sua execução ser mais rápida, porém é mais difícil debugar")
enableHeadless = input("Deseja habilitar o modo headless? (y/n) ")
if enableHeadless.lower() == 'y':
    envFile.write("headless = True\n")
else:
    envFile.write("headless = False\n")
threadNumber = int(input("Insira a quantidade de Threads (1 ~ 20): "))
envFile.write("threadNumber = "+str(threadNumber)+"\n")
if threadNumber > 1 and input("Deseja que os Thread adicionais sejam passados por Proxy? (y/n) ").lower() == 'y':
    envFile.write("proxy = True\n")
    envFile.write("proxyUsername = '"+input("Insira nome de usuário do servidor de Proxy: ")+"'\n")
    envFile.write("proxyPassword = '"+input("Insira a senha do servidor de Proxy: ")+"'\n")
    proxies = input("Insira endereços de proxy, no formato 'IP:PORT', separados por espaço: ").split(" ")
    envFile.write("proxies = "+str(proxies)+"\n")
else:
    envFile.write("proxy = False\n")
    envFile.write("proxyUsername = None\n")
    envFile.write("proxyPassword = None\n")
    envFile.write("proxies = None\n")
envFile.write("proxyString = 'https://'+proxyUsername+':'+proxyPassword+'@'\n")
print("Tudo configurado! Agora é só executar!")
envFile.close()