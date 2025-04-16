# Verificação de Vales: Comparação de Datas entre Texto e Excel

Este projeto tem como objetivo automatizar a verificação de registros de vales de pagamento.  
Ele compara datas extraídas de textos (simulando dados de um PDF) com registros oficiais armazenados em planilhas Excel, garantindo que todos os lançamentos tenham correspondência.

---

## 💡 Como Funciona

O script realiza 3 etapas principais:

1. **Extração de Dados do Texto:**  
   - Lê um texto formatado (simulando dados coletados de um PDF).
   - Extrai número de matrícula e datas vinculadas.
   - Converte em um DataFrame estruturado.

2. **Carregamento de Dados do Excel:**  
   - Lê todas as planilhas de um arquivo `.xls`
   - Limpa e formata as colunas de datas.
   - Consolida os dados num único DataFrame.

3. **Verificação de Correspondência:**  
   - Compara os registros extraídos do texto com a base Excel.
   - Exibe no terminal quais dados do texto não foram localizados no Excel.

---
