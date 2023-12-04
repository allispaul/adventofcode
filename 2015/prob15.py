ingredients = [[3, 0, 0, -3, 2],
               [-3, 3, 0, 0, 9],
               [-1, 0, 4, 0, 1],
               [0, 0, -2, 2, 8]]

test_ingredients = [[-1, -2, 6, 3, 8],
                    [2, 3, -2, -1, 3],
                    [-99, -99, -99, -99, 0],
                    [-99, -99, -99, -99, 0]]


def prob15a(ingredients):
    recipe = []
    best_score = 0
    for a in range(101):
        for b in range(101-a):
            for c in range(101-(a+b)):
                d = 100-(a+b+c)
                amounts = [a, b, c, d]
                cap = max(sum(ingredients[n][0]*amounts[n] for n in range(4)), 0)
                dur = max(sum(ingredients[n][1]*amounts[n] for n in range(4)), 0)
                flav = max(sum(ingredients[n][2]*amounts[n] for n in range(4)), 0)
                text = max(sum(ingredients[n][3]*amounts[n] for n in range(4)), 0)
                score = cap*dur*flav*text
                if score > best_score:
                    best_score = score
                    recipe = amounts
    return best_score, recipe

def prob15b(ingredients):
    recipe = []
    best_score = 0
    for a in range(101):
        for b in range(101-a):
            for c in range(101-(a+b)):
                d = 100-(a+b+c)
                amounts = [a, b, c, d]
                cap = max(sum(ingredients[n][0]*amounts[n] for n in range(4)), 0)
                dur = max(sum(ingredients[n][1]*amounts[n] for n in range(4)), 0)
                flav = max(sum(ingredients[n][2]*amounts[n] for n in range(4)), 0)
                text = max(sum(ingredients[n][3]*amounts[n] for n in range(4)), 0)
                calories = sum(ingredients[n][4]*amounts[n] for n in range(4))
                if calories != 500:
                    continue
                score = cap*dur*flav*text
                if score > best_score:
                    best_score = score
                    recipe = amounts
    return best_score, recipe

if __name__ == "__main__":
    print(prob15a(ingredients))
    print(prob15b(test_ingredients))
    print(prob15b(ingredients))
