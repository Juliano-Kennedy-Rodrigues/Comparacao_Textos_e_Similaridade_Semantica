from sentence_transformers import SentenceTransformer, util
import json
import os 
import pandas as pd
import table_maker as table_maker


base_dir = os.path.dirname(os.path.abspath(__file__)) #caminho desse arquivo, até a pasta só
json_path = os.path.join(base_dir, "scielo.json")

with open(json_path, "r", encoding="utf-8") as f:
    file = json.load(f)
    
#print(type(file))

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
    
#muitos artigos para comparar vai custar muito processamento e tempo, vou pegar 3 de 3 temas manualmente para ser base de comparação

results4_table = []

anchors = [1, 11, 27]
#anchor_medicine = 1
#anchor_science = 11
#anchor_politics = 27

for anc_index in anchors:
    #print(anc_index)
    #print(anchors)
    
    if anc_index == 1:
        anchor_tile = file[anc_index]['Título'][:45]
        anchor_embedding = embedding[anc_index]
    if anc_index == 11:
        anchor_tile = file[anc_index]['Título'][:53]
        anchor_embedding = embedding[anc_index]
    if anc_index == 27:
        anchor_tile = file[anc_index]['Título'][:46]
        anchor_embedding = embedding[anc_index]
    
    #vai medir a similaridade de uma ancora com todos os artigos e listar aquir
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
csv_path = os.path.join(base_dir, "ancoras_resultados.csv")
image_path = os.path.join(base_dir, "tabela_artigo.png")

#gera uma tabela csv
table = pd.concat(results4_table)  
table.to_csv(csv_path, index=False, encoding="utf-8-sig")
print("Tabela 'ancoras_resultados_tunados.csv' gerada")

img_tabela = table_maker.makeTable('projeto/ancoras_resultados.csv', 'projeto/resultados_imagens/')