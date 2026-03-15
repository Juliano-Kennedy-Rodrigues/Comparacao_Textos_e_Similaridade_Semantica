from sentence_transformers import SentenceTransformer, util
import os
import json

base_dir = os.path.dirname(os.path.abspath(__file__)) #caminho desse arquivo, até a pasta só
json_path = os.path.join(base_dir, "scielo.json")

with open(json_path, "r", encoding="utf-8") as f:
    file = json.load(f)

#modelos
original_model_link = 'neuralmind/bert-base-portuguese-cased'
tuned_model_path = './bertimbau_tuned_scielo_final'

original_model = SentenceTransformer(original_model_link)
tuned_model = SentenceTransformer(tuned_model_path)

#pegando na mão dois resumos parecidos do mesmo tema, vou pegar o de medicina que foi ancora e o que teve maior indice com ele
anchor_medicine = file[1]
best_match_medicine = file[10]

def testing(model, name):
    text1 = anchor_medicine['Título'] + " " + anchor_medicine['resumo']
    text2 = best_match_medicine['Título'] + " " + best_match_medicine['resumo']
    
    embedding1 = model.encode(text1, convert_to_tensor=True)
    embedding2 = model.encode(text2, convert_to_tensor=True)
    
    cos_sim = util.cos_sim(embedding1, embedding2).item() #mede similaridade do coss com os tensores gerados
    print(f"-> {name}: {cos_sim * 100:.2f}%")
    
print("\n--- Resultado da Similaridade ---")
testing(original_model, "Modelo Original (BERTimbau)")
testing(tuned_model, "Modelo Tunado (meu)")