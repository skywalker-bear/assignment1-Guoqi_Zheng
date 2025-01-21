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
from game import Directions
from typing import List

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




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    Returns a list of actions that reaches the goal.
    """
    # Stack for frontier
    frontier = util.Stack()
    
    # Each element on the stack: (current_state, path_taken_so_far)
    start_state = problem.getStartState()
    frontier.push((start_state, []))

    # Keep track of visited states
    visited = set()

    while not frontier.isEmpty():
        current_state, path = frontier.pop()

        # If we reach goal, return the path
        if problem.isGoalState(current_state):
            return path

        # If not visited, expand
        if current_state not in visited:
            visited.add(current_state)

            # Get successors
            for successor, action, step_cost in problem.getSuccessors(current_state):
                if successor not in visited:
                    # Append new action to existing path
                    new_path = path + [action]
                    frontier.push((successor, new_path))

    # If no solution found
    return []


def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue  # Use a Queue (FIFO) for BFS

    # Initialize the frontier (FIFO queue)
    frontier = Queue()

    # Push the start state and an empty path into the frontier
    start_state = problem.getStartState()
    frontier.push((start_state, []))  # (current_state, path_to_current_state)

    # Set to keep track of visited states to avoid revisiting them
    visited = set()

    while not frontier.isEmpty():
        # Pop the first element from the frontier
        current_state, path = frontier.pop()

        # Check if the current state is the goal state
        if problem.isGoalState(current_state):
            return path

        # If the current state has not been visited, expand it
        if current_state not in visited:
            visited.add(current_state)  # Mark the state as visited

            # Iterate through all successor states
            for successor, action, step_cost in problem.getSuccessors(current_state):
                if successor not in visited:
                    # Append the new action to the current path
                    new_path = path + [action]
                    # Push the successor state and its path into the frontier
                    frontier.push((successor, new_path))

    # If no solution is found, return an empty list
    return []
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue  # Use PriorityQueue for UCS

    # Priority queue to manage the frontier, prioritized by total cost
    frontier = PriorityQueue()

    # Push the start state into the frontier with a priority of 0
    start_state = problem.getStartState()
    frontier.push((start_state, [], 0), 0)  # (state, path, cost)

    # Keep track of visited states with their minimum cost
    visited = {}

    while not frontier.isEmpty():
        # Pop the state with the lowest cost
        current_state, path, cost = frontier.pop()

        # If the current state is the goal, return the path
        if problem.isGoalState(current_state):
            return path

        # If the current state has not been visited or found a cheaper path
        if current_state not in visited or cost < visited[current_state]:
            visited[current_state] = cost  # Mark state as visited with cost

            # Get all successors of the current state
            for successor, action, step_cost in problem.getSuccessors(current_state):
                new_cost = cost + step_cost  # Calculate the total cost to successor
                if successor not in visited or new_cost < visited.get(successor, float('inf')):
                    # Push the successor into the frontier with the updated cost
                    frontier.push((successor, path + [action], new_cost), new_cost)

    # Return an empty list if no solution is found
    return []
    util.raiseNotDefined()

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue  # Use a priority queue for A*

    # Priority queue to manage the frontier, prioritized by total cost (g + h)
    frontier = PriorityQueue()

    # Push the start state into the frontier with an initial cost of 0
    start_state = problem.getStartState()
    frontier.push((start_state, [], 0), 0)  # (state, path, cost)

    # Keep track of visited states with their minimum cost (g)
    visited = {}

    while not frontier.isEmpty():
        # Pop the state with the lowest total estimated cost (f = g + h)
        current_state, path, cost = frontier.pop()

        # If the current state is the goal, return the path
        if problem.isGoalState(current_state):
            return path

        # If the current state has not been visited or found a cheaper path
        if current_state not in visited or cost < visited[current_state]:
            visited[current_state] = cost  # Mark state as visited with cost

            # Get all successors of the current state
            for successor, action, step_cost in problem.getSuccessors(current_state):
                new_cost = cost + step_cost  # Calculate g (cost so far)
                estimated_cost = new_cost + heuristic(successor, problem)  # f = g + h
                if successor not in visited or new_cost < visited.get(successor, float('inf')):
                    # Push the successor into the frontier with its f cost as priority
                    frontier.push((successor, path + [action], new_cost), estimated_cost)

    # Return an empty list if no solution is found
    return []
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
