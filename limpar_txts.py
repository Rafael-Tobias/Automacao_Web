def limpar_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.truncate(0)
        print(f"Conteúdo do arquivo {nome_arquivo} foi limpo com sucesso.")
    except Exception as e:
        print(f"Erro ao limpar o arquivo {nome_arquivo}: {e}")

limpar_arquivo("sites.txt")
limpar_arquivo("videos_url.txt")
