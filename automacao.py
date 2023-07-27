import PySimpleGUI as sg
from playwright.sync_api import sync_playwright as playwright
import pyautogui, filtro, time, os, requests, organiza_pasta, limpar_txts

# Função para simular a combinação de teclas "ctrl+shift+i"
from playwright.sync_api import sync_playwright

import os
import shutil

import requests
import os

def criar_pasta_videos_baixados():
    try:
        # Caminho específico onde será criada a pasta Pasta_videos_baixados
        pasta_videos_baixados = r'C:\Users\bruno\OneDrive\Área de Trabalho\rafael_automacao\Pasta_videos_baixados'

        if not os.path.exists(pasta_videos_baixados):
            os.makedirs(pasta_videos_baixados)
            print("Pasta Pasta_videos_baixados criada com sucesso!")
        else:
            print("A pasta Pasta_videos_baixados já existe.")

        return pasta_videos_baixados

    except Exception as e:
        print("Erro ao criar a pasta Pasta_videos_baixados:", e)
        return None

def download_videos():
    arquivo_videos_url = "videos_url.txt"
    arquivo_automacao = "automacao.txt"
    pasta_destino = "C:/Users/bruno/OneDrive/Área de Trabalho/rafael_automacao/Pasta_videos_baixados"

    # Verificar se o arquivo videos_url.txt existe
    if not os.path.exists(arquivo_videos_url):
        print("Arquivo videos_url.txt não encontrado.")
        return

    # Verificar se o arquivo automacao.txt existe
    if not os.path.exists(arquivo_automacao):
        print("Arquivo automacao.txt não encontrado.")
        return

    # Criar a pasta de destino se não existir
    if not os.path.exists(pasta_destino):
        try:
            os.makedirs(pasta_destino)
            print(f"Pasta {pasta_destino} criada com sucesso.")
        except OSError as e:
            print(f"Erro ao criar pasta {pasta_destino}: {e}")
            return

    # Ler os links de download do arquivo automacao.txt e fazer tratamento
    with open(arquivo_automacao, 'r', encoding='utf-8') as arquivo_automacao:
        links_download = [link.strip() for link in arquivo_automacao.readlines() if link.strip()]

    # Ler os links do arquivo videos_url.txt e fazer o download dos vídeos
    with open(arquivo_videos_url, 'r', encoding='utf-8') as arquivo_videos:
        linhas = arquivo_videos.readlines()

        for i, linha in enumerate(linhas):
            url, _, nome_video = linha.strip().split(';')
            nome_video = nome_video.replace("</a>", "").strip()

            try:
                # Verificar se a URL de download não está vazia
                if links_download[i].strip():
                    print(f"URL de download: {links_download[i].strip()}")
                    # Fazer o download do vídeo
                    resposta = requests.get(links_download[i].strip())
                    if resposta.status_code == 200:
                        caminho_destino = os.path.join(pasta_destino, f"{nome_video}.mp4")
                        with open(caminho_destino, 'wb') as arquivo_destino:
                            arquivo_destino.write(resposta.content)
                        print(f"Download do vídeo {nome_video} concluído.")
                    else:
                        print(f"Falha ao fazer o download do vídeo {nome_video}.")
                else:
                    print(f"URL de download vazia para o vídeo {nome_video}. Pulando download.")
            except Exception as e:
                print(f"Erro ao fazer o download do vídeo {nome_video}: {e}")

    print("Todos os vídeos foram baixados com sucesso.")


def download_videos():
    arquivo_videos_url = "videos_url.txt"
    arquivo_automacao = "automacao.txt"
    pasta_destino = "C:/Users/bruno/OneDrive/Área de Trabalho/rafael_automacao/Pasta_videos_baixados"

    # Verificar se o arquivo videos_url.txt existe
    if not os.path.exists(arquivo_videos_url):
        print("Arquivo videos_url.txt não encontrado.")
        return

    # Verificar se o arquivo automacao.txt existe
    if not os.path.exists(arquivo_automacao):
        print("Arquivo automacao.txt não encontrado.")
        return

    # Criar a pasta de destino se não existir
    if not os.path.exists(pasta_destino):
        try:
            os.makedirs(pasta_destino)
            print(f"Pasta {pasta_destino} criada com sucesso.")
        except OSError as e:
            print(f"Erro ao criar pasta {pasta_destino}: {e}")
            return

    # Ler os links de download do arquivo automacao.txt e fazer tratamento
    with open(arquivo_automacao, 'r', encoding='utf-8') as arquivo_automacao:
        links_download = [link.strip() for link in arquivo_automacao.readlines() if link.strip()]

    # Ler os links do arquivo videos_url.txt e fazer o download dos vídeos
    with open(arquivo_videos_url, 'r', encoding='utf-8') as arquivo_videos:
        linhas = arquivo_videos.readlines()

        for i, linha in enumerate(linhas):
            url, _, nome_video = linha.strip().split(';')
            nome_video = nome_video.replace("</a>", "").strip()

            try:
                # Verificar se a URL de download não está vazia
                if links_download[i].strip():
                    print(f"URL de download: {links_download[i].strip()}")
                    # Fazer o download do vídeo
                    resposta = requests.get(links_download[i].strip())
                    if resposta.status_code == 200:
                        caminho_destino = os.path.join(pasta_destino, f"{nome_video}.mp4")
                        with open(caminho_destino, 'wb') as arquivo_destino:
                            arquivo_destino.write(resposta.content)
                        print(f"Download do vídeo {nome_video} concluído.")
                    else:
                        print(f"Falha ao fazer o download do vídeo {nome_video}.")
                else:
                    print(f"URL de download vazia para o vídeo {nome_video}. Pulando download.")
            except Exception as e:
                print(f"Erro ao fazer o download do vídeo {nome_video}: {e}")

    print("Todos os vídeos foram baixados com sucesso.")


def abrir_links_finais():
    arquivo_videos_url = "videos_url.txt"

    # Inicializar o contexto do navegador
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # Abrir uma nova página
        page = browser.new_page()

        # Abrir o arquivo videos_url.txt para leitura
        with open(arquivo_videos_url, 'r', encoding='utf-8') as arquivo_videos:
            # Ler as linhas do arquivo
            linhas = arquivo_videos.readlines()
            j = 0
            # Loop pelas linhas para abrir os links com o Playwright
            for linha in linhas:
                j = j + 1
                # Dividir a linha pelos separadores ';' para obter o URL
                url, _, _ = linha.strip().split(';')
                
                # Abrir o link no navegador
                page.goto(url)
                if j == 1:
                    page.fill("xpath=/html/body/div[1]/div/div/div[2]/div/div/div/span/form/div[2]/span/div/div/div[1]/div[1]/input", "brunotobi@gmail.com")
                    page.fill("xpath=/html/body/div[1]/div/div/div[2]/div/div/div/span/form/div[3]/span/div/div/div[1]/div[1]/input", "bbrR980519@")
                    page.locator("xpath=/html/body/div[1]/div/div/div[2]/div/div/div/span/form/div[6]/div/button/span").click()
                    time.sleep(6)
                    pyautogui.hotkey("alt","tab")
                    pyautogui.hotkey("ctrl","a")
                    pyautogui.press("delete")
                    pyautogui.hotkey("alt","tab")
                    simulate_ctrl_shift_i()
                time.sleep(2)
                simulate_ctrl_shift_i()
                time.sleep(2)
                simulate_ctrl_shift_i()
                time.sleep(2)
                pyautogui.hotkey("ctrl", "f")
                pyautogui.write("video-react-video")
                pyautogui.press("tab")
                pyautogui.press("enter")
                pyautogui.press("enter")
                pyautogui.press("tab")
                pyautogui.press("tab")
                pyautogui.press("tab")
                pyautogui.hotkey("ctrl", "c")
                pyautogui.hotkey("alt", "tab")
                pyautogui.hotkey("ctrl","v")
                pyautogui.press("enter")
                pyautogui.press("enter")
                pyautogui.hotkey("ctrl","s")
                pyautogui.hotkey("alt","tab")
            download_videos()
        # Fechar o navegador
        browser.close()


def abrir_urls():
    # Lista para armazenar as URLs do arquivo sites.txt
    urls = []
    j = 0

    try:
        # Abre o arquivo sites.txt para leitura
        with open('sites.txt', 'r') as arquivo_sites:
            # Lê as URLs do arquivo e as armazena na lista 'urls'
            urls = arquivo_sites.read().splitlines()

        # Inicializa o Playwright
        with sync_playwright() as p:
            # Cria uma instância do navegador (pode ser 'chromium', 'firefox' ou 'webkit')
            browser = p.chromium.launch(headless=False)

            # Cria uma nova página no navegador
            page = browser.new_page()

            # Loop para abrir cada URL e navegar até ela
            for url in urls:
                j = j + 1
                # Navega até a URL
                page.goto(url)
                if j == 1:
                    page.fill("xpath=/html/body/div[1]/div/div/div[2]/div/div/div/span/form/div[2]/span/div/div/div[1]/div[1]/input", "brunotobi@gmail.com")
                    page.fill("xpath=/html/body/div[1]/div/div/div[2]/div/div/div/span/form/div[3]/span/div/div/div[1]/div[1]/input", "bbrR980519@")
                    page.locator("xpath=/html/body/div[1]/div/div/div[2]/div/div/div/span/form/div[6]/div/button/span").click()
                    time.sleep(6)
                    simulate_ctrl_shift_i()
                time.sleep(5)
                simulate_ctrl_shift_i()
                time.sleep(3)
                simulate_ctrl_shift_i()
                time.sleep(3)
                pyautogui.hotkey("ctrl", "f")
                pyautogui.write("VideoItem")
                pyautogui.press("tab")
                pyautogui.press("enter")
                pyautogui.hotkey("ctrl", "c")
                pyautogui.hotkey("alt", "tab")
                pyautogui.hotkey("ctrl", "a")
                pyautogui.hotkey("ctrl", "v")
                pyautogui.press("enter")
                pyautogui.press("enter")
                pyautogui.hotkey("alt", "tab")

                for i in range(0, 100):
                    pyautogui.press("down")
                    pyautogui.press("down")
                    pyautogui.press("right")
                    pyautogui.press("right")
                    pyautogui.hotkey('ctrl', 'c')
                    pyautogui.hotkey("alt", "tab")
                    pyautogui.hotkey("ctrl", "v")
                    pyautogui.press("enter")
                    pyautogui.press("enter")
                    pyautogui.hotkey("ctrl", "s")
                    pyautogui.hotkey("alt", "tab")
                filtro.filtro_txt2()
            # Fecha o navegador após abrir todas as URLs
            browser.close()

    except FileNotFoundError:
        print("Arquivo sites.txt não encontrado.")
    except Exception as e:
        print("Erro ao abrir as URLs:", e)

def simulate_ctrl_shift_i():
    pyautogui.hotkey('ctrl', 'shift', 'i')

def simulate_ctrl_f():
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.write("LessonList-item")

def abrir_notepad():
    pyautogui.hotkey('win', 'r')
    time.sleep(1)
    pyautogui.write("cmd")
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.write(r"cd OneDrive\Documentos\pasta_automacao")
    pyautogui.press("enter")
    pyautogui.write("automacao.txt")
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.hotkey("alt", "tab")
    time.sleep(1)
    pyautogui.write("exit")
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.hotkey("alt", "tab")

def pega_quantidade():

#CONTROLA QUANTIDADEE+++++++++++++++++++++++++++++++++++
    for i in range(0, 30):
        if i == 0:        
            pyautogui.press('tab')
            pyautogui.press("enter")
            for i in range(0, 10):
                pyautogui.press('right')
            pyautogui.hotkey('ctrl', 'c')
            pyautogui.hotkey("alt", "tab")
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("ctrl", "v")
            pyautogui.press("enter")
            pyautogui.press("enter")
            pyautogui.hotkey("alt", "tab")
        else:
            for i in range(0, 8):
                pyautogui.press("down")
            for i in range(0, 10):
                pyautogui.press('right')
            pyautogui.hotkey('ctrl', 'c')
            pyautogui.hotkey("alt", "tab")
            pyautogui.hotkey("ctrl", "v")
            pyautogui.press("enter")
            pyautogui.press("enter")
            pyautogui.hotkey("ctrl", "s")
            pyautogui.hotkey("alt", "tab")

def automate_browser(url):
    with playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        page.fill("xpath=/html/body/div[1]/div/div/div[2]/div/div/div/span/form/div[2]/span/div/div/div[1]/div[1]/input", "brunotobi@gmail.com")
        page.fill("xpath=/html/body/div[1]/div/div/div[2]/div/div/div/span/form/div[3]/span/div/div/div[1]/div[1]/input", "bbrR980519@")
        page.locator("xpath=/html/body/div[1]/div/div/div[2]/div/div/div/span/form/div[6]/div/button/span").click()
        abrir_notepad()
        time.sleep(6)
        simulate_ctrl_shift_i()
        time.sleep(4)
        simulate_ctrl_f()
        pega_quantidade()
        filtro.filtro_txt()
        time.sleep(5)
        browser.close()

layout = [
    [sg.Text("Digite o link do site:")],
    [sg.Input(key="-URL-", size=(50,1))],
    [sg.Button("Automatizar Navegador"), sg.Button("Sair")]
]

window = sg.Window("Automatização de Navegador", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Sair":
        break
    elif event == "Automatizar Navegador":
        url = values["-URL-"]
        automate_browser(url)
        abrir_urls()
        abrir_links_finais()
        organiza_pasta.organizar_pastas()
        time.sleep(8)
        pyautogui.hotkey("alt","tab")
        pyautogui.hotkey("ctrl","a")
        pyautogui.write("************SOFTWARE FINALIZADO***************")
        pyautogui.press("enter")
        pyautogui.write("-rafael é fera mesmo.")

window.close()