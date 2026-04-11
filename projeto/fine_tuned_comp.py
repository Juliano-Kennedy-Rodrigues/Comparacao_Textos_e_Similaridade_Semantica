from sentence_transformers import SentenceTransformer, util
import json
import os 
import pandas as pd
import table_maker as table_maker


base_dir = os.path.dirname(os.path.abspath(__file__)) #caminho desse arquivo, até a pasta só
json_path = os.path.join(base_dir, "scielo.json")

with open(json_path, "r", encoding="utf-8") as f:
    file = json.load(f)
    
for item in file:
    item['Título'] = item['Título'].replace("Título: " , "")
    item['resumo'] = item['resumo'].replace("Introdução:", "")
   

resumos = [item["resumo"] for item in file]

#meu modelo treinado 
tuned_model_path = './bertimbau_tuned_scielo_final'
tuned_model = SentenceTransformer(tuned_model_path)

print(range(len(resumos)))
embedding = tuned_model.encode(resumos, convert_to_tensor=True)
    
results4_table = []

anchors = [1, 11, 27]

for anc_index in anchors:
    
    if anc_index == 1:
        anchor_tile = file[anc_index]['Título'][:45]
        anchor_embedding = embedding[anc_index]
    if anc_index == 11:
        anchor_tile = file[anc_index]['Título'][:53]
        anchor_embedding = embedding[anc_index]
    if anc_index == 27:
        anchor_tile = file[anc_index]['Título'][:46]
        anchor_embedding = embedding[anc_index]
    
    temp_similarity = []
    
    for i in range(len(embedding)):
            if i == anc_index: continue
            
            similarity = util.cos_sim(anchor_embedding, embedding[i]).item()
            
            temp_similarity.append({
                "ID": anchor_tile[:50],
                "Artigo Comparado": file[i]['Título'],
                "Similaridade": similarity
            })
            
    df_temp = pd.DataFrame(temp_similarity)
    
    
    top5 = df_temp.nlargest(5, 'Similaridade')
    bottom5 = df_temp.nsmallest(5, 'Similaridade')
    
    results4_table.append(top5)
    results4_table.append(bottom5)

#salvando na pasta certa
csv_path = os.path.join(base_dir, "resultados_treinamento.csv")

#gera uma tabela csv
table = pd.concat(results4_table)  
table.to_csv(csv_path, index=False, encoding="utf-8-sig")
print("Tabela 'resultados_treinamento.csv' gerada")


img_tabela = table_maker.makeTable('projeto/resultados_treinamento.csv', 'projeto/treinamento_imagens/')