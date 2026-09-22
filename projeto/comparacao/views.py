import os
import io
import requests
import numpy as np
from pypdf import PdfReader
from sklearn.metrics.pairwise import cosine_similarity
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from huggingface_hub import InferenceClient
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

API_URL = "https://router.huggingface.co/hf-inference/models/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Token configurado no Render
HF_TOKEN = os.getenv("HF_TOKEN")

# Sessão com retries automatizados
session = requests.Session()
retries = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)
session.mount('https://', HTTPAdapter(max_retries=retries))


# Views de Templates
def index(request):
    return render(request, 'comparacao/index.html')

def cincoArquivos(request):
    return render(request, 'comparacao/cincoArquivos.html')

def dezArquivos(request):
    return render(request, 'comparacao/dezArquivos.html')


# Funções Auxiliares
def extrair_texto(arquivo):
    nome = arquivo.name.lower()
    if nome.endswith('.pdf'):
        pdf_reader = PdfReader(io.BytesIO(arquivo.read()))
        texto = ""
        for page in pdf_reader.pages:
            texto += page.extract_text() or ""
        return texto
    else:
        conteudo = arquivo.read()
        try:
            return conteudo.decode('utf-8')
        except UnicodeDecodeError:
            return conteudo.decode('iso-8859-1', errors='ignore')


def obter_embedding(texto):
    texto_truncado = texto[:2000] if len(texto) > 2000 else texto
    
    # Inicializa o cliente oficial da Hugging Face
    client = InferenceClient(
        provider="hf-inference",
        api_key=HF_TOKEN
    )
    
    # Solicita a extração de recursos (embeddings)
    res = client.feature_extraction(
        texto_truncado,
        model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    
    embeddings = np.array(res)
    
    # Tratamento das dimensões do vetor de embeddings
    if embeddings.ndim == 3:
        embedding_medio = np.mean(embeddings[0], axis=0)
    elif embeddings.ndim == 2:
        embedding_medio = np.mean(embeddings, axis=0)
    else:
        embedding_medio = embeddings

    return embedding_medio.reshape(1, -1)

# View Principal de Comparação
@csrf_exempt
def comparar_textos(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

    arquivos = request.FILES.getlist('arquivos')

    if len(arquivos) < 2:
        return JsonResponse({'error': 'Envie pelo menos 2 arquivos.'}, status=400)

    try:
        arquivo_ancora = arquivos[0]
        texto_ancora = extrair_texto(arquivo_ancora)
        emb_ancora = obter_embedding(texto_ancora)

        resultados = []

        for arquivo_comp in arquivos[1:]:
            texto_comp = extrair_texto(arquivo_comp)
            emb_comp = obter_embedding(texto_comp)

            sim = cosine_similarity(emb_ancora, emb_comp)[0][0]

            resultados.append({
                'Artigo_Ancora': arquivo_ancora.name,
                'Artigo_Comparado': arquivo_comp.name,
                'Similaridade': f"{sim * 100:.2f}%"
            })

        return JsonResponse({'resultados': resultados})

    except Exception as e:
        return JsonResponse({'error': f"Erro no processamento: {str(e)}"}, status=500)