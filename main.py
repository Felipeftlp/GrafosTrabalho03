import sys
import time
import argparse
import statistics
from src.utils import ler_matriz_csv, ler_nomes_cidades, calcular_custo_rota, extrair_submatriz_por_ids
from src.solver import vizinho_mais_proximo, busca_local_2opt

# --- CONFIGURAÇÃO DOS 12 PROBLEMAS ---
# Mapeia o ID do problema para o tipo de matriz e a lista de cidades
CONFIG_PROBLEMAS = {
    1:  {'tipo': 'km',  'cidades': list(range(1, 49))},                 # 1 a 48
    2:  {'tipo': 'min', 'cidades': list(range(1, 49))},                 # 1 a 48
    3:  {'tipo': 'km',  'cidades': list(range(1, 37))},                 # 1 a 36
    4:  {'tipo': 'min', 'cidades': list(range(1, 37))},                 # 1 a 36
    5:  {'tipo': 'km',  'cidades': list(range(1, 25))},                 # 1 a 24
    6:  {'tipo': 'min', 'cidades': list(range(1, 25))},                 # 1 a 24
    7:  {'tipo': 'km',  'cidades': list(range(1, 13))},                 # 1 a 12
    8:  {'tipo': 'min', 'cidades': list(range(1, 13))},                 # 1 a 12
    9:  {'tipo': 'km',  'cidades': [1, 7, 8, 9, 10, 11, 12]},           # Específicos
    10: {'tipo': 'min', 'cidades': [1, 7, 8, 9, 10, 11, 12]},           # Específicos
    11: {'tipo': 'km',  'cidades': list(range(1, 7))},                  # 1 a 6
    12: {'tipo': 'min', 'cidades': list(range(1, 7))}                   # 1 a 6
}

def executar_uma_vez(algoritmo, matriz_problema):
    """Executa uma única iteração do algoritmo escolhido."""
    rota = []
    custo = float('inf')
    
    if algoritmo == 1: # Vizinho Mais Próximo + 2-Opt
        # inicio_aleatorio=True garante variedade nas 20 execuções
        rota_ini = vizinho_mais_proximo(matriz_problema, inicio_aleatorio=True) 
        rota = busca_local_2opt(rota_ini, matriz_problema)
        custo = calcular_custo_rota(rota, matriz_problema)
        
    elif algoritmo == 2: # Inserção Mais Barata
        # TODO: Chamar função do Integrante 2
        pass 
        
    elif algoritmo == 3: # Genético
        # TODO: Chamar função do Integrante 3
        pass
        
    elif algoritmo == 4: # Memético
        # TODO: Chamar função do Integrante 4
        pass

    return custo, rota

def main():
    parser = argparse.ArgumentParser(description='PCV Solver - 12 Problemas')
    parser.add_argument('--alg', type=int, required=True, help='1: Vizinho+BL, 2: Insercao, 3: Genetico, 4: Memetico')
    parser.add_argument('--prob', type=int, required=True, help='Número do problema (1 a 12)')
    args = parser.parse_args()

    # 1. Validar e Carregar Configuração
    config = CONFIG_PROBLEMAS.get(args.prob)
    if not config:
        print(f"Erro: Problema {args.prob} inválido. Escolha de 1 a 12.")
        sys.exit(1)

    tipo_arquivo = config['tipo']
    ids_cidades = config['cidades']
    
    # Define nomes dos arquivos baseados no tipo
    arquivo_matriz = "PCV__Matriz_do_problema - Km.csv" if tipo_arquivo == 'km' else "PCV__Matriz_do_problema - Min.csv"
    arquivo_cidades = "PCV__Matriz_do_problema - Cidades.csv"
    
    print(f"[*] Configurando Problema {args.prob}")
    print(f"    - Tipo: {tipo_arquivo.upper()}")
    print(f"    - Cidades ({len(ids_cidades)}): {ids_cidades}")
    print(f"    - Lendo arquivo: {arquivo_matriz}")

    # 2. Leitura dos Arquivos
    matriz_completa = ler_matriz_csv(arquivo_matriz)
    nomes_cidades = ler_nomes_cidades(arquivo_cidades)
    
    if not matriz_completa:
        print("Erro fatal: Falha ao ler matriz.")
        sys.exit(1)

    # 3. Extração da Submatriz
    # Usa a função criada no utils.py para pegar apenas as linhas/colunas certas
    matriz_problema = extrair_submatriz_por_ids(matriz_completa, ids_cidades)

    # 4. Execução (20x para estatística)
    # Se for Genético/Memético ou se quisermos estatística do Vizinho Aleatório
    n_execucoes = 20 
    
    print(f"[*] Rodando {n_execucoes} execuções do Algoritmo {args.alg}...")
    
    resultados = []
    tempos = []
    melhor_global_custo = float('inf')
    melhor_global_rota = []

    t_inicio_total = time.time()

    for i in range(n_execucoes):
        t0 = time.time()
        custo, rota = executar_uma_vez(args.alg, matriz_problema)
        t_exec = time.time() - t0
        
        # Validação simples
        if custo > 0:
            resultados.append(custo)
            tempos.append(t_exec)
            
            if custo < melhor_global_custo:
                melhor_global_custo = custo
                melhor_global_rota = rota

    tempo_total_script = time.time() - t_inicio_total

    # 5. Cálculo de Estatísticas
    if not resultados:
        print("Nenhum resultado válido gerado.")
        sys.exit(0)

    media_sol = statistics.mean(resultados)
    media_tempo = statistics.mean(tempos)
    melhor_sol = min(resultados)

    print("-" * 50)
    print(f"RESULTADO FINAL (Problema {args.prob})")
    print(f"Melhor Solução: {melhor_sol:.2f}")
    print(f"Média Soluções: {media_sol:.2f}")
    print(f"Tempo Médio:    {media_tempo:.4f}s")
    
    # Tradução da Rota (Índice Local -> ID Real -> Nome da Cidade)
    rota_nomes = []
    rota_ids = []
    for idx_local in melhor_global_rota:
        id_real = ids_cidades[idx_local]
        rota_ids.append(str(id_real))
        # Usa o dicionário de nomes (get retorna o ID se não achar o nome)
        nome = nomes_cidades.get(id_real, f"ID{id_real}")
        rota_nomes.append(nome)
        
    print(f"Rota (IDs): {' -> '.join(rota_ids)}")
    print(f"Rota (Nomes): {' -> '.join(rota_nomes)}")
    print("-" * 50)

    # 6. Salvar em Markdown (Tabela Acumulativa)
    try:
        with open("output/resumo_resultados.md", "a") as f:
            # Cria o arquivo se não existir, adiciona header se vazio
            if f.tell() == 0:
                f.write("| Problema | Algoritmo | Melhor Solução | Média Soluções | Tempo Médio |\n")
                f.write("| :--- | :--- | :--- | :--- | :--- |\n")
            
            unidade = "Km" if tipo_arquivo == 'km' else "Min"
            linha = f"| {args.prob} ({unidade}) | {args.alg} | {melhor_sol:.2f} | {media_sol:.2f} | {media_tempo:.4f} |\n"
            f.write(linha)
            print("[*] Salvo em output/resumo_resultados.md")
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")

if __name__ == "__main__":
    main()