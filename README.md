## Instalação:

### Linux:
```
$ sudo apt install git python3 python3-pip firefox firefox-geckodriver \n
$ git clone https://github.com/lrcilento/Sneakers-Bot.git
$ cd Sneakers-Bot
$ sudo pip install -r requirements.txt
```
      
### Windows:

Faça download dos seguintes arquivos:
- Firefox: https://www.mozilla.org/en-US/firefox/download/thanks/
- Git: https://git-scm.com/download/win
- Python: https://www.python.org/ftp/python/3.9.1/python-3.9.1-amd64.exe
- Geckodriver: https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-win64.zip

Instale os três primeiros e extraia o Geckodriver para dentro da pasta do Firefox, e então:
```
$ git clone https://github.com/lrcilento/Sneakers-Bot.git
$ cd Sneakers-Bot
$ pip install -r requirements.txt
```
      
## Uso:
```
$ python setup.py
$ python main.py
```

## Troubleshooting:
1. Tente 'python3' ao invés de 'python' e 'pip3' ao invés de 'pip' caso algum desses comando dê problema.
2. Caso haja algum problema com o firefox e/ou geckodriver, assegure-se de que os caminhos são os listados abaixo:
   - Linux:
     - Firefox: /usr/lib/firefox/firefox/
     - Geckodriver: /usr/local/bin/geckodriver/
   - Windows:
     - Firefox: C:\Program Files\Mozilla Firefox\firefox.exe
     - Geckodriver: C:\Program Files\Mozilla Firefox\geckodriver.exe
