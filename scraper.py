#FAZENDO SCRAPER, PREPARANDO INFOS PRO FINE TUNING 

import json
import requests
from bs4 import BeautifulSoup
from langdetect import detect
import time

#salvando oq peguei do scielo num json para poder fazer fine tuning depois
def save_data(data, file_name="scielo.json"):
    try:
        with open(file_name, "w", encoding="utf-8") as f: #abro arquivo pra write
            json.dump(data, f, ensure_ascii=False, indent=4)
        print('Salvou no json')
    except Exception as e:
        print(f"erro ao salvar {e}")


def get_papers(num_pages = 1):
    #scielo filtrado pro Brasil
    url = 'https://search.scielo.org/?fb=&where=&filter%5Bin%5D%5B%5D=scl'
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
        papers = html.select('.item .line a')
        valid_papers = [p for p in papers if 'script=sci_arttext' in p.get('href', '')] #pega só os links que levam a um artigo, se tiver link de rede social, ou pesquisa, pula
        
        for vp in valid_papers:
            ptTitle = vp.get('title') #o título em PORTUGUÊS está dentro do <a> no title
            
            #tento ver se tem título em pt, para garantir que não vai dar ruim no meu Bertimbau
            if not ptTitle:
                ptTitle = vp.get_text(strip=True)
                
            if len(ptTitle) < 20: 
                continue

            try:
                if detect(ptTitle) == "pt":
                    paper_title = ptTitle
                    paper_url = vp['href']

                    #pegar resumo
                    print(f"  -> Extraindo resumo de: {paper_title[:50]}...")
                    abstract = get_abstract(paper_url, headers) 
                
                    if (abstract):
                        results.append({"Título": paper_title, "resumo": abstract})
                        print("COLETOU MSM")
                        time.sleep(2)
                        
                    if abstract:
                        item = {"Título": paper_title, "resumo": abstract}
                        results.append(item) #pego o titulo = o titulo em portigues e o resumo que peguei juntando os <p> 
                        save_data(results)
                        time.sleep(2) #pra não levar um ban cis s2
                                        
                else:
                    #se o título não for em pt, pula. Comentando pro terminal não ficar cheio
                    #print(f"Pulando artigo em inglês: {ptTitle[:30]}...")
                    pass
            except:
                continue
        

def get_abstract(paper_url, headers):  
    try:
        response = requests.get(paper_url, headers=headers)
        html = BeautifulSoup(response.text, 'html.parser')
    
        #articleText > div.articleSection.articleSection--resumo --> achei inspecionando com F12
        abstract_div = html.select_one('div.articleSection.articleSection--resumo')
        
        #se eu conseguir entrar na página e pegar a div com o RESUMO
        if abstract_div:
            #a div com o resumo tem vários <p> com os textos, vou juntar num texto só
            text = abstract_div.find_all('p')
            full_abstract = " ".join([t.get_text(strip=True) for t in text])
            return full_abstract
    except:
        return None
    return None
    
    