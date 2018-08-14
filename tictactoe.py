
import random
import sys


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
              (self.board[0][2] == x and self.board[1][1] == x and self.board[2][0])
        col = (self.board[0][0] == x and self.board[1][0] == x and self.board[2][0]==x) or \
              (self.board[0][1] == x and self.board[1][1] == x and self.board[2][1]==x) or \
              (self.board[0][2] == x and self.board[1][2] == x and self.board[2][2] == x)
        return (row or diag or col)


class Player():

    def __init__(self, firstplayer, name, ai, mark:
        if testmode:
            if firstplayer:
                name = "Player1test"
                ai = False
                mark = 'x'
            else:
                name = "player2test"
                ai = False
                mark = 'o'
        else:
            firstplayer, name, ai, mark = self.get_player_variables(firstplayer)

        self.firstplayer = firstplayer
        self.name = name
        self.ai = ai
        self.mark = mark

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
                name = sys.stdin.readlin()
            print(name + " will be placing o's")
            print()
        return firstplayer, name, ai, mark


    def get_move(self, board):
        if self.ai:
            move = self.get_move_from_ai(board)
        else:
            move = self.get_move_from_human(board)
        return move

    def get_move_from_agent(self, board):

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

    def __init__(self, board, player, other_player, firstplayer):
        self.p1 = player
        self.p2 = other_player

    def get_next_player(self,current):
        player1 = self.p1
        player2 = self.p2
        if current.firstplayer:
            next_player = player2
        else:
            next_player = player1
        return next_player

    def utility(self, board, player):
        mark_of_other_player = self.get_next_player(player)
        if board.three_in_a_row(player.mark):
            return 1
        elif board.three_in_a_row(mark_of_other_player):
            return -1
        else:
            return 0

    def game_over(self, board):
        return board.is_full() or board.three_in_a_row('x') or board.three_in_a_row('o')

    def minimax(self, board, player):
        if self.game_over(board):
            return self.utility(board, player)

        maximizing_player = (self.p1.firstplayer == player.firstplayer)
        if maximizing_player:
            bestval = -float('inf')
            for move in board.open_moves():
                row, col = move
                board.change_board(row, col, player.mark)
                value = self.minimax(board, self.get_next_player(player))
                board.change_board(row, col, player.mark)
                bestval = max(bestval, value)
                return bestval

        else:
            bestval = float('inf')
            for move in board.open_moves():
                row, col = move
                board.change_board(row, col, player.mark)
                val = self.minimax(board, self.get_next_player(player))
                board.change_board(row, col, ' ')
                bestval = min(bestval, val)
                return bestval

class Game():

    def __init__(self, testmode):
        self.board = Board()
        name, ai = self.get_player_variables(True)
        if ai:
            self.p1 = Agent(True, name)
        else:
            self.p1 = Player(True, name, mark)
        secondplayer2, name2, ai2, mark2 = self.get_player_variables(False)
        if ai2:
            self.p2 = Agent(False, name2)
        else:
            self.p2 = Player(False)

        self.p1 = Player(True, testmode)
        self.p2 = Player(False, testmode)

    def get_player_something(self, firstplayer):


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
                name = sys.stdin.readlin()
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
    g = Game(testmode)
    g.run_game()

#test1()
#test2()
test3()


def __main__():
    print('hello')
    g = Game()
    #player 1 name? : "ben" enter
    #player 2 name? : "computer" enter
    #print board
    #player 1's turn: a3
    #print board
    #player 2's turn - player 2 played in B1
    #print board
    #player 1's turn:
    #...
    #player 2 won!

#__main__()
