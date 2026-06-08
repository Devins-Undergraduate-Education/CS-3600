# search.py͏󠄂͏️͏󠄌͏󠄎͏︁͏󠄑͏︈
# ---------͏󠄂͏️͏󠄌͏󠄎͏︁͏󠄑͏︈
# Licensing Information:  You are free to use or extend these projects for͏󠄂͏️͏󠄌͏󠄎͏︁͏󠄑͏︈ 
# educational purposes provided that (1) you do not distribute or publish͏󠄂͏️͏󠄌͏󠄎͏︁͏󠄑͏︈ 
# solutions, (2) you retain this notice, and (3) you provide clear͏󠄂͏️͏󠄌͏󠄎͏︁͏󠄑͏︈ 
# attribution to UC Berkeley, including a link to͏󠄂͏️͏󠄌͏󠄎͏︁͏󠄑͏︈ 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html͏󠄂͏️͏󠄌͏󠄎͏︁͏󠄑͏︈
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.͏󠄂͏️͏󠄌͏󠄎͏︁͏󠄑͏︈
# The core projects and autograders were primarily created by John DeNero͏󠄂͏️͏󠄌͏󠄎͏︁͏󠄑͏︈ 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).͏󠄂͏️͏󠄌͏󠄎͏︁͏󠄑͏︈
# Student side autograding was added by Brad Miller, Nick Hay, and͏󠄂͏️͏󠄌͏󠄎͏︁͏󠄑͏︈ 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).͏󠄂͏️͏󠄌͏󠄎͏︁͏󠄑͏︈


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).
    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state
        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state
        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take
        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    return baseSearchAlgorithm(problem, util.Stack())


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    return baseSearchAlgorithm(problem, util.Queue())



def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """
    "*** YOUR CODE HERE ***"
    return baseSearchAlgorithm(problem, util.PriorityQueueWithFunction(lambda var : var[2]))


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    "*** YOUR CODE HERE ***"
    return baseSearchAlgorithm(problem, util.PriorityQueueWithFunction(lambda var : var[2] + heuristic(var[0], problem)))

def baseSearchAlgorithm(problem, dataStructure):
    fringe = dataStructure # set the fringe to the needed data structure
    visitedNodes = set() # no need to reorder/index entries, so a set works
    parentNodes = {} # needed list for parent nodes, not required for dfs
    # Nodes follow the format: ((X, Y), DIRECTION, DIST FROM GOAL)

    startPos = problem.getStartState() # position, starting with start

    for successor in problem.getSuccessors(startPos):
        parentNodes[successor] = startPos
        fringe.push(successor)

    visitedNodes.add(startPos)

    cliff = fringe.isEmpty() # if the node cannot go anywhere (ie. a cliff), let it be known!

    while not cliff:

        node = fringe.pop() # explores new node
        position, _, distToGoal = node

        if problem.isGoalState(position):
            break
        if position in visitedNodes:
            continue
        visitedNodes.add(position)
        
        nextNodes = problem.getSuccessors(position)
        for successor in nextNodes:
            newNode = (successor[0], successor[1], successor[2] + distToGoal)
            fringe.push(newNode)
            parentNodes.setdefault(newNode, node)

        cliff = fringe.isEmpty() # cliff check

    result = []

    while node != startPos:
        action = node[1]
        result.append(action)
        node = parentNodes.get(node)

    result.reverse()
    return result


# Abbreviations͏󠄂͏️͏󠄌͏󠄎͏︁͏󠄑͏︈
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch