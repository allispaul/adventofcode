spell_costs = {"Magic Missile": 53,
               "Drain": 73,
               "Shield": 113,
               "Poison": 173,
               "Recharge": 299}

class OutOfSpellsException(Exception):
    pass


class Player():
    def __init__(self, hp, armor, mana):
        self.hp = hp
        self.armor = armor
        self.mana = mana

    def take_damage(self, boss_damage):
        effective_damage = max(1, boss_damage - self.armor)
        self.hp = max(0, self.hp - effective_damage)
        return effective_damage

    def available_spells(self):
        return [spell for spell in spell_costs.keys()
                if spell_costs[spell] <= self.mana]


class Boss():
    def __init__(self, hp, damage):
        self.hp = hp
        self.damage = damage

    def take_damage(self, player_damage):
        self.hp = max(0, self.hp - player_damage)


class Game():

    def __init__(self, *, spell_gen, player_hp, player_mana, boss_hp,
                 boss_damage, verbose):
        self.player = Player(hp=player_hp,
                             armor=0,
                             mana=player_mana)
        self.boss = Boss(hp=boss_hp,
                         damage=boss_damage)
        self.effects = {"Poison": 0, "Shield": 0, "Recharge": 0}
        self.is_players_turn = True
        self.spell_gen = spell_gen
        self.verbose = verbose
        self.won = None
        self.mana_spent = 0

    def player_turn(self):
        self.apply_effects()
        if len(self.player.available_spells()) == 0:
            raise OutOfSpellsException
        spell = next(self.spell_gen)
        while spell_costs[spell] > self.player.mana:
            self.game_print("You can't afford that spell.")
            spell = next(self.spell_gen)
        self.player.mana -= spell_costs[spell]
        self.mana_spent += spell_costs[spell]
        if spell == "Magic Missile":
            self.game_print("You cast Magic Missile, doing 4 damage.")
            self.boss.take_damage(4)
        elif spell == "Drain":
            self.game_print("You cast Drain, doing 2 damage and healing you for 2.")
            self.boss.take_damage(2)
            self.player.hp += 2
        elif spell == "Shield":
            self.game_print("You cast Shield, increasing armor by 7.")
            self.effects["Shield"] = 6
            self.player.armor = 7
        elif spell == "Poison":
            self.game_print("You cast Poison.")
            self.effects["Poison"] = 6
        elif spell == "Recharge":
            self.game_print("You cast Recharge.")
            self.effects["Recharge"] = 5
        else:
            raise ValueError("Unrecognized spell", spell)
        if self.boss.hp <= 0:
            self.boss.hp = 0
            self.won = True

    def boss_turn(self):
        self.apply_effects()
        damage = self.player.take_damage(self.boss.damage)
        self.game_print(f"Boss deals {damage} damage!")
        if self.player.hp <= 0:
            self.game_print("You die!")
            self.won = False

    def play_game(self):
        while self.won is None:
            self.show_status_line()
            if self.is_players_turn:
                try:
                    self.player_turn()
                except OutOfSpellsException:
                    self.game_print("No available spells! You die!")
                    self.won = False
            else:
                self.boss_turn()
            self.is_players_turn = not self.is_players_turn
        return self.won

    def apply_effects(self):
        for effect in self.effects:
            if self.effects[effect] > 0:
                self.effects[effect] -= 1
                if effect == "Shield":
                    self.game_print(f"Shield's timer is now {self.effects['Shield']}.")
                elif effect == "Poison":
                    self.game_print("Poison deals 3 damage; " +
                                    f"its timer is now {self.effects['Poison']}.")
                    self.boss.take_damage(3)
                elif effect == "Recharge":
                    self.game_print("Recharge recovers 101 mana; " +
                                    f"its timer is now {self.effects['Recharge']}.")
                    self.player.mana += 101
                else:
                    raise ValueError("Unrecognized effect", effect)
                if self.effects[effect] == 0:
                    self.game_print(f"{effect} wears off.")
                    if effect == "Shield":
                        self.player.armor -= 7


    def show_status_line(self):
        self.game_print("")
        if self.is_players_turn:
            self.game_print("---- Your turn ----")
        else:
            self.game_print("--- Boss's turn ---")
        self.game_print(f"You have {self.player.mana} mana and {self.player.hp} HP.")
        self.game_print(f"The boss has {self.boss.hp} HP.")
        if self.is_players_turn:
            spell_string = "Available spells: " \
                + ", ".join(self.player.available_spells()) \
                + "."
            self.game_print(spell_string)

    def game_print(self, string):
        if self.verbose:
            print(string)


class InteractiveGame(Game):

    def interactive_gen(self):
        while True:
            spell = input("Cast a spell: ").title()
            if spell.title() not in spell_costs:
                print("I didn't understand that.")
            else:
                yield spell

    def __init__(self, *, player_hp, player_mana, boss_hp, boss_damage):
        interactive_gen = self.interactive_gen()
        super().__init__(spell_gen=interactive_gen,
                         player_hp=player_hp, player_mana=player_mana,
                         boss_hp=boss_hp, boss_damage=boss_damage,
                         verbose=True)


class GameFromTree(Game):

    def tree_gen(self, choices):
        for choice in choices:
            spells = self.player.available_spells()
            if choice < len(spells):
                yield spells[choice]
            else:
                yield spells[-1]

    def __init__(self, *, player_hp, player_mana, boss_hp, boss_damage,
                 spell_choices, verbose):
        super().__init__(spell_gen=self.tree_gen(spell_choices),
                         player_hp=player_hp, player_mana=player_mana,
                         boss_hp=boss_hp, boss_damage=boss_damage,
                         verbose=verbose)

# TODO:
# Iterate through possible spell orders

if __name__ == "__main__":
    player_hp = 50
    player_mana = 500
    boss_hp = 58
    boss_damage = 9

    g = GameFromTree(player_hp=player_hp, player_mana=player_mana,
                     boss_hp=boss_hp, boss_damage=boss_damage,
                     verbose=True, spell_choices = [0, 1, 2, 3, 4, 3, 2, 1, 0])
    g.play_game()
