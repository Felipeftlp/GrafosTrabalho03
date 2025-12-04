import random
import copy
from src.utils import calcular_custo_rota

def vizinho_mais_proximo(matriz_distancias, inicio_aleatorio=False, cidade_inicial=0):
    """
    Implementa a Heurística Construtiva do Vizinho Mais Próximo (Nearest Neighbor).
    
    Lógica:
    1. Escolhe uma cidade inicial.
    2. Viaja para a cidade não visitada mais próxima.
    3. Repete até visitar todas.
    4. Retorna à cidade inicial.
    
    Args:
        matriz_distancias (list): Matriz NxN.
        inicio_aleatorio (bool): Se True, começa de uma cidade random. Se False, usa cidade_inicial.
        cidade_inicial (int): Cidade inicial quando inicio_aleatorio=False (padrão: 0)
        
    Returns:
        list: A rota construída (ex: [0, 4, 1, 2, 3, 0])
    """
    num_cidades = len(matriz_distancias)
    visitadas = set()
    
    # Passo 1: Escolher cidade inicial
    cidade_atual = random.randint(0, num_cidades - 1) if inicio_aleatorio else cidade_inicial
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
    print(f"Numero de cidades: {num_cidades}")
    
    # Passo inicial: encontrar o vértice mais próximo de s (escolha gulosa)
    v0 = -1
    menor_distancia = float('inf')
    for v in range(num_cidades):
        if v != vertice_inicial:
            distancia = matriz_distancias[vertice_inicial][v]
            if distancia < menor_distancia:
                menor_distancia = distancia
                v0 = v
    
    # Inicializar rota com ciclo inicial [s, v0, s]
    rota = [vertice_inicial, v0, vertice_inicial]
    
    # C: vértices já inseridos
    C = {vertice_inicial, v0}
    
    # R: vértices restantes
    R = set(range(num_cidades)) - C
    
    # Loop principal: enquanto há vértices para inserir
    while R:
        # Passo 1: escolher o vértice mais próximo do ciclo atual
        melhor_r = None
        menor_dist_ao_ciclo = float('inf')
        
        for r in R:
            # Calcular distância mínima de r para qualquer vértice em C
            dist_r = float('inf')
            for c in C:
                dist_r = min(dist_r, matriz_distancias[r][c])
            
            # Escolher r* = argmin_r(dist_r)
            if dist_r < menor_dist_ao_ciclo:
                menor_dist_ao_ciclo = dist_r
                melhor_r = r
        
        r_estrela = melhor_r
        
        # Passo 2: encontrar melhor posição para inserção de r*
        melhor_custo = float('inf')
        melhor_pos = None
        
        # Para i de 1 até |rota|-1 (excluindo a última posição que é igual à primeira)
        for i in range(1, len(rota) - 1):
            u = rota[i - 1]  # vértice anterior
            v = rota[i]      # vértice atual
            
            # Calcular custo de inserção: d(u, r*) + d(r*, v) - d(u, v)
            custo = (matriz_distancias[u][r_estrela] + 
                    matriz_distancias[r_estrela][v] - 
                    matriz_distancias[u][v])
            
            if custo < melhor_custo:
                melhor_custo = custo
                melhor_pos = i
        
        # Inserir r* na melhor posição encontrada
        rota.insert(melhor_pos, r_estrela)
        
        # Atualizar conjuntos
        C.add(r_estrela)
        R.remove(r_estrela)
    
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