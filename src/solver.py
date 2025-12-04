import random
import copy
from src.utils import calcular_custo_rota

def vizinho_mais_proximo(matriz_distancias, cidade_inicial):
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
    cidade_atual = cidade_inicial
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

def insercao_mais_barata(matriz_distancias, vertice_inicial):
    """
    Implementa a Heurística Construtiva de Inserção Mais Barata.
    
    Lógica:
    1. Começa com um pequeno ciclo: O vértice inicial e seu vizinho mais próximo.
    2. Iterativamente insere o vértice que causa o menor aumento de custo na rota.
    3. Repete até incluir todos os vértices.
    
    Args:
        matriz_distancias (list): Matriz NxN.
        vertice_inicial (int): Vértice de início da rota.
        
    Returns:
        list: A rota construída (ex: [0, 2, 1, 3, 0])
    """
    num_cidades = len(matriz_distancias)
    
    # Passo inicial: encontrar o vértice mais próximo de s (escolha gulosa)
    vertice_proximo = -1
    menor_distancia = float('inf')
    for vertice in range(num_cidades):
        if vertice != vertice_inicial:
            distancia = matriz_distancias[vertice_inicial][vertice]
            if distancia < menor_distancia:
                menor_distancia = distancia
                vertice_proximo = vertice
    
    rota = [vertice_inicial, vertice_proximo, vertice_inicial]
    
    vertices_inseridos = {vertice_inicial, vertice_proximo}
    
    vertices_restantes = set(range(num_cidades)) - vertices_inseridos
    
    while vertices_restantes:
        # Passo 1: escolher o vértice mais próximo do ciclo atual
        melhor_vertice = None
        menor_dist_ao_ciclo = float('inf')
        
        for vertice_r in vertices_restantes:
            dist_r = float('inf')
            for vertice_i in vertices_inseridos:
                dist_r = min(dist_r, matriz_distancias[vertice_r][vertice_i])
            
            # Escolher r* = argmin_r(dist_r)
            if dist_r < menor_dist_ao_ciclo:
                menor_dist_ao_ciclo = dist_r
                melhor_vertice = vertice_r
                
        # Passo 2: encontrar melhor posição para inserção de melhor_vertice
        melhor_custo = float('inf')
        melhor_posicao = None
        
        # Para i de 1 até |rota|-1 (excluindo a última posição que é igual à primeira)
        for i in range(1, len(rota) - 1):
            vertice_anterior = rota[i - 1]  
            vertice_atual = rota[i]      
            
            custo = (matriz_distancias[vertice_anterior][melhor_vertice] + 
                    matriz_distancias[melhor_vertice][vertice_atual] - 
                    matriz_distancias[vertice_anterior][vertice_atual])
            
            if custo < melhor_custo:
                melhor_custo = custo
                melhor_posicao = i
        
        rota.insert(melhor_posicao, melhor_vertice)
        vertices_inseridos.add(melhor_vertice)
        vertices_restantes.remove(melhor_vertice)
    
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