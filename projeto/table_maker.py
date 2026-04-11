import pandas as pd
import matplotlib.pyplot as plt
import os

def makeTable (csv_path, output_dir):
    
    # Cria a pasta de saída se ela não existir
    os.makedirs(output_dir, exist_ok=True)

    # Carrega o DataFrame com os resultados do modelo tunado
    df = pd.read_csv(csv_path)

    col_ancora = 'ID' 
    col_texto = 'Artigo Comparado'  
    col_sim = 'Similaridade' 

    ancoras_unicas = df[col_ancora].unique()

    for i, ancora_nome in enumerate(ancoras_unicas, 1):
        print(f"Processando Âncora {i}: {ancora_nome}...")

        # Filtra o DataFrame apenas para a âncora atual
        df_ancora = df[df[col_ancora] == ancora_nome]

        df_sorted = df_ancora.sort_values(by=col_sim, ascending=False)

        # Pega Top 5 e Bottom 5
        top5 = df_sorted.head(5)
        btt5 = df_sorted.tail(5)

        #coloca na tabelah
        top5 = top5.copy()
        top5['Tipo'] = 'TOP 5'
        btt5 = btt5.copy()
        btt5['Tipo'] = 'BOTTOM 5'
        
        table_df = pd.concat([top5, btt5])
        
        table_final = table_df[['Tipo', col_texto, col_sim]]

        fig, ax = plt.subplots(figsize=(12, 6))  # Aumentei um pouco a largura
        ax.axis('off')
        
        titulo_ancora = (ancora_nome + '..') 
        ax.set_title(f'Resultados Extremos - Âncora {i}: {titulo_ancora}', fontsize=14, fontweight='bold', pad=20)

        # Cria a tabela
        tab = ax.table(
            cellText=table_final.values, 
            colLabels=table_final.columns, 
            loc='center', 
            cellLoc='left', # Alinhamento à esquerda para textos longos
            colWidths=[0.15, 0.7, 0.15] # Ajuste manual das larguras das colunas
        )
            
        table_final = table_df[['Tipo', col_texto, col_sim]].copy()
        table_final[col_sim] = table_final[col_sim].map('{:.4f}'.format)
        
        table_final[col_texto] = table_final[col_texto].apply(lambda x: (str(x)[:67] + '...') if len(str(x)) > 70 else str(x))
        
        tab = ax.table(
        cellText=table_final.values, 
        colLabels=table_final.columns, 
        loc='center', 
        cellLoc='left',
        colWidths=[0.15, 0.75, 0.15]
        ) 
        
        for (row, col), cell in tab.get_celld().items():
            if row == 0:
                cell.set_text_props(fontweight='bold', color='white')
                cell.set_facecolor("#747474") 
            elif row <= 5: # Linhas do Top 5 
                pass
            else: # Linhas do Bottom 5 
                pass

        image_name = f'tabela{i}.png'
        image_path = os.path.join(output_dir, image_name)
        
        plt.savefig(image_path, bbox_inches='tight', dpi=300)
        plt.close(fig) # Fecha a figura para liberar memória
        print(f"Imagem {image_name} salva com sucesso em {output_dir}")

    print("\n OK mo deu certo vai ver")