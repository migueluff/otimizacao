



coins = [1,5,12,24,50,100]

N = 27
def get_sublist(change, coins):
    idx = 0
    for coin in coins:
        if change >= coin:
            idx += 1
        else:
            break
    coins = coins[:idx]

    return coins

def min_MCP(change, coins):

    coins = get_sublist(change, coins)

    if change == 0:
        return 0
    else:

        cm = -1

        for coin in coins:
            if cm == -1:
                cm = 1+min_MCP(change - coin, coins)
            else:
                cm = min(cm, 1+min_MCP(change - coin, coins))

        return cm

print(min_MCP(N, coins))
