"""
Questão 3 - Prática 3 - AEDS II
Implementação de Heurística Gulosa para Caminho Mínimo
Autores: Arthur de Brito Silva
Rafael Eustáquio Pinto 
Rafael Cristo
Data: 28 de maio de 2026
"""

import random
import os
import time

import matplotlib
matplotlib.use('Agg')  # sem janela, salva direto em arquivo
import matplotlib.pyplot as plt

# -------------------------------------------------------
# Grafo
# -------------------------------------------------------

class Grafo:
    """Classe que representa um grafo direcionado ponderado."""
    
    def __init__(self, num_vertices):
        """
        Inicializa um grafo vazio com num_vertices vértices.
        
        Args:
            num_vertices: Número de vértices do grafo
        """
        self.num_vertices = num_vertices
        # índice 0 descartado (recebe vazio)
        self.adj = [[] for _ in range(num_vertices + 1)]

    def adicionar_aresta(self, u, v, peso):
        """
        Adiciona uma aresta direcionada de u para v com peso w.
        
        Args:
            u: Vértice de origem
            v: Vértice de destino
            peso: Peso da aresta
        """
        self.adj[u].append((v, peso))

    @staticmethod
    def grafo_completo(n, peso_min=1, peso_max=100):
        """
        Cria um grafo completo com n vértices.
        Cada aresta tem um peso aleatório entre peso_min e peso_max.
        
        Args:
            n: Número de vértices
            peso_min: Peso mínimo para as arestas
            peso_max: Peso máximo para as arestas
            
        Returns:
            Grafo completo com pesos aleatórios
        """
        g = Grafo(n)
        for u in range(1, n + 1):
            for v in range(1, n + 1):
                if u != v:
                    g.adicionar_aresta(u, v, random.randint(peso_min, peso_max))
        return g

    @staticmethod
    def carregar_txt(caminho_arquivo):
        """
        Carrega um grafo de um arquivo de texto em formato DIMACS.
        Formato esperado:
        - Linhas com 'c': comentários
        - Linhas com 'p': descrição (p sp num_vertices num_arestas)
        - Linhas com 'a': arestas (a origem destino peso)
        
        Args:
            caminho_arquivo: Caminho para o arquivo
            
        Returns:
            Tupla (grafo, num_vertices, num_arestas)
        """
        num_vertices = 0
        arestas = []

        with open(caminho_arquivo, 'r') as f:
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue
                partes = linha.split()
                tipo = partes[0]

                if tipo == 'c':
                    if 'nodes' in linha and 'arcs' in linha:
                        try:
                            num_vertices = int(partes[partes.index('nodes') - 1])
                        except (ValueError, IndexError):
                            pass
                    continue

                if tipo == 'p':
                    try:
                        num_vertices = int(partes[2])
                    except (ValueError, IndexError):
                        pass
                    continue

                if tipo == 'a':
                    try:
                        u, v, w = int(partes[1]), int(partes[2]), int(partes[3])
                        arestas.append((u, v, w))
                        if u > num_vertices:
                            num_vertices = u
                        if v > num_vertices:
                            num_vertices = v
                    except (ValueError, IndexError):
                        pass

        g = Grafo(num_vertices)
        for u, v, w in arestas:
            g.adicionar_aresta(u, v, w)

        print(f"  {num_vertices} vertices, {len(arestas)} arestas")
        return g, num_vertices, len(arestas)


# -------------------------------------------------------
# Heurística Gulosa (Greedy)
# -------------------------------------------------------

def greedy_shortest_path(grafo, origem):
    """
    Calcula o caminho mínimo usando uma heurística gulosa.
    
    Algoritmo:
    1. Inicializa distâncias com infinito, exceto origem = 0
    2. Marca a origem como visitada
    3. Enquanto existem vértices não visitados:
       a) Encontra o vértice não visitado com menor distância (busca linear)
       b) Marca como visitado
       c) Relaxa as arestas saindo dele
    
    Diferença de Dijkstra:
    - Dijkstra usa heap para encontrar o próximo vértice eficientemente
    - Greedy usa busca linear, o que torna menos eficiente mas educativo
    
    Args:
        grafo: Grafo para processar
        origem: Vértice de origem
        
    Returns:
        Tupla (vetor_distâncias, número_comparações)
    """
    n = grafo.num_vertices
    INF = float('inf')

    # Inicializa estruturas
    dist = [INF] * (n + 1)  # Distância de origem para cada vértice
    visitado = [False] * (n + 1)  # Marca se vértice foi processado
    dist[origem] = 0
    comparacoes = 0

    # Processa n vértices
    for _ in range(n):
        # Encontra vértice não visitado com menor distância (busca linear)
        u = -1
        min_dist = INF

        for v in range(1, n + 1):
            comparacoes += 1  # Conta cada comparação
            if not visitado[v] and dist[v] < min_dist:
                min_dist = dist[v]
                u = v

        # Se não encontrou vértice alcançável, termina
        if u == -1 or dist[u] == INF:
            break

        # Marca como visitado
        visitado[u] = True

        # Relaxa as arestas saindo de u
        for v, peso in grafo.adj[u]:
            comparacoes += 1  # Conta cada comparação
            nova_dist = dist[u] + peso
            if nova_dist < dist[v]:
                dist[v] = nova_dist

    return dist, comparacoes


# -------------------------------------------------------
# Gráfico PNG com matplotlib
# -------------------------------------------------------

def gerar_png(tamanhos, comparacoes, titulo="", caminho_saida="greedy_comparacoes.png"):
    """
    Gera um gráfico mostrando a relação entre número de vértices e comparações.
    
    Args:
        tamanhos: Lista com número de vértices
        comparacoes: Lista com número de comparações para cada tamanho
        titulo: Título do gráfico
        caminho_saida: Caminho para salvar o PNG
    """
    fig, ax = plt.subplots(figsize=(11, 7))

    # Plota área preenchida e linha
    ax.fill_between(tamanhos, comparacoes, alpha=0.15, color='royalblue')
    ax.plot(tamanhos, comparacoes, color='royalblue', linewidth=2.5,
            marker='o' if len(tamanhos) <= 80 else None, markersize=4)

    ax.set_xlabel("Número de Vértices (N)", fontsize=13)
    ax.set_ylabel("Número de Comparações", fontsize=13)
    ax.set_title(titulo, fontsize=15, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

    fig.tight_layout()
    fig.savefig(caminho_saida, dpi=150)
    plt.close(fig)
    print(f"  Gráfico salvo: {caminho_saida}")


# -------------------------------------------------------
# Testes com Grafos Completos
# -------------------------------------------------------

def grafos_completos(n_max=2000, passo=50, seed=42):
    """
    Testa a heurística gulosa em grafos completos com tamanhos crescentes.
    
    Args:
        n_max: Tamanho máximo de grafo (vértices)
        passo: Intervalo entre tamanhos testados
        seed: Seed para reprodutibilidade
        
    Returns:
        Tupla (lista_tamanhos, lista_comparacoes)
    """
    random.seed(seed)
    tamanhos = list(range(4, n_max + 1, passo))
    comparacoes_lista = []

    print(f"\n{'='*60}")
    print(f"  TESTES COM GRAFOS COMPLETOS (Heurística Gulosa)")
    print(f"{'='*60}")
    print(f"  Grafos: 4 → {n_max} vértices (passo: {passo})")
    print(f"{'='*60}")
    print(f"  {'Vértices':>12}  {'Comparações':>18}  {'Tempo (s)':>12}")
    print(f"  {'-'*12}  {'-'*18}  {'-'*12}")

    for n in tamanhos:
        g = Grafo.grafo_completo(n)
        
        inicio = time.time()
        _, comp = greedy_shortest_path(g, origem=1)
        tempo = time.time() - inicio
        
        comparacoes_lista.append(comp)
        print(f"  {n:>12}  {comp:>18,}  {tempo:>12.4f}")

    print(f"{'='*60}\n")
    return tamanhos, comparacoes_lista


# -------------------------------------------------------
# Testes com Arquivos Reais
# -------------------------------------------------------

def rodar_instancia(caminho_arquivo, nome, origem=1):
    """
    Executa a heurística gulosa em um arquivo de grafo real.
    
    Args:
        caminho_arquivo: Caminho para o arquivo
        nome: Nome descritivo do arquivo
        origem: Vértice de origem
        
    Returns:
        Tupla (distância_mínima, número_comparações)
    """
    print(f"\n{'='*60}")
    print(f"  {nome}")
    print(f"{'='*60}")

    if not os.path.exists(caminho_arquivo):
        print(f"  ERRO: arquivo não encontrado: {caminho_arquivo}")
        return None, None

    print(f"  Carregando {caminho_arquivo}...")
    grafo, n, num_arestas = Grafo.carregar_txt(caminho_arquivo)

    print(f"  Executando heurística gulosa (1 → {n})...")
    inicio = time.time()
    dist, comp = greedy_shortest_path(grafo, origem=1)
    tempo = time.time() - inicio

    d = dist[n]
    print(f"  Distância mínima (1 → {n}): {d if d != float('inf') else 'INALCANÇÁVEL'}")
    print(f"  Comparações: {comp:,}")
    print(f"  Tempo de execução: {tempo:.4f}s")
    print(f"{'='*60}")

    return d, comp


# -------------------------------------------------------
# Main
# -------------------------------------------------------

def main():
    """Função principal que executa todos os testes."""
    
    print("\n")
    print("╔" + "═"*58 + "╗")
    print("║  QUESTÃO 3 - HEURÍSTICA GULOSA PARA CAMINHO MÍNIMO  ║")
    print("║  Algoritmos e Estruturas de Dados II - AEDS II      ║")
    print("╚" + "═"*58 + "╝")

    # ========== PARTE 1: TESTES COM GRAFOS COMPLETOS ==========
    print("\n\n")
    print("█" * 60)
    print("  PARTE I: TESTES COM GRAFOS COMPLETOS")
    print("█" * 60)
    
    n_max = 2000  # Como pedido pelo usuário, ao invés de 1.000.000
    tamanhos, comparacoes = grafos_completos(n_max=n_max, passo=50)

    # Gera gráfico
    gerar_png(
        tamanhos, comparacoes,
        titulo=f"Heurística Gulosa - Grafos Completos (4 a {n_max} vértices)",
        caminho_saida="greedy_grafos_completos.png"
    )

    # ========== PARTE 2: TESTES COM ARQUIVOS REAIS ==========
    print("\n\n")
    print("█" * 60)
    print("  PARTE II: TESTES COM INSTÂNCIAS REAIS")
    print("█" * 60)

    instancias = [
        ("NY_Dist.txt", "NY - Distância"),
        ("NY_time.txt", "NY - Tempo Médio"),
        ("SF_Dist.txt", "San Francisco - Distância"),
        ("SF_time.txt", "San Francisco - Tempo Médio"),
    ]

    resultados = []
    for arq, nome in instancias:
        d, c = rodar_instancia(arq, nome, origem=1)
        if d is not None:
            resultados.append((nome, d, c))

    # Imprime resumo final
    print("\n\n")
    print("╔" + "═"*58 + "╗")
    print("║  RESUMO DOS RESULTADOS - INSTÂNCIAS REAIS            ║")
    print("╚" + "═"*58 + "╝")
    print()
    print(f"  {'Instância':<40}  {'Dist/Tempo':<15}  {'Comparações':>15}")
    print(f"  {'-'*40}  {'-'*15}  {'-'*15}")
    for nome, dist, comp in resultados:
        d_str = f"{dist:,.0f}" if dist != float('inf') else "INALCANÇÁVEL"
        print(f"  {nome:<40}  {d_str:>15}  {comp:>15,}")
    print()


if __name__ == "__main__":
    main()
