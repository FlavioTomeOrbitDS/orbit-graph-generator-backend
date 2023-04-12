from flask import Flask, request, jsonify, send_file
import pandas as pd
import numpy as np

from flask_cors import CORS


#*****************************************************************************************
def createMatrixDataframe(dataframe):
    ''''
    1. Cria um dataframe do tipo matriz onde as linhas e as colunas são as columas do dataframe
    informado como argumento da função;
    
    2. Preenche todos os valores de linhas e colunas com 0;
    '''
    df_matrix = pd.DataFrame(columns=dataframe.columns,
                             index=dataframe.columns)

    df_matrix.fillna(0, inplace=True)

    return df_matrix

#*****************************************************************************************
def populateMatrix(df1, matrixDataframe):
    '''
    1. Preenche a matriz com os valores correlacionados em df1;
    
    2. A função começa com um loop for que itera sobre cada linha do DataFrame df1.
    
    3. Para cada linha, ele verifica se a linha contém pelo menos um valor igual a 1 usando o
        método any() do pandas.
        
    4. Se a linha contém pelo menos um valor igual a 1, ele cria uma lista chamada lista contendo
        as colunas que possuem valor 1 na linha atual.

    '''
    for index, row in df1.iterrows():
        #print("Row:", index)
        if (row == 1).any():
            # linha da matriz principal que possui alguma menção
            lista = list(row[row == 1].index)
            #print("Columns:", lista)
            for i in lista:
                for j in lista:
                    try:
                        matrixDataframe.loc[i, j] += 1
                    except:
                        continue

#*****************************************************************************************
def remove_mirror_values(matrix):
    '''
    1. O código define uma função chamada remove_mirror_values que recebe um objeto matrix e retorna
        um objeto DataFrame com os valores abaixo da diagonal principal da matriz original, excluindo
        valores espelhados.

    2. A primeira linha de código importa a biblioteca NumPy. Em seguida, ele usa a função np.tril do
        NumPy para obter somente os valores à esquerda da diagonal principal da matriz, com um deslocamento
        k=-1. Os valores à direita da diagonal principal são espelhados, então estamos ignorando esses valores.

    3. A partir do array de valores à esquerda da diagonal principal, o código cria um novo DataFrame chamado 
        left_values_df e o converte em um DataFrame de pares com a função stack(). Em seguida, ele renomeia as colunas
        do DataFrame resultante para 'A', 'B' e 'TOTAL'.

    4. O próximo passo é filtrar os valores do DataFrame resultante, removendo quaisquer valores com um total igual a zero
        ou onde o valor 'A' é igual ao valor 'B'.

    5. O código então converte o valor 'A' de cada linha em um rótulo de coluna, usando a lista de colunas da matriz original.

    6. Por fim, a função retorna o DataFrame resultante com os valores abaixo da diagonal principal da matriz original,
        sem valores espelhados.

    7. Em resumo, essa função remove os valores espelhados da matriz e retorna uma lista de pares de colunas com seus 
        respectivos valores abaixo da diagonal principal.
    '''
    # Obtenha somente os valores à esquerda da diagonal principal
    left_values = np.tril(matrix, k=-1)

    left_values_df = pd.DataFrame(left_values)
    # Visualize os valores à esquerda da diagonal principal
    # print(df_esquerda)

    result_df = left_values_df.stack().reset_index()
    result_df.columns = ['A', 'B', 'TOTAL']

    result_df = result_df[result_df['TOTAL'] != 0]
    result_df = result_df[result_df['A'] != result_df['B']]
    # result_df.to_excel("results/resultado3.xlsx")
    result_df.reset_index(inplace=True)
    result_df['A'] = result_df['A'].astype(str)

    columns_list = matrix.columns

    for index, row in result_df.iterrows():
        labelA = columns_list[int(row['A'])]
        labelB = columns_list[int(row['B'])]
        result_df.at[index, 'A'] = labelA
        result_df.at[index, 'B'] = labelB

    return result_df

#*****************************************************************************************
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}},
     methods={"POST", "GET"}, supports_credentials=True)

#***************************** ROUTES *****************************************************
@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/teste", methods=['POST', 'GET'])
def teste():
    return jsonify("Hello TESTE")


@app.route("/api/download", methods=['POST', 'GET'])
def download():
    '''
    1. O código define uma rota Flask chamada download que é acessada por um método HTTP GET ou POST.
        Essa rota recebe um JSON de dados na requisição e processa esses dados para gerar um arquivo Excel
        com os resultados.

    2. A primeira linha da função exibe uma mensagem "inciando o processo!!" na saída padrão.

    3. Em seguida, o código obtém o JSON de dados da solicitação HTTP usando a função request.get_json().
        Ele cria um DataFrame Pandas a partir dos dados do JSON e exclui a primeira linha do DataFrame 
        (que contém os nomes das colunas).

    4. A função então chama a função createMatrixDataframe para criar uma nova matriz DataFrame com base no
        DataFrame original.

    5. Em seguida, ele chama a função populateMatrix para preencher a matriz com valores apropriados com base no
        DataFrame original.

    6. Depois disso, ele chama a função remove_mirror_values para remover valores espelhados da matriz e retornar
        um DataFrame final com as informações necessárias.

    7. O código então cria um arquivo Excel com o DataFrame final usando a biblioteca xlsxwriter.
        O arquivo Excel é chamado de 'dados.xlsx' e é enviado para o usuário como um anexo por meio da função send_file().
    '''
    print("inciando o processo!!")
    # print("Carregando dados...")
    json_data = request.get_json()
    # print(json_data)
    df = pd.DataFrame(json_data, columns=json_data[0])
    df = df.drop(df.index[0])
    #print(df)
    #df.to_excel("originaldf.xlsx")
    df.drop_duplicates(inplace=True)
    print("Gerando matriz...")
    matrix_df = createMatrixDataframe(df)
    #print(matrix_df)
    #matrix_df.to_excel("matriz.xlsx")
    
    print("Populate matrix")    
    populateMatrix(df, matrix_df)
    
    print("Remove Mirror")
    final_df = remove_mirror_values(matrix_df)
    print(final_df)

    print("enviando os dados...")
    # Salvar o DataFrame em um arquivo Excel
    writer = pd.ExcelWriter('dados.xlsx', engine='xlsxwriter')
    final_df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.close()
    return send_file('dados.xlsx', as_attachment=True)
    #return jsonify("teste")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

