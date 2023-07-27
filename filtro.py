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
                if conteudo.startswith('<a class="VideoItem"'):
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