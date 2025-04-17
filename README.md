# Verificação de Vales — Auditoria de Pagamentos com Python 🧾

<p align="justify">
Este projeto foi criado para automatizar a conferência de registros pagamentos de benefícios, comparando dados extraídos de relatórios de texto (PDFs) com planilhas Excel. Focado em reforçar a consistência de dados em processos administrativos e financeiros de forma simples e eficiente com Python.
</p>

## 🎯 Objetivo
- Garantir a integridade de dados entre planilhas e relatórios manuais.
- Automatizar processos de conferência para evitar erros humanos.
- Automação de tarefas repetitivas visando a maior produtividade do trabalho.


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

## Exemplo de Saída
- Caso todos os dados sejam encontrados:
``` 
✅ Todos os registros do PDF foram encontrados no Excel.
``` 
- Caso Haja Registros ausentes:
``` 
❌ Registros presentes no PDF que não constam no Excel:
   Matrícula       Data  Índice
9       0010 2025-02-15       0
10      0010 2025-02-15       1

```
