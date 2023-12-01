import math


def turns_to_defeat(damage, enemy_armor, enemy_hp):
    effective_damage = max(damage-enemy_armor, 1)
    return math.ceil(enemy_hp / effective_damage)


# For a given damage, what's the least armor that will win the fight?
def armor_from_damage(boss_damage, boss_armor, boss_hp, my_damage, my_hp=100):
    for my_armor in range(11):
        if turns_to_defeat(my_damage, boss_armor, boss_hp) <= \
           turns_to_defeat(boss_damage, my_armor, my_hp):
            return my_armor


def test():
    print(turns_to_defeat(5, 2, 12))
    print(turns_to_defeat(7, 5, 8))
    my_armor = armor_from_damage(7, 2, 12, 5, 8)
    print(my_armor)
    print(turns_to_defeat(7, my_armor, 8))


if __name__ == "__main__":
    boss_hp = 109
    boss_damage = 8
    boss_armor = 2
    damage_costs = {4: 8,
                    5: 10,
                    6: 25,
                    7: 40,
                    8: 65,
                    9: 90,
                    10: 124,
                    11: 159,
                    12: 190,
                    13: 224}
    armor_costs = {0: 0,
                   1: 13,
                   2: 31,
                   3: 51,
                   4: 71,
                   5: 91,
                   6: 113,
                   7: 135}
    print("WINNING STRATS:")
    for my_damage in range(4, 14):
        my_armor = armor_from_damage(boss_damage, boss_armor, boss_hp,
                                     my_damage)
        damage_cost = damage_costs[my_damage]
        armor_cost = armor_costs[my_armor]
        total_cost = damage_cost + armor_cost
        print(f"{my_damage=}, {my_armor=}, {damage_cost=}, {armor_cost=}, {total_cost=}")
    print("LOSING STRATS:")
    damage_costs = {4: 8,
                    5: 33, # 1 ring
                    6: 58, # 1 ring
                    7: 108, # 1 ring
                    8: 133, # 2 rings, 110 with 1 ring
                    9: 158, # 2 rings, 125 with 1 ring
                    10: 160} # 2 rings
    armor_costs = {0: 0,
                   1: 20, # 1 ring
                   2: 40, # 1 ring
                   3: 80, # 1 ring
                   4: 100, # 2 rings
                   5: 120, # 2 rings
                   6: 133} # 1 ring
    for my_damage in range(4, 14):
        my_armor = armor_from_damage(boss_damage, boss_armor, boss_hp,
                                     my_damage)
        if my_armor == 0:
            continue
        damage_cost = damage_costs[my_damage]
        armor_cost = armor_costs[my_armor-1]
        total_cost = damage_cost + armor_cost
        print(f"{my_damage=}, my_armor={my_armor-1}, {damage_cost=}, {armor_cost=}, {total_cost=}")
