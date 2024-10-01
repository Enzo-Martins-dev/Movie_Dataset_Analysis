import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('df_tratado')

def categoria_decada():
    df['Decade'] = (df['Release year'] // 10) * 10

    min_decade = int(df['Decade'].min())
    max_decade = int(df['Decade'].max())
    selected_decades = st.slider('Selecione o período (décadas)', min_decade, max_decade, (min_decade, max_decade), step=10)

    filtered_df = df[(df['Decade'] >= selected_decades[0]) & (df['Decade'] <= selected_decades[1])]

    decade_genero_counts = filtered_df.groupby(['Decade', 'Genre']).size().unstack(fill_value=0)
    decade_genero_counts['Total'] = decade_genero_counts.sum(axis=1)

    for category in decade_genero_counts.columns:
        if category != 'Total':
            decade_genero_counts[category] = ((decade_genero_counts[category] / decade_genero_counts['Total']) * 100)
            decade_genero_counts[category] = decade_genero_counts[category].round(2)

    decade_genero_counts = decade_genero_counts.drop(columns=['Total'])
            

    st.write(f"### Porcentagem de Filmes lançados de {selected_decades[0]} até {selected_decades[1]}, por gênero")
    st.dataframe(decade_genero_counts)

    plt.figure(figsize=(12, 6))
    sns.heatmap(decade_genero_counts, annot=True, fmt='.2f', cmap='Blues', cbar_kws={'label': 'Número de filmes'}, linewidths=0.5, linecolor='black')
    plt.title(f"Porcentagem de Filmes lançados de {selected_decades[0]} até {selected_decades[1]}, por gênero")
    plt.xlabel("Gênero")
    plt.ylabel("Década")
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()

    st.pyplot(plt)
    plt.close()

categoria_decada()

def nota_faturamento_dist():
    '''
    Plotar Gráfico que mostre a relação entre nota IMDb do filme e seu faturamento.
    Aceitar filtro para mostrar apenas elementos com nota e/ou faturamento entre x e y.

    Pode mostrar tanto individualmente quando por nota média.
    
    nota_min = st.text_input('Digite a nota mínima', 0, len(df['IMDb score'].max()))
    nota_max = st.text_input('Digite a nota máxima', 0, len(df['IMDb score'].max()))
    faturamento_min = st.text_input('Digite o faturamento mínimo', 0, len(df['Earnings'].max()))
    faturamento_max = st.text_input('Digite o faturamento máximo', 0, len(df['Earnings'].max()))
    '''
    
    st.write('Gráfico de relação entre nota IMDb e faturamento')

    nota_min = float(st.text_input('Digite a nota mínima', 0, 4, key='nota_min_dist'))
    nota_max = float(st.text_input('Digite a nota máxima', 0, 4, key='nota_max_dist'))
    faturamento_min = float(st.text_input('Digite o faturamento mínimo', 0, 12, key='faturamento_min_dist'))
    faturamento_max = float(st.text_input('Digite o faturamento máximo', 0, 12, key='faturamento_max_dist'))

    df_filtrado = df[(df['IMDb score'] >= nota_min) & (df['IMDb score'] <= nota_max)
                     & (df['Earnings'] >= faturamento_min) & (df['Earnings'] <= faturamento_max)]

    sns.set_theme(style='darkgrid')

    grafico_nota_faturamento = sns.relplot(
        data = df_filtrado,
        x = 'IMDb score',
        y = 'Earnings',
    )

    grafico_nota_faturamento.set(xlabel='Nota IMDb', ylabel='Faturamento')
    
    st.pyplot(plt)
    plt.close()

nota_faturamento_dist()


def nota_faturamento_media():
    st.write('Gráfico com média de faturamento por grupo de nota IMDb')

    nota_min = float(st.text_input('Digite a nota mínima', 0, 4, key='nota_min_media'))
    nota_max = float(st.text_input('Digite a nota máxima', 0, 4, key='nota_max_media'))
    faturamento_min = float(st.text_input('Digite o faturamento mínimo', 0, 12, key='faturamento_min_media'))
    faturamento_max = float(st.text_input('Digite o faturamento máximo', 0, 12, key='faturamento_max_media'))

    df_filtrado_novo = df[(df['IMDb score'] >= nota_min) & (df['IMDb score'] <= nota_max)
                     & (df['Earnings'] >= faturamento_min) & (df['Earnings'] <= faturamento_max)]
    
    bins = [i for i in range(0, 11)]
    labels = [f'{i}-{i+1}' for i in range(0,10)] 

    df_filtrado_novo['IMDb group'] = pd.cut(df_filtrado_novo['IMDb score'], bins = bins, labels = labels, include_lowest = True)
    
    df_filtrado_agrupado_media = df_filtrado_novo.groupby('IMDb group')['Earnings'].mean().reset_index()


    grafico_media_nota_faturamento = sns.barplot(
        data = df_filtrado_agrupado_media,
        x = 'IMDb group',
        y = 'Earnings'
    )

    grafico_media_nota_faturamento.set(xlabel = 'Nota IMDb', ylabel = 'Faturamento Médio')

    st.pyplot(plt)
    plt.close()
    


nota_faturamento_media()


def duracao_genero():
    duracao_minima = int(df['Running time'].min())
    duracao_maxima = int(df['Running time'].max())
    selected = st.slider('Duração do Filme', duracao_minima, duracao_maxima, (duracao_maxima, duracao_minima))
    duracao_minima = selected[0]
    duracao_maxima = selected[1]

    st.text(f'Duração média de filmes por gênero')

    df_filtrado = df.loc[(df['Running time'] >= duracao_minima) & (df['Running time'] <= duracao_maxima)]
    df_filtrado_agrupado = df_filtrado.groupby('Genre')['Running time'] 

    df_filtrado['Genre'] = df['Genre'].apply(lambda x: x[:2])

    values = df_filtrado['Running time']
    labels = df_filtrado['Genre']

    sns.violinplot(
        data=df_filtrado,
        x='Genre',
        y='Running time',
        inner='quartile'
    )

    #plt.show()
    st.pyplot(plt)
    plt.close() 


duracao_genero()



def lucro_por_numero_premiacoes():
    return 0