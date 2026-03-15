#FAZENDO SCRAPER, PREPARANDO INFOS PRO FINE TUNING 

import json
import requests
from bs4 import BeautifulSoup
from langdetect import detect
import time
import os 

#salvando oq peguei do scielo num json para poder fazer fine tuning depois
def save_data(data, file_name="scielo.json"):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "scielo.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print('Salvou no json')
    except Exception as e:
        print(f"erro ao salvar {e}")


def get_papers(num_pages = 1):
    #scielo filtrado pro Brasil
    url = 'https://search.scielo.org/?fb=&q=*&lang=pt&where=&filter%5Bin%5D%5B%5D=scl&filter%5Bla%5D%5B%5D=pt&filter%5Btype%5D%5B%5D=research-article'
    results = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://www.google.com/'
    }
    

    for page in range(1, num_pages + 1):
        print(f"Nessa página {page}")
        #https://search.scielo.org/?fb=&where=&filter%5Bin%5D%5B%5D=scl&from=16&page=2
        params = {
            'q': '(ab:(PT))',
            'where': 'scl', #where=&filter%5Bin%5D%5B%5D=sc
            'from': (page-1)*15 + 1, #from é pq exibe 15 artigos por página
            'filter[in][]': 'scl'
        }
        
        #entra na pag e pega todo o html
        response = requests.get(url, params=params, headers=headers)
        html = BeautifulSoup(response.text, 'html.parser')  
        
        for social in html.select('.socialLinks, .articleShareLink'):
            social.decompose()      
        
        primeiro_link = html.select_one('.item .title') 
        if primeiro_link:
            print(f"O Python está vendo este primeiro: {primeiro_link.get_text()}")        
            
        ##S0101-28002026000200303-scl > div.col-md-11.col-sm-10.col-xs-11 > div:nth-child(1) > a (classe da div é 'line')
            
        #pega o título que tem o link
        
        #S0101-28002026000200301-scl > div.col-md-11.col-sm-10.col-xs-11
        #S0101-28002026000100304-scl > div.col-md-11.col-sm-10.col-xs-11
        
        #papers = html.select_one('.content .searchForm .container resultBlock .col-md-9 col-sm-8 .results .item  .line a')
        papers_list = html.select('.item .line a[href*="sci_arttext"]')
        print('coletou algo sim')

        for papers in papers_list:        
            paper_title = papers.get('title')
            paper_url = papers.get('href')

            not_this = ["Compartilhar Facebook", " Twitter", "Português", "Inglês", "Espanhol", "Francês"]
            if not paper_title or paper_title in not_this:
                continue
            
            try:
                if detect(paper_title) != 'pt':
                    continue
            except Exception as e: 
                print(e)
                continue

            print(f"Extraindo resumo de: {paper_title[:50]}...")
            abstract = get_abstract(paper_url, headers)
            
            if abstract:
                item = {"Título": paper_title, "resumo": abstract}
                results.append(item)
                save_data(results)
                time.sleep(2)
            else:
                print(f"error: Resumo não encontrado para: {paper_title[:30]}")

def get_abstract(paper_url, headers):  
    try:
        response = requests.get(paper_url, headers=headers)
        html = BeautifulSoup(response.text, 'html.parser')
        
    
        #articleText > div.articleSection.articleSection--resumo --> achei inspecionando com F12
        abstract_div = html.select_one('div.articleSection.articleSection--resumo')
        
        if not abstract_div:
            abstract_div = html.select_one('#resumo, #abstract')
        
        #se eu conseguir entrar na página e pegar a div com o RESUMO
        if abstract_div:
            #a div com o resumo tem vários <p> com os textos, vou juntar num texto só
            text = abstract_div.find_all('p')
            full_abstract = " ".join([t.get_text(strip=True) for t in text])
            return full_abstract
    except:
        return None
    return None
    
    