# Solução do Problema do Caixeiro Viajante (PCV)

Este repositório contém a implementação de soluções heurísticas e meta-heurísticas para o Problema do Caixeiro Viajante (Travel Salesman Problem - TSP), desenvolvido como requisito parcial da disciplina de Grafos.

O projeto visa comparar o desempenho de algoritmos construtivos simples com técnicas evolutivas mais robustas (Genéticos e Meméticos) utilizando um conjunto de 12 instâncias de teste (6 baseadas em distância e 6 baseadas em tempo).

## 📋 Funcionalidades Implementadas

Conforme especificado, foram desenvolvidos os seguintes algoritmos:

1.  **Heurística do Vizinho Mais Próximo (Nearest Neighbor)**
    * Refinamento: Busca Local (Hill Climbing ou 2-Opt).
    * Execução: Determinística (1 execução).
2.  **Heurística da Inserção Mais Barata (Cheapest Insertion)**
    * Refinamento: Busca Local.
    * Execução: Determinística (1 execução).
3.  **Algoritmo Genético (AG)**
    * População inicial gerada aleatoriamente ou via heurísticas.
    * Operadores de Cruzamento (Crossover) e Mutação.
    * Execução: Estocástica (20 execuções por instância para coleta de estatísticas).
4.  **Algoritmo Memético (AM)**
    * Híbrido de Algoritmo Genético com Busca Local.
    * Implementação de pelo menos **3 técnicas de busca local** distintas.
    * Execução: Estocástica (20 execuções por instância).

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Interpretador:** Python 3.8 ou superior
* **Ambiente de Desenvolvimento:** VS Code
* **Bibliotecas:** [Listar bibliotecas se houver, ex: NumPy, Matplotlib, ou "Bibliotecas padrão do Python"]

## 📂 Estrutura do Projeto

* `/src`: Código fonte da aplicação. Todo o código está comentado em português, detalhando funções, entradas e saídas.
* `/instances`: Arquivos de entrada com as 12 instâncias do problema.
* `/docs`: Contém o relatório final em PDF.
    * `Relatorio_PCV.pdf`: Comparativo com o artigo base, detalhes de hardware, parametrização e tabelas de resultados.
* `/output`: Diretório onde são gerados os arquivos de resultados.
    * `resumo_resultados.txt`: Resumo estatístico (Melhor, Média, Tempo) das 20 execuções dos algoritmos evolutivos.

## 🚀 Como Executar

### Pré-requisitos

Certifique-se de ter o Python 3 instalado. Caso utilize bibliotecas externas, instale-as via pip:

```bash
pip install -r requirements.txt
# ou instale manualmente, ex: pip install numpy
````

### Exacução

O programa aceita argumentos via linha de comando para definir qual algoritmo e qual instância rodar.

### Formato

```bash
python main.py --alg [ALGORTIMO(1-4)] --prob [PROBLEMA(1-12)]
```

### Opções de algoritmo

* `1`: Vizinho Mais Próximo + Busca Local
* `2`: Inserção Mais Barata + Busca Local
* `3`: Algoritmo Genético
* `4`: Algoritmo Memético

### Exemplo de uso

```bash
python main.py --alg 1 --prob 11
```

Nota: Para os algoritmos Genético e Memético, o software executará automaticamente as 20 iterações exigidas e salvará o resumo estatístico no arquivo de saída.

## 📊 Entradas e Saídas

### Formato de entrada

Os arquivos de instância seguem o padrão descrito no artigo anexo, contendo a matriz de distâncias/tempos entre as cidades.

### Formato de Saída (Relatório TXT)

Para os algoritmos evolutivos, será gerado um arquivo `resumo_resultados.txt` contendo:

* Instância processada.
* Menor valor encontrado (Best Sol).
* Valor médio das soluções (Avg Sol).
* Tempo médio de execução (Avg Time).

## 📝 Lista de Atividades por Integrante

Abaixo detalha-se a participação efetiva de cada membro na concepção, implementação, revisão e testes:

| Integrante          | Atividades Desenvolvidas                                                                                                                                                                  |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Felipe Freitas** | Implementação da Heurística do Vizinho Mais Próximo e sua Busca Local; Estrutura base do projeto em Python.                                                                                |
| **[Nome do Aluno 2]** | Implementação da Heurística de Inserção Mais Barata e sua Busca Local; Leitura e parse dos arquivos de instância.                                                                           |
| **Kaio Eduardo** | Desenvolvimento do Algoritmo Genético (Geração de população, Seleção e Mutação); Coleta de dados estatísticos (média/tempo).                                                                |
| **[Nome do Aluno 4]** | Implementação do Algoritmo Memético; Desenvolvimento das 3 estratégias de Busca Local (ex: 2-opt, Swap, Insertion).                                                                         |
| **[Nome do Aluno 5]** | Análise dos resultados e comparação com GLPK; Elaboração do relatório PDF; Revisão de código e testes finais.                                                                              |

### Observações

* Os resultados comparativos com a solução exata (GLPK) e com o artigo base encontram-se na Tabela 4 do arquivo `docs/Relatorio_PCV.pdf`.
