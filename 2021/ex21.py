def deterministic_game(pos1, pos2):
    die = 1 # number on die
    score1, score2 = 0, 0 # scores
    player1sturn = True # is it player 1's turn?
    rolls = 0 # total rolls of die
    while score1 < 1000 and score2 < 1000:
        if player1sturn:
            # advance pawn
            pos1 += die + (die+1) + (die+2)
            pos1 = ((pos1-1) % 10) + 1 # reduce to be in [1,10]
            # increase score
            score1 += pos1
        else:
            # advance pawn
            pos2 += die + (die+1) + (die+2)
            pos2 = ((pos2-1) % 10) + 1 # reduce to be in [1,10]
            # increase score
            score2 += pos2
        # increase die
        die += 3
        die = ((die - 1) % 100) + 1
        # count roll
        rolls += 3
        # change turn
        player1sturn = not player1sturn
    print(f"Player 1's score: {score1}, Player 2's score: {score2}, Die rolls: {rolls}")


# This dict stores the number of ways to get a given total from 3 rolls of a 3-sided die,
# out of a total of 27 possible rolls.
frequencies = {3: 1,
               4: 3,
               5: 6,
               6: 7,
               7: 6,
               8: 3,
               9: 1}

def dirac_game(pos1, pos2, score1=0, score2=0, winning_score=21, turn = 1):
    # if turn == 1:
    #     print(f"Running game at positions {pos1}, {pos2}, with scores {score1}, {score2}.")
    # elif turn == 2:
    #     print(f"Running game at positions {pos2}, {pos1}, with scores {score2}, {score1}.")
    # else:
    #     raise Exception("Unknown turn", turn)
    # is the game won?
    if score1 >= winning_score:
        return 1, 0
    elif score2 >= winning_score:
        return 0, 1
    wins1 = 0
    wins2 = 0
    for die in frequencies:
        nextpos1 = pos1 + die
        nextpos1 = ((nextpos1-1) % 10) + 1
        nextscore1 = score1 + nextpos1
        results = dirac_game(pos2, nextpos1, score2, nextscore1, winning_score, 3 - turn)
        wins2 += frequencies[die] * results[0]
        wins1 += frequencies[die] * results[1]
    return wins1, wins2
