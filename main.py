import tkinter as tk
from tkinter import filedialog 
from sentence_transformers import SentenceTransformer, util
from scraper import get_abstract

#abrindo janela de selecionar arquivos 
def select_file():
  path = filedialog.askopenfilename(title="Selecione um arquivo .txt", filetypes=[("Text files", "*.txt")]) 
  if path:
    with open(path,'r', encoding='utf-8') as f:
      return f.read()
  return None 


print("Selecione o primeiro arquivo:")
file1 = select_file()

print("Selecione o segundo arquivo:")
file2 = select_file()

#meu modelo pré treinado vai ser BERTimbau
model_name = 'neuralmind/bert-base-portuguese-cased'
model = SentenceTransformer(model_name)

#transforma txt em núemro e monta num array multidimensional 
if file1 and file2:
  embeddingf1 = model.encode(file1, convert_to_tensor=True)
  embeddingf2 = model.encode(file2, convert_to_tensor=True)

#similaridade é encontrada pelos cossenos https://www.ibm.com/br-pt/think/topics/cosine-similarity
#cos_sin usa tensor pra calcular "Computes the cosine similarity between two tensors.""
  similarity = util.cos_sim(embeddingf1, embeddingf2)

  percentage = similarity.item()*100

  print(f"\nÍndice de Correlação: {percentage:.2f}%")
else:
    print("Arquivos não selecionados corretamente.")



################################################
#meus_dados = get_abstract(num_paginas=2)