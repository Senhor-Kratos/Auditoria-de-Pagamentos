# Verificação de Vales — Auditoria de Pagamentos com Python 🧾

<p align="justify">
Este projeto foi criado para automatizar a conferência de registros de vales de pagamento, comparando dados extraídos de relatórios de texto (PDFs) com planilhas Excel. Focado em reforçar a consistência de dados em processos administrativos e financeiros de forma simples e eficiente com Python.
</p>

## 💡 Como Funciona

O script executa três etapas principais:

1️⃣ **Extração de Dados do Texto:**  
- Interpreta um texto com padrão fixo (muito comum após extração manual de PDFs).
- Isola matrículas e datas.
- Estrutura em DataFrame para análise.

2️⃣ **Carregamento dos Dados do Excel:**  
- Lê todas as planilhas de um arquivo `.xls`.
- Converte a coluna `DATA` para formato `datetime`.
- Organiza em DataFrame consolidado.

3️⃣ **Verificação de Correspondência:**  
- Compara os dados do texto com os dados do Excel.
- Exibe quais registros do texto **não constam** no Excel.
- Mensagem clara no terminal sobre a consistência dos dados.
