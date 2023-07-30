import os

def executar_arquivo_caminho(caminho):
    try:
        # Verifica se o caminho é um arquivo válido
        if os.path.isfile(caminho):
            os.system(f'python "{caminho}"')
        else:
            print(f"O caminho '{caminho}' não aponta para um arquivo válido.")
    except Exception as e:
        print(f"Ocorreu um erro ao tentar executar o arquivo: {e}")

if __name__ == "__main__":
    caminho_arquivo = r"C:\Users\bruno\OneDrive\Documentos\pasta_automacao\automacao.py"
    executar_arquivo_caminho(caminho_arquivo)
