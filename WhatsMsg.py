from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import time


class WhatsMsg:
    # Define os diretórios do driver, cache do navegador e pasta de midia.
    dir_path = os.getcwd()
    chromedriver = dir_path + "/driver/chromedriver"
    dir_cache = dir_path + "/cache"
    dir_img = dir_path + "/midia/"

    def __init__(self):
        try:
            print("Inicializando programa...")
            self.cache = webdriver.ChromeOptions()
            self.cache.add_argument(r"user-data-dir={}".format(self.dir_cache))
            self.chrome = webdriver.Chrome(self.chromedriver, options=self.cache)
            print("Abrindo Whatsapp no Navegador Chrome")
            self.chrome.get("https://web.whatsapp.com")
            print("Aguardando 15 segundos. Escanear QrCode / Carregamento da página...\n")
            time.sleep(15)
            print("Funções disponiveis:\n"
                  "* Enviar Mensagem/Midia\n"
                  "* Enviar Mensagem/Midia numero telefone\n"
                  "* Mensagens não lidas\n"
                  "* Enviar Mensagem/Midia Flood\n"
                  "* Ver contatos (teste)\n"
                  "** Para sair obj.sair()\n")
        except Exception as e:
            print("Erro ao inicializar", e)

    def __buscar_contatos(self, nome_contato):
        try:
            print(f"Fazendo a busca nos contatos por: {nome_contato}")
            # noinspection PyStatementEffect
            self.chrome.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]').click
            self.chrome.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]').send_keys(nome_contato)
            self.chrome.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]').send_keys(Keys.ENTER)
        except Exception as e:
            print("Erro ao buscar contato", e)

    def __mensagem(self, mensagem):
        try:
            print(f"Escrevendo a mensagem: {mensagem}")
            self.chrome.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]').click()
            self.chrome.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]').send_keys(mensagem)
            self.chrome.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]').send_keys(Keys.ENTER)
            print("Mensagem enviada...")
        except Exception as e:
            print("Erro ao enviar mensagem", e)

    def __enviar_midia(self, nome_arquivo):
        try:
            self.chrome.find_element_by_css_selector("span[data-icon='clip']").click()
            # Seleciona input
            adicionar = self.chrome.find_element_by_css_selector("input[type='file']")
            # Adiciona arquivo
            print(f"Inserindo imagem: {nome_arquivo}")
            adicionar.send_keys(self.dir_img + nome_arquivo)
            time.sleep(3)
            print("Enviando imagem...")
            self.chrome.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/span/div/div/span').click()
        except Exception as e:
            print("Erro ao enviar midia", e)

    def enviar_mensagem(self, contato, mensagem):
        try:
            self.__buscar_contatos(contato)
            self.__mensagem(mensagem)
        except Exception as e:
            print("Erro ao enviar mensagem", e)

    def enviar_msg_numerofone(self, fone_numero, mensagem):
        try:
            self.chrome.get(f"https://web.whatsapp.com/send?phone=+{fone_numero}")
            print("Aguardando 15 segundos para carregamento da página...")
            time.sleep(15)
            self.__mensagem(mensagem)
            print(f"Mensagem: {mensagem} enviada para {fone_numero}")
        except Exception as e:
            print("Erro ", e)

    def enviar_midia_numerofone(self, fone_numero, nome_arquivo):
        try:
            self.chrome.get(f"https://web.whatsapp.com/send?phone=+{fone_numero}")
            print("Aguardando 15 segundos para carregamento da página...")
            time.sleep(15)
            self.__enviar_midia(nome_arquivo)
            print(f"Mídia: {nome_arquivo} enviada para {fone_numero}")
        except Exception as e:
            print("Erro ", e)

    def enviar_midia(self, contato, nome_arquivo):
        try:
            self.__buscar_contatos(contato)
            self.__enviar_midia(nome_arquivo)
        except Exception as e:
            print("Erro ao enviar midia", e)

    def enviar_msg_flood(self, contato, mensagem, qtd):
        self.qtd = qtd
        try:
            self.__buscar_contatos(contato)
            n = 0
            while n < qtd:
                self.__mensagem(mensagem)
                time.sleep(2)
                n += 1
            print("Mensagens enviadas...")
        except Exception as e:
            print("Erro ao enviar flood", e)

    def enviar_midia_flood(self, contato, nome_arquivo, qtd):
        self.qtd = qtd
        n = 0
        try:
            self.__buscar_contatos(contato)
            while n < qtd:
                self.__enviar_midia(nome_arquivo)
                n += 1
                time.sleep(5)
        except Exception as e:
            print("Erro ao enviar midia", e)

    def ver_contatos(self):
        try:
            self.chrome.find_element_by_xpath('//*[@id="side"]/header/div[2]/div/span/div[2]/div/span').click()

            contatos = self.chrome.find_elements_by_class_name('N2dUK')
            for contato in contatos:
                print(contato.text)
        except Exception as e:
            print("Erro ao puxar os contatos", e)

    def msgs_nao_lidas(self):
        naolidas = self.chrome.find_elements_by_class_name("_1V5O7")
        try:
            for naolida in naolidas:
                lista = list(naolida.text)
                lista.insert(0, "Nome: ")
                if lista.__contains__("\n"):
                    index = lista.index("\n")
                    lista.pop(index)
                    lista.insert(index,"\nHora: ")
                if lista.__contains__("\n"):
                    index = lista.index("\n")
                    lista.pop(index)
                    lista.insert(index,"\nÚltima Mensagem: ")
                if lista.__contains__("\n"):
                    index = lista.index("\n")
                    lista.pop(index)
                    lista.insert(index,"\nQtd Mensagem: ")
                    tamanho_lista = len(lista)
                    lista.insert(tamanho_lista + 1, "\n-------------------")
                retorno = ''.join(lista)
                print(retorno)
            print("Não há novas mensagens!")
        except Exception as e:
            print("Erro ", e)

    def bot(self):

        global msg, nome
        while True:
            print("Aguardando mensagem...")
            naolidas = self.chrome.find_elements_by_class_name("_1V5O7")
            try:
                for naolida in naolidas:
                    lista = list(naolida.text)
                    lista.insert(0, "Nome: ")
                    if lista.__contains__("\n"):
                        index = lista.index("\n")
                        lista.pop(index)
                        lista.insert(index,"\nHora: ")
                    if lista.__contains__("\n"):
                        index = lista.index("\n")
                        lista.pop(index)
                        lista.insert(index,"\nÚltima Mensagem: ")
                    if lista.__contains__("\n"):
                        index = lista.index("\n")
                        lista.pop(index)
                        lista.insert(index,"\nQtd Mensagem: ")
                    nome = lista.index("Nome: ")
                    hora = lista.index("\nHora: ")
                    nome = lista[nome+1:hora]
                    msg = lista.index("\nÚltima Mensagem: ")
                    qtd = lista.index("\nQtd Mensagem: ")
                    msg = lista[msg+1:qtd]
                    nome = ''.join(nome)
                    msg = ''.join(msg)

                    if msg == "/ajuda":
                        self.enviar_mensagem(nome, "Opa! :smiling" + Keys.ENTER + Keys.SPACE + "vou te ajudar! Minhas opções no momento são: "
                                            "\n */catálogo*")
                        time.sleep(3)
                        self.chrome.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button/span').click()
                        self.chrome.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div[11]/div/div/div/div[2]/div[2]/div[2]/span[1]/div/span').click()
                        time.sleep(5)

                    elif msg == "/catálogo" or msg == "/catalogo":
                        self.enviar_mensagem(nome, "Ok! Aqui está :)")
                        self.enviar_midia(nome, "whatsmsg.png")
                        self.chrome.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div[11]/div/div/div/div[2]/div[2]/div[2]/span[1]/div/span').click()
                        time.sleep(5)

                    else:
                        self.enviar_mensagem(nome, "Olá eu sou o PyWhatsMsg_Bot! :robot" + Keys.ENTER + Keys.SPACE + " "
                                                    "\n digite */ajuda* para ver as opções.")
                        time.sleep(3)
                        self.chrome.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button/span').click()
                        self.chrome.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div[11]/div/div/div/div[2]/div[2]/div[2]/span[1]/div/span').click()
                        time.sleep(5)

            except Exception as e:
                print("Erro ", e)
                continue

    def sair(self):
        try:
            print("Encerrando aplicação...")
            self.chrome.quit()
        except Exception as e:
            print("Erro ao encerrar", e)
