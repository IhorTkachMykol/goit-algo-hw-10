COINS = [50, 25, 10, 5, 2, 1]


def find_coins_greedy(amount: int) -> dict:
    """
    Жадібний алгоритм видачі решти.
    Складність: O(n), де n — кількість номіналів монет.
    """
    result = {}
    for coin in COINS:
        if amount <= 0:
            break
        count = amount // coin
        if count > 0:
            result[coin] = count
            amount -= coin * count
    return result


def find_min_coins(amount: int) -> dict:
    """
    Алгоритм динамічного програмування для мінімальної кількості монет.
    Складність: O(amount * n), де n — кількість номіналів монет.
    """
    # dp[i] = мінімальна кількість монет для суми i
    dp = [float("inf")] * (amount + 1)
    dp[0] = 0
    # coin_used[i] = номінал монети, використаної останньою для суми i
    coin_used = [0] * (amount + 1)

    for i in range(1, amount + 1):
        for coin in COINS:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                coin_used[i] = coin

    # Відновлення набору монет
    result = {}
    current = amount
    while current > 0:
        coin = coin_used[current]
        result[coin] = result.get(coin, 0) + 1
        current -= coin

    return dict(sorted(result.items()))


if __name__ == "__main__":
    import time

    test_amounts = [113, 1_000, 10_000, 100_000]

    print(f"{'Сума':<12} {'Жадібний (мс)':<18} {'ДП (мс)':<15} {'Жадібний результат':<35} {'ДП результат'}")
    print("-" * 110)

    for amount in test_amounts:
        # Жадібний
        t0 = time.perf_counter()
        greedy = find_coins_greedy(amount)
        t1 = time.perf_counter()
        greedy_ms = (t1 - t0) * 1000

        # ДП
        t0 = time.perf_counter()
        dp = find_min_coins(amount)
        t1 = time.perf_counter()
        dp_ms = (t1 - t0) * 1000

        greedy_str = str(greedy) if amount <= 1000 else f"монет: {sum(greedy.values())}"
        dp_str = str(dp) if amount <= 1000 else f"монет: {sum(dp.values())}"

        print(f"{amount:<12} {greedy_ms:<18.4f} {dp_ms:<15.4f} {greedy_str:<35} {dp_str}")

