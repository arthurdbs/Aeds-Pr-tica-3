
import heapq
import random
import os

import matplotlib
matplotlib.use('Agg')  # sem janela, salva direto em arquivo
import matplotlib.pyplot as plt

# -------------------------------------------------------
# Grafo
# -------------------------------------------------------

class Grafo:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        # indice 0 descartado (recebe vazio)
        self.adj = [[] for _ in range(num_vertices + 1)]

    def adicionar_aresta(self, u, v, peso):
        self.adj[u].append((v, peso))
    @staticmethod
    def grafo_completo(n, peso_min=1, peso_max=100): # randomiza  arestas de 1 a 100 e as adiciona
        g = Grafo(n)
        for u in range(1, n + 1):
            for v in range(1, n + 1):
                if u != v:
                    g.adicionar_aresta(u, v, random.randint(peso_min, peso_max))
        return g
    @staticmethod
    def carregar_txt(caminho_arquivo): 
        num_vertices = 0
        arestas = []

        with open(caminho_arquivo, 'r') as f: #abre arquivo para leitura
            for linha in f:
                linha = linha.strip() # Remove espaços
                if not linha:
                    continue
                partes = linha.split() # Divide linha em partes
                tipo = partes[0]
                #diferentes linhas:
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
                        # maior vértice visto vira o tamanho do grafo
                        if u > num_vertices: num_vertices = u
                        if v > num_vertices: num_vertices = v
                    except (ValueError, IndexError):
                        pass

        g = Grafo(num_vertices) # adiciona as arestas
        for u, v, w in arestas:
            g.adicionar_aresta(u, v, w)

        print(f"  {num_vertices} vertices, {len(arestas)} arestas")
        return g, num_vertices, len(arestas)


# -------------------------------------------------------
# Dijkstra
# -------------------------------------------------------

def dijkstra(grafo, origem):
    n   = grafo.num_vertices
    INF = float('inf')

    dist     = [INF]   * (n + 1)# Inicializa todas as distâncias com infinito
    visitado = [False] * (n + 1) #vetor de visitados
    dist[origem] = 0
    comparacoes  = 0

    heap = [(0, origem)] #[(distância, vertice)]

    while heap:
        d_u, u = heapq.heappop(heap) # Remove menor distância
        comparacoes += 1 #conta comparação

        if visitado[u]:
            continue  # descarta visitado
        visitado[u] = True

        for v, peso in grafo.adj[u]:
            comparacoes += 1 
            nova = dist[u] + peso # Calcula nova distância
            if nova < dist[v]: 
                dist[v] = nova # Atualiza distância
                heapq.heappush(heap, (nova, v)) # Insere no heap

    return dist, comparacoes





# -------------------------------------------------------
# Gráfico PNG com matplotlib
# -------------------------------------------------------

def gerar_png(tamanhos, comparacoes,
              titulo="Dijkstra - Comparações vs Vértices",
              caminho_saida="dijkstra_comparacoes.png"):

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.fill_between(tamanhos, comparacoes, alpha=0.15, color='royalblue')
    ax.plot(tamanhos, comparacoes, color='royalblue', linewidth=2.5,
            marker='o' if len(tamanhos) <= 80 else None, markersize=4)

    ax.set_xlabel("Número de Vértices (N)", fontsize=13)
    ax.set_ylabel("Número de Comparações", fontsize=13)
    ax.set_title(titulo, fontsize=15)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x):,}'))

    fig.tight_layout()
    fig.savefig(caminho_saida, dpi=150)
    plt.close(fig)


# -------------------------------------------------------
# grafos completos de 4 a max vértices
# -------------------------------------------------------

def grafos_completos(n_max=50, passo=1, seed=42):
    random.seed(seed)
    tamanhos = list(range(4, n_max + 1, passo))
    comparacoes_lista = []


    print(f"  Grafos completos: 4 → {n_max} vértices")
    print(f"{'='*50}")
    print(f"  {'vertices':>10}  {'comparacoes':>15}")
    print(f"  {'-'*10}  {'-'*15}")

    for n in tamanhos:
        g = Grafo.grafo_completo(n)  # Cria grafo completo
        _, comp = dijkstra(g, origem=1) # Executa Dijkstra
        comparacoes_lista.append(comp) # Salva comparações
        print(f"  {n:>10}  {comp:>15,}") #imprime vertices e comparções

    return tamanhos, comparacoes_lista


# -------------------------------------------------------
# Dijkstra para os arquivos
# -------------------------------------------------------

def rodar_instancia(caminho_arquivo, nome, origem=1):
    print(f"\n{'='*50}")
    print(f"  {nome}")
    print(f"{'='*50}")

    if not os.path.exists(caminho_arquivo): 
        print(f"  arquivo nao encontrado: {caminho_arquivo}")
        return None, None


    grafo, n, _ = Grafo.carregar_txt(caminho_arquivo)

    dist, comp = dijkstra(grafo, origem)
    if "Distancia" in nome: #imprime menor distancia
        d = dist[n]
        print(f"  dist minima (1 → {n}): {d if d != float('inf') else 'inalcançavel'}")
        print(f"  comparacoes: {comp:,}")

        return d, comp
    
    if "Tempo" in nome: #imprime menor tempo
        d = dist[n]
        print(f"  tempo minimo (1 → {n}): {d if d != float('inf') else 'inalcançavel'}")
        print(f"  comparacoes: {comp:,}")

        return d, comp


# -------------------------------------------------------
# Main
# -------------------------------------------------------

def main():
    n_max = int(input("N maximo para grafos completos (ex: 100): ").strip() or "100")

    tamanhos, comparacoes = grafos_completos(n_max=n_max)
    gerar_png(tamanhos, comparacoes,
              titulo=f"Dijkstra - Grafos Completos (4 a {n_max} vertices)",
              caminho_saida="dijkstra_comparacoes.png")

    instancias = [
        ("NY_Dist.txt",  "NY - Distancia"),
        ("NY_time.txt",  "NY - Tempo medio"),
        ("SF_Dist.txt",  "San Francisco - Distancia"),
        ("SF_time.txt",  "San Francisco - Tempo medio"),
    ]

    print("\n\n\n")


    resultados = []
    for arq, nome in instancias:
        d, c = rodar_instancia(arq, nome)
        resultados.append((nome, d, c))



if __name__ == "__main__":
    main()