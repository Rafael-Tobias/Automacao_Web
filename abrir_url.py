from playwright.sync_api import sync_playwright
import pyautogui

def abrir_urls():
    # Lista para armazenar as URLs do arquivo sites.txt
    urls = []

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
                # Navega até a URL
                page.goto(url)

                page.fill("xpath=/html/body/div[1]/div/div/div[2]/div/div/div/span/form/div[2]/span/div/div/div[1]/div[1]/input", "brunotobi@gmail.com")
                page.fill("xpath=/html/body/div[1]/div/div/div[2]/div/div/div/span/form/div[3]/span/div/div/div[1]/div[1]/input", "bbrR980519@")
                page.locator("xpath=/html/body/div[1]/div/div/div[2]/div/div/div/span/form/div[6]/div/button/span").click()
                

                page.wait_for_load_state("domcontentloaded", timeout=5000)
                
            # Fecha o navegador após abrir todas as URLs
            browser.close()

    except FileNotFoundError:
        print("Arquivo sites.txt não encontrado.")
    except Exception as e:
        print("Erro ao abrir as URLs:", e)
abrir_urls()