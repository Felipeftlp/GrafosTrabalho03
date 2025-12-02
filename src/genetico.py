"""
Algoritmo Genético para o Problema do Caixeiro Viajante (PCV)

Este módulo implementa um Algoritmo Genético completo para resolver o PCV,
seguindo a estrutura:
1. Inicialização de população
2. Avaliação (fitness)
3. Seleção de pais
4. Cruzamento
5. Mutação
6. Formação de nova população
7. Repetição até critério de parada

"""

import random
import copy
from src.utils import calcular_custo_rota


def inicializar_populacao(tamanho_populacao, num_cidades, usar_heuristica=True, matriz_distancias=None):
    """
    Inicializa a população inicial de soluções candidatas.
    
    Estratégia: 
    - Parte da população é gerada aleatoriamente (diversidade)
    - Parte pode usar heurística do vizinho mais próximo (qualidade inicial)
    
    Args:
        tamanho_populacao (int): Número de indivíduos na população
        num_cidades (int): Número de cidades no problema
        usar_heuristica (bool): Se True, usa heurística para parte da população
        matriz_distancias (list): Matriz de distâncias (necessária se usar_heuristica=True)
    
    Returns:
        list: Lista de rotas (cada rota é uma lista de índices de cidades)
              Formato: [[0,1,2,3,0], [2,0,1,3,2], ...]
              Nota: A rota não inclui o retorno ao início na representação interna
    """
    populacao = []
    
    # Calcula quantos indivíduos serão gerados por heurística
    num_heuristica = tamanho_populacao // 4 if usar_heuristica and matriz_distancias else 0
    
    # Gera parte da população usando heurística (se habilitado)
    if num_heuristica > 0:
        from src.solver import vizinho_mais_proximo
        for _ in range(num_heuristica):
            rota_heuristica = vizinho_mais_proximo(matriz_distancias, inicio_aleatorio=True)
            # Remove o último elemento (retorno ao início) para representação interna
            rota_interna = rota_heuristica[:-1]
            populacao.append(rota_interna)
    
    # Gera o restante da população aleatoriamente
    cidades = list(range(num_cidades))
    for _ in range(tamanho_populacao - len(populacao)):
        rota_aleatoria = cidades.copy()
        random.shuffle(rota_aleatoria)
        populacao.append(rota_aleatoria)
    
    return populacao


def calcular_fitness(rota, matriz_distancias):
    """
    Calcula o fitness (aptidão) de uma rota.
    
    Para o PCV, o fitness é o inverso do custo total da rota.
    Quanto menor o custo, maior o fitness.
    
    Args:
        rota (list): Rota como lista de índices [0,1,2,3] (sem retorno ao início)
        matriz_distancias (list): Matriz de distâncias entre cidades
    
    Returns:
        float: Valor de fitness (quanto maior, melhor)
    """
    # Adiciona o retorno ao início para calcular o custo completo
    rota_completa = rota + [rota[0]]
    custo = calcular_custo_rota(rota_completa, matriz_distancias)
    
    # Se a rota for inválida (custo infinito), retorna fitness zero
    if custo == float('inf'):
        return 0.0
    
    # Fitness é o inverso do custo (quanto menor o custo, maior o fitness)
    # Adiciona 1 no denominador para evitar divisão por zero
    fitness = 1.0 / (custo + 1.0)
    return fitness


def avaliar_populacao(populacao, matriz_distancias):
    """
    Avalia todos os indivíduos da população calculando seus fitness.
    
    Args:
        populacao (list): Lista de rotas (população)
        matriz_distancias (list): Matriz de distâncias
    
    Returns:
        list: Lista de tuplas (fitness, rota) ordenada por fitness decrescente
    """
    individuos_avaliados = []
    for rota in populacao:
        fitness = calcular_fitness(rota, matriz_distancias)
        individuos_avaliados.append((fitness, rota))
    
    # Ordena por fitness decrescente (melhores primeiro)
    individuos_avaliados.sort(reverse=True, key=lambda x: x[0])
    return individuos_avaliados


def selecao_roleta(populacao_avaliada, num_pais):
    """
    Seleciona pais usando o método da Roleta (Fitness Proportional Selection).
    
    A probabilidade de um indivíduo ser selecionado é proporcional ao seu fitness.
    
    Args:
        populacao_avaliada (list): Lista de tuplas (fitness, rota) já avaliadas
        num_pais (int): Número de pais a selecionar
    
    Returns:
        list: Lista de rotas selecionadas (pais)
    """
    # Extrai apenas os fitness
    fitness_values = [ind[0] for ind in populacao_avaliada]
    
    # Calcula a soma total de fitness
    soma_fitness = sum(fitness_values)
    
    # Se a soma for zero (todos inválidos), seleciona aleatoriamente
    if soma_fitness == 0:
        return [random.choice(populacao_avaliada)[1] for _ in range(num_pais)]
    
    # Normaliza os fitness para criar probabilidades
    probabilidades = [f / soma_fitness for f in fitness_values]
    
    # Seleciona os pais usando roleta
    pais_selecionados = []
    for _ in range(num_pais):
        # Gera número aleatório entre 0 e 1
        r = random.random()
        
        # Encontra o indivíduo correspondente na roleta
        acumulado = 0.0
        for i, prob in enumerate(probabilidades):
            acumulado += prob
            if r <= acumulado:
                pais_selecionados.append(populacao_avaliada[i][1])
                break
    
    return pais_selecionados


def selecao_torneio(populacao_avaliada, num_pais, tamanho_torneio=3):
    """
    Seleciona pais usando o método de Torneio.
    
    Para cada pai, seleciona aleatoriamente 'tamanho_torneio' indivíduos
    e escolhe o melhor entre eles.
    
    Args:
        populacao_avaliada (list): Lista de tuplas (fitness, rota) já avaliadas
        num_pais (int): Número de pais a selecionar
        tamanho_torneio (int): Número de participantes em cada torneio (padrão: 3)
    
    Returns:
        list: Lista de rotas selecionadas (pais)
    """
    pais_selecionados = []
    
    for _ in range(num_pais):
        # Seleciona aleatoriamente 'tamanho_torneio' indivíduos
        participantes = random.sample(populacao_avaliada, min(tamanho_torneio, len(populacao_avaliada)))
        
        # Escolhe o melhor (maior fitness)
        melhor = max(participantes, key=lambda x: x[0])
        pais_selecionados.append(melhor[1])
    
    return pais_selecionados

def cruzamento_ox(pai1, pai2):
    """
    Realiza cruzamento OX entre dois pais.
    
    Args:
        pai1 (list): Primeira rota (pai)
        pai2 (list): Segunda rota (pai)
    
    Returns:
        tuple: (filho1, filho2) - Dois filhos gerados
    """

    n = len(pai1)
    # Garante pontos aleatórios ordenados
    ponto1, ponto2 = sorted(random.sample(range(n), 2))
    
    # Inicializa filhos
    filho1 = [None] * n
    filho2 = [None] * n
    
    # Copia o segmento fixo (herança genética direta)
    filho1[ponto1:ponto2+1] = pai1[ponto1:ponto2+1]
    filho2[ponto1:ponto2+1] = pai2[ponto1:ponto2+1]
    
    # Cria sets para verificação instantânea O(1)
    # Isso é o segredo da performance em Python
    set_f1 = set(filho1[ponto1:ponto2+1])
    set_f2 = set(filho2[ponto1:ponto2+1])
    
    def preencher_restante(filho, pai_origem, conjunto_existente):
        # Começa a preencher logo após o segundo ponto de corte
        pos_atual = (ponto2 + 1) % n
        # Começa a ler o outro pai também após o segundo ponto de corte
        idx_pai = (ponto2 + 1) % n
        
        count = 0
        while count < n: # Percorre o pai circularmente
            cidade = pai_origem[idx_pai]
            if cidade not in conjunto_existente:
                filho[pos_atual] = cidade
                pos_atual = (pos_atual + 1) % n
            idx_pai = (idx_pai + 1) % n
            count += 1
            
    preencher_restante(filho1, pai2, set_f1)
    preencher_restante(filho2, pai1, set_f2)
    
    return filho1, filho2

def cruzamento_pmx(pai1, pai2):
    """
    Realiza cruzamento Partially Mapped Crossover (PMX) entre dois pais.
    
    PMX preserva segmentos dos pais e mapeia conflitos de forma inteligente.
    
    Args:
        pai1 (list): Primeira rota (pai)
        pai2 (list): Segunda rota (pai)
    
    Returns:
        tuple: (filho1, filho2) - Dois filhos gerados
    """
    n = len(pai1)
    
    # Seleciona dois pontos de corte aleatórios
    ponto1 = random.randint(0, n - 1)
    ponto2 = random.randint(0, n - 1)
    
    if ponto1 > ponto2:
        ponto1, ponto2 = ponto2, ponto1
    
    def criar_filho_pmx(pai_origem, pai_mapeamento):
        """Cria um filho usando PMX"""
        filho = [None] * n
        
        # Copia o segmento do pai_origem
        for i in range(ponto1, ponto2 + 1):
            filho[i] = pai_origem[i]
        
        # Cria mapeamento entre os segmentos
        mapeamento = {}
        for i in range(ponto1, ponto2 + 1):
            if pai_mapeamento[i] not in filho:
                mapeamento[pai_origem[i]] = pai_mapeamento[i]
        
        # Preenche o restante usando o mapeamento
        for i in range(n):
            if filho[i] is None:
                cidade = pai_mapeamento[i]
                # Resolve conflitos usando o mapeamento
                while cidade in filho and cidade in mapeamento:
                    cidade = mapeamento[cidade]
                filho[i] = cidade
        
        return filho
    
    filho1 = criar_filho_pmx(pai1, pai2)
    filho2 = criar_filho_pmx(pai2, pai1)
    
    return filho1, filho2


def mutacao_swap(rota, probabilidade_mutacao=0.1):
    """
    Aplica mutação por troca (swap) em uma rota.
    
    Com uma certa probabilidade, troca duas cidades aleatórias de posição.
    
    Args:
        rota (list): Rota a ser mutada
        probabilidade_mutacao (float): Probabilidade de mutação (0.0 a 1.0)
    
    Returns:
        list: Rota mutada (ou original se não houve mutação)
    """
    if random.random() > probabilidade_mutacao:
        return rota
    
    rota_mutada = rota.copy()
    n = len(rota_mutada)
    
    # Seleciona duas posições aleatórias diferentes
    pos1 = random.randint(0, n - 1)
    pos2 = random.randint(0, n - 1)
    
    while pos1 == pos2:
        pos2 = random.randint(0, n - 1)
    
    # Troca as cidades
    rota_mutada[pos1], rota_mutada[pos2] = rota_mutada[pos2], rota_mutada[pos1]
    
    return rota_mutada


def mutacao_inversao(rota, probabilidade_mutacao=0.1):
    """
    Aplica mutação por inversão em uma rota.
    
    Com uma certa probabilidade, inverte um segmento aleatório da rota.
    
    Args:
        rota (list): Rota a ser mutada
        probabilidade_mutacao (float): Probabilidade de mutação (0.0 a 1.0)
    
    Returns:
        list: Rota mutada (ou original se não houve mutação)
    """
    if random.random() > probabilidade_mutacao:
        return rota
    
    rota_mutada = rota.copy()
    n = len(rota_mutada)
    
    # Seleciona dois pontos aleatórios
    ponto1 = random.randint(0, n - 1)
    ponto2 = random.randint(0, n - 1)
    
    if ponto1 > ponto2:
        ponto1, ponto2 = ponto2, ponto1
    
    # Inverte o segmento
    rota_mutada[ponto1:ponto2+1] = rota_mutada[ponto1:ponto2+1][::-1]
    
    return rota_mutada


def algoritmo_genetico(matriz_distancias, 
                       tamanho_populacao=200,
                       num_geracoes=500,
                       probabilidade_cruzamento=0.9,
                       probabilidade_mutacao=0.05,
                       metodo_selecao='torneio',
                       metodo_cruzamento='ox',
                       metodo_mutacao='inversao',
                       tamanho_torneio=5,
                       taxa_elitismo=0.1):
    """
    Executa o Algoritmo Genético completo para resolver o PCV.
    
    Fluxo principal:
    1. Inicializa população
    2. Avalia população
    3. Para cada geração:
       3.1. Seleciona pais
       3.2. Aplica cruzamento
       3.3. Aplica mutação
       3.4. Forma nova população (com elitismo)
    4. Retorna melhor solução encontrada
    
    Args:
        matriz_distancias (list): Matriz de distâncias entre cidades
        tamanho_populacao (int): Tamanho da população (padrão: 50)
        num_geracoes (int): Número de gerações (padrão: 100)
        probabilidade_cruzamento (float): Probabilidade de cruzamento (0.0 a 1.0)
        probabilidade_mutacao (float): Probabilidade de mutação (0.0 a 1.0)
        metodo_selecao (str): 'roleta' ou 'torneio' (padrão: 'torneio')
        metodo_cruzamento (str): 'ox' ou 'pmx' (padrão: 'ox')
        metodo_mutacao (str): 'swap' ou 'inversao' (padrão: 'swap')
        taxa_elitismo (float): Percentual de melhores indivíduos mantidos (0.0 a 1.0)
    
    Returns:
        tuple: (melhor_rota, melhor_custo, historico_fitness)
            - melhor_rota: Lista com a melhor rota encontrada (com retorno ao início)
            - melhor_custo: Custo da melhor rota
            - historico_fitness: Lista com o melhor fitness de cada geração
    """
    num_cidades = len(matriz_distancias)
    
    # 1. Inicialização da população
    populacao = inicializar_populacao(tamanho_populacao, num_cidades, 
                                      usar_heuristica=True, 
                                      matriz_distancias=matriz_distancias)
    
    # Variáveis para rastreamento
    melhor_custo_global = float('inf')
    melhor_rota_global = None
    historico_fitness = []
    
    # Calcula número de indivíduos para elitismo
    num_elite = max(1, int(tamanho_populacao * taxa_elitismo))

    geracoes_sem_melhora = 0
    taxa_mutacao_atual = probabilidade_mutacao
    
    # 2. Loop principal (gerações)
    for geracao in range(num_geracoes):
        # 2.1. Avaliação da população
        populacao_avaliada = avaliar_populacao(populacao, matriz_distancias)
        
        # Atualiza melhor global
        melhor_fitness_geracao = populacao_avaliada[0][0]
        melhor_rota_geracao = populacao_avaliada[0][1]
        
        # Calcula custo da melhor rota desta geração
        rota_completa = melhor_rota_geracao + [melhor_rota_geracao[0]]
        custo_geracao = calcular_custo_rota(rota_completa, matriz_distancias)
        
        if custo_geracao < melhor_custo_global:
            melhor_custo_global = custo_geracao
            melhor_rota_global = rota_completa.copy()
        
        historico_fitness.append(melhor_fitness_geracao)
        
        # 2.2. Elitismo: mantém os melhores indivíduos
        nova_populacao = [ind[1] for ind in populacao_avaliada[:num_elite]]
        
        # 2.3. Gera novos indivíduos até completar a população
        while len(nova_populacao) < tamanho_populacao:
            # Seleção de pais
            if metodo_selecao == 'roleta':
                pais = selecao_roleta(populacao_avaliada, 2)
            else: # torneio
                pais = selecao_torneio(populacao_avaliada, 2, tamanho_torneio=tamanho_torneio)
            
            pai1, pai2 = pais[0], pais[1]
            
            # Cruzamento
            if random.random() < probabilidade_cruzamento:
                if metodo_cruzamento == 'ox':
                    filho1, filho2 = cruzamento_ox(pai1, pai2)
                else:  # pmx
                    filho1, filho2 = cruzamento_pmx(pai1, pai2)
            else:
                # Sem cruzamento, os filhos são cópias dos pais
                filho1, filho2 = pai1.copy(), pai2.copy()
            
            # Mutação
            if metodo_mutacao == 'swap':
                filho1 = mutacao_swap(filho1, probabilidade_mutacao)
                filho2 = mutacao_swap(filho2, probabilidade_mutacao)
            else:  # inversao
                filho1 = mutacao_inversao(filho1, probabilidade_mutacao)
                filho2 = mutacao_inversao(filho2, probabilidade_mutacao)
            
            # Adiciona os filhos à nova população
            if filho1 != pai1 and filho1 != pai2:
                nova_populacao.append(filho1)
            else:
                # Se for clone, aplica uma mutação forçada para diferenciar
                nova_populacao.append(mutacao_inversao(filho1, probabilidade_mutacao=1.0))

            if len(nova_populacao) < tamanho_populacao:
                if filho2 != pai1 and filho2 != pai2:
                    nova_populacao.append(filho2)
                else:
                    nova_populacao.append(mutacao_inversao(filho2, probabilidade_mutacao=1.0))
        
        # Atualiza população para próxima geração
        populacao = nova_populacao
    
    return melhor_rota_global, melhor_custo_global, historico_fitness
