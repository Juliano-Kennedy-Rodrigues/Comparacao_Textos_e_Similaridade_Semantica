import tkinter as tk
from tkinter import filedialog 
from sentence_transformers import SentenceTransformer, util
import json
import os 

base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, "scielo.json")

with open(json_path, "r", encoding="utf-8") as f:
    file = json.load(f)
    
print(type(file))

#file é uma lista, e cada elemento da lista é um item do dicionário json do arquivo scielo.json
for item in file:
    item['Título'] = item['Título'].replace("Título: " , "")
    item['resumo'] = item['resumo'].replace("Introdução:", "")
   
    
#print(file[0]['resumo'])

resumos = [item["resumo"] for item in file]
#item['resumo']

#meu modelo pré treinado vai ser BERTimbau
model_name = 'neuralmind/bert-base-portuguese-cased'
model = SentenceTransformer(model_name)

print(range(len(resumos)))
embedding = model.encode(resumos, convert_to_tensor=True)
        
if file:
    for r in range(len(embedding)):
        for j in range(len(embedding)):
            similarity = util.cos_sim(embedding[r], embedding[j])
            percentage = similarity.item()*100
            print(f"\nÍndice de Correlação: artigo {r} e artigo {j} é de {percentage:.2f}%")
else:
    print("Arquivos não selecionados corretamente.")