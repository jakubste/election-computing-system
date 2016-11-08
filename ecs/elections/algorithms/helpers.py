def binom(n, k):
    """
    calculates some small binoms, if result is too high, we use constant value
    """
    EDGE = 3
    MAX = 50
    if n > 20 and not (k < EDGE or k + EDGE >= n):
        return MAX
    up = 1
    down = 1
    s = n - k
    while n:
        up *= n
        n -= 1
    while k:
        down *= k
        k -= 1
    while s:
        down *= s
        s -= 1
    return max(up/down, MAX)