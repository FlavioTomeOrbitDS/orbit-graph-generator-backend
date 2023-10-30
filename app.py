from flask import Flask, request, jsonify, send_file
import pandas as pd
import numpy as np

from flask_cors import CORS


'''The code then uses these functions to read an Excel file, create a matrix DataFrame,
    populate the matrix DataFrame with mentions, remove mirror values from the matrix,
    and save the final DataFrame to an Excel file.

1. readExcelFile(filename) - reads an Excel file and returns a refactored pandas DataFrame.
2. createMatrixDataframe(dataframe) - creates an empty pandas DataFrame with column and index labels from a given DataFrame.
3. populateMatrix(df1, matrixDataframe) - populates a given pandas DataFrame with mentions from another pandas DataFrame.
'''
import pandas as pd

def readCsv(filename):
    
    df = pd.read_csv(filename,sep=',')
    df.fillna(0, inplace=True)
    
    return df

def createMatrixDataframe(dataframe):
    df_matrix = pd.DataFrame(columns=dataframe.columns,
                             index=dataframe.columns)

    df_matrix.fillna(0, inplace=True)
    return df_matrix


def populateMatrix(df1, matrixDataframe):
    for index, row in df1.iterrows():
        #print("Row:", index)
        if (row == 1).any():
            # linha da matriz principal que possui alguma menção
            lista = list(row[row == 1].index)
            #print("Columns:", lista)
            for i in lista:
                for j in lista:
                    matrixDataframe.loc[i, j] += 1


def remove_mirror_values(matrix):
    import numpy as np

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

def exportAsExcel(dataframe):
    import datetime


    # Obtenha a data e hora atual
    agora = datetime.datetime.now()

    # Formate a data e hora como uma string
    agora_str = agora.strftime("%d%m%Y_%H%M")

    # Imprima a string formatada
    print(agora_str)

    dataframe.to_excel('results/result_'+agora_str+'.xlsx')

#*****************************************************************************************
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}},
     methods={"POST", "GET"}, supports_credentials=True)

#***************************** ROUTES *****************************************************
@app.route("/upload", methods=['POST'])
def upload():
  
  file = request.files['file']
  
  df= pd.read_csv(file, sep=';')  
  print(df)
  return jsonify("arquivo recebido!")


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
    # lê os dados
    file = request.files['file']
    df = readCsv(file)
    # cria a matrix
    print("criando a matriz")
    matrixDf = createMatrixDataframe(df)
    # insere os dados de menções na matriz
    populateMatrix(df, matrixDf)
    print("gerando os resultados")
    final_df = remove_mirror_values(matrixDf)
    
    print("enviando os dados...")
    # Salvar o DataFrame em um arquivo Excel
    writer = pd.ExcelWriter('dados.xlsx', engine='xlsxwriter')
    final_df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.close()
    return send_file('dados.xlsx', as_attachment=True)
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)


# @app.route("/api/generateGraphData", methods=['POST', 'GET'])
# def generateGraphData():
#     import itertools

#     file = request.files['file']
#     df= pd.read_csv(file, sep=';')   
    
#     print("gerando resultados")
#     combs = list(itertools.combinations(df.columns, 2))
#     df2 = pd.DataFrame(columns=['A', 'B', 'total'])

#     for comb in combs:
#         # Calculate the total number of rows where both columns have a value of 1
#         total = df[(df[comb[0]] == 1) & (df[comb[1]] == 1)].shape[0]
        
#         # Create a new DataFrame with the results for this combination of columns
#         new_df = pd.DataFrame({'A': [comb[0]], 'B': [comb[1]], 'total': [total]})
        
#         # Append the new DataFrame to the existing DataFrame
#         df2 = pd.concat([df2, new_df], ignore_index=True)


#     df2 = df2[df2.total != 0]
#     print(df2)
#     # Salvar o DataFrame em um arquivo Excel
#     writer = pd.ExcelWriter('dados.xlsx', engine='xlsxwriter')
#     df2.to_excel(writer, sheet_name='Sheet1', index=False)
#     writer.close()
#     return send_file('dados.xlsx', as_attachment=True)


@app.route("/readspreadsheet", methods=['POST', 'GET'])
def readspreadsheet():

    json_file = r"C:\Users\flavi\Downloads\orbit-web-apps-hub-970cecfcb810.json"
    worksheet = 'Página1'
    sheet_name = 'teste'
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1ofmrhncmRWHQDrgzux7TQK5kkvWPY2lG8p8amOS5YCQ/edit#gid=0'
    spreadsheet_key = '1ofmrhncmRWHQDrgzux7TQK5kkvWPY2lG8p8amOS5YCQ'
    
    return jsonify("Hello spreadsheet")
