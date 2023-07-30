import os
import shutil
import requests
import time
import PySimpleGUI as sg
import pyautogui
from playwright.sync_api import sync_playwright

# Função para limpar o conteúdo de um arquivo
def limpar_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.truncate(0)
        print(f"Conteúdo do arquivo {nome_arquivo} foi limpo com sucesso.")
    except Exception as e:
        print(f"Erro ao limpar o arquivo {nome_arquivo}: {e}")

# Função para extrair as URLs do arquivo 'automacao.txt' e salvar em 'sites.txt'
def extrair_urls():
    urls_encontrados = set()

    try:
        with open('automacao.txt', 'r', encoding='utf-8') as arquivo:
            conteudos = arquivo.read().split('\n')

            bloco_atual = ''

            for linha in conteudos:
                if linha.startswith('<a class="Collapse-header" tabindex="0" href='):
                    inicio_url = linha.find('href=') + 6
                    fim_url = linha.find('>', inicio_url) - 1
                    url = linha[inicio_url:fim_url]

                    if bloco_atual == '':
                        bloco_atual = url
                    elif url.startswith(bloco_atual):
                        continue
                    else:
                        bloco_atual = url

                    urls_encontrados.add("https://www.estrategiaconcursos.com.br" + url)

        with open('sites.txt', 'w') as arquivo_sites:
            for url in urls_encontrados:
                arquivo_sites.write(url + '\n')

        print("Extração de URLs concluída com sucesso!")

    except UnicodeDecodeError as e:
        print("Erro de decodificação Unicode no arquivo automacao.txt:", e)

# Função para extrair informações de vídeos do arquivo 'automacao.txt' e salvar em 'videos_url.txt'
def extrair_informacoes_videos():
    videos_info = {}

    try:
        with open('automacao.txt', 'r', encoding='utf-8') as arquivo:
            conteudos = arquivo.read().split('\n\n')

            for conteudo in conteudos:
                if conteudo.startswith('<a class="VideoItem"'):
                    inicio_href = conteudo.find('href=') + 6
                    fim_href = conteudo.find('>', inicio_href) - 1
                    url_video = conteudo[inicio_href:fim_href]
                    url_video = "https://www.estrategiaconcursos.com.br" + url_video

                    inicio_nome = conteudo.find('VideoItem-info-title">') + len('VideoItem-info-title">')
                    fim_nome = conteudo.find('</span>', inicio_nome)
                    nome_video = conteudo[inicio_nome:fim_nome].replace('</a>', '').strip()

                    inicio_sobrenome = conteudo.find('</span>', fim_nome + 1) + len('</span>')
                    sobrenome_video = conteudo[inicio_sobrenome:].strip()

                    inicio_nome_aula = url_video.find('aulas/') + len('aulas/')
                    fim_nome_aula = url_video.find('/videos')
                    nome_aula = url_video[inicio_nome_aula:fim_nome_aula]

                    videos_info[url_video] = (nome_aula, sobrenome_video, nome_video)

        with open('videos_url.txt', 'w', encoding='utf-8') as arquivo_videos:
            for url, info in videos_info.items():
                nome_aula, sobrenome_video, nome_video = info
                arquivo_videos.write(f"{url};{nome_aula};{nome_video}\n")

        print("Extração de informações de vídeos concluída com sucesso!")

    except FileNotFoundError:
        print("Arquivo automacao.txt não encontrado.")
    except Exception as e:
        print("Erro ao processar o arquivo automacao.txt:", e)

# Função para criar a pasta 'Pasta_videos_baixados' se não existir
def criar_pasta_videos_baixados():
    try:
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

# Função para fazer o download dos vídeos a partir das URLs em 'videos_url.txt'
def download_videos():
    arquivo_videos_url = "videos_url.txt"
    pasta_destino = "C:/Users/bruno/OneDrive/Área de Trabalho/rafael_automacao/Pasta_videos_baixados"

    if not os.path.exists(arquivo_videos_url):
        print("Arquivo videos_url.txt não encontrado.")
        return

    if not os.path.exists(pasta_destino):
        try:
            os.makedirs(pasta_destino)
            print(f"Pasta {pasta_destino} criada com sucesso.")
        except OSError as e:
            print(f"Erro ao criar pasta {pasta_destino}: {e}")
            return

    with open(arquivo_videos_url, 'r', encoding='utf-8') as arquivo_videos:
        linhas = arquivo_videos.readlines()

        for i, linha in enumerate(linhas):
            url, _, nome_video = linha.strip().split(';')
            nome_video = nome_video.replace("</a>", "").strip()

            try:
                if url.strip():
                    print(f"URL de download: {url.strip()}")
                    resposta = requests.get(url.strip())
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

# Função para organizar os vídeos baixados em pastas de acordo com os códigos encontrados em 'videos_url.txt'
def organizar_pastas():
    pasta_videos = "C:/Users/bruno/OneDrive/Área de Trabalho/rafael_automacao/Pasta_videos_baixados"
    arquivo_videos_url = "videos_url.txt"
    pasta_destino = "C:/Users/bruno/OneDrive/Área de Trabalho/rafael_automacao"

    if not os.path.exists(pasta_videos):
        print("Pasta de vídeos não encontrada.")
        return

    if not os.path.exists(arquivo_videos_url):
        print("Arquivo videos_url.txt não encontrado.")
        return

    if not os.path.exists(pasta_destino):
        try:
            os.makedirs(pasta_destino)
            print(f"Pasta {pasta_destino} criada com sucesso.")
        except OSError as e:
            print(f"Erro ao criar pasta {pasta_destino}: {e}")
            return

    with open(arquivo_videos_url, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

        for linha in linhas:
            url, codigo, nome_video = linha.strip().split(';')
            codigo = codigo.strip()
            nome_video = nome_video.strip()

            video_path = os.path.join(pasta_videos, f"{nome_video}.mp4")
            if os.path.exists(video_path):
                pasta_codigo = os.path.join(pasta_destino, codigo)
                if not os.path.exists(pasta_codigo):
                    os.makedirs(pasta_codigo)

                shutil.move(video_path, os.path.join(pasta_codigo, f"{nome_video}.mp4"))
                print(f"Vídeo {nome_video} movido para a pasta {pasta_codigo} com sucesso.")
            else:
                print(f"Vídeo {nome_video}.mp4 não encontrado na pasta de vídeos. Pulando movimentação.")

    print("Organização concluída.")

# Função para automatizar o navegador utilizando Playwright
def automatizar_navegador(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url)
            page.fill("xpath=/html/body/div[1]/div/div/div[2]/div/div/div/span/form/div[2]/span/div/div/div[1]/div[1]/input", "brunotobi@gmail.com")
            page.fill("xpath=/html/body/div[1]/div/div/div[2]/div/div/div/span/form/div[3]/span/div/div/div[1]/div[1]/input", "bbrR980519@")
            page.locator("xpath=/html/body/div[1]/div/div/div[2]/div/div/div/span/form/div[6]/div/button/span").click()
            time.sleep(6)
            pyautogui.hotkey("alt", "tab")
            pyautogui.hotkey("ctrl", "shift", "i")
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
            pyautogui.hotkey("ctrl", "w")
            time.sleep(2)
            pyautogui.hotkey("alt", "tab")
            time.sleep(2)
            pyautogui.hotkey("ctrl", "t")
            time.sleep(2)
            pyautogui.write("https://www.estrategiaconcursos.com.br/cursosPorConcurso/")
            pyautogui.press("enter")
            time.sleep(6)
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("ctrl", "c")
            time.sleep(2)

    except Exception as e:
        print(f"Erro na automação do navegador: {e}")

# Função para abrir o navegador e acessar a página de login do Estratégia Concursos
def acessar_pagina_login():
    url_login = "https://www.estrategiaconcursos.com.br/login/"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url_login)
            time.sleep(3)
            pyautogui.hotkey("alt", "tab")

    except Exception as e:
        print(f"Erro ao acessar a página de login: {e}")

# Função principal para executar todas as tarefas
def main():
    limpar_arquivo('sites.txt')
    extrair_urls()
    extrair_informacoes_videos()
    criar_pasta_videos_baixados()
    download_videos()
    organizar_pastas()
    automatizar_navegador('https://www.estrategiaconcursos.com.br/cursosPorConcurso/')
    acessar_pagina_login()

# Execução do programa
if __name__ == "__main__":
    main()
