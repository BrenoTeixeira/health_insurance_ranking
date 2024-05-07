[![en](https://img.shields.io/badge/lang-en-red.svg)](README.en.md)

# Projeto de Cross-Sell de Seguro de Veículo

<img src='imagens/readme/cross_sell.png'>

Aviso: O contexto deste projeto é totalmente fictício.

## Sumário

* [1.0. Problema de Negócio](#10-problema-de-negócio)
* [2.0. Suposições de Negócio](#20-suposições-de-negócio)
    * [2.1. Dicionário de Dados](#21-dicionário-de-dados)

* [3.0. Estratégia de Solução](#30-estratégia-de-solução)

* [4.0. Principais 3 Insights de Dados](#40-principais-3-insights-de-dados)
* [5.0. Modelo de Aprendizado de Máquina Aplicado](#50-modelo-de-aprendizado-de-máquina-aplicado)
    * [5.1. Métricas de Avaliação](#51-métricas-de-avaliação)
    * [5.2. Desempenho dos Modelos - Validação Cruzada](#52-desempenho-dos-modelos---validação-cruzada)
* [6.0. Desempenho do Modelo de Aprendizado de Máquina](#60-desempenho-do-modelo-de-aprendizado-de-máquina)
* [7.0. Resultados de Negócio](#70-resultados-de-negócio)
    * [7.1. Perguntas do CEO](#71-perguntas-do-ceo)
* [8.0. Conclusões](#80-conclusões)
* [9.0. Próximos Passos para Melhorar](#90-próximos-passos-para-melhorar)
* [10.0. Demonstração no Google Sheets](#100-demonstração-no-google-sheets)


# 1.0. Problema de Negócio

A Insurance All é uma empresa de seguros que oferece planos de seguro de saúde aos seus clientes e está analisando a possibilidade de oferecer um novo produto a eles — seguro de veículo.

Este novo plano de seguro de veículo funcionará como o plano de seguro de saúde. O cliente tem que pagar uma taxa anual para a Insurance All, e a empresa cobre as despesas em caso de acidente automobilístico eventual.

No ano passado, a empresa entrevistou 380.000 clientes sobre seu interesse em adquirir um novo produto — seguro de veículo. Os clientes tiveram que responder se estavam ou não interessados no plano de seguro de veículo. Suas respostas e [atributos](#21-dicionário-de-dados) foram salvos em um banco de dados.

Então, 127.037 novos clientes, que não participaram da pesquisa no ano passado, foram selecionados para participar de uma campanha na qual a empresa irá oferecer-lhes o plano de seguro de veículo. A equipe de vendas fará isso através de chamadas telefônicas. No entanto, a equipe de vendas só pode fazer 20.000 chamadas no período da campanha.

Neste contexto, meu desafio como consultor de ciência de dados é projetar uma solução que permita à Insurance All segmentar os clientes mais inclinados a adquirir o seguro de veículo. Assim, a empresa pode obter o maior lucro possível das 20.000 chamadas.

Também será necessário entregar um relatório com as respostas para as seguintes perguntas:

1. Quais são os insights mais interessantes sobre os atributos mais relevantes dos clientes interessados em adquirir seguro de veículo?

2. Qual é a porcentagem de clientes interessados em seguro de veículo que a equipe de vendas poderá contatar fazendo 20.000 chamadas?

3. Se a equipe de vendas pudesse fazer 40.000 chamadas, qual seria a porcentagem de clientes interessados que eles poderiam contatar?

4. Quantas chamadas a equipe de vendas precisa fazer para contatar 80% dos clientes interessados em adquirir seguro de veículo?
</br><br/>

# 2.0. Suposições de Negócio

O plano de seguro de veículo custará $ 4.500 por ano.

## 2.1. Dicionário de Dados
|Característica|	Descrição|
|--------------|-------------|
id|	ID único do cliente|
Gênero|	Gênero do cliente|
Idade|	Idade do cliente|
Carteira_de_Habilitação|	0: Cliente não tem CNH, 1: Cliente já tem CNH|
Código_de_Região|	Código único para a região do cliente|
Previamente_Segurado|	1: Cliente já possui Seguro de Veículo, 0: Cliente não possui Seguro de Veículo|
Idade_do_Veículo|	Idade do Veículo|
Dano_do_Veículo|	1: Cliente teve seu veículo danificado no passado, 0: Cliente não teve seu veículo danificado no passado|
Prêmio_Anual|	O valor que o cliente precisa pagar por ano|
Canal_de_Venda|	Código anonimizado para o canal de contato com o cliente, ou seja, Diferentes Agentes, Por Correio, Por Telefone, Pessoalmente, etc.|
Vintage|	Número de Dias que o cliente está associado à empresa|
Resposta|	1: Cliente está interessado, 0: Cliente não está interessado|
</br><br/>	

# 3.0. Estratégia de Solução

O método CRISP-DM foi utilizado para desenvolver este projeto.

<img src='imagens/readme/crisp.png'/>

Minha estratégia para resolver este desafio foi:

**Passo 00. Coleta de Dados:** Coletar os dados de um banco de dados Postgres. Dividir os dados em treino e teste.

**Passo 01. Descrição dos Dados:** Utilizar estatísticas descritivas para obter uma compreensão inicial do conjunto de dados. Verificar a dimensão dos dados e inconsistências - valores ausentes, tipos de dados e duplicatas.

**Passo 02. Engenharia de Atributos:** Criar um mapa mental das Hipóteses e fazer transformações em alguns atributos.

**Passo 03. Filtragem de Dados:** Este passo não foi necessário.

**Passo 04. Análise Exploratória de Dados:** Análise univariada de cada variável em relação à variável alvo. Análise bivariada (Numérica x Numérica, Numérica x Categórica e Categórica x Categórica) em relação à variável alvo. Análise multivariada e validação de hipóteses.

**Passo 05. Preparação de Dados:** Definindo os métodos de codificação para variáveis categóricas e métodos de escalonamento para variáveis numéricas.

**Passo 06. Seleção de Atributos:** Usar o boruta para selecionar os atributos mais relevantes para ajustar os modelos.

**Passo 07. Modelagem de Aprendizado de Máquina:** Treinar cinco modelos usando pipelines para preparar os dados com os métodos definidos no passo 05 e usar apenas as variáveis selecionadas no passo 06. Analisar o desempenho dos modelos e escolher o melhor para o próximo passo (ajuste fino).

**Passo 08. Ajuste Fino de Hiperparâmetros:** Encontrar os melhores parâmetros para o modelo selecionado no passo 07 usando validação cruzada e optuna (framework de otimização de hiperparâmetros).

**Passo 09. Análise de Resultados do Modelo e Desempenho de Negócio:** Avaliar a capacidade do modelo de se adaptar a dados previamente não vistos retirados da mesma distribuição que a usada para criar o modelo. Avaliar o desempenho de negócio com a implementação do modelo final.

**Passo 10. Implementação do Modelo em Produção:** Criar um script no Google Sheets para solicitar uma API, com um clique, que retorne os scores de propensão dos clientes e ordene a lista de clientes em ordem decrescente com base nos scores.
</br><br/>

# 4.0. Principais Insights de Dados

**H1:** Pessoas na faixa etária de 40 a 47 anos têm uma maior propensão a adquirir seguro de veículo.

<img src='imagens/idade_cohort.png' /> 

**H2:** A porcentagem de pessoas interessadas em seguro de veículo é maior entre aqueles com carros mais antigos.

<img src='imagens/idade_veiculo.png' /> 

**H3:** Quase ninguém das pessoas que não teve problemas com seu veículo no passado está interessado em seguro de veículo.

<img src='imagens/dano_veiculo.png' /> 
</br><br/>

# 5.0. Modelo de Aprendizado de Máquina Aplicado

Para este projeto, diferentes modelos foram testados:

- Regressão Logística
- K-Vizinhos Mais Próximos
- Classificador LigthGBM
- ExtraTreesClassifier
- GaussianNB
</br><br/>

## 5.1. Métricas de Avaliação

As seguintes métricas foram usadas para avaliar os modelos: precision_at_20000, recall_at_20000 e lift_score.

precision_at_20000: esta métrica diz, em uma lista ordenada pelo score dado pelo modelo, a porcentagem de clientes interessados nos primeiros 20.000 (k) elementos da lista.

recall_at_20000: esta métrica diz, de todos os clientes interessados, qual porcentagem está nos primeiros 20.000 elementos de uma lista ordenada pelo score dado pelo modelo.

lift_score: mede o quão melhor o modelo é em comparação com um modelo aleatório. Em nosso caso, nos diz que podemos esperar capturar N(lift) vezes mais clientes interessados usando o modelo do que capturaríamos aleatoriamente o mesmo número de clientes.
</br><br/>

## 5.2. Desempenho dos Modelos - Validação Cruzada

|Modelo|	precision_at_20000|	recall_at_20000	lift_score|
|------|----------------------|---------------------------|
|Regressão Logística|	0.1983 +/- 0.0002|	0.9987 +/- 0.0009|	2.0558 +/- 0.0196|
|KNN|	0.1973 +/- 0.0004|	0.9937 +/- 0.0022|	2.2385 +/- 0.0261|
|LGBM|	0.1983 +/- 0.0001|	0.999 +/- 0.0008|	2.3005 +/- 0.0262|
|ExtraTrees|	0.195 +/- 0.0005|	0.9821 +/- 0.0023|	2.2376 +/- 0.021|
|Gaussian|	0.1981 +/- 0.0002|	0.9979 +/- 0.0009|	2.3082 +/- 0.0309|

# 6.0. Desempenho do Modelo de Aprendizado de Máquina

Dos resultados anteriores, o LGBMClassifier foi escolhido para ajuste fino de hiperparâmetros. Em seguida, re-treinamos o modelo usando os conjuntos de treinamento e validação e avaliamos o desempenho de generalização do modelo usando o conjunto de teste (dados previamente não vistos).
</br><br/>

Modelo|	precision_at_20000|	recall_at_20000	lift_score|
|-----|-------------------|---------------------------|
|LGBM Ajustado|	0.286636|	0.818182|	2.052952|
</br><br/>			

# 7.0. Resultados de Negócio

Curva de Ganho Cumulativo

<img src='imagens/readme/ganho_cumulativo.png'/>

A curva acima nos diz que se pudermos contatar 40% da população (ordenada pelo score de propensão), podemos alcançar 90% dos clientes que estão interessados em seguro de veículo.
</br><br/>

Curva de Lift

<img src='imagens/readme/curva_lift.png'/>

Na curva acima, para 20% dos dados ordenados, há um lift de quase 3. Isso significa que, se os 20% principais de clientes forem contatados, espera-se alcançar três vezes mais clientes interessados do que seria alcançado contatando o mesmo número de clientes aleatoriamente.
</br><br/>

## 7.1. Perguntas do CEO

No conjunto de teste, há 12,26% de clientes interessados. A mesma proporção é assumida para os novos clientes (127.037) para responder às seguintes perguntas:
</br><br/>

### 1. Qual é a porcentagem de clientes interessados em seguro de veículo que a equipe de vendas será capaz de contatar fazendo 20.000 chamadas?

Com 20.000 chamadas, é possível contatar 15,75% dos 127.037 clientes — ordenados pelo score do modelo — que não participaram da pesquisa. Então, espera-se alcançar 42% (6.541) dos clientes interessados em seguro de veículo.

<img src='imagens/readme/ganho_cumulativo_negocio.png'/>

Espera-se alcançar 15,75% (2453) dos clientes interessados se 15,75% dos clientes oram contatados aleatoriamente.

<img src='imagens/readme/desempenho_negocio_20k.PNG'/>
</br><br/>

O modelo é 2,66 vezes melhor do que abordar os clientes de forma aleatória. Espera-se 2,66 vezes mais receita usando o modelo.
</br><br/>

### 3. Se a equipe de vendas pudesse fazer 40.000 chamadas, qual seria a porcentagem de clientes interessados que eles seriam capazes de contatar?

Com 40.000 chamadas, é possível contatar 31,50% dos 127.037 clientes. Então, espera-se alcançar 75,70% (11.790) dos clientes interessados em seguro de veículo.

<img src='imagens/readme/ganho_cumulativo_negocio_40.png'/>

Espera-se alcançar 31,50% (4906) dos clientes interessados se 31,50% dos clientes oram contatados aleatoriamente.

<img src='imagens/readme/desempenho_negocio_40k.PNG'/>
</br><br/>

O modelo é 2,40 vezes melhor do que abordar os clientes de forma aleatória. Espera-se 2,40 vezes mais receita usando o modelo.
</br><br/>

### 4. Quantas chamadas a equipe de vendas precisa fazer para contatar 80% dos clientes interessados em adquirir seguro de veículo?

A equipe de vendas precisa fazer 43.107 chamadas para alcançar 80% dos clientes interessados em adquirir seguro de veículo.

<img src='imagens/readme/ganho_cumulativo_negocio_80p.png'/>

Aleatoriamente, seriam necessárias 101.630 chamadas para alcançar 80% dos clientes interessados.

# 8.0. Conclusões

Os objetivos do projeto foram alcançados.
A empresa pode priorizar os clientes com maiores probabilidades de adquirir seguro de veículo com a solução desenvolvida neste projeto. Isso significa que melhores resultados podem ser alcançados com menos recursos.

Com a implementação do modelo, reduzimos os custos e aumentamos a receita.
</br><br/>

# 9.0. Próximos Passos para Melhorar

Criar novos recursos para melhorar o desempenho do modelo.
Testar diferentes métodos de codificação e escalonamento.

# 10.0. Demonstração no Google Sheets

<img src='imagens/readme/google_sheets_demo2.gif'>
</br><br/>

#### Este projeto foi desenvolvido por Breno Teixeira.
