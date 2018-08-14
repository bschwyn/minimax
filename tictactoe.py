
import random
import sys


#different ways that this could go:
#player has agent

#agent / minimax needs to know mark of both players to put on the board, and a boolean value for which player is associated w/ each mark
#player needs a mark and a location
#game could have an agent which knows both players and is called upon by a player when they want to use an AI
#marks could just be isolated from players and instead associated with firstplayer and secondplayer

#philosophy get it done vs philosophy get it done the "right way"



class Board():

    def __init__(self):
        self.board = [[' ',' ',' '],
                      [' ',' ',' '],
                      [' ',' ',' ']]

    def change_board(self,row, col, marker):
        self.board[row][col] = marker

    def initialize_board(self, b):
        self.board = b

    def is_full(self):
        full = True
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    return False
        return full

    def game_over(self):
        return self.is_full() or self.three_in_a_row('x') or self.three_in_a_row('o')

    def open_moves(self):
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    moves.append((i,j))
        return moves

    def print_board(self):
        print('  1 2 3')
        print('a ' + self.board[0][0] + '|' + self.board[0][1] + '|' + self.board[0][2])
        print('b ' + self.board[1][0] + '|' + self.board[1][1] + '|' + self.board[1][2])
        print('c ' + self.board[2][0] + '|' + self.board[2][1] + '|' + self.board[2][2])
        print()

    def three_in_a_row(self, x):
        row = (self.board[0] == [x,x,x] or self.board[1] == [x,x,x] or self.board[2] ==[x,x,x])

        diag = (self.board[0][0] == x and self.board[1][1] == x and self.board[2][2] == x) or \
               (self.board[0][2] == x and self.board[1][1] == x and self.board[2][0] == x)

        col = (self.board[0][0] == x and self.board[1][0] == x and self.board[2][0]==x) or \
              (self.board[0][1] == x and self.board[1][1] == x and self.board[2][1]==x) or \
              (self.board[0][2] == x and self.board[1][2] == x and self.board[2][2] == x)
        return (row or diag or col)


class Player():

    def __init__(self, firstplayer, name, ai, mark):

        self.firstplayer = firstplayer
        self.name = name
        self.ai = ai
        self.mark = mark

        if ai:
            self.agent = Agent(mark)

    def get_move(self, board):
        if self.ai:
            move = self.get_move_from_ai(board)
        else:
            move = self.get_move_from_human(board)
        return move

    def get_move_from_ai(self, board):
        (row, col) = self.agent.get_move(board, self.mark)
        return (row, col)

    def get_move_from_human(self, board):
        print(self.name + " - enter a row, column. [format 'a,3' for upper right]" )
        position = sys.stdin.readline()
        try:
            row, col= position.strip().split(',')
            mapping = {'a':0, 'b':1, 'c':2, '1':0, '2':1, '3':2}
            row = mapping[row]
            col = mapping[col]
            if self.is_position_ok(board, row, col):
                return (row, col)
            else:
                print("that move was not valid. Please enter another")
                return self.get_move_from_human(board)
        except Exception:
            print("that move was not valid. Please enter another")
            return self.get_move_from_human(board)



    def is_position_ok(self, board, row, col):
        if row < 0 or row > 2 or col < 0 or col > 2:
            return False
        if board.board[row][col] == 'x' or board.board[row][col] == 'o':
            return False
        else:
            return True

    def get_random_position(self):
        row = random.randint(0,3)
        col = random.randint(0,3)
        return row, col


    def play_move(self, board):
        row,col = self.get_move(board)
        self.place_move(board, row, col)

    def place_move(self,board, row, col):
        board.change_board(row, col, self.mark)

class Agent():

    def __init__(self,  mark):
        self.mark = mark

    def other_mark(self, mark):
        if mark == 'x':
            return 'o'
        else:
            return 'x'

    def utility(self, board, original_mark):
        mark_of_other_player = self.other_mark(original_mark)
        if board.three_in_a_row(original_mark):
            return 1
        elif board.three_in_a_row(mark_of_other_player):
            return -1
        else:
            return 0

    def get_move(self, board, mark):

        best_val = -float('inf')
        best_move = None

        for move in board.open_moves():
            row, col = move
            board.change_board(row, col, mark)
            m = self.other_mark(mark)
            move_val = self.minimax(board, m, False)
            board.change_board(row, col, ' ')

            if move_val > best_val:
                best_val = move_val
                best_move = (row, col)
        return best_move


    def minimax(self, board, mark, maximizing_player):

        if board.game_over():
            return self.utility(board, mark)

        if maximizing_player:
            bestval = -float('inf')
            for move in board.open_moves():
                row, col = move
                board.change_board(row, col, mark)
                value = self.minimax(board, self.other_mark(mark), False)
                board.change_board(row, col, ' ')
                bestval = max(bestval, value)
            return bestval

        else:
            bestval = float('inf')
            for move in board.open_moves():
                row, col = move
                board.change_board(row, col, mark)
                val = self.minimax(board, self.other_mark(mark), True)
                board.change_board(row, col, ' ')
                bestval = min(bestval, val)
            return bestval

class Game():

    def __init__(self):
        self.board = Board()

        first, p1name, p1ai, p1mark = self.get_player_variables(True)
        self.p1 = Player(True, p1name, p1ai, p1mark)

        second, p2name, p2ai, p2mark = self.get_player_variables(False)
        self.p2 = Player(False, p2name, p2ai, p2mark)


    def get_player_variables(self,firstplayer):
        if firstplayer:
            mark = 'x'
            print("is player 1 human? (y/n)")
            human = sys.stdin.readline().strip()
            if human == "y" or human == "yes":
                ai = False
                print("Player 1 - what is your name?:")
                name = sys.stdin.readline().strip()
            else:
                ai = True
                print("What will Player1bot's name be?")
                name = sys.stdin.readline().strip()
            print(name + " will placing x's")
            print()
        else:
            mark = 'o'
            print("is player 2 human? (y/n)")
            human = sys.stdin.readline().strip()
            if human == "y" or human == "yes":
                ai = False
                print("Player 2 - what is your name?:")
                name = sys.stdin.readline().strip()
            else:
                ai = True
                print("what will Player2bot's name be?")
                name = sys.stdin.readline()
            print(name + " will be placing o's")
            print()
        return firstplayer, name, ai, mark

    def end_game(self):
        return self.board.is_full() or self.win_condition_met()

    def win_condition_met(self):
        return self.board.three_in_a_row('o') or self.board.three_in_a_row('x')

    def get_next_player(self,current):
        player1 = self.p1
        player2 = self.p2
        if current.firstplayer:
            next_player = player2
        else:
            next_player = player1
        return next_player

    def run_game(self):
        current_player = self.p2
        while not self.end_game():
            self.board.print_board()
            current_player = self.get_next_player(current_player)
            current_player.play_move(self.board)
        self.board.print_board()


        if self.board.three_in_a_row(current_player.mark):
            print(current_player.name + " has won the game!")
        else:
            print("draw!")
        return

def test1():
    b = Board()
    b.print_board()

    b.initialize_board([['x','o','x'],['x','o','o'],[' ','o','x']])

    b.print_board()
    print(b.three_in_a_row('o'))
    b.initialize_board([['x','.','.'],['.','x','.'],['.','.','x']])
    b.print_board()
    print(b.three_in_a_row('x'))
    print(b.three_in_a_row('o'))

def test2():
    b = Board()
    p1 = Player(0, False, "ben")
    p2 = Player(1, False, "sam")
    p1.place_move(b,0,1)
    p2.place_move(b,1,1)
    b.print_board()

def test_get_current_player():
    g = Game(testmode=True)
    current_player = g.p1
    #print(current_player.p1.)

def test3():
    testmode = False
    g = Game()
    g.run_game()

def test4():
    somethingwrong = [['x', ' ', 'x'],
     [' ', 'x', ' '],
     ['o', ' ', 'o']]
    b = Board()
    b.board = somethingwrong
    print(b.three_in_a_row('x'))

#test4()
#test1()
#test2()
test3()


def __main__():
    print('hello')
    g = Game()

#__main__()
