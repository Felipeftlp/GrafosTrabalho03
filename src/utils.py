import csv

def ler_nomes_cidades(caminho_arquivo):
    """
    Lê o arquivo de Cidades considerando que ele pode ter múltiplas colunas de dados.
    Formato observado: ID, NOME, ID, NOME
    """
    nomes = {}
    codificacoes = ['utf-8-sig', 'latin-1', 'cp1252'] # Tenta várias codificações
    
    for encoding in codificacoes:
        try:
            with open(caminho_arquivo, 'r', encoding=encoding) as f:
                leitor = csv.reader(f)
                for linha in leitor:
                    # Limpa espaços em branco de cada célula
                    linha = [x.strip() for x in linha]
                    
                    # Tenta ler par 1 (Colunas 0 e 1)
                    if len(linha) >= 2 and linha[0].isdigit():
                        nomes[int(linha[0])] = linha[1]
                        
                    # Tenta ler par 2 (Colunas 2 e 3) - O arquivo que você mandou tem isso
                    if len(linha) >= 4 and linha[2].isdigit():
                        nomes[int(linha[2])] = linha[3]
            
            # Se leu com sucesso, para o loop de codificações
            if len(nomes) > 0:
                break
                
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"[Aviso] Erro ao ler cidades com {encoding}: {e}")

    return nomes

def ler_matriz_csv(caminho_arquivo):
    """
    Lê a matriz tratando aspas, vírgulas decimais e possíveis falhas de formatação.
    Retorna uma lista de listas (Matriz NxN).
    """
    dados_brutos = {}
    max_id = 0
    
    # Tenta abrir com utf-8-sig (padrão Excel) ou latin-1
    codificacoes = ['utf-8-sig', 'latin-1']
    linhas_validas = []

    for encoding in codificacoes:
        try:
            with open(caminho_arquivo, 'r', encoding=encoding) as f:
                leitor = csv.reader(f) # O csv.reader já trata as aspas "38,8" automaticamente
                linhas_validas = list(leitor)
            if linhas_validas:
                break
        except UnicodeDecodeError:
            continue
            
    if not linhas_validas:
        print("[Erro Crítico] Não foi possível ler o arquivo da matriz (Encoding).")
        return []

    # Processa as linhas lidas
    for linha in linhas_validas:
        if not linha: continue
        
        # Pega a primeira célula (ID da linha)
        primeira_celula = linha[0].strip()
        
        if primeira_celula.isdigit():
            id_linha = int(primeira_celula)
            max_id = max(max_id, id_linha)
            valores_linha = []
            
            # Itera sobre as colunas de dados (pula a primeira que é o ID)
            # O arquivo tem ID na col 0, então dados começam na col 1
            for val_str in linha[1:]:
                val_str = val_str.strip()
                
                # Célula vazia (geralmente a diagonal principal) -> 0.0
                if val_str == '':
                    valores_linha.append(0.0)
                    continue
                
                # Trata decimal: "38,8" (já sem aspas graças ao csv.reader) vira "38.8"
                val_str = val_str.replace(',', '.')
                
                try:
                    val = float(val_str)
                    valores_linha.append(val)
                except ValueError:
                    # Se não for número, assume infinito (bloqueio)
                    valores_linha.append(float('inf'))
            
            dados_brutos[id_linha] = valores_linha

    # Monta a matriz final quadrada ordenada por ID (1 a 48)
    matriz_final = []
    # Se max_id for detectado como 0 (arquivo vazio), retorna erro
    if max_id == 0:
        return []

    for i in range(1, max_id + 1):
        linha = dados_brutos.get(i, [])
        
        # Preenchimento de segurança: se a linha for curta, completa com Infinito
        if len(linha) < max_id:
            linha += [float('inf')] * (max_id - len(linha))
            
        # Pega apenas as primeiras 'max_id' colunas (caso haja lixo no final da linha)
        matriz_final.append(linha[:max_id])
            
    return matriz_final

def extrair_submatriz_por_ids(matriz_completa, lista_ids_reais):
    """
    Cria a sub-matriz apenas com as cidades solicitadas.
    """
    if not matriz_completa:
        return []
        
    nova_matriz = []
    indices_python = [id_real - 1 for id_real in lista_ids_reais]
    
    total_linhas = len(matriz_completa)
    
    for i in indices_python:
        if i >= total_linhas:
            # Proteção se pedir ID 48 mas matriz só tem 47 linhas
            linha_nova = [float('inf')] * len(indices_python)
        else:
            linha_orig = matriz_completa[i]
            linha_nova = []
            for j in indices_python:
                if j < len(linha_orig):
                    linha_nova.append(linha_orig[j])
                else:
                    linha_nova.append(float('inf'))
        nova_matriz.append(linha_nova)
        
    return nova_matriz

def calcular_custo_rota(rota, matriz_distancias):
    """
    Calcula custo. Retorna Infinito se a rota for inválida ou incompleta.
    """
    # Uma rota válida de TSP para N cidades tem tamanho N+1 (volta ao início)
    if len(rota) < len(matriz_distancias) + 1:
        return float('inf')
        
    custo = 0
    for i in range(len(rota) - 1):
        u, v = rota[i], rota[i+1]
        dist = matriz_distancias[u][v]
        if dist == float('inf'):
            return float('inf')
        custo += dist
    return custo