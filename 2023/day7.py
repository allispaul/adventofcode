# This is a problem about sorting based on a weird order.
# Python's built-in sort is really fast, so we'll take advantage of it by
# defining an orderable object.

from functools import total_ordering
from collections import Counter
from enum import IntEnum

class HandType(IntEnum):
    # Using IntEnum rather than Enum for comparison
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

CARDS = {
        'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10,
        '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4,
        '3': 3, '2': 2,
        }

CARDS_WITH_JOKER = {
        'A': 14, 'K': 13, 'Q': 12, 'T': 10,
        '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4,
        '3': 3, '2': 2, 'J': 1,
        }

@total_ordering
class Hand:
    def __init__(self, cards_str, use_jokers = False):
        self.use_jokers = use_jokers
        if use_jokers:
            self.cards = [CARDS_WITH_JOKER[c] for c in cards_str]
        else:
            self.cards = [CARDS[c] for c in cards_str]
    
    def hand_type(self):
        counter = Counter(self.cards)
        num_jokers = counter[1] if self.use_jokers else 0
        counts = list(counter.values())
        counts.sort()
        if 5 in counts:
            return HandType.FIVE_OF_A_KIND
        elif 4 in counts:
            if num_jokers > 0:
                return HandType.FIVE_OF_A_KIND
            return HandType.FOUR_OF_A_KIND
        elif 3 in counts and 2 in counts:
            if num_jokers > 0:
                return HandType.FIVE_OF_A_KIND
            return HandType.FULL_HOUSE
        elif 3 in counts:
            if num_jokers > 0:
                return HandType.FOUR_OF_A_KIND
            return HandType.THREE_OF_A_KIND
        elif counts == [1, 2, 2]:
            if num_jokers == 2:
                return HandType.FOUR_OF_A_KIND
            elif num_jokers == 1:
                return HandType.FULL_HOUSE
            return HandType.TWO_PAIR
        elif 2 in counts:
            if num_jokers == 2:
                return HandType.THREE_OF_A_KIND
            elif num_jokers == 1:
                return HandType.THREE_OF_A_KIND
            return HandType.ONE_PAIR
        else:
            if num_jokers == 1:
                return HandType.ONE_PAIR
            return HandType.HIGH_CARD

    def __eq__(self, other):
        return self.cards == other.cards
        
    def __lt__(self, other):
        if self.hand_type() < other.hand_type():
            return True
        elif self.hand_type() > other.hand_type():
            return False
        return self.cards < other.cards

def prob7a(text):
    lines = text.split("\n")
    hands = [(Hand(line.split()[0]), int(line.split()[1]))
             for line in lines]
    hands.sort(key=lambda x: x[0])
    total = 0
    for i, (hand, bid) in enumerate(hands):
        total += (i+1)*bid
    return total

def prob7b(text):
    lines = text.split("\n")
    hands = [(Hand(line.split()[0], True), int(line.split()[1]))
             for line in lines]
    hands.sort(key=lambda x: x[0])
    total = 0
    for i, (hand, bid) in enumerate(hands):
        total += (i+1)*bid
    return total

test = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

if __name__ == "__main__":
    # some tests
    hands = [
            "23456", "32456", "T2456", "J2456", "Q89T3", "K9872", "A3K2J",
            "22456", "23537", "T45T9", "A983A",
            "24323", "56677", "898A9", "KK2A2",
            "222A3", "3A3K3", "99KA9", "QJJJ3", "QAAA3",
            "22AAA", "2AAA2", "AKAAK", "AAA22", "AAAKK",
            "23222", "66366", "AAAAK",
            "22222", "99999",
            ]
    for i in range(len(hands)):
        for j in range(i+1, len(hands)):
            assert Hand(hands[i]) < Hand(hands[j]), hands[i] + " " + hands[j]
            assert Hand(hands[j]) > Hand(hands[i]), hands[i] + " " + hands[j]
    assert prob7a(test) == 1*765 + 2*220 + 3*28 + 4*684 + 5*483
    hands = [
            "23456", "32456", "T2456", "Q89T3", "K9872", 
            "J2456", "22456", "23537", "T45T9", "A3K2J", "A983A",
            "24323", "56677", "898A9", "KK2A2",
            "JA3K3", "222A3", "2245J", "3A3K3", "99KA9", "QAAA3",
            "22AAA", "2AAA2", "AKAAK", "AAA22", "AAAKK",
            "23222", "66366", "QJJJ3", "AAAAK",
            "JJJJJ", "22222", "9JJJJ", "9JJJ9", "9J99J", "99J99", "99999"
            ]
    for i in range(len(hands)):
        for j in range(i+1, len(hands)):
            assert Hand(hands[i], True) < Hand(hands[j], True), \
                    hands[i] + " " + hands[j]
            assert Hand(hands[j], True) > Hand(hands[i], True), \
                    hands[i] + " " + hands[j]
    assert prob7b(test) == 5905

#    for line in open("input7", "r").read()[:-1].split("\n"):
#        if "J" in line:
#            cards = line.split()[0]
#            print(cards, Hand(cards).hand_type().name, Hand(cards, True).hand_type().name)

    print(prob7a(open("input7", "r").read()[:-1]))
    print(prob7b(open("input7", "r").read()[:-1]))

