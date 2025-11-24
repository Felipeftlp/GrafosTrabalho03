from src.utils import ler_matriz_csv, ler_nomes_cidades

# Carrega os arquivos
print("Lendo arquivos...")
matriz = ler_matriz_csv("PCV__Matriz_do_problema - Km.csv")
nomes = ler_nomes_cidades("PCV__Matriz_do_problema - Cidades.csv")

# Teste 1: Verificar nomes
print(f"\nCidade 1: {nomes.get(1)}") # Deve ser ANGICOS
print(f"Cidade 6: {nomes.get(6)}") # Deve ser Mossoró

# Teste 2: Verificar uma distância conhecida
# Vamos ver a distância entre Cidade 1 (Angicos) e Cidade 6 (Mossoró)
# Na matriz, índice 0 é cidade 1, índice 5 é cidade 6.
dist_1_6 = matriz[0][5] 

print(f"\nDistância Angicos -> Mossoró: {dist_1_6} Km")
# Abra o CSV no Excel e veja se bate com o valor da linha 1, coluna 6.

# Teste 3: Verificar se há infinitos nos primeiros 6 itens
print("\nVerificando sub-matriz 6x6:")
for i in range(6):
    linha = matriz[i][:6]
    print(f"Linha {i+1}: {linha}")