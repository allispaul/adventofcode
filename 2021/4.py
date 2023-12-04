# Read input
INPUT = "input4.txt"
data = open(INPUT, "r").read().split("\n\n")
# 0th entry is a list of numbers to be called
nums_to_call = [int(x) for x in data[0].split(",")]
# other entries are bingo boards
boards = [[int(x) for x in board_string.split()] for board_string in data[1:]]
# each board should be a list of length 25
for board in boards:
    assert len(board) == 25

# this holds colors for printing
color = {"RED": "\033[31m", "END": "\033[0m"}

class Board():
    """This contains a 5x5 bingo board, together with information about which numbers
    on the board have been marked. A Board is considered winning if all numbers in a
    row or column are marked.
    """

    def __init__(self, nums):
        self.nums = [nums[i:i+5] for i in range(0,25,5)]
        self.marked = [[0]*5 for _ in range(5)]

    def __repr__(self):
        board_str = ""
        for x in range(5):
            for y in range(5):
                if self.marked[x][y]:
                    board_str = board_str + color["RED"] + \
                        "{:>5}".format(self.nums[x][y]) + color["END"]
                else:
                    board_str = board_str + "{:>5}".format(self.nums[x][y])
            board_str = board_str + "\n"
        return board_str

    def mark(self, num):
        for x in range(5):
            for y in range(5):
                if self.nums[x][y] == num:
                    self.marked[x][y] = 1

    def is_winning(self):
        for n in range(5):
            if self.marked[n] == [1]*5:
                return True
            if [self.marked[x][n] for x in range(5)] == [1]*5:
                return True
        return False

    def score(self):
        """The score is the sum of all the unmarked numbers."""
        score = 0
        for x in range(5):
            for y in range(5):
                if not self.marked[x][y]:
                    score = score + self.nums[x][y]
        return score



class Table():
    """Holds a set of Boards. Calling a number will mark that number on all Boards,
    and then check if any Boards are winning.
    """
    def __init__(self, boards):
        self.boards = []
        for board in boards:
            self.boards.append(Board(board))

    def __repr__(self):
        return "="*30 + "\n" + "\n".join([repr(b) for b in self.boards]) + "="*30

    def mark(self, num):
        for b in self.boards:
            b.mark(num)

    def winning_boards(self):
        """Returns a list of all winning boards."""
        board_list = []
        for b in self.boards:
            if b.is_winning():
                board_list.append(b)
        return board_list

    def non_winning_boards(self):
        """Returns a list of all non-winning boards."""
        board_list = []
        for b in self.boards:
            if not b.is_winning():
                board_list.append(b)
        return board_list


class Game():
    """Holds a Table and a sequence of numbers to be called. On playing the Game,
    the numbers are called in order until a Board wins, at which point the final
    score is returned.
    """
    def __init__(self, nums_to_call, boards):
        self.table = Table(boards)
        self.nums = nums_to_call
        self.final_board = None

    def play(self):
        """Plays until a Board wins and returns the final score. This is the product
        of the score of the winning board and the number just called.
        """
        for n in nums_to_call:
            self.table.mark(n)
            if self.table.winning_boards():
                self.final_board = self.table.winning_boards()[0]
                return self.final_board.score()*n
        return None

    def play_misere(self):
        """Plays until all boards have won, and returns the final score calculated
        from the last board to win.
        """
        for n in nums_to_call:
            self.table.mark(n)
            # if one board left, save it as the final board
            if len(self.table.non_winning_boards()) == 1:
                self.final_board = self.table.non_winning_boards()[0]
            # if no boards left, calculate score from final board
            if len(self.table.non_winning_boards()) == 0:
                return self.final_board.score()*n
        return None

def prob4a():
    my_game = Game(nums_to_call, boards)
    score = my_game.play()
    print(my_game.final_board)
    print("Score:", score)

def prob4b():
    my_game = Game(nums_to_call, boards)
    score = my_game.play_misere()
    print(my_game.final_board)
    print("Score:", score)

prob4b()
