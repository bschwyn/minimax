
import random

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

    def __init__(self, player, AI, name):
        self.player = player
        self.AI = False
        self.name = name
        if player == 0:
            self.mark = 'x'
        else:
            self.mark = 'o'

    def get_move(self):
        pass

    def is_position_ok(self, board, row, col):
        if board[row][col] == 'x' or board[row][col] == 'o':
            return False
        else:
            return True

    def get_random_position(self):
        row = random.randint(0,3)
        col = random.randint(0,3)
        return row, col


    def play_move(self, board):
        row,col = self.get_position()
        if self.is_position_ok(board, row, col):
            row, col = self.get_random_position
            self.place_move(board, row, col)
        else:
            print("This was not an acceptable move. Play again")
            #potential infinite loop
            self.play_move()
            #return error

    def place_move(self,board, row, col):
        board.change_board(row, col, self.mark)

    def get_player_info(self):
        pass


class Game():

    def __init(self):
        self.board = Board()
        self.p1 = Player(0,False, "ben")
        self.p2 = Player(1, False, "sam")

    def end_game(self):
        return self.board.is_full() or self.win_condition_met()

    def win_condition_met(self):
        return self.board.three_in_a_row('o') or self.board.three_in_a_row('x')

    def get_next_player(current, player1, player2):
        if current.player == 0:
            next_player = player2
        else:
            next_player = player1
        return next_player

    def run_game(self):
        current_player = self.p1
        while not self.end_game():
            self.b.print_board()
            self.get_next_player(current_player, self.p1, self.p2).play_move(self.b)
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

def test3():
    g = Game()
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

__main__()
