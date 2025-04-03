import os
import re
import sys
import subprocess
import zipfile
from urllib.parse import urljoin

def verificar_instalacao_bibliotecas():
    bibliotecas_necessarias = [
        'requests',
        'beautifulsoup4',
    ]
    
    faltando = []
    for biblioteca in bibliotecas_necessarias:
        try:
            __import__(biblioteca)
        except ImportError:
            faltando.append(biblioteca)
    
    if faltando:
        print("\nVerificando bibliotecas necessárias...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *faltando])
            print("\nBibliotecas instaladas com sucesso!")
        except Exception as e:
            print(f"\nErro ao instalar bibliotecas: {str(e)}")
            print("Por favor, instale manualmente com:")
            print(f"pip install {' '.join(faltando)}")
            return False
    return True

def download_ans_anexos():
    if not verificar_instalacao_bibliotecas():
        return False

    import requests
    from bs4 import BeautifulSoup

    url_base = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    pasta_downloads = "anexos_ans"
    arquivo_zip = "anexos_ans.zip"

    padroes_anexos = [
        r'Anexo I(?!\w)',
        r'Anexo II(?!\w)'
    ]
    
    os.makedirs(pasta_downloads, exist_ok=True)
    
    try:
        print(f"\nAcessando o site: {url_base}")
        response = requests.get(url_base, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        links_pdf = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            texto_link = link.get_text().strip()
            
            if not href.lower().endswith('.pdf'):
                continue
                
            for padrao in padroes_anexos:
                if (re.search(padrao, texto_link) or (re.search(padrao, href, re.IGNORECASE))):
                    absolute_url = urljoin(url_base, href)
                    if absolute_url not in links_pdf:
                        links_pdf.append(absolute_url)
        
        if not links_pdf:
            print("Nenhum link para Anexo I ou Anexo II encontrado.")
            return False
        
        arquivos_baixados = []
        for pdf_url in links_pdf:
            try:
                nome_arquivo = os.path.join(pasta_downloads, os.path.basename(pdf_url))
                print(f"\nBaixando: {pdf_url}")
                
                with requests.get(pdf_url, stream=True, timeout=10) as r:
                    r.raise_for_status()
                    with open(nome_arquivo, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                
                arquivos_baixados.append(nome_arquivo)
                print(f"Arquivo salvo como: {nome_arquivo}")
                
            except Exception as e:
                print(f"Erro ao baixar {pdf_url}: {str(e)}")
                continue
        
        if not arquivos_baixados:
            print("Nenhum arquivo foi baixado.")
            return False

        print(f"\nCriando arquivo compactado: {arquivo_zip}")
        with zipfile.ZipFile(arquivo_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for arquivo in arquivos_baixados:
                zipf.write(arquivo, os.path.basename(arquivo))
    
        print("\nProcesso concluído com sucesso!")
        print(f"Arquivos baixados: {len(arquivos_baixados)}")
        print(f"Arquivo ZIP criado em: {os.path.abspath(arquivo_zip)}")
        return True
    
    except Exception as e:
        print(f"\nOcorreu um erro: {str(e)}")
        return False

if __name__ == "__main__":
    download_ans_anexos()