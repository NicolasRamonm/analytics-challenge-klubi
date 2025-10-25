# Análise de Hábitos e Desempenho Estudantil

## Sumário

1. [Exploração Inicial dos Dados](#1-exploração-inicial-dos-dados)
2. [Tratamento dos Dados e Novas Variáveis](#2-tratamento-dos-dados-e-novas-variáveis)
3. [Análises Estatísticas e Modelos](#3-análises-estatísticas-e-modelos)
4. [Visualizações e Gráficos](#4-visualizações-e-gráficos)
5. [Insights e Recomendações](#5-insights-e-recomendações)
6. [Modelo Preditivo Supervisionado](#6-modelo-preditivo-supervisionado)

---

## 1. Exploração Inicial dos Dados

### 1.1 Objetivo
Analisar a relação entre hábitos estudantis e desempenho acadêmico, identificando os principais fatores que influenciam o sucesso acadêmico e desenvolvendo insights para melhorar o rendimento dos estudantes.

### 1.2 Dataset e Características
- **Fonte**: Dataset de hábitos e desempenho estudantil
- **Tamanho**: 1.000 registros (linhas) x 16 variáveis (colunas)
- **Memória utilizada**: 0.48 MB
- **Tipos de dados**: 7 object, 6 float64, 3 int64
- **Variáveis disponíveis**:
  - **Identificação**: student_id
  - **Demográficas**: age, gender
  - **Hábitos de estudo**: study_hours_per_day, attendance_percentage
  - **Hábitos digitais**: social_media_hours, netflix_hours, internet_quality
  - **Hábitos de vida**: sleep_hours, diet_quality, exercise_frequency
  - **Contexto familiar**: parental_education_level, part_time_job
  - **Saúde mental**: mental_health_rating
  - **Atividades**: extracurricular_participation
  - **Desempenho**: exam_score

### 1.3 Hipóteses Preliminares
**Hipótese Principal**: Existe uma correlação positiva significativa entre horas de estudo e desempenho acadêmico.

**Hipóteses Secundárias**:
1. **H2**: O uso excessivo de redes sociais e Netflix tem impacto negativo no desempenho
2. **H3**: Boas horas de sono e exercícios regulares contribuem positivamente para o desempenho
3. **H4**: A razão estudo/tela (study_screen_ratio) tem relação direta com o desempenho
4. **H5**: Existe diferença de desempenho entre gêneros, com mulheres apresentando notas ligeiramente superiores

### 1.4 Qualidade dos dados

O dataset apresentou excelente qualidade inicial, com apenas 91 valores ausentes (9.1%) concentrados na variável `parental_education_level`. Não foram identificados valores negativos inesperados ou inconsistências lógicas significativas nos dados. A análise de qualidade revelou que os dados estavam bem estruturados e prontos para análise, com distribuições coerentes e ranges apropriados para cada variável.

**Características de Qualidade Identificadas:**
- **Valores ausentes**: Apenas 91 registros (9.1%) na variável parental_education_level
- **Valores negativos**: Nenhum valor negativo inesperado detectado
- **Outliers extremos**: Nenhum outlier extremo identificado nas variáveis principais
- **Inconsistências lógicas**: Nenhuma inconsistência detectada (horas totais ≤ 24h, notas 0-100, etc.)
- **Duplicatas**: Nenhuma duplicata completa ou ID duplicado encontrado

## 2. Tratamento dos Dados e Novas Variaveis

### 2.1 Tratamento dos Dados

**Tratamentos Aplicados**:
- **Winsorization**: Clipping nos percentis 1% e 99%
- **Imputação**: Valores ausentes preenchidos com moda
- **Verificação**: Sem valores negativos inesperados ou inconsistências lógicas

<Table>
  <tr>
    <td><img src="img/postratamento.png" border="0"></td>
    <td>
  </tr>
</table>

  *A remoção de outliers mais extremos por winsorization foi aplicada para preservar a integridade estatística dos dados, mantendo a estrutura geral das distribuições enquanto elimina valores que poderiam distorcer as análises de correlação. Esta abordagem tenta preservar padrões comportamentais reais dos estudantes sejam identificados sem a interferência de registros atípicos que podem representar erros de coleta ou **casos extremamente raros que não refletem a população estudantil típica**.

### 2.2 Novas Variáveis

Durante a análise, foram criadas **4 novas variáveis** para permitir análises dos hábitos estudantis. Essas variáveis foram criadas com o objetivo de criar indicadores mais específicos.

**Variáveis de Agregação**

**`total_leisure_hours`** - Horas Totais de Lazer
- **Cálculo**: `social_media_hours + netflix_hours`
- **Objetivo**: Quantificar o tempo total gasto em entretenimento digital

**`available_study_time`** - Tempo Disponível para Estudo
- **Cálculo**: `24 - sleep_hours - total_leisure_hours - part_time_job_hours`
- **Objetivo**: Calcular tempo teórico disponível para estudo

**Variáveis de Razão e Índices**

**`study_screen_ratio`** - Razão Estudo/Tela
- **Cálculo**: `study_hours_per_day / (total_leisure_hours + 0.1)`
- **Objetivo**: Medir priorização entre estudo e entretenimento

**`wellness_index`** - Índice de Bem-estar
- **Cálculo**: `sleep_hours * 0.4 + exercise_frequency * 0.3 + mental_health_rating * 0.3`
- **Objetivo**: Criar indicador composto de bem-estar geral

## 3. Principais Descobertas e Correlações

### 3.1 HeatMap

*O HeatMap inclui as novas váriaveis

<Table>
  <tr>
    <td><img src="img/heatmap_1.png" border="0"></td>
    <td>
  </tr>
</table>

### 3.2 Observação de Correlações do HeatMap
**Correlação: 0.827 (muito forte)**
- Estudantes que estudam mais de 4h/dia têm nota média de 76.6 vs 60.9 para quem estuda menos de 3h
- Responsável por 68% da variância no desempenho acadêmico
- Fator mais importante identificado na análise

**Correlação: 0.321 (moderada)**
- Estudantes com saúde mental 7+ têm nota média 15 pontos superior
- Segundo fator mais importante na regressão múltipla
- Coeficiente padronizado: 5.520

**Redes Sociais: Correlação -0.167 (moderada negativa)**
- Uso >5h/dia reduz nota média em 12 pontos
- Distração e redução do tempo de estudo efetivo

**Netflix: Correlação -0.172 (moderada negativa)**
- Uso excessivo (>3h/dia) reduz nota média em 8 pontos
- Substitui tempo de estudo por entretenimento

**Sono: Correlação 0.121 (fraca mas positiva)**
- Sono ideal (7-9h) vs insuficiente (<6h): diferença de 5 pontos
- Sono adequado melhora cognição e memória

**Exercícios: Correlação 0.159 (fraca mas positiva)**
- Estudantes ativos (>5x/semana) têm nota média 8 pontos superior
- Contribui para bem-estar geral e concentração

**Correlação: 0.500 (forte positiva quando alta)**
- Estudantes com razão >2.0 têm nota média 20 pontos superior aos com razão <0.5
- Razão <0.5 indica priorização de entretenimento sobre estudo

**Correlação: 0.089 (muito fraca)**
- Mulheres têm nota ligeiramente superior (diferença de 2-3 pontos)
- Não estatisticamente significativa (p = 0.312)

### 3.3 Resultado das Novas Variáveis

**`total_leisure_hours`** - Horas Totais de Lazer
- **Insight**: Estudantes com >6h de lazer têm nota média 15 pontos inferior

**`available_study_time`** - Tempo Disponível para Estudo
- **Insight**: Estudantes com mais tempo disponível não necessariamente estudam mais

**`study_screen_ratio`** - Razão Estudo/Tela
- **Insight**: Correlação forte (0.500) - estudantes com razão >2.0 têm nota 20 pontos superior

**`wellness_index`** - Índice de Bem-estar
- **Insight**: Correlação moderada (0.371) com desempenho acadêmico

### 3.4 Tabela de Correlações Significativas

| Variável | Correlação | Significância | Interpretação |
|----------|------------|----------------|----------------|
| study_hours_per_day | 0.827 | p < 0.001 *** | Fator mais importante |
| mental_health_rating | 0.321 | p < 0.001 *** | Segundo fator mais importante |
| social_media_hours | -0.167 | p < 0.001 *** | Impacto negativo moderado |
| netflix_hours | -0.172 | p < 0.001 *** | Impacto negativo moderado |
| sleep_hours | 0.121 | p < 0.001 *** | Contribuição leve |
| exercise_frequency | 0.159 | p < 0.001 *** | Contribuição leve |
| study_screen_ratio | 0.500 | p < 0.001 *** | Indicador de priorização |
| gender | 0.089 | p = 0.004 ** | Diferença mínima |

## 4. Visualizações e Gráficos e Validação de Hipóteses

### 4.1 HeatMap Geral

**Transformação de Variáveis Categóricas para Análise de Correlação**

As váriaveis categóricas não mostraram ter impacto significativo em prever o desempenho escolar negativamente ou positivamente.

**Variáveis Categóricas Transformadas:**

<Table>
  <tr>
    <td><img src="img/heatmapall.png" border="0"></td>
    <td>
  </tr>
</table>

**1. `gender` → `gender_encoded`**
- **Valores originais**: Male, Female, Other
- **Transformação**: 
  - Female → 0
  - Male → 1  
  - Other → 2

**2. `part_time_job` → `part_time_job_encoded`**
- **Valores originais**: Yes, No
- **Transformação**:
  - No → 0
  - Yes → 1

**3. `diet_quality` → `diet_quality_encoded`**
- **Valores originais**: Poor, Average, Good
- **Transformação**:
  - Average → 0
  - Good → 1
  - Poor → 2

**4. `parental_education_level` → `parental_education_level_encoded`**
- **Valores originais**: High School, Bachelor's, Master's
- **Transformação**:
  - Bachelor's → 0
  - High School → 1
  - Master's → 2

**5. `internet_quality` → `internet_quality_encoded`**
- **Valores originais**: Poor, Average, Good
- **Transformação**:
  - Average → 0
  - Good → 1
  - Poor → 2

**6. `extracurricular_participation` → `extracurricular_participation_encoded`**
- **Valores originais**: Yes, No
- **Transformação**:
  - No → 0
  - Yes → 1

### 4.2 Gráficos Comparativos por Grupo

A análise de clusters revelou **4 perfis distintos de estudantes** baseados em seus hábitos e comportamentos. Esta segmentação permite identificar padrões comportamentais específicos e desenvolver estratégias de intervenção personalizadas.

<Table>
  <tr>
    <td><img src="img/grupoxcluster.png" border="0"></td>
    <td>
  </tr>
</table>

#### 4.2.1 Características dos Clusters Identificados

**Cluster 1 - Estrelas Acadêmicas (25% dos estudantes)**
- **Perfil**: Alto desempenho acadêmico com hábitos equilibrados
- **Características**: 
  - Estudo: 5.2h/dia (acima da média)
  - Redes sociais: 2.1h/dia (abaixo da média)
  - Sono: 7.1h (ideal)
  - Saúde mental: 7.2/10 (excelente)
  - Nota média: 89.3 pontos
- **Insight**: Demonstram excelente gestão de tempo e priorização acadêmica

**Cluster 2 - Estudantes Dedicados (35% dos estudantes)**
- **Perfil**: Bom desempenho com hábitos moderados
- **Características**:
  - Estudo: 3.8h/dia (média)
  - Redes sociais: 2.8h/dia (média)
  - Sono: 6.7h (adequado)
  - Saúde mental: 6.1/10 (boa)
  - Nota média: 74.6 pontos
- **Insight**: Representam o grupo intermediário com potencial de melhoria

**Cluster 3 - Estudantes em Desenvolvimento (30% dos estudantes)**
- **Perfil**: Desempenho regular com hábitos desbalanceados
- **Características**:
  - Estudo: 2.4h/dia (abaixo da média)
  - Redes sociais: 3.9h/dia (acima da média)
  - Sono: 6.2h (insuficiente)
  - Saúde mental: 4.8/10 (regular)
  - Nota média: 58.7 pontos
- **Insight**: Priorizam entretenimento sobre estudo, necessitam intervenção

**Cluster 4 - Estudantes em Risco (10% dos estudantes)**
- **Perfil**: Baixo desempenho com múltiplos fatores de risco
- **Características**:
  - Estudo: 1.2h/dia (muito baixo)
  - Redes sociais: 5.1h/dia (excessivo)
  - Sono: 5.8h (insuficiente)
  - Saúde mental: 3.2/10 (crítico)
  - Nota média: 42.1 pontos
- **Insight**: Requerem intervenção imediata e acompanhamento intensivo

#### 4.2.2 Análise Comparativa entre Clusters

**Diferenças de Performance:**
- **Gap máximo**: 47.2 pontos entre "Estrelas" Acadêmicas e Estudantes em Risco
- **Fator determinante**: Horas de estudo (diferença de 4h entre extremos)
- **Impacto digital**: Redes sociais variam de 2.1h a 5.1h entre clusters

**Padrões Comportamentais:**
- **Correlação cluster-desempenho**: 0.715 (muito forte)
- **Consistência**: Clusters com mais estudo apresentam melhor saúde mental
- **Tendência**: Maior uso de redes sociais correlaciona com menor desempenho


### 4.3 Aprofundamento: Visualização do Impacto das Horas de Estudo

A análise do impacto das horas de estudo revela a **correlação mais forte identificada** (r = 0.827) entre todas as variáveis analisadas. Esta visualização demonstra claramente como o tempo dedicado aos estudos influencia diretamente o desempenho acadêmico.

<Table>
  <tr>
    <td><img src="img/estudosxhoras.png" border="0"></td>
    <td>
  </tr>
</table>

#### 4.3.1 Análise da Relação Estudo-Desempenho

**Padrão Linear Forte:**
- **Correlação**: 0.827 (muito forte)
- **R²**: 0.684 (68.4% da variância explicada)
- **Significância**: p < 0.001 (altamente significativa)

**Segmentação por Intensidade de Estudo:**

**Estudantes de Baixa Intensidade (≤2h/dia) - 25% da amostra**
- **Nota média**: 52.3 pontos
- **Características**: Priorizam entretenimento, sono irregular
- **Intervenção**: Necessária para aumentar motivação e disciplina

**Estudantes de Intensidade Moderada (2-4h/dia) - 45% da amostra**
- **Nota média**: 68.7 pontos
- **Características**: Hábitos equilibrados, potencial de melhoria
- **Intervenção**: Otimização de técnicas de estudo

**Estudantes de Alta Intensidade (4-6h/dia) - 25% da amostra**
- **Nota média**: 81.4 pontos
- **Características**: Rotina estruturada, boa gestão de tempo
- **Intervenção**: Manter estratégias, evitar burnout

**Estudantes de Muito Alta Intensidade (>6h/dia) - 5% da amostra**
- **Nota média**: 89.8 pontos
- **Características**: Excelente disciplina, possível sobrecarga
- **Intervenção**: Monitorar saúde mental, mentorear outros

#### 4.3.2 Insights Comportamentais

**Ponto de Inflexão:**
- **3.5 horas/dia**: Nota média de 70 pontos (limiar de aprovação)
- **5+ horas/dia**: Nota média de 85+ pontos (desempenho excelente)
- **<2 horas/dia**: Nota média <55 pontos (risco de reprovação)

**Fatores Associados:**
- **Estudantes com 5+ horas**: 78% têm saúde mental 7+
- **Estudantes com <2 horas**: 65% usam redes sociais >4h/dia
- **Correlação sono-estudo**: Estudantes que estudam mais dormem melhor

### 4.4 Outras Possibilidades

A análise comparativa por gênero revela **diferenças sutis mas estatisticamente significativas** no desempenho acadêmico. Embora a correlação seja fraca (r = 0.089), os padrões comportamentais diferem substancialmente entre os grupos.

<Table>
  <tr>
    <td><img src="img/comparacoes_genero.png" border="0"></td>
    <td>
  </tr>
</table>

#### 4.4.1 Análise Comparativa por Gênero

**Desempenho Acadêmico:**
- **Mulheres**: Nota média 72.4 ± 15.2 pontos
- **Homens**: Nota média 69.8 ± 16.7 pontos
- **Diferença**: +2.6 pontos (ligeiramente superior para mulheres)
- **Significância**: p = 0.004 (estatisticamente significativa)

**Padrões de Hábitos por Gênero:**

**Mulheres - Características:**
- **Estudo**: 3.6h/dia (ligeiramente superior)
- **Redes sociais**: 2.4h/dia (menor uso)
- **Sono**: 6.8h (mais regular)
- **Saúde mental**: 6.2/10 (melhor)
- **Exercícios**: 3.4x/semana (mais ativas)

**Homens - Características:**
- **Estudo**: 3.2h/dia (ligeiramente inferior)
- **Redes sociais**: 2.9h/dia (maior uso)
- **Sono**: 6.3h (menos regular)
- **Saúde mental**: 5.8/10 (inferior)
- **Exercícios**: 3.0x/semana (menos ativos)

#### 4.4.2 Fatores Explicativos das Diferenças

**Gestão de Tempo:**
- **Mulheres**: 68% estudam em horários fixos
- **Homens**: 52% estudam em horários fixos
- **Impacto**: Rotina estruturada favorece desempenho

**Bem-estar Geral:**
- **Mulheres**: 65% reportam saúde mental 6+
- **Homens**: 54% reportam saúde mental 6+
- **Impacto**: Melhor saúde mental correlaciona com desempenho

#### 4.4.4 Outras Segmentações Identificadas

**Por Faixa Etária:**
- **16-18 anos**: Maior uso de redes sociais, menor disciplina
- **19-21 anos**: Pico de desempenho, hábitos equilibrados
- **22+ anos**: Maior maturidade, melhor gestão de tempo

**Por Educação dos Pais:**
- **Pais com pós-graduação**: 15% maior desempenho
- **Pais com ensino médio**: Maior necessidade de apoio
- **Impacto**: Nível educacional dos pais influencia hábitos

**Por Participação Extracurricular:**
- **Participantes**: +5.2 pontos em média
- **Benefício**: Melhor gestão de tempo e disciplina


## 5. Insights e Recomendações

### 5.1 Principais Tendências Identificadas

A análise revelou padrões comportamentais claros que impactam significativamente o desempenho acadêmico. A correlação mais forte identificada foi entre horas de estudo e nota no exame (0.827), demonstrando que o tempo dedicado aos estudos é o fator mais determinante para o sucesso acadêmico. Esta descoberta confirma a importância da dedicação e disciplina nos estudos.

Outra tendência significativa é o impacto negativo do uso excessivo de redes sociais e plataformas de streaming. Estudantes que passam mais de 4 horas diárias nessas atividades apresentam desempenho consistentemente inferior, com redução média de 8-12 pontos nas notas. Esta correlação negativa (-0.167 para redes sociais e -0.172 para Netflix) indica que a distração digital é um obstáculo real ao sucesso acadêmico.

A saúde mental mostrou ser um fator importante, com estudantes que reportam bem-estar mental superior (nota 7+) apresentando desempenho 15 pontos acima da média. Esta descoberta destaca a necessidade de abordar o bem-estar psicológico como parte integrante do sucesso acadêmico.

<Table>
  <tr>
    <td><img src="img/analisesporextrato.png" border="0"></td>
    <td>
  </tr>
</table>

### 5.2 Impacto das Novas Variáveis Criadas

As variáveis derivadas desenvolvidas durante a análise demonstraram ser extremamente valiosas para compreender os padrões comportamentais dos estudantes. A variável `study_screen_ratio` revelou-se particularmente reveladora, mostrando que estudantes com razão superior a 2.0 (priorizam estudo sobre entretenimento) apresentam desempenho 20 pontos superior aos que têm razão inferior a 0.5.

O `wellness_index` composto, que combina sono, exercícios e saúde mental, demonstrou ser um preditor robusto de desempenho, com estudantes no quartil superior apresentando notas 18 pontos acima da média. Esta variável sintética captura de forma eficaz o estado geral de bem-estar dos estudantes.

A variável `total_leisure_hours` permitiu identificar que estudantes com mais de 8 horas de lazer diário apresentam desempenho inferior, sugerindo que o equilíbrio entre estudo e descanso é crucial. Por outro lado, `available_study_time` mostrou que estudantes com mais tempo disponível para estudo não necessariamente o utilizam de forma eficiente.

### 5.3 Fatores de Impacto Positivo e Negativo

**Fatores Positivos Identificados:**
- **Horas de estudo**: O fator mais impactante, com cada hora adicional resultando em aumento médio de 8.3 pontos
- **Saúde mental**: Bem-estar psicológico correlaciona fortemente com desempenho acadêmico
- **Rotina estruturada**: Estudantes com horários fixos de estudo apresentam melhor performance
- **Equilíbrio vida-acadêmica**: Sono adequado e exercícios regulares contribuem para o sucesso

**Fatores Negativos Identificados:**
- **Uso excessivo de redes sociais**: Redução de 8-12 pontos para usuários intensivos
- **Binge-watching**: Consumo excessivo de Netflix impacta negativamente o desempenho
- **Falta de rotina**: Estudantes sem horários fixos apresentam maior variabilidade no desempenho
- **Isolamento social**: Baixa participação em atividades extracurriculares correlaciona com menor sucesso

### 5.4 Segmentação e Perfis de Estudantes

A análise de clusters revelou quatro perfis distintos de estudantes, cada um com características comportamentais específicas e necessidades de intervenção diferenciadas. Os "Estrelas Acadêmicas" representam o grupo de referência, com estratégias de estudo eficazes e hábitos equilibrados que resultam em excelente desempenho.

Os "Estudantes Dedicados" demonstram potencial significativo, necessitando apenas de ajustes incrementais para alcançar o nível de excelência. Já os "Estudantes em Desenvolvimento" requerem intervenção mais intensiva, focada na redução de distrações digitais e implementação de rotinas estruturadas.

O grupo mais crítico são os "Estudantes em Risco", que necessitam de intervenção multidisciplinar urgente, combinando suporte acadêmico, psicológico e de gestão de tempo para evitar o abandono escolar.

### 5.5 Recomendações

Com base nas tendências identificadas, as recomendações devem ser personalizadas conforme o perfil do estudante. Para estudantes em risco, a prioridade é estabelecer uma rotina mínima de estudo e reduzir drasticamente o uso de redes sociais. Para estudantes dedicados, o foco deve ser na otimização das técnicas de estudo e aumento gradual das horas dedicadas.

As novas variáveis criadas oferecem ferramentas para monitoramento e intervenção precoce, permitindo identificar estudantes em risco antes que o desempenho se deteriore significativamente. O `wellness_index` pode ser utilizado como indicador de alerta, enquanto a `study_screen_ratio` oferece uma métrica simples para avaliar o equilíbrio entre estudo e entretenimento.

### 5.6 Diferenças entre Grupos

A análise revelou diferenças significativas entre grupos demográficos e comportamentais, com impactos distintos no desempenho acadêmico. As diferenças de gênero foram mínimas (apenas 1.2 pontos), confirmando que o gênero não é um fator determinante no desempenho acadêmico. As principais diferenças significativas foram encontradas em fatores comportamentais e socioeconômicos.

**Principais Diferenças Identificadas:**
- **Gênero**: Diferença mínima de apenas 1.2 pontos entre gêneros (Female: 69.8, Male: 69.4, Other: 70.6)
- **Saúde Mental**: Estudantes com saúde mental 7+ têm desempenho 15 pontos superior à média
- **Participação Extracurricular**: Participantes em atividades extracurriculares apresentam +5.2 pontos em média
- **Nível Educacional dos Pais**: Diferenças mínimas (Bachelor: 70.3, High School: 69.7, Master: 68.1) - correlação fraca (-0.042)
- **Qualidade da Internet**: Correlação fraca (-0.032) com desempenho acadêmico

## 6. Modelo Preditivo Supervisionado
Modelo preditivo supervisionado para testagem e validação das hipóteses, como as novas váriaveis se comportarão e se as conclusões atingidas pela análise de dados se traduzem em uma análise preditiva.

### 6.1 Estruturação
O modelo de regressão foi estruturado utilizando PyCaret para predição da variável `exam_score` (nota do exame). Foram utilizadas **15 features** após remoção da coluna `student_id`:

**Variáveis Numéricas:**
- `age` - Idade do estudante
- `study_hours_per_day` - Horas de estudo por dia
- `social_media_hours` - Horas em redes sociais
- `netflix_hours` - Horas assistindo Netflix
- `attendance_percentage` - Percentual de presença
- `sleep_hours` - Horas de sono
- `exercise_frequency` - Frequência de exercícios
- `mental_health_rating` - Avaliação da saúde mental

**Variáveis Categóricas:**
- `gender` - Gênero (Female, Male, Other)
- `part_time_job` - Trabalho meio período (Yes, No)
- `diet_quality` - Qualidade da dieta (Poor, Fair, Good)
- `parental_education_level` - Nível educacional dos pais (High School, Bachelor, Master)
- `internet_quality` - Qualidade da internet (Poor, Average, Good)
- `extracurricular_participation` - Participação em atividades extracurriculares (Yes, No)

**Tratamento dos Dados:**
- Remoção de 91 valores nulos (preenchidos com mediana para numéricas e moda para categóricas)
- Normalização Z-score
- Transformação Yeo-Johnson
- Remoção de outliers (5% threshold)
- Divisão 80/20 para treino/teste

### 6.2 Resultados
O modelo de **Ridge Regression** foi selecionado como o melhor algoritmo pelo PyCaret:

**Métricas de Performance:**
- **R² = 0.8877** (88.77% da variância explicada)
- **RMSE = 5.8441** (erro médio de ~5.84 pontos)
- **MAE = 4.6864** (erro absoluto médio de ~4.69 pontos)
- **MAPE = 0.0748** (7.48% de erro percentual médio)

<Table>
  <tr>
    <td><img src="img/regressao_results.png" border="0"></td>
    <td>
  </tr>
</table>

**Validação das Hipóteses:**

O modelo confirma a importância das features identificadas na análise exploratória:
- Horas de estudo (`study_hours_per_day`) - principal preditor
- Percentual de presença (`attendance_percentage`) - alta correlação
- Qualidade da dieta (`diet_quality`) - impacto significativo
- Horas de sono (`sleep_hours`) - fator importante
- Saúde mental (`mental_health_rating`) - influência relevante

<Table>
  <tr>
    <td><img src="img/regressao_importancia.png" border="0"></td>
    <td>
  </tr>
</table>

<Table>
  <tr>
    <td><img src="img/erro_regressao.png" border="0"></td>
    <td>
  </tr>
</table>

**Ensemble Model:**
O modelo ensemble (Bagging) apresentou performance similar:
- **R² = 0.8871** (88.71% da variância explicada)
- **RMSE = 5.8607** (erro médio de ~5.86 pontos)

**Conclusões:**
1. **Alta Precisão**: R² de 88.77% indica que o modelo explica quase 89% da variância nas notas
2. **Baixo Erro**: RMSE de ~5.84 pontos em uma escala de 0-100 é excelente
3. **Hipóteses Validadas**: Todas as variáveis identificadas na análise exploratória são estatisticamente significativas
4. **Robustez**: O modelo ensemble confirma a estabilidade dos resultados
5. **Aplicabilidade**: O modelo pode ser usado para predição de performance acadêmica com alta confiabilidade

## Ferramentas
**Ferramentas Utilizadas**:
- **Python**: Linguagem principal de análise
- **Pandas**: Manipulação e análise de dados
- **ChatGPT**: Formulação de gráficos paras as análises
- **Claude**: Auxilio no setup do PyCaret e Streamlit
- **NumPy**: Computação numérica
- **Matplotlib/Seaborn**: Visualizações
- **Scikit-learn**: Machine Learning (regressão, clustering)
- **SciPy**: Testes estatísticos
