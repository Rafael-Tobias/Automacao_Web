import PySimpleGUI as sg
from playwright.sync_api import sync_playwright as playwright
import pyautogui, time

# Função para simular a combinação de teclas "ctrl+shift+i"
from playwright.sync_api import sync_playwright

def simulate_ctrl_shift_i():
    pyautogui.hotkey('ctrl', 'shift', 'i')

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
        # Fechar o navegador
        browser.close()
abrir_links_finais()