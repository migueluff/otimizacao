# Execicio Prático: Problema da mochila


### Disciplina: Multiobjective Optimization
#### Professor: Igor Machado Coelho
#### Alunos: Douglas Brum e Miguel Freitas
- Create a constructive heuristic function to build a random initial
solution, given timelimit of t seconds (otherwise, just return an empty
solution).

- Create a constructive heuristic function which is smarter to build an
initial solution. Also respect a given timelimit of t seconds (otherwise,
just return an empty solution).
- Generate 10 different initial solutions and compare them. Which of the
two constructive methods is better on average?


Entrada:
N 5

Q 10

Pi  1 1 1 5 5 5 3 6

W(i)    1 2 3 7 8 10 5 3

- Número de itens (N);
- Capacidade da mochila (Q);
- Lista com ganhos dos itens (Pi);
- Lista com pesos dos itens (Wi);


Obs.: Os testes trabalham apenas com soluções viáveis.

## 1 Teste com solução aleatória
Number of items (n): 8
Capacity (Q): 10
Items profit and weight: [(1, 1), (1, 2), (1, 3), (5, 7), (5, 8), (5, 10), (3, 5), (6, 3)]


[[(6, 3), (5, 7)], [(6, 3), (5, 7)], [(6, 3), (5, 7)], [(6, 3), (5, 7)], [(6, 3), (5, 7)], [(6, 3), (5, 7)], [(6, 3), (5, 7)], [(6, 3), (5, 7)], [(6, 3), (5, 7)], [(6, 3), (5, 7)]]


Best profit: 11
[(6, 3), (5, 7)]



## 2 Teste com solução deterministica usando razao profit/weight
[[(6, 3, 2.0), (1, 1, 1.0)], [(6, 3, 2.0), (1, 1, 1.0)], [(6, 3, 2.0), (1, 1, 1.0)], [(6, 3, 2.0), (1, 1, 1.0)], [(6, 3, 2.0), (1, 1, 1.0)], [(6, 3, 2.0), (1, 1, 1.0)], [(6, 3, 2.0), (1, 1, 1.0)], [(6, 3, 2.0), (1, 1, 1.0)], [(6, 3, 2.0), (1, 1, 1.0)], [(6, 3, 2.0), (1, 1, 1.0)]]
Best profit: 7
[(6, 3, 2.0), (1, 1, 1.0)]

## 2 Teste com solução deterministica ordenando pelo profit
[[(6, 3), (5, 7)], [(6, 3), (5, 7)], [(6, 3), (5, 7)], [(6, 3), (5, 7)], [(6, 3), (5, 7)], [(6, 3), (5, 7)], [(6, 3), (5, 7)], [(6, 3), (5, 7)], [(6, 3), (5, 7)], [(6, 3), (5, 7)]]
Best profit: 11
[(6, 3), (5, 7)]
