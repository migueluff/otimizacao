import random
import time
from pathlib import Path

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

    # Ordenar os itens com base no critério lucro/peso
    sorted_items = sorted(enumerate(items), key=lambda x: x[1][0] / x[1][1], reverse=True)
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
        print(item_index, profit, weight)

        # Verificar se o item cabe na mochila
        if total_weight + weight <= capacity:
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





def find_first(f, N, timelimit, s):
    """
    Procedimento FindFirst para o problema da mochila.

    Parâmetros:
    f -- Função objetivo a ser maximizada (lucro total dos itens selecionados).
    N -- Função que retorna a vizinhança de uma solução.
    stop -- Função que determina o critério de parada.
    s -- Solução atual (lista binária representando itens selecionados).

    Retorna:
    m -- O primeiro movimento que melhora a solução atual.
    """
    m = first_move(N, s)  # Obtém o primeiro movimento na vizinhança

    start_time = time.time()
    print(time.time() - start_time)
    while m is not None and ( time.time() - start_time < timelimit) :
        delta_f = f(m) - f(s)  # Avalia a diferença na função objetivo (lucro)
        #print(delta_f)
        if delta_f > 0:  # Se a mudança melhora a solução (maximização do lucro)

            return m
        else:
            #print(len(N))
            m = next_move(N, s, m)

    return m  # Se nenhum movimento melhorar, retorna None


def f(s, items, capacity):

    """ Função objetivo que calcula o lucro total da solução s sem ultrapassar a capacidade. """

    total_weight = sum([s[i] * items[i][1] for i in range(len(items))])
    total_profit = sum([s[i] * items[i][0] for i in range(len(items))])


    if total_weight > capacity:
        return -float('inf')
    return total_profit


def N(s):
    """ Gera a vizinhança de uma solução s (adiciona ou remove um item da mochila). """
    neighbors = []
    for i in range(len(s)):
        # Cria uma nova solução trocando o valor do item i
        neighbor = s[:]
        neighbor[i] = 1 - neighbor[i]  # Se estava dentro (1), agora estará fora (0), e vice-versa
        neighbors.append(neighbor)
    return neighbors


def first_move(N, s):
    """ Retorna o primeiro movimento possível na vizinhança da solução atual. """
    neighbors = N(s)  # Obtém os vizinhos da solução atual

    return neighbors[0] if neighbors else None


def next_move(N, s, current_move):
    """ Retorna o próximo movimento na vizinhança. """
    neighbors = N(s)
    current_index = neighbors.index(current_move)
    #print(current_move)
    #print(current_index)
    if current_index + 1 < len(neighbors):
        return neighbors[current_index + 1]
    else:

        return neighbors[0]


def stop(time_start, f_s, max_time=60):
    """ Critério de parada após um tempo limite de 60 segundos. """
    return (time.time() - time_start) > max_time

if __name__ == '__main__':
    file_path = 'large_scale/knapPI_1_100_1000_1'
    file_path = Path(file_path)
    if file_path.exists():
        size, Q, items = read_knapscak_data_02(file_path)
        aleatory_alpha = random.uniform(0.2, 0.4)
        time_limit = 0.5
        solucao, lucro = greedy_randomized_knapsack(items, Q, aleatory_alpha, time_limit)
        selected_items, total_weight, total_profit = reconstruct_solution(solucao, items)

        #print(Q, total_weight, total_profit)
        #print(Q, total_weight, total_profit)
        #print(items)
        #print(solucao, lucro)
        #print(solucao, lucro)

        best_move = find_first(lambda s: f(solucao, items, Q), N,time_limit, solucao)
        #print(best_move)
        #Mostra a solução encontrada
        #print("Melhor solução encontrada:", best_move)
        #print("Lucro da solução:", f(best_move, items, Q))
