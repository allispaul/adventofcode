import hashlib

def prob4(secret_key, num_zeros):
    m = hashlib.md5()
    m.update(secret_key.encode())
    num = 1
    while True:
        m1 = m.copy()
        m1.update(str(num).encode())
        hash = m1.hexdigest()
        if hash[:num_zeros] == "0" * num_zeros:
            return num
        num += 1
        if num % 10000 == 0:
            print(num)

if __name__ == "__main__":
    print(prob4("iwrupvqb", 6))
