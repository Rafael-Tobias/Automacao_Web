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
    try:
        # Criar a pasta 'Pasta_videos_baixados' no caminho específico
        videos_folder = criar_pasta_videos_baixados()

        if videos_folder:
            # Abrir o arquivo videos_url.txt para leitura
            with open('videos_url.txt', 'r', encoding='utf-8') as arquivo:
                # Ler as linhas do arquivo
                linhas = arquivo.readlines()

                # Loop pelas linhas para baixar os vídeos e organizá-los nas pastas
                for linha in linhas:
                    # Dividir a linha pelos separadores ';' para obter a URL, código e nome do vídeo
                    url, codigo, nome_video = linha.strip().split(';')

                    # Criar a pasta para o código, caso não exista
                    pasta_codigo = os.path.join(videos_folder, f'Pasta_{codigo}')
                    if not os.path.exists(pasta_codigo):
                        os.makedirs(pasta_codigo)

                    # Definir o caminho do arquivo de vídeo com o nome completo
                    caminho_video = os.path.join(pasta_codigo, f'{nome_video}.mp4')

                    # Baixar o vídeo da URL e salvar no caminho especificado
                    response = requests.get(url, stream=True)
                    with open(caminho_video, 'wb') as arquivo_video:
                        for chunk in response.iter_content(chunk_size=8192):
                            arquivo_video.write(chunk)

            print("Download dos vídeos concluído com sucesso!")

    except FileNotFoundError:
        print("Arquivo videos_url.txt não encontrado.")
    except Exception as e:
        print("Erro ao baixar os vídeos:", e)

# Chamada da função para criar a pasta Pasta_videos_baixados e fazer o download dos vídeos
download_videos()
