"""
File that represents all player's classes in the game
"""
import copy
import math
import time

from Observable import Observable
from Board import Board
from Cards import *

"""
User player class
"""


class Player(Observable):

    def __init__(self, id):
        super().__init__()
        self.currElem = None
        self.nextElem = None
        self.id = id
        self.cards = [Remove("remove", "img/cards/20.png", 1, None), None, None, None, None, None]
        self.initials = "(you)"
        self.block = False  # variable for checking if block card is active and how many
        self.score = 0
        self.stat = 0  # stat for counting how many Three of a Kinds have been made
        self.booster = 0
        self.opponent = None

    # method for initializing the player's elements
    def initialize(self, elements):
        if self.id == "X":
            self.currElem = elements["cross"]
            self.nextElem = elements["triangle"]
        else:
            self.currElem = elements["circle"]
            self.nextElem = elements["square"]

    def removeCard(self, index):
        self.cards[index] = None

    def swap(self):
        self.currElem, self.nextElem = self.nextElem, self.currElem

    def playMove(self, cell):
        cell.insert(self.currElem)
        self.swap()

    def updateScore(self, update):
        if self.booster > 0:
            self.score += 2 * update
            self.booster -= 1
        else:
            self.score += update

    def updateBlock(self):
        for card in self.cards:
            if type(card) == Block:
                if card.active:
                    self.block = True
                    return
        self.block = False

    def removeBlock(self):
        for i in range(len(self.cards)):
            if type(self.cards[i]) == Block:
                if self.cards[i].active:
                    self.removeCard(i)
                    self.updateBlock()
                    break

    def insertCard(self, card):
        for i in range(len(self.cards)):
            if self.cards[i] is None:
                self.cards[i] = card
                break

    def updateStat(self, stat):
        self.stat += stat

    # method for drawing cards if a sequence has been made
    def drawCard(self, args, deck):
        while self.stat >= 3:
            self.stat -= 3
            self.insertCard(deck.draw(1))
        for i in range(len(args)):
            for j in range(len(args[i])):
                self.insertCard(deck.draw(i + 1))


"""
Abstract class for representing AI players
"""


class AI(Player):

    def __init__(self, id):
        super(AI, self).__init__(id)
        self.id = id

    def playMove(self, board):
        pass


"""
Following are variable and functions that are needed 
for the development of the AIs below
"""

boardData = Board(16, 16)
boardData.loadBoard()

# method that return all the empty cells
def getEmptyCells(board):
    empty = []
    grid = board.getBoard()
    for x in range(len(grid)):
        for cell in grid[x]:
            if not cell.hasElement():
                empty += [cell]
    return empty

# method that optimizes the empty cells in one that have adjacent non-empty cell
def optimizeEmptyCells(board):
    result, vectors, cells = [], [], []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                cells += [(i, j)]
    for i in range(2):
        for j in range(2):
            if (i, j) == (0, 0):
                continue
            vectors += [(i, j)]
            vectors += [(-i, -j)]
            vectors += [(i, -j)]
    for cell in cells:
        for rx, ry in vectors:
            try:
                x, y = cell[0] + rx, cell[1] + ry
                if board[x][y] is not None and x >= 0 and y >= 0:
                    result += [cell]
                    break
            except:
                pass
    return result

# parsing an original board into a string board
def parseBoard(board):
    output = []
    for i in range(len(board)):
        row = []
        for j in range(len(board[i])):
            if board[i][j].element is not None:
                row += [board[i][j].element.name]
            else:
                row += [None]
        output += [row]
    return output


"""
Random AI class
"""


class RandomAI(AI):

    def __init__(self, id):
        super(RandomAI, self).__init__(id)
        self.initials = "(RandomAI)"

    def playMove(self, board):
        empty = getEmptyCells(board)
        cell = random.choice(empty)
        cell.insert(self.currElem)
        self.swap()
        return cell


"""
Monte Carlo Tree Search Player 
"""


class MCTS(AI):

    def __init__(self, id):
        super(MCTS, self).__init__(id)
        self.initials = "(MCTS)"

    def playMove(self, board):
        state = parseBoard(board.getBoard())
        start = Node(state)
        start.scores = [self.opponent.score, self.score]
        start.element_queue = [self.currElem.getName(), self.opponent.currElem.getName(),
                               self.nextElem.getName(), self.opponent.nextElem.getName()]
        expand(start)

        for i in range(2000):
            current = select(start)
            if current is None:
                break
            while True:
                if not current.children:
                    if current.n == 0:
                        value = calculate(current)
                        backpropagate(current, value)
                        break
                    else:
                        expand(current)
                        if not current.end:
                            current = select(current)
                        else:
                            break
                else:
                    current = select(current)
                    if current is None:
                        break
        node = getBest(start)
        if node is None:
            x, y = 7, 7
        else:
            x, y = node.cell
        cell = board.getBoard()[x][y]
        cell.insert(self.currElem)
        self.swap()
        return cell

def getBest(node):
    v = float("-inf")
    best = None
    for n in node.children:
        if n.scores[0] >= 100:
            return n
        # if n.n < node.n / len(node.children):
        #     continue
        end = visits(n)
        score = (end.scores[0] - end.scores[1]) * 10
        if not end.turn:
            score = -score
        final = n.n + score
        if v < final:
            best = n
            v = final
    return best

class Node:

    def __init__(self, board):
        self.state = board
        self.turn = False  # used to check if it is MCTS AI player turn
        self.scores = [] # used to check the scores of the players
        self.cell = None
        self.end = False # used to check if it is an end node
        self.element_queue = []
        self.value = 0
        self.children = []
        self.parent = []
        self.n = 0
        self.depth = 0

    def update(self, value):
        self.value += value
        self.n += 1

    def initialize(self, node):
        self.parent = node
        self.turn = not node.turn
        self.depth = node.depth + 1
        node.children += [self]
        self.element_queue = copy.deepcopy(node.element_queue)
        self.element_queue.append(self.element_queue.pop(0))
        self.scores = copy.deepcopy(node.scores)
        self.scores.append(self.scores.pop(0))


def ucb(node):
    if node.n == 0:
        if node.turn:
            return float("inf")
        else:
            return float("-inf")
    v = node.value
    return v + 2 * math.sqrt(math.log(node.parent.n) / node.n)

def select(node):
    v = float("-inf")
    selected = None
    for child in node.children:
        if child.end:
            continue
        score = ucb(child)
        if child.turn:
            if v < score:
                v = score
                selected = child
        else:
            if v < -score:
                v = -score
                selected = child
    if selected is None:
        node.end = True
    return selected

def expand(node):
    if node.scores[0] >= 100:
        node.end = True
    elif node.depth > 3:
        node.end = True
    else:
        optimized_empty = optimizeEmptyCells(node.state)
        for x, y in optimized_empty:
            copy_state = copy.deepcopy(node.state)
            child = Node(copy_state)
            child.initialize(node)
            copy_state[x][y] = node.element_queue[0]
            child.cell = (x, y)

# method for calculating the score of the node
def calculate(node):
    boardData.map(node.state)
    x, y = node.cell
    value = boardData.checkSeq(x, y)[0]
    node.scores[0] += value
    if not node.turn:
        value = value * -1
    return value

def backpropagate(node, value):
    current = node
    while current:
        current.update(value)
        current = current.parent

def visits(node):
    current = node
    v = 0
    while current.children:
        selected = None
        for child in current.children:
            if child.n > v:
                v = child.n
                selected = child
        current = selected
        v = 0
    return current


"""
Minimax Player 
"""

class MiniMax(AI):

    def __init__(self, id, type):
        super(MiniMax, self).__init__(id)
        self.initials = "(Minimax)"
        self.move = None
        self.map = {}
        self.depth = 0
        self.start = 0
        self.type = type

    def playMove(self, board):
        state = parseBoard(board.getBoard())

        p1 = {"score": self.score,
              "elem": self.currElem.getName(),
              "next": self.nextElem.getName()}

        p2 = {"score": self.opponent.score,
              "elem": self.opponent.currElem.getName(),
              "next": self.opponent.nextElem.getName()}

        self.start = time.time()
        depth = 1
        move = None
        while depth < 5 and not timeOut(self.start, 5):
            self.depth = depth
            self.minimax([state, None], depth, [p1, p2], 0, True, float("-inf"), float("inf"))
            if timeOut(self.start, 5) and move is not None:
                self.move = move
            else:
                move = copy.deepcopy(self.move)
            depth += 1

        if self.move is None:
            self.move = (7, 7)
        x, y = self.move
        cell = board.getBoard()[x][y]
        cell.insert(self.currElem)
        self.swap()

        self.map = {}
        self.move = None

        return cell

    def minimax(self, state, depth, players, reward, max_turn, alpha, beta):
        if timeOut(self.start, 5):
            return reward
        if players[0]["score"] >= 100:
            return 100
        if players[1]["score"] >= 100:
            return -100
        if depth == 0:
            return reward
        if max_turn:
            v, v0 = float("-inf"), float("-inf")
            succ = successors(state, players[0]["elem"])
            if succ and self.type == 2:
                succ = optimizeSuccessor(succ, players[1]["elem"])
            for s in succ:
                s_str = str(s)
                s_hash = hash(s_str)
                if s_hash in self.map:
                    score = self.map[s_hash]
                else:
                    score = evaluate(s)
                    self.map[s_hash] = score
                player_copy = copy.deepcopy(players[0])
                update_player(player_copy, reward + score)
                v = max(v, self.minimax(s, depth - 1, [player_copy, players[1]],
                                        reward + score, False, alpha, beta))
                if v >= beta:
                    return v
                if v > alpha:
                    alpha = v
                if v != v0 and depth == self.depth and not timeOut(self.start, 5):
                    self.move = s[1]
                    v0 = v
            return v
        else:
            v = float("inf")
            succ = successors(state, players[1]["elem"])
            succ = optimizeSuccessor(succ, players[0]["elem"])
            for s in succ:
                s_str = str(s)
                s_hash = hash(s_str)
                if s_hash in self.map:
                    score = self.map[s_hash]
                else:
                    score = evaluate(s)
                    self.map[s_hash] = score
                player_copy = copy.deepcopy(players[1])
                update_player(player_copy, reward + score)
                v = min(v, self.minimax(s, depth - 1, [players[0], player_copy],
                                        reward - score, True, alpha, beta))
                if v <= alpha:
                    return v
                if v < beta:
                    beta = v
            return v


def timeOut(start, limit):
    end = time.time()
    if end - start > limit:
        return True
    return False

def successors(state, element):
    coordinate = optimizeEmptyCells(state[0])
    res = []
    for x, y in coordinate:
        copy_state = copy.deepcopy(state[0])
        copy_state[x][y] = element
        res += [[copy_state, (x, y)]]
    return res

def optimizeSuccessor(succs, element):
    map1 = {}
    map2 = {}
    i = 0
    for s in succs:
        x, y = s[1]
        score1 = evaluate(s)
        s[0][x][y] = element
        score2 = evaluate(s)
        map1[i] = score1
        map2[i] = score2
        i += 1
    sort1 = sorted(map1.items(), key=lambda kv: (kv[1], kv[0]))
    sort2 = sorted(map2.items(), key=lambda kv: (kv[1], kv[0]))
    length = len(sort1)-1
    return [succs[sort1[length][0]],
            succs[sort1[length-1][0]],
            succs[sort2[length][0]],
            succs[sort2[length-1][0]]]

def evaluate(state):
    boardData.map(state[0])
    x, y = state[1]
    return boardData.checkSeq(x, y)[0]

def update_player(player, score):
    player["score"] += score
    player["elem"], player["next"] = player["next"], player["elem"]
