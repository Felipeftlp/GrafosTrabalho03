import sys
import time
import argparse
import statistics
from src.utils import ler_matriz_csv, ler_nomes_cidades, calcular_custo_rota, extrair_submatriz_por_ids
from src.solver import vizinho_mais_proximo, busca_local_2opt
from src.genetico import algoritmo_genetico

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
        # Executa o algoritmo genético
        rota, custo, _ = algoritmo_genetico(
            matriz_problema,
            tamanho_populacao=50,
            num_geracoes=100,
            probabilidade_cruzamento=0.8,
            probabilidade_mutacao=0.1,
            metodo_selecao='torneio',
            metodo_cruzamento='ox',
            metodo_mutacao='swap',
            taxa_elitismo=0.1
        )
        
    elif algoritmo == 4: # Memético
        # TODO: Chamar função do Integrante 4
        pass

    return custo, rota

def executar_problema(args, num_problema):
    """
    Executa um problema específico com 20 iterações.
    
    Args:
        args: Argumentos da linha de comando
        num_problema (int): Número do problema (1 a 12)
    
    Returns:
        dict: Dicionário com os resultados do problema
    """
    # 1. Validar e Carregar Configuração
    config = CONFIG_PROBLEMAS.get(num_problema)
    if not config:
        print(f"Erro: Problema {num_problema} inválido. Escolha de 1 a 12.")
        return None

    tipo_arquivo = config['tipo']
    ids_cidades = config['cidades']
    
    # Define nomes dos arquivos baseados no tipo
    arquivo_matriz = "PCV__Matriz_do_problema - Km.csv" if tipo_arquivo == 'km' else "PCV__Matriz_do_problema - Min.csv"
    arquivo_cidades = "PCV__Matriz_do_problema - Cidades.csv"
    
    print(f"\n{'='*70}")
    print(f"[*] Executando Problema {num_problema}")
    print(f"    - Tipo: {tipo_arquivo.upper()}")
    print(f"    - Cidades ({len(ids_cidades)}): {ids_cidades[:5]}..." if len(ids_cidades) > 5 else f"    - Cidades ({len(ids_cidades)}): {ids_cidades}")
    print(f"    - Lendo arquivo: {arquivo_matriz}")

    # 2. Leitura dos Arquivos
    matriz_completa = ler_matriz_csv(arquivo_matriz)
    nomes_cidades = ler_nomes_cidades(arquivo_cidades)
    
    if not matriz_completa:
        print(f"Erro fatal: Falha ao ler matriz para problema {num_problema}.")
        return None

    # 3. Extração da Submatriz
    matriz_problema = extrair_submatriz_por_ids(matriz_completa, ids_cidades)

    # 4. Execução (20x para estatística)
    n_execucoes = 20 
    
    print(f"[*] Rodando {n_execucoes} execuções do Algoritmo {args.alg}...")
    
    resultados = []
    tempos = []
    melhor_global_custo = float('inf')
    melhor_global_rota = []

    t_inicio_total = time.time()

    for i in range(n_execucoes):
        print(f"    Execução {i+1}/{n_execucoes}...", end='\r')
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
    print(f"    Execução {n_execucoes}/{n_execucoes} concluída!          ")

    # 5. Cálculo de Estatísticas
    if not resultados:
        print(f"    Nenhum resultado válido gerado para problema {num_problema}.")
        return None

    media_sol = statistics.mean(resultados)
    media_tempo = statistics.mean(tempos)
    melhor_sol = min(resultados)

    print(f"    Melhor Solução: {melhor_sol:.2f}")
    print(f"    Média Soluções: {media_sol:.2f}")
    print(f"    Tempo Médio:    {media_tempo:.4f}s")
    print(f"{'='*70}")

    # 6. Salvar em Markdown (Tabela Acumulativa)
    try:
        with open("output/resumo_resultados.md", "a") as f:
            # Cria o arquivo se não existir, adiciona header se vazio
            if f.tell() == 0:
                f.write("| Problema | Algoritmo | Melhor Solução | Média Soluções | Tempo Médio |\n")
                f.write("| :--- | :--- | :--- | :--- | :--- |\n")
            
            unidade = "Km" if tipo_arquivo == 'km' else "Min"
            linha = f"| {num_problema} ({unidade}) | {args.alg} | {melhor_sol:.2f} | {media_sol:.2f} | {media_tempo:.4f} |\n"
            f.write(linha)
    except Exception as e:
        print(f"    Erro ao salvar arquivo MD: {e}")

    # 7. Salvar em TXT (para algoritmos genéticos e meméticos)
    resultado_dict = None
    if args.alg in [3, 4]:  # Genético ou Memético
        try:
            nome_arquivo = "output/resumo_resultados.txt"
            with open(nome_arquivo, "a") as f:
                # Escreve cabeçalho se arquivo estiver vazio
                if f.tell() == 0:
                    f.write("=" * 70 + "\n")
                    f.write("RESUMO DE RESULTADOS - ALGORITMOS EVOLUTIVOS\n")
                    f.write("=" * 70 + "\n\n")
                
                unidade = "Km" if tipo_arquivo == 'km' else "Min"
                nome_algoritmo = "Algoritmo Genético" if args.alg == 3 else "Algoritmo Memético"
                
                f.write(f"Instância: Problema {num_problema} ({unidade})\n")
                f.write(f"Algoritmo: {nome_algoritmo}\n")
                f.write(f"Menor valor encontrado: {melhor_sol:.2f} {unidade}\n")
                f.write(f"Valor médio: {media_sol:.2f} {unidade}\n")
                f.write(f"Tempo médio de execução: {media_tempo:.4f} segundos\n")
                f.write("-" * 70 + "\n\n")
            
            resultado_dict = {
                'problema': num_problema,
                'tipo': tipo_arquivo,
                'unidade': unidade,
                'melhor_sol': melhor_sol,
                'media_sol': media_sol,
                'media_tempo': media_tempo
            }
        except Exception as e:
            print(f"    Erro ao salvar arquivo TXT: {e}")

    return resultado_dict

def main():
    parser = argparse.ArgumentParser(description='PCV Solver - 12 Problemas')
    parser.add_argument('--alg', type=int, required=True, help='1: Vizinho+BL, 2: Insercao, 3: Genetico, 4: Memetico')
    parser.add_argument('--prob', type=int, help='Número do problema (1 a 12). Use --all para executar todos.')
    parser.add_argument('--all', action='store_true', help='Executa todos os 12 problemas automaticamente')
    args = parser.parse_args()

    # Validação: deve ter --prob OU --all
    if not args.all and args.prob is None:
        print("Erro: Você deve especificar --prob <número> ou --all para executar todos os problemas.")
        sys.exit(1)

    # Se --all foi especificado, executa todos os 12 problemas
    if args.all:
        print("\n" + "="*70)
        print("EXECUTANDO TODOS OS 12 PROBLEMAS")
        print(f"Algoritmo: {args.alg}")
        print("="*70)
        
        # Limpa o arquivo TXT antes de começar (apenas para algoritmos evolutivos)
        if args.alg in [3, 4]:
            try:
                with open("output/resumo_resultados.txt", "w") as f:
                    f.write("=" * 70 + "\n")
                    f.write("RESUMO DE RESULTADOS - ALGORITMOS EVOLUTIVOS\n")
                    f.write("=" * 70 + "\n\n")
            except:
                pass
        
        tempo_inicio_total = time.time()
        resultados_todos = []
        
        # Executa cada problema de 1 a 12
        for num_prob in range(1, 13):
            resultado = executar_problema(args, num_prob)
            if resultado:
                resultados_todos.append(resultado)
        
        tempo_total = time.time() - tempo_inicio_total
        
        # Resumo final
        print("\n" + "="*70)
        print("RESUMO FINAL - TODAS AS INSTÂNCIAS")
        print("="*70)
        print(f"Total de problemas executados: {len(resultados_todos)}/12")
        print(f"Tempo total de execução: {tempo_total:.2f} segundos ({tempo_total/60:.2f} minutos)")
        print(f"Arquivo de resultados: output/resumo_resultados.txt")
        print("="*70 + "\n")
        
    else:
        # Executa apenas um problema específico
        executar_problema(args, args.prob)

if __name__ == "__main__":
    main()