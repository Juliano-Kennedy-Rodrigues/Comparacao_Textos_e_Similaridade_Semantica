#FAZENDO SCRAPER, PREPARANDO INFOS PRO FINE TUNING 

import requests
from bs4 import BeautifulSoup
from langdetect import detect
import time


def get_papers(num_pages = 1):
    #scielo filtrado pro Brasil
    url = 'https://search.scielo.org/?fb=&where=&filter%5Bin%5D%5B%5D=scl'
    results = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    

    for page in range(1, num_pages + 1):
        print(f"Nessa página {page}")
        #https://search.scielo.org/?fb=&where=&filter%5Bin%5D%5B%5D=scl&from=16&page=2
        params = {
            'q': '*',
            'where': 'scl', #where=&filter%5Bin%5D%5B%5D=sc
            'from': (page-1)*15 + 1, #from é pq exibe 15 artigos por página
            'filter[in][]': 'scl'
        }
        
        #entra na pag e pega todo o html
        response = requests.get(url, params=params, headers=headers)
        html = BeautifulSoup(response.text, 'html.parser')                
            
        ##S0101-28002026000200303-scl > div.col-md-11.col-sm-10.col-xs-11 > div:nth-child(1) > a (classe da div é 'line')
            
        #pega o título que tem o link
        papers = BeautifulSoup.select('div.line a')
        
        for p in papers:
            ptTitle = p.get('tile') #o título em PORTUGUÊS está dentro do <a> no title
            
            #tento ver se tem título em pt, para garantir que não vai dar ruim no meu Bertimbau
            if not ptTitle:
                ptTitle = p.get_text(strip=True)

            try:
                if detect(ptTitle) == "pt":
                    paper_title = ptTitle
                    paper_url = p['href']

                    #pegar resumo
                    print(f"  -> Extraindo resumo de: {paper_title[:50]}...")
                    abstract = get_abstract(paper_url, headers) 
                
                    if (abstract):
                        results.append({"Título": paper_title, "resumo": abstract})
                    time.sleep(1.5)
                                        
                else:
                    #se o título não for em pt, pula
                    print(f"Pulando artigo em inglês: {ptTitle[:30]}...")
                    continue
            except:
                continue


def get_abstract(paper_url, headers):
    #articleText > div.articleSection.articleSection--resumo --> achei inspecionando com F12
    #links = html.select('div.articleSection articleSection--resumo')
    print()
    
    
    
    
    #fiz: entrei no site, peguei HTML, filtrei pela div, peguei o título em português, peguei o link e entrei no artigo
    #fazer: pegar a div com o RESUMO no artigo, que tem vários <p>. Juntar os <p> num texto só 
    #tento o resumo num texto só, posso chamar get_abstract para percorrer um n x de paginas e pegar varios resumo
    #aí uso eles para fazer fine tuning. Amanhã 22/02 farei o resto do scrapper. Aniversário do meu pai 21/02 bjs