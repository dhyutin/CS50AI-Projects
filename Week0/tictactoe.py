"""
Tic Tac Toe Player
"""
from copy import deepcopy
import math

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_num = 0
    o_num = 0
    for row in board:
        for column in row:
            if(column == 'X'):
                x_num = x_num + 1
            elif(column == 'O'):
                o_num = o_num + 1
   
    if(x_num <= o_num):
        return X
    elif(x_num > o_num):
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    # Returns all positions which are filled as None
    for row in range(len(board)):
        for column in range(len(board[row])):
            if(board[row][column] == None):
                possible_actions.add((row, column))

    return possible_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    result_board = deepcopy(board)

    # returns 'X' or 'O'
    next_move = player(board)

    row = action[0]
    column = action[1]

    if(board[row][column] == None):
        result_board[row][column] = next_move
    else:
        raise Exception

    # print(result_board)

    return result_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check for winners(if any) : Rows
    for row in board:
        if(row[0] != None):
            if((row[0] == row[1]) and (row[2] == row[1])):
                return row[0]
    
    # Check for winners(if any) : Columns
    for i in range(3):
        if(board[i][0] != None):
            if((board[i][0] == board[i][1]) and (board[i][2] == board[i][1])):
                return board[i][0]

    # Check for winners(if any) : Diagonal 1
    if(board[0][0] != None):
        if((board[0][0] == board[1][1]) and (board[2][2] == board[1][1])):
            return board[0][0]

    # Check for winners(if any) : Diagonal 2
    if(board[0][2] != None):
        if((board[0][2] == board[1][1]) and (board[2][0] == board[1][1])):
            return board[0][2]
    
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if(winner(board) != None):
        return True

    for row in board:
        if EMPTY in row:
            return False
    
    # If no possible moves, return True
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    value = winner(board)
    if(value == 'X'):
        return 1
    elif(value == 'O'):
        return -1
    else:
        return 0

def min_value(board):
    best_move = ()
    if(terminal(board) == True):
        return utility(board), best_move
    else:
        limit = 5
        for action in actions(board):
            max = max_value(result(board, action))[0]
            if max < limit:
                limit = max
                best_move = action
    return limit, best_move


def max_value(board):
    best_move = ()
    if(terminal(board) == True):
        return utility(board), best_move
    else:
        limit = -5
        for action in actions(board):
            min = min_value(result(board, action))[0]
            if min > limit:
                limit = min
                best_move = action
    return limit, best_move


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    current_player = player(board)

    if(terminal(board) == True):
        return None
    elif(current_player == 'X'):
        return max_value(board)[1]
    elif(current_player == 'O'):
        return min_value(board)[1]
    
