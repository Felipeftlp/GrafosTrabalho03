"""
Algoritmo Memético para o Problema do Caixeiro Viajante (PCV)

Este módulo implementa um Algoritmo Memético completo para resolver o PCV,
seguindo a estrutura:
1. Inicialização de população
2. Avaliação (fitness)
3. Seleção de pais
4. Cruzamento
5. Mutação
6. Busca uma melhoria na população com auxílio de buscas locais
7. Formação de nova população
8. Repetição até critério de parada

"""

import random
import copy
from src.utils import calcular_custo_rota
# Estamos reutilizando funções do algoritmo genético
from src.genetico import mutacao_inversao, mutacao_swap, cruzamento_ox, cruzamento_pmx
from src.genetico import selecao_roleta, selecao_torneio, avaliar_populacao, inicializar_populacao

def mutacao_shift(rota, probabilidade_mutacao=0.1):
    """
    Aplica mutação por deslocamento (shift) em uma rota.
    
    Com uma certa probabilidade, remove uma cidade de uma posição
    e reinsere em outra posição da rota.
    
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

    # Seleciona a posição de origem e destino (devem ser diferentes)
    origem = random.randint(0, n - 1)
    destino = random.randint(0, n - 1)

    while origem == destino:
        destino = random.randint(0, n - 1)

    # Remove a cidade da posição de origem
    cidade = rota_mutada.pop(origem)  # cidade removida

    # Insere a cidade na nova posição
    # Obs.: após o pop, o tamanho reduz, então destino pode mudar
    if destino > origem:
        destino -= 1  # ajusta índice se necessário

    rota_mutada.insert(destino, cidade)

    return rota_mutada

def mutacao_2_opt(rota, probabilidade_mutacao=0.1):
    """
    Aplica mutação 2-OPT em uma rota.

    Remove duas arestas e reconecta invertendo o segmento entre duas posições.
    """
    if random.random() > probabilidade_mutacao:
        return rota

    n = len(rota)
    rota_mutada = rota.copy()

    # Seleciona duas posições distintas
    i = random.randint(0, n - 2)
    j = random.randint(i + 1, n - 1)

    # Inverte o segmento entre i e j
    rota_mutada[i:j+1] = reversed(rota_mutada[i:j+1])

    return rota_mutada

def busca_local_2_opt(rota, matriz_distancias):
    # Cálculo do custo atual
    melhor_rota = rota
    melhor_custo = calcular_custo_rota(rota + [rota[0]], matriz_distancias)

    # Executa tentativas de melhoria
    for _ in range(len(rota)):
        nova = mutacao_2_opt(melhor_rota, probabilidade_mutacao=1.0)
        novo_custo = calcular_custo_rota(nova + [nova[0]], matriz_distancias)

        if novo_custo < melhor_custo:
            melhor_rota = nova
            melhor_custo = novo_custo

    return melhor_rota

def busca_local_shift(rota, matriz_distancias):
    # Custo atual
    melhor_rota = rota
    melhor_custo = calcular_custo_rota(rota + [rota[0]], matriz_distancias)

    # Tenta até achar uma melhoria
    for _ in range(len(rota)):
        nova = mutacao_shift(melhor_rota, probabilidade_mutacao=1.0)
        novo_custo = calcular_custo_rota(nova + [nova[0]], matriz_distancias)

        if novo_custo < melhor_custo:
            melhor_rota = nova
            melhor_custo = novo_custo

    return melhor_rota


def busca_local_swap(rota, matriz_distancias):
    # Custo atual
    melhor_rota = rota
    melhor_custo = calcular_custo_rota(rota + [rota[0]], matriz_distancias)

    # Tenta até achar uma melhoria
    for _ in range(len(rota)):
        nova = mutacao_swap(melhor_rota, probabilidade_mutacao=1.0)
        novo_custo = calcular_custo_rota(nova + [nova[0]], matriz_distancias)

        if novo_custo < melhor_custo:
            melhor_rota = nova
            melhor_custo = novo_custo

    return melhor_rota


def busca_local_inversao(rota, matriz_distancias):
    # Custo atual
    melhor_rota = rota
    melhor_custo = calcular_custo_rota(rota + [rota[0]], matriz_distancias)

    # Tenta até achar uma melhoria
    for _ in range(len(rota)):
        nova = mutacao_inversao(melhor_rota, probabilidade_mutacao=1.0)
        novo_custo = calcular_custo_rota(nova + [nova[0]], matriz_distancias)

        if novo_custo < melhor_custo:
            melhor_rota = nova
            melhor_custo = novo_custo

    return melhor_rota


def algoritmo_memetico(matriz_distancias, 
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
    Executa o Algoritmo Memético completo para resolver o PCV.
    
    Fluxo principal:
    1. Inicializa população
    2. Avalia população
    3. Para cada geração:
       3.1. Seleciona pais
       3.2. Aplica cruzamento
       3.3. Aplica mutação
       3.4. Aplica busca local para melhoria
       3.5. Forma nova população (com elitismo)
    4. Retorna melhor solução encontrada
    
    Args:
        matriz_distancias (list): Matriz de distâncias entre cidades
        tamanho_populacao (int): Tamanho da população (padrão: 50)
        num_geracoes (int): Número de gerações (padrão: 100)
        probabilidade_cruzamento (float): Probabilidade de cruzamento (0.0 a 1.0)
        probabilidade_mutacao (float): Probabilidade de mutação (0.0 a 1.0)
        metodo_selecao (str): 'roleta' ou 'torneio' (padrão: 'torneio')
        metodo_cruzamento (str): 'ox' ou 'pmx' (padrão: 'ox')
        metodo_mutacao (str): 'swap', 'shift' ou 'inversao' (padrão: 'swap')
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
            elif metodo_mutacao == 'shift':
                filho1 = mutacao_shift(filho1, probabilidade_mutacao)
                filho2 = mutacao_shift(filho2, probabilidade_mutacao)
            else:
                filho1 = mutacao_inversao(filho1, probabilidade_mutacao)
                filho2 = mutacao_inversao(filho2, probabilidade_mutacao)

            # Busca local de melhoria (Escolhe aleatoriamente uma das quatro estratégias)
            escolha = random.choice(['shift', 'swap', 'inversao', '2opt'])
            if escolha == 'shift':
                filho1 = busca_local_shift(filho1, matriz_distancias)
                filho2 = busca_local_shift(filho2, matriz_distancias)
            elif escolha == 'swap':
                filho1 = busca_local_swap(filho1, matriz_distancias)
                filho2 = busca_local_swap(filho2, matriz_distancias)
            elif escolha == 'inversao':
                filho1 = busca_local_inversao(filho1, matriz_distancias)
                filho2 = busca_local_inversao(filho2, matriz_distancias)
            else:  # '2opt'
                filho1 = busca_local_2_opt(filho1, matriz_distancias)
                filho2 = busca_local_2_opt(filho2, matriz_distancias)

            
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
