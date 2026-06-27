import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Buscando os dados e criando filtros
try:
    # obtendo dados
    print('Obtendo dados...')
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'
    
    # criando df e ajustando nomeclaturas
    df_recuperacao_veiculos = pd.read_csv(ENDERECO_DADOS, sep=";", encoding="iso-8859-1")

    # delimitando variáveis
    df_recuperacao_veiculos = df_recuperacao_veiculos[['recuperacao_veiculos', 'cisp',]]

    # agrupando
    df_recuperacao_veiculos = df_recuperacao_veiculos.groupby('cisp', as_index=False)['recuperacao_veiculos'].sum()

    #organizado
    df_recuperacao_veiculos = df_recuperacao_veiculos.sort_values(by='recuperacao_veiculos', ascending=False) 

except Exception as e:
    print(f'Erro ao carregar dados: {e}')

# Calculando Medidas
try:
    array_recuperacao_veiculos = np.array(df_recuperacao_veiculos['recuperacao_veiculos'])

    media = np.mean(array_recuperacao_veiculos)
    mediana = np.median(array_recuperacao_veiculos)
    distancia = abs((media - mediana)/mediana)
    q1=np.quantile(array_recuperacao_veiculos, 0.25)
    q3=np.quantile(array_recuperacao_veiculos, 0.75)
    maximo = np.max(array_recuperacao_veiculos)
    minimo = np.min(array_recuperacao_veiculos)
    amplitude = maximo - minimo
    iqr = q3 - q1
    limite_inferior = q1 - (1.5 * iqr)
    limite_superior = q3 + (1.5 * iqr)
    assimetria = df_recuperacao_veiculos['recuperacao_veiculos'].skew()
    curtose = df_recuperacao_veiculos['recuperacao_veiculos'].kurtosis()
    variancia = np.var(array_recuperacao_veiculos)
    distancia_variancia = variancia / (media**2)
    desvio_padrao = np.std(array_recuperacao_veiculos)
    coef_variacao = desvio_padrao / media
    df_menores_recuperacoes = df_recuperacao_veiculos[df_recuperacao_veiculos['recuperacao_veiculos']]<q1
    df_maiores_recuperacoes = df_recuperacao_veiculos[df_recuperacao_veiculos['recuperacao_veiculos']]>q3
    
except Exception as e:
    print(f"Erro ao calcular medidas: {e}")

# Mostrando as medidas para analise
try:
    print("\nMedidas - KPI")
    print(f'Média: {media:.0f}')
    print(f'Mediana: {mediana:.0f}')
    print(f'Distância: {distancia:.0%}')
    print(f'O fato da média estar muito maior que a mediana sugere que não há padrão nos dados.\n'
          f'Os dados são assimetricos portanto a média não poderá ser considerada como referência\n'      
          f'A distância entre média e mediana é de 137% confirmando a assimetria dos dados'
          f'Valores extremos podem estar puxando os números pra cima'
          )

    print('\nQuartis')
    print(f'Q1 = {q1:.0f}')
    print(f'Q2 ou Mediana = {mediana:.0f}')
    print(f'Q3 = {q3:.0f}')
    print(f'Q1 indica que 25% das recuperações de veículo tem números até 394'
          f'Enquanto 25% tem números superiores a 5425'          
          )

    print(f'\nMunípios que Menos Recuperam Veículos')
    print(df_menores_recuperacoes.sort_values(by='recuperacao_veiculos', ascending=True).head(10))

    print(f'\nMunípios que Mais Recuperam Veículos')
    print(df_maiores_recuperacoes.sort_values(by='recuperacao_veiculos', ascending=False).head(10))


except Exception as e:
    print(f'Erro ao demonstrar quartis: {e}')

try:
    print('\nMedidas de Dispersão')
    print(f'Maior Valor: {maximo}')
    print(f'Menor Valor: {minimo}')
    print(f'Amplitude Total: {amplitude}')
    print(f'A amplitude está mais próxima do valor máximo o que indica alta dispersão nos dados'
         )

except Exception as e:
    print(f'Erro ao demonstrar medidas de dispersão: {e}')

try:
    df_outliers_superior = df_recuperacao_veiculos.loc[df_recuperacao_veiculos['recuperacao_veiculos'] > limite_superior]
    df_outliers_inferior = df_recuperacao_veiculos.loc[df_recuperacao_veiculos['recuperacao_veiculos'] < limite_inferior]

    print(f'\nCalculando Outliers')
    print(f'IQR: {iqr:.0f}')
    print(f'Limite Inferior: {limite_inferior:.0f}')
    print(f'Limite Superior: {limite_superior:.0f}')
    print(f'O limite inferior negativo indica que não há Outliers inferiores '
          f'enquanto todo valor acima de 13.136 é considerado Outliers Alto '
          f'O IQR indica que 5140 unidades estão entre 50% dos dados'
          )
    if len(df_outliers_inferior) == 0:
        print('Não há Outliers Inferiores')
    else:
        print(df_outliers_inferior.sort_values(by='recuperacao_veiculos', ascending=False).head(10))
    
    if len(df_outliers_superior) == 0:
        print('Não existem Outliers Superiores')
    else:
        print(df_outliers_superior.sort_values(by='recuperacao_veiculos', ascending=False).head(10))

    print(f'\nNota-se que 9 CISPs com volume de recuperação maior que o limite de 13.136'
          f'A existência de outliers superiores confirma a assimetria dos dados'
          )
except Exception as e:
    print(f'Erro ao calcular Outliers {e}')

try:
    print(f'Cálculo da Assimetria')
    print(f'Assimetria: {assimetria:.0f}')
    print(f'Assimetria calculada é de 3 indicando Assimetria Positva Alta,'
          f'\nonde os valores muito altos estão puxando a média pra cima.'
          f'\nA média maior que a mediana reafirma os dados assimetricos'
          f'\nGráfico possui a calda longa'
          )
except Exception as e:
    print(f'Erro ao demonstrar assimetria')


try:
    print(f'\nCálculo da Curtose')
    print(f'Curtose: {curtose:.0f}')
    print(f'Curtose de 8 indica que é Leptocúrtica com pico gráfico mais alto'
          f'\nMuitos valores estão concentrados próximos a média'
          f'\nA calda dos gráficos é mais pesada'
          )
except Exception as e:
    print(f'Erro ao demonstrar curtose:{e}')

try:
    print(f'\nCálculo de Variabilidade')
    print(f'Variância: {variancia:.0f}')
    print(f'Distância entre a Média e a Variância: {distancia_variancia:.0%}')
    print(f'Desvio Padrão: {desvio_padrao:.0f}')
    print(f'Coeficiente de Variação: {coef_variacao:.0%}')
    print(f'Desvio de 5.689 afastada da média que é de 3.820 indica que os dados'
          f'\nsão muito espalhados. O coeficiente de variação acima de 30% reafirma a dispersão'
          f'\nextrema. A distância é de 222% 2x maior que a média distorcendo toda a distribuição'
          )
except Exception as e:
    print(f'Erro ao demonstrar curtose:{e}')

try:
    plt.subplots(2,2, figsize=(22,12))

    # Posição1
    plt.subplot(2, 2, 1)
    plt.boxplot(array_recuperacao_veiculos, vert=False, showmeans=True)
    plt.title('BoxPlot - Recuperação de Veículos')

    # Posição 2
    plt.subplot(2, 2, 2)
    plt.text(0.1, 0.9, f'Média: {media:.0f}',fontsize=9)
    plt.text(0.1, 0.8, f'Distância: {distancia:.0%}',fontsize=9)
    plt.text(0.1, 0.7, f'Limite Inferior: {limite_inferior:.0f}',fontsize=9, color="red")
    plt.text(0.1, 0.6, f'Mínimo: {minimo:.0f}',fontsize=9)
    plt.text(0.1, 0.5, f'Q1: {q1:.0f}',fontsize=9)
    plt.text(0.1, 0.4, f'Mediana: {mediana:.0f}',fontsize=9)
    plt.text(0.1, 0.3, f'Q3: {q3:.0f}',fontsize=9)
    plt.text(0.1, 0.2, f'Limite Superior: {limite_superior:.0f}',fontsize=9)
    plt.text(0.1, 0.1, f'Máximo: {maximo:.0f}',fontsize=9)
    plt.text(0.1, 0.0, f'Amplitude Total: {amplitude:.0f}',fontsize=9)
    plt.text(0.5, 0.9, f'Assimetria: {assimetria:.0f}',fontsize=9)
    plt.text(0.5, 0.8, f'Curtose: {curtose:.0f}',fontsize=9)
    plt.text(0.5, 0.7, f'Variância: {variancia:.0f}',fontsize=9)
    plt.text(0.5, 0.6, f'Distância Variância: {distancia_variancia:.0%}',fontsize=9)
    plt.text(0.5, 0.5, f'Desvio Padrão: {desvio_padrao:.0f}',fontsize=9)
    plt.text(0.5, 0.4, f'Coeficiente de Variação: {coef_variacao:.0%}',fontsize=9)
    plt.axis('off')
    plt.title('Resumo Estatístico')


    # Posição 3 - Outliers Superiores
    plt.subplot(2, 2, 3)
    plt.bar(df_outliers_superior['cisp'].astype(str), df_outliers_superior['recuperacao_veiculos'], color='tomato')
    deslocamento = max(df_outliers_superior['recuperacao_veiculos']) * 0.01
    for i, valor in enumerate(df_outliers_superior['recuperacao_veiculos']):
            plt.text(
                i, #posição Y
                valor + deslocamento, #posição X
                f'{valor:,}',
                ha='center'
            )
    plt.title('Municípios c/ Outliers Superiores')

    # Posição 4 - Histograma
    plt.subplot(2, 2, 4)
    plt.hist(array_recuperacao_veiculos, bins=390)
    plt.axvline(media, color='green', linewidth=1, label='Média')
    plt.axvline(mediana, color='orange', linewidth=1, label='Mediana')
    plt.legend()

    contagens, limites = np.histogram(array_recuperacao_veiculos, bins=390)
    print('\nFaixas do Histoma')
    for i in range(len(contagens)):
        if contagens[i] > 0:
            print(f'Faixa {i+1} -'
            f' {limites[i]:.0f} até {limites[i+1]:.0f} => {contagens[i]} CISP'
            )
    print(f'O histograma confirma visualmente tudo que as métricas já indicavam:'
          f' distribuição extremamente assimétrica, com massa concentrada no início e uma cauda longa e esparsa.'
          f'Os gaps entre faixas (8, 10, 12, 25...) reforçam a descontinuidade dos dados — '
          f'não existe uma progressão suave, os valores saltam de forma irregular.')
    plt.tight_layout(pad=3.0) # Ajusta o layout

    plt.show()
     
except Exception as e:
    print(f'Erro ao gerar gráficos: {e}')