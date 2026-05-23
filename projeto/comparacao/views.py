from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import pdfplumber
import os 
from sentence_transformers import SentenceTransformer, util

# Create your views here.
def index(request):
    return render(request, 'comparacao/index.html')

def dezArquivos(request):
    return render(request, 'comparacao/dezArquivos.html')

def cincoArquivos(request):
    return render(request, 'comparacao/cincoArquivos.html')


TUNED_MODEL_PATH = './bertimbau_tuned_scielo_final'

if os.path.exists(TUNED_MODEL_PATH):
    tuned_model = SentenceTransformer(TUNED_MODEL_PATH)
else:
    tuned_model = SentenceTransformer('neuralmind/bert-base-portuguese-cased')
    
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
                    texto_completo = "".join([page.extract_text() for page in pdf.pages])
                    textos.append(texto_completo)
                    
        if len(textos) < 2:
            return JsonResponse({'error': 'Envie pelo menos 2 arquivos para comparação.'}, status=400)
        
        embeddings = tuned_model.encode(textos, convert_to_tensor=True)
        
        anchor_embedding = embeddings[0]
        anchor_name = nomes_arquivos[0]
        
        resultados_similaridade = []

        for i in range(1, len(embeddings)):
            similarity_tensor = util.cos_sim(anchor_embedding, embeddings[i])
            
            porcentagem = round(similarity_tensor.item() * 100, 2)

            resultados_similaridade.append({
                "ID": i,
                "Artigo_Ancora": anchor_name[:40],       #
                "Artigo_Comparado": nomes_arquivos[i][:40],
                "Similaridade": f"{porcentagem}%"
            })

        return JsonResponse({'resultados': resultados_similaridade})
    
    return JsonResponse({'error': 'Método inválido ou arquivos não detectados.'}, status=400)