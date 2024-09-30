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

    decade_genre_counts = filtered_df.groupby(['Decade', 'Genre']).size().unstack(fill_value=0)

    st.write(f"### Quantidade de Filmes lançados de {selected_decades[0]} até {selected_decades[1]}, por gênero")
    st.dataframe(decade_genre_counts)

    plt.figure(figsize=(12, 6))
    sns.heatmap(decade_genre_counts, annot=True, fmt='d', cmap='Blues', cbar_kws={'label': 'Número de filmes'}, linewidths=0.5, linecolor='black')
    plt.title(f"Quantidade de Filmes lançados de {selected_decades[0]} até {selected_decades[1]}, por gênero")
    plt.xlabel("Gênero")
    plt.ylabel("Década")
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()

    st.pyplot(plt)

categoria_decada()

def nota_faturamento():
    '''Plotar Gráfico que mostre a relação entre nota IMDb do filme e seu faturamento.
    Aceitar filtro para mostrar apenas elementos com nota e/ou faturamento entre x e y.

    Pode mostrar tanto individualmente quando por nota média.
    
    nota_min = st.text_input('Digite a nota mínima', 0, len(df['IMDb score'].max()))
    nota_max = st.text_input('Digite a nota máxima', 0, len(df['IMDb score'].max()))
    faturamento_min = st.text_input('Digite o faturamento mínimo', 0, len(df['Earnings'].max()))
    faturamento_max = st.text_input('Digite o faturamento máximo', 0, len(df['Earnings'].max()))
    '''

    nota_min = float(st.text_input('Digite a nota mínima', 0, 4))
    nota_max = float(st.text_input('Digite a nota máxima', 0, 4))
    faturamento_min = float(st.text_input('Digite o faturamento mínimo', 0, 12))
    faturamento_max = float(st.text_input('Digite o faturamento máximo', 0, 12))

    df_filtrado = df[(df['IMDb score'] >= nota_min) & (df['IMDb score'] <= nota_max)
                     & (df['Earnings'] >= faturamento_min) & (df['Earnings'] <= faturamento_max)]

    sns.set_theme(style='darkgrid')

    grafico_nota_faturamento = sns.relplot(
        data = df_filtrado,
        x = 'IMDb score',
        y = 'Earnings',
    )

    grafico_nota_faturamento.set(xlabel='Nota IMDb', ylabel='Earnings (Em Milhões)')
    
    st.pyplot(plt)

nota_faturamento()