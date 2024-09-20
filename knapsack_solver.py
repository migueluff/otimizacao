from pathlib import Path
from random import randint
import time
import random
import matplotlib.pyplot as plt


def read_knapsack_data(file_path):

    with open(file_path, 'r') as file:

        # Read the number of items N
        N = int(file.readline().strip())

        # Read the capacity Q
        Q = int(file.readline().strip())

        # Read the profits
        profits = list(map(int, file.readline().strip().split()))

        # Read the weights
        weights = list(map(int, file.readline().strip().split()))

        items =  list(zip(profits, weights))
    return N, Q, items

def get_remaning(Q, current):
    current_weight = 0
    for item in current:
        current_weight += item[1]

    return Q - current_weight

def get_randomized(Q, current):
    remaning = get_remaning(Q, current)
    for item in current:
        if item[1] > remaning:

            current.remove(item)
    if len(current) > 0:
        index = randint(0, len(current) - 1)
        return current[index], current
    return  None, []

def randomized_solution(N,Q,items, timelimit):
    C = []
    start_time = time.time()

    while time.time() - start_time < timelimit:
        current = items.copy()
        solution = []
        while len(current) > 0:
            new_item, current = get_randomized(Q, current)
            if new_item is not None:
                current.remove(new_item)
                solution.append(new_item)
        if solution:
            C.append(solution)
    return C

def verify_solution(C,Q):
    best = 0
    best_index = 0
    index = 0
    for s in C:
        current_capacity = 0
        current_profit = 0
        for item in s:
            if ( current_capacity + item[1])  <= Q:
                current_profit += item[0]
                current_capacity += item[1]
            else:
                current_profit = -1
                break
        if current_profit > best:
            best = current_profit
            best_index = index
        index += 1
    return best, best_index

def get_sorted_for_profit(items):

    sorted_items = sorted(items, key=lambda x: x[0], reverse=True)
    return sorted_items

def get_ratios_and_sorted(items):

    ratios = [(profit, weight, profit / weight) for profit, weight in items]
    sorted_items = sorted(ratios, key=lambda x: x[-1], reverse=True)

    return sorted_items

def maybe_smarter_solution(Q, items, timelimit):
    C = []
    start_time = time.time()

    while time.time() - start_time < timelimit:
        current = items.copy()
        solution = []
        sorted_items = get_ratios_and_sorted(current)
        current_capacity = 0
        for item in sorted_items:
            if (current_capacity + item[1]) <= Q:
                solution.append(item)
                current_capacity += item[1]
            else:
                break
        if solution:
            C.append(solution)
    return C

def maybe_smarter_solution_2(Q, items, timelimit):
    C = []
    start_time = time.time()

    while time.time() - start_time < timelimit:
        current = items.copy()
        solution = []
        sorted_items = get_sorted_for_profit(current)
        current_capacity = 0
        for item in sorted_items:
            if (current_capacity + item[1]) <= Q:
                solution.append(item)
                current_capacity += item[1]
            else:
                break
        if solution:
            C.append(solution)
    return C


def greedy_randomized_knapsack(items, capacity, alpha, time_limit):
    start_time = time.time()
    solution = [0] * len(items)
    total_weight = 0
    total_profit = 0

    # Ordenar os itens com base no critério lucro/peso
    sorted_items = sorted(enumerate(items), key=lambda x: x[1][0] / x[1][1], reverse=True)

    while time.time() - start_time < time_limit:
        # Selecionar um subconjunto de candidatos com base em alpha
        limit = int(alpha * len(sorted_items))
        if limit == 0:
            limit = 1
        candidates = sorted_items[:limit]

        # Escolher um item aleatoriamente entre os candidatos
        item_index, (profit, weight) = random.choice(candidates)

        # Verificar se o item cabe na mochila
        if total_weight + weight <= capacity:
            solution[item_index] = 1  # Adicionar o item à solução
            total_weight += weight
            total_profit += profit

    return solution, total_profit

# Função para reconstruir e exibir a solução
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

def get_10_better(C):
    better_solutions = []
    profit_all_solutions = []
    idx = 0
    for s in C:
        sum_profit = 0
        for item in s:
            sum_profit += item[0]
        profit_all_solutions.append( ( idx, sum_profit) )
        idx += 1
    sorted_items = sorted(profit_all_solutions, key=lambda x: x[1], reverse=True)
    if( len(sorted_items) >= 10):
        for item in sorted_items[:10]:
            better_solutions.append(C[ item[0] ])
        return better_solutions
    else:
        for item in sorted_items:
            better_solutions.append(C[item[0]])
        return better_solutions
if __name__ == '__main__':
    file_path = 'knapsack_data.txt'
    file_path = Path(file_path)
    if file_path.exists():
        N, Q, items = read_knapsack_data(file_path)

        """
        print(f"Number of items (n): {N}")
        print(f"Capacity (Q): {Q}")
        print(f"Items profit and weight: {items}")
        C = randomized_solution(N,Q,items, 1)
        print(get_10_better(C))
        best_profit, index = verify_solution(C,Q)
        print(f"Total profit: {best_profit}")
        print(C[index])

        #Soluções deterministicas
        C = maybe_smarter_solution(Q, items, 1)
        print(get_10_better(C))
        best_profit, index = verify_solution(C, Q)
        print(f"Total profit: {best_profit}")
        print(C[index])

        C = maybe_smarter_solution_2(Q, items, 1)
        print(get_10_better(C))
        best_profit, index = verify_solution(C, Q)
        print(f"Total profit: {best_profit}")
        print(C[index])
        """
        # Listas para armazenar os resultados
        alpha_values = []
        profit_values = []

        #alpha = 0.5  # Grau de aleatoriedade (0.0 é completamente guloso, 1.0 é completamente aleatório)
        time_limit = 1  # Tempo limite de 2 segundos para construir a solução
        alpha = 0.0
        for i in range(101):

            solucao, lucro = greedy_randomized_knapsack(items, Q, alpha, time_limit)
            selected_items, total_weight, total_profit = reconstruct_solution(solucao, items)

            # Armazenar os valores de alpha e lucro
            alpha_values.append(alpha)
            profit_values.append(total_profit)

            #print(f"Alpha: {alpha}\nPeso: {total_weight} - Lucro: {total_profit}\nSolução: {selected_items}")
            alpha += 0.01

        #print(f"Founded Solution: {solucao}")
        #print(f"Total profit: {lucro}")
        plt.plot(alpha_values, profit_values, marker='o')
        plt.xlabel('Alpha')
        plt.ylabel('Lucro')
        plt.title('Lucro vs Alpha na Heurística Gulosa Randomizada')
        plt.grid(True)
        plt.show()