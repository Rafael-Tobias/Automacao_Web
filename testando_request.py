import os
import requests

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
download_videos()