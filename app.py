import json
from flask import Flask,request, jsonify, send_file
import pandas as pd
import numpy as np
import io

from flask_cors import CORS


def download_excel():
    # cria um dataframe com alguns dados
    df = pd.DataFrame({'coluna_1': [1, 2, 3],
                       'coluna_2': ['a', 'b', 'c']})

    # cria um arquivo Excel a partir do dataframe
    output = pd.ExcelWriter('dados.xlsx')
    df.to_excel(output)
    output.save()

    # envia o arquivo Excel para o frontend
    return send_file('dados.xlsx', as_attachment=True)

def readExcelFile(filename):
    df   = pd.read_excel(filename)
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
    #print(agora_str)

    dataframe.to_excel('results/result_'+agora_str+'.xlsx')


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}},methods={"POST","GET"} , supports_credentials=True)


@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/teste", methods=['POST','GET'])
def teste():
    return jsonify("Hello TESTE")


@app.route("/iniciaupload", methods=['POST', 'GET'])
def upload():
    print("inciando o processo!!")
    
    # print("Carregando dados...")
    json_data = request.get_json()
    #print(json_data)
    df = pd.DataFrame(json_data, columns=json_data[0])
    df = df.drop(df.index[0])
    
    print("Gerando matriz...")
    matrix_df= createMatrixDataframe(df)
    populateMatrix(df, matrix_df)
    final_df = remove_mirror_values(matrix_df)
    
    print("exportando os dados...")
    output = pd.ExcelWriter('dados.xlsx')
    final_df.to_excel(output)
    output.close()

    # envia o arquivo Excel para o frontend
    data = {'name': 'John', 'age': 30}
    return jsonify(data)

        #print(final_df)
    




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
