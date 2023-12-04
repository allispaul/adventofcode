from sympy.ntheory import factorint


def presents(n):
    factorization = factorint(n)
    product = 1
    for p in factorization:
        sum = 0
        for k in range(factorization[p]+1):
            sum += p**k
        product *= sum
    return product*10
    # sum = 0
    # for d in range(1, n+1):
    #     if n % d == 0:
    #         sum += d
    # return sum*10

def foo(n, target):
    best = n
    for m in range(n, 2, -1):
        if presents(m) >= target:
            best = m
            print(m)
    return best


if __name__ == "__main__":
    for n in range(1, 11):
        print(n, presents(n))
    n = 1
    while presents(n) < 29000000:
        n += 1
        if n % 10000 == 0:
            print(n)
    print(n, presents(n))

