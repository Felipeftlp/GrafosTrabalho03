import random
import copy
from src.utils import calcular_custo_rota

def vizinho_mais_proximo(matriz_distancias, inicio_aleatorio=False):
    """
    Implementa a Heurística Construtiva do Vizinho Mais Próximo (Nearest Neighbor).
    
    Lógica:
    1. Escolhe uma cidade inicial.
    2. Viaja para a cidade não visitada mais próxima.
    3. Repete até visitar todas.
    4. Retorna à cidade inicial.
    
    Args:
        matriz_distancias (list): Matriz NxN.
        inicio_aleatorio (bool): Se True, começa de uma cidade random. Se False, começa da 0.
        
    Returns:
        list: A rota construída (ex: [0, 4, 1, 2, 3, 0])
    """
    num_cidades = len(matriz_distancias)
    visitadas = set()
    
    # Passo 1: Escolher cidade inicial
    cidade_atual = random.randint(0, num_cidades - 1) if inicio_aleatorio else 0
    rota = [cidade_atual]
    visitadas.add(cidade_atual)
    
    # Passo 2 e 3: Construir a rota
    while len(visitadas) < num_cidades:
        melhor_distancia = float('inf')
        proxima_cidade = -1
        
        # Procura o vizinho mais próximo não visitado
        for candidato in range(num_cidades):
            if candidato not in visitadas:
                distancia = matriz_distancias[cidade_atual][candidato]
                if distancia < melhor_distancia:
                    melhor_distancia = distancia
                    proxima_cidade = candidato
        
        # Move para a próxima cidade
        if proxima_cidade != -1:
            rota.append(proxima_cidade)
            visitadas.add(proxima_cidade)
            cidade_atual = proxima_cidade
        else:
            # Caso de erro (grafo desconexo), mas improvável em TSP completo
            break
            
    # Passo 4: Retorna ao início para fechar o ciclo
    rota.append(rota[0])
    
    return rota

def busca_local_2opt(rota, matriz_distancias):
    """
    Aplica a busca local 2-Opt (Best Improvement ou First Improvement).
    O objetivo é remover cruzamentos na rota trocando arestas.
    
    Args:
        rota (list): Rota inicial completa (ex: [0, 1, 2, 0])
        matriz_distancias (list): Matriz de custos.
        
    Returns:
        list: Rota otimizada.
    """
    melhor_rota = copy.deepcopy(rota)
    melhor_custo = calcular_custo_rota(melhor_rota, matriz_distancias)
    
    melhoria = True
    
    while melhoria:
        melhoria = False
        # Percorre todas as arestas possíveis para troca (i e j)
        # Ignora a primeira e última aresta fixa de retorno se necessário, 
        # mas aqui tratamos rota completa.
        for i in range(1, len(melhor_rota) - 2):
            for j in range(i + 1, len(melhor_rota) - 1):
                
                # Cria uma nova rota trocando as arestas
                # A lógica do 2-opt é inverter o segmento entre i e j
                nova_rota = melhor_rota[:i] + melhor_rota[i:j+1][::-1] + melhor_rota[j+1:]
                
                novo_custo = calcular_custo_rota(nova_rota, matriz_distancias)
                
                if novo_custo < melhor_custo:
                    melhor_custo = novo_custo
                    melhor_rota = nova_rota
                    melhoria = True # Continua buscando se achou melhoria
                    # Se fosse First Improvement, poderíamos dar break aqui
                    
    return melhor_rota