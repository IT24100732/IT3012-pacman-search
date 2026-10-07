# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions

    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """

    # Create a stack for DFS
    fringe = util.Stack()

    # Get the starting state
    start_state = problem.getStartState()

    # Store: (state, path)
    fringe.push((start_state, []))

    # Keep track of states that have already been expanded
    visited = set()

    while not fringe.isEmpty():

        # Get the next node from the stack
        state, path = fringe.pop()

        # If this is the goal, return the path
        if problem.isGoalState(state):
            return path

        # Only expand a state once
        if state not in visited:
            visited.add(state)

            # Add all successors to the stack
            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in visited:
                    fringe.push((successor, path + [action]))

    # No solution
    return []


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""

    # Create a queue for BFS
    fringe = util.Queue()

    # Get the starting state
    start_state = problem.getStartState()

    # Store: (state, path)
    fringe.push((start_state, []))

    # Keep track of states that have already been expanded
    visited = set()

    while not fringe.isEmpty():

        # Get the next node from the queue
        state, path = fringe.pop()

        # If this is the goal, return the path
        if problem.isGoalState(state):
            return path

        # Only expand a state once
        if state not in visited:
            visited.add(state)

            # Add all successors to the queue
            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in visited:
                    fringe.push((successor, path + [action]))

    # No solution
    return []


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    # Priority queue for A*
    fringe = util.PriorityQueue()

    # Starting state
    start_state = problem.getStartState()

    # g(n) = cost travelled so far
    start_cost = 0

    # f(n) = g(n) + h(n)
    start_priority = start_cost + heuristic(start_state, problem)

    # Store: (state, path, cost)
    fringe.push((start_state, [], start_cost), start_priority)

    # Keep track of the cheapest known cost to each state
    visited = {}

    while not fringe.isEmpty():

        # Get the node with the lowest f(n)
        state, path, cost = fringe.pop()

        # If this is the goal, return the path
        if problem.isGoalState(state):
            return path

        # Expand only when this is the cheapest path to the state
        if state not in visited or cost < visited[state]:
            visited[state] = cost

            # Expand successors
            for successor, action, stepCost in problem.getSuccessors(state):

                new_cost = cost + stepCost

                # h(n) = estimated remaining cost
                h = heuristic(successor, problem)

                # f(n) = g(n) + h(n)
                priority = new_cost + h

                if successor not in visited or new_cost < visited[successor]:
                    fringe.push(
                        (successor, path + [action], new_cost),
                        priority
                    )

    # No solution
    return []

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""

    # Priority queue for UCS
    fringe = util.PriorityQueue()

    # Starting state
    start_state = problem.getStartState()

    # Store: (state, path, cost)
    # Priority = total path cost
    fringe.push((start_state, [], 0), 0)

    # Keep track of the cheapest cost at which we have expanded a state
    visited = {}

    while not fringe.isEmpty():

        # Get the node with the lowest cost
        state, path, cost = fringe.pop()

        # If this is the goal, return the path
        if problem.isGoalState(state):
            return path

        # Expand only if this is the cheapest path to this state
        if state not in visited or cost < visited[state]:
            visited[state] = cost

            # Add successors
            for successor, action, stepCost in problem.getSuccessors(state):

                new_cost = cost + stepCost

                if successor not in visited or new_cost < visited[successor]:
                    fringe.push(
                        (successor, path + [action], new_cost),
                        new_cost
                    )

    # No solution
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
