import random
import time
from pathlib import Path
import itertools
import matplotlib.pyplot as plt


def read_knapscak_data_02(file_path):
    with open(file_path, 'r') as file:
        instance_count = 0
        profits = []
        weights = []

        for line in file.readlines():
            if instance_count == 0:
                N, Q = line.split()
                N = int(N)
                Q = int(Q)
            elif ( instance_count > 0) and (instance_count <= N):
                profits.append(int(line.split()[0]))
                weights.append(int(line.split()[1]))

            instance_count += 1

        #items = list(zip(range(N),zip(profits, weights)))
        items = list(zip(profits, weights))
    return N, Q, items

def greedy_randomized_knapsack(items, capacity, alpha, time_limit):
    start_time = time.time()
    solution = [0] * len(items)
    total_weight = 0
    total_profit = 0

    items_indexed = [(index, (profit, weight)) for index, (profit, weight) in enumerate(items)]

    sorted_items = sorted(items_indexed, key=lambda x: x[1][0] / x[1][1], reverse=True)

    #print(sorted_items)
    while (time.time() - start_time) < time_limit:
        # Selecionar um subconjunto de candidatos com base em alpha
        limit = int(alpha * len(sorted_items))
        if limit == 0:
            limit = 1
        candidates = sorted_items[:limit]

        #print(candidates)
        # Escolher um item aleatoriamente entre os candidatos
        item_index, (profit, weight) = random.choice(candidates)


        # Verificar se o item cabe na mochila
        if ( (total_weight + weight) <= capacity ) and solution[item_index] == 0:

            solution[item_index] = 1  # Adicionar o item à solução
            total_weight += weight
            total_profit += profit

    return solution, total_profit

def reconstruct_solution(solution, items):

    selected_items = []
    total_weight = 0
    total_profit = 0

    items = sorted(enumerate(items), key=lambda x: x[1][0] / x[1][1], reverse=True)

    #print(items)
    for i, selected in enumerate(solution):
        if selected == 1:  # Item foi selecionado
            profit, weight = items[i][1]
            selected_items.append((profit, weight))
            total_weight += weight
            total_profit += profit

    return selected_items, total_weight, total_profit

def f(s, items, capacity):

    """ Função objetivo que calcula o lucro total da solução s sem ultrapassar a capacidade. """

    #print(capacity)
    total_weight = sum([s[i] * items[i][1] for i in range(len(items))])
    total_profit = sum([s[i] * items[i][0] for i in range(len(items))])


    if total_weight > capacity:
        return -float('inf')
    return total_profit


def first_move(s):
    """ Retorna o primeiro movimento possível na vizinhança da solução atual. """
    neighbors = N(s)  # Obtém os vizinhos da solução atual
    return neighbors[0] if neighbors else None

def random_move(s):
    """ Retorna um movimento aleatório na vizinhança da solução atual. """
    neighbors = N(s)  # Obtém os vizinhos da solução atual
    return random.choice(neighbors)

def N(s, flip=2):
    """
    Gera a vizinhança de uma solução 's' de acordo com o valor de 'flip':
    - flip = 1: Troca de 1 item.
    - flip = 2: Troca entre dois itens.
    - flip = 3: Troca de blocos de 5 itens.

    Parâmetros:
    - s: Solução atual.
    - flip: Estratégia de geração de vizinhança.

    Retorna:
    - neighbors: Lista de soluções vizinhas.
    """
    neighbors = []

    if flip == 1:
        # Troca o valor de um item de cada vez
        for i in range(len(s)):
            neighbor = s[:]
            neighbor[i] = 1 - neighbor[i]  # Se estava dentro (1), agora estará fora (0), e vice-versa
            neighbors.append(neighbor)

    elif flip == 2:
        # Troca entre dois itens
        for i in range(len(s)):
            for j in range(i + 1, len(s)):
                neighbor = s[:]
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]  # Troca dois itens de posição
                neighbors.append(neighbor)

    elif flip == 3:
        # Troca blocos de 5 itens
        for i in range(0, len(s), 3):
            neighbor = s[:]
            for j in range(i, min(i + 3, len(s))):
                neighbor[j] = 1 - neighbor[j]  # Inverte os valores em blocos de 5 itens
            neighbors.append(neighbor)

    return neighbors

def N6(s, k=20):
    """ Gera a vizinhança trocando k itens da mochila. """
    neighbors = []
    for i in range(len(s)):
        neighbor = s[:]
        for j in range(k):

            r = random.randint(0, len(s) - 1)

            neighbor[r] = 1 - neighbor[r]

        neighbors.append(neighbor)
    return neighbors

def N2(s, k=2):
    """ Gera a vizinhança trocando k itens simultaneamente. """
    neighbors = []
    indices = list(range(len(s)))
    for combo in itertools.combinations(indices, k):
        neighbor = s[:]
        for i in combo:
            neighbor[i] = 1 - neighbor[i]
        neighbors.append(neighbor)
    return neighbors

def N3(s):
    """ Gera a vizinhança trocando dois itens da mochila. """
    neighbors = []
    for i in range(len(s)):
        for j in range(i + 1, len(s)):
            neighbor = s[:]
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors

def N4(s, block_size=5):
    """ Gera a vizinhança alterando blocos de itens. """
    neighbors = []
    for i in range(0, len(s), block_size):
        neighbor = s[:]
        for j in range(i, min(i + block_size, len(s))):
            neighbor[j] = 1 - neighbor[j]
        neighbors.append(neighbor)
    return neighbors


def next_move(s, neighbors, current_index):
    """ Retorna o próximo movimento na vizinhança, dado um índice. """
    if current_index + 1 < len(neighbors):
        return neighbors[current_index + 1], current_index + 1
    else:
        return None, current_index


def find_first(timelimit, s, items, Q):
    """
    Procedimento FindFirst para o problema da mochila.

    Parâmetros:
    s -- Solução atual (lista binária representando itens selecionados).
    Retorna:
    m -- O primeiro movimento que melhora a solução atual.
    """
    initial_solution = s.copy()
    neighbors = N(s)  # Gera a vizinhança uma vez
    current_index = 0

    start_time = time.time()

    while current_index < len(neighbors) and (time.time() - start_time < timelimit):
        m = neighbors[current_index]
        delta_f = f(m, items, Q) - f(s, items, Q)  # Avalia a diferença na função objetivo (lucro)
        #print(f"Delta f: {delta_f}")
        if delta_f > 0:  # Se a mudança melhora a solução (maximização do lucro)
            return m
        else:
            m, current_index = next_move(s, neighbors, current_index)

    return initial_solution


def find_best(timelimit, s, items, Q):
    """
    Procedimento FindBest para o problema da mochila.

    Parâmetros:
    s -- Solução atual (lista binária representando itens selecionados).
    Retorna:
    m -- O melhor movimento que melhora a solução atual.
    """
    initial_solution = s.copy()
    best_solution = initial_solution
    best_delta_f = -float('inf')  # Inicialmente, não há melhoria
    neighbors = N(s)  # Gera a vizinhança uma vez
    start_time = time.time()

    while (time.time() - start_time < timelimit):
        for neighbor in neighbors:
            delta_f = f(neighbor, items, Q) - f(s, items, Q)  # Avalia a diferença na função objetivo (lucro)

            # Se encontrar um movimento que melhora a solução e é o melhor até agora
            if delta_f > best_delta_f:
                best_delta_f = delta_f
                best_solution = neighbor

    # Retorna a melhor solução encontrada (se houver uma melhor, senão retorna a inicial)
    return best_solution if best_delta_f > 0 else initial_solution



def hill_climbing_first(time_limit, s, items, Q):
    """
    Algoritmo Hill Climbing para o problema da mochila.

    Parâmetros:
    - time_limit: Tempo limite para cada iteração de busca local.
    - s: Solução inicial (lista binária representando itens selecionados).
    - items: Lista de itens (lucros e pesos).
    - Q: Capacidade máxima da mochila.

    Retorna:
    - s: A melhor solução encontrada.
    """
    current_solution = s.copy()
    best_solution = current_solution
    start_time = time.time()

    while (time.time() - start_time) < time_limit:
        # Tenta encontrar uma solução melhor usando find_first
        new_solution = find_first(time_limit, current_solution, items, Q)

        # Se a nova solução for melhor que a atual, atualiza a solução
        if f(new_solution, items, Q) > f(current_solution, items, Q):
            current_solution = new_solution
            best_solution = new_solution
        else:
            # Se não houver mais melhorias, interrompe a busca
            break

    return best_solution

def hill_climbing_best(time_limit, s, items, Q):
    """
    Algoritmo Hill Climbing para o problema da mochila utilizando find_best.

    Parâmetros:
    - time_limit: Tempo limite total para o algoritmo de busca.
    - s: Solução inicial (lista binária representando itens selecionados).
    - items: Lista de itens (lucros e pesos).
    - Q: Capacidade máxima da mochila.

    Retorna:
    - s: A melhor solução encontrada.
    """
    current_solution = s.copy()  # Inicia com a solução atual
    best_solution = current_solution
    start_time = time.time()  # Tempo de início

    while (time.time() - start_time) < time_limit:
        # Calcula o tempo restante para garantir que o find_best respeite o limite total de tempo
        remaining_time = time_limit - (time.time() - start_time)

        # Encontra a melhor solução vizinha com o tempo restante
        new_solution = find_best(remaining_time, current_solution, items, Q)

        # Verifica se a nova solução encontrada é melhor que a solução atual
        if f(new_solution, items, Q) > f(current_solution, items, Q):
            current_solution = new_solution  # Atualiza a solução atual
            best_solution = new_solution  # Atualiza a melhor solução
        else:
            # Se não houver mais melhorias, interrompe o algoritmo
            break

    return best_solution


def random_descent(time_limit, s, items, Q, Kmax):
    """
    Algoritmo Random Descent para o problema da mochila.
    """
    current_solution = s.copy()
    best_solution = current_solution
    start_time = time.time()
    k = 0
    while k < Kmax and ( (time.time() - start_time) < time_limit):
        # Tenta encontrar uma solução melhor usando find_first
        new_solution = random_move(s)
        if f(new_solution, items, Q) - f(current_solution, items, Q) > 0:
            current_solution = new_solution
            k = 0
        else:
            k += 1
    return best_solution

if __name__ == '__main__':
    file_path = 'large_scale/knapPI_1_100_1000_1'
    file_path = Path(file_path)

    reference_solution = 9147
    if file_path.exists():
        size, Q, items = read_knapscak_data_02(file_path)

        # Intervalo de alphas para gerar soluções iniciais
        alpha_values = [0.1,0.11,0.12, 0.13, 0.14, 0.15]
        time_limit = 2

        profits_first = []  # Para armazenar os lucros do Hill Climbing First
        profits_best = []  # Para armazenar os lucros do Hill Climbing Best
        profits_random = []  # Para armazenar os lucros do Random Descent

        for alpha in alpha_values:
            # Gera uma solução inicial usando o alpha atual
            solucao_inicial, lucro_inicial = greedy_randomized_knapsack(items, Q, alpha, time_limit)
            print(f"Solução inicial: {solucao_inicial}, Lucro inicial: {lucro_inicial}")

            # Aplica o Hill Climbing First
            melhor_solucao_first = hill_climbing_first(time_limit, solucao_inicial, items, Q)
            melhor_lucro_first = f(melhor_solucao_first, items, Q)
            profits_first.append(melhor_lucro_first)
            print(f"Hill Climbing First - Melhor lucro: {melhor_lucro_first}")

            # Aplica o Hill Climbing Best
            melhor_solucao_best = hill_climbing_best(time_limit, solucao_inicial, items, Q)
            melhor_lucro_best = f(melhor_solucao_best, items, Q)
            profits_best.append(melhor_lucro_best)
            print(f"Hill Climbing Best - Melhor lucro: {melhor_lucro_best}")

            # Aplica o Random Descent
            melhor_solucao_random = random_descent(time_limit, solucao_inicial, items, Q, 100)
            melhor_lucro_random = f(melhor_solucao_random, items, Q)
            profits_random.append(melhor_lucro_random)
            print(f"Random Descendent - Melhor lucro: {melhor_lucro_random}")

        # Gerar o gráfico comparativo
        plt.figure(figsize=(10, 6))

        plt.plot(alpha_values, profits_first, label="Hill Climbing First", marker='o')
        plt.plot(alpha_values, profits_best, label="Hill Climbing Best", marker='x')
        plt.plot(alpha_values, profits_random, label="Random Descent", marker='^')
        plt.axhline(y=reference_solution, color='r', linestyle='--', label="Reference Solution")

        plt.title("Comparação de Lucro: Hill Climbing First, Best, Random Descent e Solução de Referência")
        plt.xlabel("Alpha")
        plt.ylabel("Lucro")
        plt.legend()
        plt.grid(True)

        # Exibe o gráfico
        plt.show()