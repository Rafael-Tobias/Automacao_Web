import os
import shutil

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