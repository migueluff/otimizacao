from pathlib import Path
from random import randint
import time

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

if __name__ == '__main__':
    file_path = 'knapsack_data.txt'
    file_path = Path(file_path)
    if file_path.exists():
        N, Q, items = read_knapsack_data(file_path)


        print(f"Number of items (n): {N}")
        print(f"Capacity (Q): {Q}")
        print(f"Items profit and weight: {items}")
        C = randomized_solution(N,Q,items, 1)
        best_profit, index = verify_solution(C,Q)
        print(f"Best profit: {best_profit}")
        print(C[index])

        #Soluções deterministicas
        C = maybe_smarter_solution(Q, items, 1)
        best_profit, index = verify_solution(C, Q)
        print(f"Best profit: {best_profit}")
        print(C[index])

        C = maybe_smarter_solution_2(Q, items, 1)
        best_profit, index = verify_solution(C, Q)
        print(f"Best profit: {best_profit}")
        print(C[index])
