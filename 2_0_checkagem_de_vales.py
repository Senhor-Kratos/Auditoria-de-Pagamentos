import pandas as pd
import re

texto = """

000001 / LEONARDO MARTINS 4
11/02/2025 15:10
12/02/2025 15:31
13/02/2025 14:55
15/02/2025 Afastamento Trabalhado
000003 / DEVYSON DIAS 3
13/02/2025 15:16
15/02/2025 15:08
15/02/2025 Afastamento Trabalhado
000008 / GRAZI MARTINS 2
10/02/2025 15:05
16/02/2025 Afastamento Trabalhado
000010 / JOHAN KOTARO 2
15/02/2025 15:17
15/02/2025 Afastamento Trabalhado
"""

# Regex para capturar Matrícula (formato: 000001 / Leonardo Martins)
matriculas = re.findall(r'(\d{6}) / [A-Za-z\s]+', texto)

# Regex para capturar as datas no formato dd/mm/aaaa
datas = re.findall(r'\d{2}/\d{2}/\d{4}', texto)

# Criar uma lista de dados para estruturação
dados_pdf = []

# Variáveis para controle
matricula_atual = None

# Iterar pelas linhas do texto e associar datas
for linha in texto.split('\n'):
    # Verificar se a linha é uma matrícula
    matricula_match = re.match(r'(\d{6}) / [A-Za-z\s]+', linha)
    if matricula_match:
        matricula_atual = matricula_match.group(1)  # Captura a matrícula
        matricula_atual_4dig = matricula_atual[2:]  # Remove os dois primeiros dígitos para 4 dígitos

    # Verificar se a linha contém uma data
    data_match = re.match(r'(\d{2}/\d{2}/\d{4})', linha)
    if data_match and matricula_atual:
        dados_pdf.append([matricula_atual_4dig, data_match.group(1)])  # Usar a matrícula formatada

# Criar DataFrame do PDF
df_pdf = pd.DataFrame(dados_pdf, columns=["Matrícula", "Data"])

# Converter a coluna 'Data' para datetime
df_pdf['Data'] = pd.to_datetime(df_pdf['Data'], format='%d/%m/%Y', errors='coerce')

# Adicionar a coluna 'Índice' para lidar com múltiplas entradas no mesmo dia
df_pdf['Índice'] = df_pdf.groupby(['Matrícula', 'Data']).cumcount()

print("Dados do PDF:")
print(df_pdf)

# Caminho do arquivo Excel
arquivo_excel = 'Multiconvênio Motorista 10_02_2025 à 16_02_2025.xls'  # Substitua pelo caminho correto do seu arquivo Excel

# Ler todas as planilhas do Excel
excel = pd.ExcelFile(arquivo_excel)

# Inicializar uma lista para armazenar os dados de todas as matrículas
dados_matriculas = []

# Iterar sobre todas as planilhas (exceto "Resumo" e "Base", que não contém dados de matrícula)
for sheet_name in excel.sheet_names:
    if sheet_name not in ['Resumo', 'Base']:  # Verifica se a planilha não é 'Resumo' nem 'Base'
        try:
            # Ler os dados da planilha de uma matrícula específica, pulando as primeiras 17 linhas
            df_matricula = pd.read_excel(arquivo_excel, sheet_name=sheet_name, skiprows=17)

            # Adicionar a coluna de Matrícula
            df_matricula['Matrícula'] = sheet_name  # Nome da planilha é a matrícula

            # Selecionar apenas a coluna de data e a coluna de matrícula
            df_matricula_dados = df_matricula[['DATA', 'Matrícula']]

            # Renomear a coluna 'DATA' para 'Data'
            df_matricula_dados = df_matricula_dados.rename(columns={'DATA': 'Data'})

            # Converter a coluna 'Data' para datetime, invalidando qualquer valor não conversível
            df_matricula_dados['Data'] = pd.to_datetime(df_matricula_dados['Data'], errors='coerce')

            # Remover as linhas onde a data é inválida (NaT, Not a Time)
            df_matricula_dados = df_matricula_dados.dropna(subset=['Data'])

            # Adicionar os dados dessa matrícula à lista de dados
            dados_matriculas.append(df_matricula_dados)
        except Exception as e:
            print(f"Erro ao processar a matrícula {sheet_name}: {e}")

# Concatenar os dados de todas as matrículas em um único DataFrame
df_completo = pd.concat(dados_matriculas, ignore_index=True)

# Adicionar a coluna de índice temporário (cumcount) ao df_completo
df_completo['Índice'] = df_completo.groupby(['Matrícula', 'Data']).cumcount()

# Exibir as primeiras linhas do DataFrame resultante
print(df_completo)

def verificar_conteudo(df_pdf, df_completo):
    # Fazer merge entre df_pdf e df_completo considerando 'Matrícula', 'Data' e 'Índice'
    merged = df_pdf.merge(
        df_completo,
        how='left',
        on=['Matrícula', 'Data', 'Índice'],
        indicator=True
    )

    # Filtrar as linhas que estão apenas no df_pdf
    apenas_no_df_pdf = merged[merged['_merge'] == 'left_only']

    if apenas_no_df_pdf.empty:
        print("Todos os dados do DataFrame PDF estão contidos no DataFrame Completo.")
    else:
        print("Os seguintes dados do DataFrame PDF não estão contidos no DataFrame Completo:")
        print(apenas_no_df_pdf[['Matrícula', 'Data', 'Índice']])

# Chamando a função para verificar os dados
verificar_conteudo(df_pdf, df_completo)

