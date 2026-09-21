import os
import requests
import numpy as np
from numpy.linalg import norm
import pdfplumber

from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'comparacao/index.html')

def dezArquivos(request):
    return render(request, 'comparacao/dezArquivos.html')

def cincoArquivos(request):
    return render(request, 'comparacao/cincoArquivos.html')


HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/neuralmind/bert-base-portuguese-cased"
headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

def obter_embedding_api(texto):
    payload = {
        "inputs": texto,
        "options": {"wait_for_model": True}
    }
    
    response = requests.post(
        "https://api-inference.huggingface.co/models/neuralmind/bert-base-portuguese-cased",
        headers=headers,
        json=payload,
        timeout=30  
    )
    
    if response.status_code == 200:
        dados = response.json()
        arr = np.array(dados)
        if arr.ndim == 3:
            return arr.mean(axis=1).flatten()
        elif arr.ndim == 2:
            return arr.mean(axis=0)
        return arr.flatten()
    else:
        raise Exception(f"Erro na API HF (Status {response.status_code}): {response.text}")
    
def similaridade_cosseno(v1, v2):
        dot = np.dot(v1, v2)
        norma_v1 = norm(v1)
        norma_v2 = norm(v2)
        
        if norma_v1 == 0 or norma_v2 == 0:
            return 0.0
        
        return float(dot / (norma_v1 * norma_v2))
    
def comparar_textos(request):
        if request.method == 'POST' and request.FILES.getlist('arquivos'):
            arquivos = request.FILES.getlist('arquivos')
            
            textos = []
            nomes_arquivos = []
            
            for f in arquivos:
                nomes_arquivos.append(f.name)
                if f.name.endswith('.txt'):
                    textos.append(f.read().decode('utf-8'))
                elif f.name.endswith('.pdf'):
                    with pdfplumber.open(f) as pdf:
                        texto_completo = "".join([page.extract_text() or "" for page in pdf.pages])
                        textos.append(texto_completo)
                        
            if len(textos) < 2:
                return JsonResponse({'error': 'Envie pelo menos 2 arquivos para comparação.'}, status=400)
            
            try:
                embeddings = [obter_embedding_api(txt) for txt in textos]
                
                anchor_embedding = embeddings[0]
                anchor_name = nomes_arquivos[0]
                
                resultados_similaridade = []

                for i in range(1, len(embeddings)):
                    sim = similaridade_cosseno(anchor_embedding, embeddings[i])
                    porcentagem = round(sim * 100, 2)

                    resultados_similaridade.append({
                        "ID": i,
                        "Artigo_Ancora": anchor_name[:40],
                        "Artigo_Comparado": nomes_arquivos[i][:40],
                        "Similaridade": f"{porcentagem}%"
                    })

                return JsonResponse({'resultados': resultados_similaridade})

            except Exception as e:
                return JsonResponse({'error': f"Erro no processamento: {str(e)}"}, status=500)
        
        return JsonResponse({'error': 'Método inválido ou arquivos não detectados.'}, status=400)  
                