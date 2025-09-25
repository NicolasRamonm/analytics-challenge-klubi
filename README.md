# 🤖 Desafio - Análise de SalesOps

Bem-vindo(a) ao nosso desafio técnico! 🎯

Queremos avaliar como você pensa, estrutura código, manipula dados e apresenta análises. O foco é **simplicidade, clareza e qualidade do resultado final**.

## 🧠 Contexto

O time de **SalesOps** precisa consolidar dados de vendas e gerar um **relatório diário** para apoiar decisões do time de negócios.

Sua tarefa é criar uma aplicação em **Python** que faça a extração, transformação e carga (ETL) desses dados em uma ferramenta de **BI (Tableau)**, usando os arquivos CSV fornecidos como fonte.

Você pode escolher entre:

- **Script Python** simples que execute todo o ETL e produza um dashboard funcional no Tableau.

- **DAG do Apache Airflow**, com ambiente Docker, que orquestre a atualização diária dos dados e alimente um dashboard dinâmico no Tableau.

Seja criativo e funcional. Nem sempre o simples é o suficiente, ou o complexo é a melhor opção. A escolha é totalmente sua!

## 📁 Materiais Disponíveis

Forneceremos quatro arquivos `.csv` com os seguintes dados:
- **Vendas**
- **Clientes**
- **Produtos**
- **Parceiros**

## 🧪 Critérios de Avaliação

Sua solução será avaliada nos pontos abaixo:

1. **Ingestão**
- Criar um banco de dados **SQLite**.
- Desenvolver um script para carregar os CSV no banco.

2. **Modelagem dos Dados**
- Desenhar o modelo lógico com os relacionamentos entre as tabelas.

2. **Transformação**
- Implementar um script em Python para tratamento e criação de tabelas/views (joins, limpezas, etc.).

4. **Consultas SQL**
-  Fornecer um arquivo `.sql` com cálculos de **KPIs relevantes**, prontos para consulta.

5. **Dashboard no BI**
- Com os dados tratados, criar um **dashboard** no **Tableau** que exiba os principais indicadores.
- Sugestão: Use a trilha gratuita de Tableau: https://www.primecursos.com.br/tableau-completo

6. **Opcional**
- Criar uma imagem Docker com o **Apache Airflow** e orquestrar o processo via DAG, agendando a execução diária às **3h da manhã**.

## 🛠️ Requisitos Técnicos

• **Linguagem e execução:** Python 3.10+ rodando localmente (crie um ambiente virtual utilizando o `uv`). Opcional: Docker para empacotar o ambiente. Script único ou arquitetura modular com etapas claras.

• **Dados e armazenamento:** Leitura dos 4 CSVs fornecidos. Criação de um SQLite local com tabelas brutas e tabelas tratadas. Tipagem consistente (datas, numéricos, chaves). Remoção de duplicidades e nulos críticos (caso haja).

• **Modelagem e transformações:** diagrama lógico simples mostrando relacionamentos. Views ou tabelas derivadas para análises. Joins declarados ou idempotentes. Coluna de controle `row_updated_at`.

• **Consultas e KPIs:** Arquivo com consultas para, por exemplo: Receita, Vendas, Ticket Médio, Conversão, Cancelamento, % Pagto até vencimento. Cada KPI com comentário explicando a lógica.

• **BI (Tableau):** Dashboard com filtros. Mínimo: cards de KPIs e série temporal de receita/vendas. Entrega do `.twbx` ou instruções claras para conexão ao SQLite.

## 📦 Como entregar

1. **Repositório público no GitHub com seu projeto**.

2. **README** contendo:

• Passo a passo para rodar localmente e/ou via Docker.

• Como gerar o SQLite e conectar no Tableau.

• Prints ou GIF do dashboard em uso.

• Decisões técnicas e trade-offs.

• Limitações e próximos passos.

---

**_Se tiver qualquer dúvida durante o processo, sinta-se à vontade para perguntar. Boa sorte e divirta-se construindo! 🚀_**
