import PySimpleGUI as sg
from playwright.sync_api import sync_playwright as playwright
import pyautogui, time, os, requests

# Função para simular a combinação de teclas "ctrl+shift+i"
from playwright.sync_api import sync_playwright

import os
import shutil

import requests
import os

import os
import shutil

def filtro_txt():
    # Conjunto para armazenar os URLs encontrados (garante que não haverá repetições)
    urls_encontrados = set()

    try:
        # Abre o arquivo automacao.txt para leitura usando a codificação 'utf-8'
        with open('automacao.txt', 'r', encoding='utf-8') as arquivo:
            # Lê o conteúdo do arquivo e divide os conteúdos separados por quebras de linhas
            conteudos = arquivo.read().split('\n')

            # Variável auxiliar para verificar se o conteúdo atual faz parte de um mesmo bloco
            bloco_atual = ''

            # Loop pelos conteúdos para encontrar os URLs
            for linha in conteudos:
                if linha.startswith('<a class="Collapse-header" tabindex="0" href='):
                    # Encontra a posição inicial e final do URL dentro da linha
                    inicio_url = linha.find('href=') + 6
                    fim_url = linha.find('>', inicio_url) - 1

                    # Extrai o URL
                    url = linha[inicio_url:fim_url]

                    # Verifica se o conteúdo atual faz parte do mesmo bloco
                    if bloco_atual == '':
                        bloco_atual = url
                    elif url.startswith(bloco_atual):
                        continue
                    else:
                        bloco_atual = url

                    # Adiciona o URL completo (com prefixo) ao conjunto de URLs encontrados
                    urls_encontrados.add("https://www.estrategiaconcursos.com.br" + url)

        # Abre o arquivo sites.txt para escrita
        with open('sites.txt', 'w') as arquivo_sites:
            # Escreve os URLs completos encontrados no arquivo sites.txt
            for url in urls_encontrados:
                arquivo_sites.write(url + '\n')

        print("Extração 1 de URLs concluída com sucesso!")

    except UnicodeDecodeError as e:
        print("Erro de decodificação Unicode no arquivo automacao.txt:", e)

def filtro_txt2():
    # Dicionário para armazenar as informações de cada vídeo
    videos_info = {}

    try:
        # Abre o arquivo automacao.txt para leitura
        with open('automacao.txt', 'r', encoding='utf-8') as arquivo:
            # Lê o conteúdo do arquivo e divide os conteúdos separados por quebras de linhas
            conteudos = arquivo.read().split('\n\n')

            # Loop pelos conteúdos para encontrar os vídeos
            for conteudo in conteudos:
                # Verifica se o conteúdo começa com '<a class="VideoItem"'
                if conteudo.startswith('<a class="VideoItem"') or conteudo.startswith('<a class="VideoItem isSelected"'):
                    # Encontra a posição inicial e final do href dentro do conteúdo
                    inicio_href = conteudo.find('href=') + 6
                    fim_href = conteudo.find('>', inicio_href) - 1

                    # Extrai a URL do vídeo
                    url_video = conteudo[inicio_href:fim_href]

                    # Adiciona o prefixo "https://www.estrategiaconcursos.com.br/" à URL
                    url_video = "https://www.estrategiaconcursos.com.br" + url_video

                    # Encontra o início e o fim do nome do vídeo
                    inicio_nome = conteudo.find('VideoItem-info-title">') + len('VideoItem-info-title">')
                    fim_nome = conteudo.find('</span>', inicio_nome)

                    # Extrai o nome do vídeo e remove a tag "</a>"
                    nome_video = conteudo[inicio_nome:fim_nome].replace('</a>', '').strip()

                    # Encontra o início do sobrenome do vídeo
                    inicio_sobrenome = conteudo.find('</span>', fim_nome + 1) + len('</span>')

                    # Extrai o sobrenome do vídeo
                    sobrenome_video = conteudo[inicio_sobrenome:].strip()

                    # Encontra o nome do vídeo, que está depois de "aulas/"
                    inicio_nome_aula = url_video.find('aulas/') + len('aulas/')
                    fim_nome_aula = url_video.find('/videos')

                    # Extrai o nome da aula (antes do primeiro '/')
                    nome_aula = url_video[inicio_nome_aula:fim_nome_aula]

                    # Adiciona as informações do vídeo ao dicionário videos_info
                    videos_info[url_video] = (nome_aula, sobrenome_video, nome_video)

        # Abre o arquivo videos_url.txt para escrita no modo "a" (append) com a codificação 'utf-8'
        with open('videos_url.txt', 'a', encoding='utf-8') as arquivo_videos:
            # Escreve as informações dos vídeos no arquivo videos_url.txt
            for url, info in videos_info.items():
                nome_aula, sobrenome_video, nome_video = info
                arquivo_videos.write(f"{url};{nome_aula};{nome_video}\n")

        print("Extração de URLs concluída com sucesso!")

    except FileNotFoundError:
        print("Arquivo automacao.txt não encontrado.")
    except Exception as e:
        print("Erro ao processar o arquivo automacao.txt:", e)

def limpar_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.truncate(0)
        print(f"Conteúdo do arquivo {nome_arquivo} foi limpo com sucesso.")
    except Exception as e:
        print(f"Erro ao limpar o arquivo {nome_arquivo}: {e}")

def organizar_pastas():
    pasta_videos = "C:/Users/bruno/OneDrive/Área de Trabalho/rafael_automacao/Pasta_videos_baixados"
    arquivo_videos_url = "videos_url.txt"
    pasta_destino = "C:/Users/bruno/OneDrive/Área de Trabalho/rafael_automacao"

    # Verificar se a pasta de vídeos existe
    if not os.path.exists(pasta_videos):
        print("Pasta de vídeos não encontrada.")
        return

    # Verificar se o arquivo videos_url.txt existe
    if not os.path.exists(arquivo_videos_url):
        print("Arquivo videos_url.txt não encontrado.")
        return

    # Criar a pasta de destino se não existir
    if not os.path.exists(pasta_destino):
        try:
            os.makedirs(pasta_destino)
            print(f"Pasta {pasta_destino} criada com sucesso.")
        except OSError as e:
            print(f"Erro ao criar pasta {pasta_destino}: {e}")
            return

    # Ler as informações do arquivo videos_url.txt
    with open(arquivo_videos_url, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

        for linha in linhas:
            url, codigo, nome_video = linha.strip().split(';')
            codigo = codigo.strip()
            nome_video = nome_video.strip()

            # Verificar se o vídeo está na pasta de vídeos
            video_path = os.path.join(pasta_videos, f"{nome_video}.mp4")
            if os.path.exists(video_path):
                # Criar a pasta de destino com o código, se não existir
                pasta_codigo = os.path.join(pasta_destino, codigo)
                if not os.path.exists(pasta_codigo):
                    os.makedirs(pasta_codigo)

                # Mover o vídeo para a pasta de destino
                shutil.move(video_path, os.path.join(pasta_codigo, f"{nome_video}.mp4"))
                print(f"Vídeo {nome_video} movido para a pasta {pasta_codigo} com sucesso.")
            else:
                print(f"Vídeo {nome_video}.mp4 não encontrado na pasta de vídeos. Pulando movimentação.")

    print("Organização concluída.")

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
                time.sleep(4)
                simulate_ctrl_shift_i()
                time.sleep(4)
                simulate_ctrl_shift_i()
                time.sleep(4)
                pyautogui.hotkey("ctrl", "f")
                time.sleep(0.5)
                pyautogui.write("video-react-video")
                pyautogui.press("tab")
                pyautogui.press("enter")
                pyautogui.press("enter")
                pyautogui.press("tab")
                pyautogui.press("tab")
                pyautogui.press("tab")
                pyautogui.hotkey("ctrl", "c")
                pyautogui.hotkey("alt", "tab")
                time.sleep(0.5)
                pyautogui.hotkey("ctrl","v")
                pyautogui.press("enter")
                pyautogui.press("enter")
                pyautogui.hotkey("ctrl","s")
                pyautogui.hotkey("alt","tab")
                time.sleep(0.5)
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
                time.sleep(4)
                simulate_ctrl_shift_i()
                time.sleep(4)
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
            

#QUANTIDADE DE VIDEOS
                for i in range(0, 110):
                    pyautogui.press("down")
                    time.sleep(0.2)
                    pyautogui.press("down")
                    time.sleep(0.2)
                    pyautogui.press("right")
                    time.sleep(0.2)
                    pyautogui.press("right")
                    pyautogui.hotkey('ctrl', 'c')
                    pyautogui.hotkey("alt", "tab")
                    time.sleep(0.5)
                    pyautogui.hotkey("ctrl", "v")
                    pyautogui.press("enter")
                    pyautogui.press("enter")
                    pyautogui.hotkey("ctrl", "s")
                    pyautogui.hotkey("alt", "tab")
                    time.sleep(0.5)
                filtro_txt2()
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
    time.sleep(0.5)
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
    for i in range(0, 35):
        if i == 0:        
            pyautogui.press('tab')
            pyautogui.press("enter")
            for i in range(0, 10):
                pyautogui.press('right')
            pyautogui.hotkey('ctrl', 'c')
            pyautogui.hotkey("alt", "tab")
            time.sleep(0.5)
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("ctrl", "v")
            pyautogui.press("enter")
            pyautogui.press("enter")
            pyautogui.hotkey("alt", "tab")
            time.sleep(0.5)
        else:
            for i in range(0, 8):
                pyautogui.press("down")
            for i in range(0, 10):
                pyautogui.press('right')
            pyautogui.hotkey('ctrl', 'c')
            pyautogui.hotkey("alt", "tab")
            time.sleep(0.5)
            pyautogui.hotkey("ctrl", "v")
            pyautogui.press("enter")
            pyautogui.press("enter")
            pyautogui.hotkey("ctrl", "s")
            pyautogui.hotkey("alt", "tab")
            time.sleep(0.5)

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
        filtro_txt()
        time.sleep(5)
        browser.close()

layout = [
    [sg.Text("Confira se o CAPS LOCK está desativado. ")],
    [sg.Text("COPIE O LINK DO SITE NESTE FORMATO: ")],
    [sg.Text("LINK DE EXEMPLO: https://www.estrategiaconcursos.com.br/app/dashboard/cursos/240663/aulas")],
    [sg.Input(key="-URL-", size=(50,1))],
    [sg.Button("Start"), sg.Button("Sair")]
]

window = sg.Window("Automatização de Navegador", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Sair":
        break
    elif event == "Start":
        url = values["-URL-"]
        limpar_arquivo("sites.txt")
        limpar_arquivo("videos_url.txt")
        print("executando automate")
        automate_browser(url)
        print("executando abrir urls")
        abrir_urls()
        print("executando abrir_links_finais")
        abrir_links_finais()
        print("executando organizar pastas")
        organizar_pastas()
        pyautogui.hotkey("ctrl","a")
        time.sleep(0.5)
        pyautogui.press("F")
        pyautogui.press("I")
        pyautogui.press("N")
        pyautogui.press("A")
        pyautogui.press("L")
        pyautogui.press("I")
        pyautogui.press("Z")
        pyautogui.press("A")
        pyautogui.press("D")
        pyautogui.press("O")
        pyautogui.write(" [rafael eh fera mesmo.]")
        time.sleep(1)

window.close()