"""
Tic Tac Toe Player

PULAKSH
"""

import math
import copy

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
    x=0 #initialize counter for 'X'
    o=0 #initialize counter for 'X'
    if len(actions(board))==0: #if no action left return None
        return None
    for i in range(3): #iterate for each row
        x+=board[i].count(X) #count number of 'X' for each row
        o+=board[i].count(O) #count number of 'X' for each row
    if x>o: #if more x then turn of O
        return O
    elif o==x: # if equal then turn of X since X goes first
        return X
    else:
        raise Exception("player(b) o>x")
    #raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    list = set() #initialize empty set
    for i in range(3): #iterate over rows
        for j in range(3): #iterate over columns
            if board[i][j]==EMPTY: #if space is empty then
                list.add(tuple((i,j))) #it is a possible action
    return list

#    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    b=copy.deepcopy(board) #deepcopy board
    #print(b)
    p=player(board) #get turn player
    #print (b)
    #print(type(b),action)
    if p == None: #if None player
        raise Exception("result(b) invalid action -", action," p ",p)
    elif b[action[0]][action[1]] == EMPTY: #if empty
        #print("prob", action)
        #print(b)
        b[action[0]][action[1]] = p #assign value
        return b
    else:
        raise Exception("result(b) invalid action - ", action," location already occupied by -",b[action[0],action[1]])
#    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    won=utility(board) #retun value according to utility
    if won==1:
        return X
    elif won == -1:
        return O
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if len(actions(board)) == 0 or winner(board) != None : #if someone has won or no-more actions possible
        return True
    else:
        return False
    #raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    for i in range(3): #iterate for middle row
        c = board[1][i]
        if (c== EMPTY): #check if cell empty
            continue
        if c==board[0][i] and c==board[2][i]: #if middle cell = upper cell and lower cell return the winning player
            if c==X:
                return 1
            else:
                return -1
            #return c
        elif i==1:
            if( (board[1][1]==board[0][0] and board[1][1]==board[2][2]) or (board[1][1]==board[0][2] and board[1][1]==board[2][0])):
                #print("abcd") #if any diagonal are equal then return winning player
                if c==X:
                    return 1
                elif c==O:
                    return -1

    for i in range(3): #iterate over rows
        c = board[i][0]
        if (c== EMPTY):
            continue
        if c==board[i][1] and c==board[i][2]: #if all vaues in row equal return winning player
            if c==X:
                return 1
            elif c==O:
                return -1
    if len(actions(board)) == 0: #if no one won and no more actions possible then return 0 (tie)
        return 0
    
    #raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #print("prunning")
    boardCopy=copy.deepcopy(board) #copy the board
    if terminal(board): #return None for terminal board
        return None
    p=player(board) #save the current player
    at=actions(board) #save list of actions
    if len(at)==9:
        return tuple((0,1))
    if p==O: #for O min implementation
        minInt= 20 #initialize to infinity
        miat=set() #initialize empty set
        for i in at: #iterate over list of possible actions
            b=copy.deepcopy(boardCopy)
            mint=(minimaxSearch(result(b,i),minInt)) #save result of minimaxSearch
            if mint == -1:
                return i
            if mint < minInt: #if better value -min
                minInt= mint #save
                miat=i
        #print(miat)
        return miat

    elif p==X:
        maxInt= -20 #initialize to -infinity
        maat=set() #initialize empty set
        for i in at: #iterate over list
            b=copy.deepcopy(boardCopy)
            maxt=(minimaxSearch(result(b,i),maxInt)) #save result from minimaxSearch
            if maxt == 1:
                return i
            if maxt > maxInt: #if better value - max
                maxInt= maxt #save
                maat=i
        #print (maxt)
        return maat

def minimaxSearch(board, prunInt):
    #print("called minimaxSearch")
    boardCopy=copy.deepcopy(board) #copy board
    at=actions(board) #list of possible actions
    p=player(board) #player turn
    if terminal(board):
        return utility(boardCopy)#return 0

    if p==O: #min
        minInt= 20 #initialize to infinity
        for i in at: #iterate over list
            b=copy.deepcopy(boardCopy)
            res=result(b,i) #save result board
            ut=utility(res) #calculate result utility
            if (ut == 1) or (ut == -1) or (ut == 0): #if won or tie confirm return value
                #print(ut)
                if ut<minInt:
                    minInt=ut
                #return ut
            else:
                mint=minimaxSearch(res,minInt)
                if mint<prunInt:
                    return mint
                if mint<minInt:
                    minInt=mint
        return minInt

    elif p==X:
        maxInt= -20
        for i in at:
            b=copy.deepcopy(boardCopy)
            res=result(b,i)
            ut=utility(res)
            #print("res ",res," ut ",ut, "maxInt", maxInt)
            if (ut == 1) or (ut == -1) or (ut == 0):
                #print(ut)
                if ut>maxInt:
                    maxInt=ut
                #return ut
            else:
                maxt=minimaxSearch(res,maxInt)
                #print("maxt",maxt)
                if maxt>prunInt:
                    return maxt
                if maxt>maxInt:
                    maxInt=maxt
        return maxInt
