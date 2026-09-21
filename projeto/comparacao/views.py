import io
import numpy as np
from pypdf import PdfReader
from sklearn.metrics.pairwise import cosine_similarity
from huggingface_hub import InferenceClient
from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

client = InferenceClient(model="neuralmind/bert-base-portuguese-cased")

def index(request):
    return render(request, 'index.html')

def cincoArquivos(request):
    """Renderiza a página para comparação de até 5 arquivos."""
    return render(request, 'cincoArquivos.html')

def dezArquivos(request):
    """Renderiza a página para comparação de até 10 arquivos."""
    return render(request, 'dezArquivos.html')

def extrair_texto(arquivo):
    """Lê o conteúdo do arquivo enviado (.txt ou .pdf) e retorna como texto."""
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

@csrf_exempt
def obter_embedding(texto):
    """Obtém os embeddings do texto através da API de Inferência do Hugging Face."""
    texto_truncado = texto[:2000] if len(texto) > 2000 else texto
    
    response = client.feature_extraction(texto_truncado)
    
    embeddings = np.array(response)
    if embeddings.ndim == 3:
        
        embedding_medio = np.mean(embeddings[0], axis=0)
    elif embeddings.ndim == 2:
        embedding_medio = np.mean(embeddings, axis=0)
    else:
        embedding_medio = embeddings

    return embedding_medio.reshape(1, -1)

@csrf_exempt
def comparar(request):
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