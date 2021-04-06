from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time


class WhatsMsg:
    # Define os diretórios do driver, cache do navegador e pasta imagem.
    dir_path = os.getcwd()
    chromedriver = dir_path + "/chromedriver"
    dir_cache = dir_path + "/cache"
    dir_img = dir_path + "/images/"

    def __init__(self):
        try:
            print("Inicializando programa...")
            self.cache = webdriver.ChromeOptions()
            self.cache.add_argument(r"user-data-dir={}".format(self.dir_cache))
            self.chrome = webdriver.Chrome(self.chromedriver, options=self.cache)
            print("Abrindo Whatsapp no Navegador Chrome")
            self.chrome.get("https://web.whatsapp.com")
            print("Aguardando escanear QrCode / Carregamento da página...\n")
            time.sleep(15)
            print("Funções disponiveis:\n"
                  "* Enviar Mensagem\n"
                  "* Enviar Imagem\n"
                  "* Enviar Mensagem Flood\n"
                  "* Enviar Imagem Flood\n"
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
            print("Mensagens enviadas...")
        except Exception as e:
            print("Erro ao enviar mensagem", e)

    def enviar_mensagem(self, contato, mensagem):
        try:
            self.__buscar_contatos(contato)
            self.__mensagem(mensagem)
        except Exception as e:
            print("Erro ao enviar mensagem", e)

    def enviar_imagem(self, contato, nome_arquivo):
        try:
            self.__buscar_contatos(contato)

            # Clica no botão adicionar
            self.chrome.find_element_by_css_selector("span[data-icon='clip']").click()
            # Seleciona input
            attach = self.chrome.find_element_by_css_selector("input[type='file']")
            # Adiciona arquivo
            print(f"Inserindo imagem: {nome_arquivo}")
            attach.send_keys(self.dir_img + nome_arquivo)
            time.sleep(3)
            # Seleciona botão enviar
            print("Enviando imagem...")
            send = self.chrome.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/span/div/div/span')
            # Clica no botão enviar
            send.click()
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

    def enviar_msg_flood(self, contato, mensagem, qtd):
        self.qtd = int(qtd)
        try:
            self.__buscar_contatos(contato)
            x = 0
            while x < qtd:
                self.__mensagem(mensagem)
                time.sleep(2)
                x += 1
            print("Mensagens enviadas...")
        except Exception as e:
            print("Erro ao enviar flood", e)

    def enviar_img_flood(self, contato, nome_arquivo, qtd):
        self.qtd = qtd
        x = 0
        try:
            self.__buscar_contatos(contato)
            while x < qtd:
                # Clica no botão adicionar
                self.chrome.find_element_by_css_selector("span[data-icon='clip']").click()
                # Seleciona input
                attach = self.chrome.find_element_by_css_selector("input[type='file']")
                # Adiciona arquivo
                print(f"Inserindo imagem: {nome_arquivo}")
                attach.send_keys(self.dir_img + nome_arquivo)
                time.sleep(3)
                # Seleciona botão enviar
                print("Enviando imagem...")
                send = self.chrome.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/span/div/div/span')
                # Clica no botão enviar
                send.click()
                x += 1
                time.sleep(5)
        except Exception as e:
            print("Erro ao enviar midia", e)

    def sair(self):
        try:
            print("Encerrando aplicação...")
            self.chrome.quit()
        except Exception as e:
            print("Erro ao encerrar", e)