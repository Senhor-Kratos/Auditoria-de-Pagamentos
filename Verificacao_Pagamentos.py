import pandas as pd
import re

# Simulação de dados extraídos do PDF
texto = """
000001 / JOHAN KOTARO 4
11/02/2025
12/02/2025 
13/02/2025 
15/02/2025 
000003 / DEVYSON DIAS 3
13/02/2025 
15/02/2025 
15/02/2025 
000008 / GRAZI MARTINS 2
10/02/2025 
16/02/2025 
000010 / Leonardo Martins 2
15/02/2025 
15/02/2025 
"""

# Extração de matrículas e datas do texto
dados_pdf = []
matricula_atual = None

for linha in texto.split('\n'):
    matricula_match = re.match(r'(\d{6}) / [A-Za-z\s]+', linha)
    if matricula_match:
        matricula_atual = matricula_match.group(1)[2:]
    data_match = re.match(r'(\d{2}/\d{2}/\d{4})', linha)
    if data_match and matricula_atual:
        dados_pdf.append([matricula_atual, data_match.group(1)])

# DataFrame do conteúdo extraído do texto
df_pdf = pd.DataFrame(dados_pdf, columns=["Matrícula", "Data"])
df_pdf['Data'] = pd.to_datetime(df_pdf['Data'], format='%d/%m/%Y', errors='coerce')
df_pdf['Índice'] = df_pdf.groupby(['Matrícula', 'Data']).cumcount()

print("📄 Dados do PDF extraído:")
print(df_pdf)

# Caminho do arquivo Excel com dados de controle
arquivo_excel = 'Multiconvênio Motorista 10_02_2025 à 16_02_2025.xls'
excel = pd.ExcelFile(arquivo_excel)

dados_matriculas = []

# Processa cada planilha, exceto as de controle
for sheet_name in excel.sheet_names:
    if sheet_name not in ['Resumo', 'Base']:
        try:
            df_matricula = pd.read_excel(arquivo_excel, sheet_name=sheet_name, skiprows=17)
            df_matricula['Matrícula'] = sheet_name
            df_matricula = df_matricula.rename(columns={'DATA': 'Data'})
            df_matricula['Data'] = pd.to_datetime(df_matricula['Data'], errors='coerce')
            df_matricula = df_matricula.dropna(subset=['Data'])
            dados_matriculas.append(df_matricula[['Data', 'Matrícula']])
        except Exception as e:
            print(f"⚠️ Erro ao processar a planilha {sheet_name}: {e}")

# Consolidação de todas as planilhas num DataFrame único
df_completo = pd.concat(dados_matriculas, ignore_index=True)
df_completo['Índice'] = df_completo.groupby(['Matrícula', 'Data']).cumcount()

print("\n💾 Dados consolidados do Excel:")
print(df_completo)

# Função para comparar e listar registros faltantes
def verificar_conteudo(df_pdf, df_completo):
    merged = df_pdf.merge(df_completo, on=['Matrícula', 'Data', 'Índice'], how='left', indicator=True)
    apenas_no_pdf = merged[merged['_merge'] == 'left_only']

    if apenas_no_pdf.empty:
        print("\n✅ Todos os registros do PDF foram encontrados no Excel.")
    else:
        print("\n❌ Registros presentes no PDF que não constam no Excel:")
        print(apenas_no_pdf[['Matrícula', 'Data', 'Índice']])

# Executa a verificação
verificar_conteudo(df_pdf, df_completo)