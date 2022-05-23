from util import Pair
import copy
from propositionLayer import PropositionLayer
from planGraphLevel import PlanGraphLevel
from Parser import Parser
from action import Action

try:
    from search import SearchProblem
    from search import aStarSearch

except:
    from CPF.search import SearchProblem
    from CPF.search import aStarSearch


class PlanningProblem():
    def __init__(self, domain, problem):
        """
    Constructor
    """
        p = Parser(domain, problem)
        self.actions, self.propositions = p.parseActionsAndPropositions()
        # list of all the actions and list of all the propositions
        self.initialState, self.goal = p.pasreProblem()
        # the initial state and the goal state are lists of propositions
        self.createNoOps() 											# creates noOps that are used to propagate existing propositions from one layer to the next
        PlanGraphLevel.setActions(self.actions)
        PlanGraphLevel.setProps(self.propositions)
        self._expanded = 0


    def getStartState(self):
        # An obvious implementation
        return self.initialState

    def isGoalState(self, state):
        """
        Hint: you might want to take a look at goalStateNotInPropLayer function
        """
        for goal in self.goal:
            if goal not in state:
                return False
        return True

    def getSuccessors(self, state, stepCost=1):
        """
        For a given state, this should return a list of triples, 
        (successor, action, stepCost), where 'successor' is a 
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental 
        cost of expanding to that successor, 1 in our case.
        You might want to this function:
        For a list of propositions l and action a,
        a.allPrecondsInList(l) returns true if the preconditions of a are in l

        step cost is good featcher that can be usefull
        """
        self._expanded += 1
        successors = []
        for action in self.actions:
            # if an action is not an noOp, and all preconditions are met in the current state
            if not action.isNoOp() and action.allPrecondsInList(state):
                # Add ourself and all the additions from the actions
                successor = state + [x for x in action.getAdd() if x not in state]
                # Remove all the deletions
                successor = [x for x in successor if x not in action.getDelete()]

                # stepCost is 1
                successors.append((successor, action, stepCost))

        return successors

        # todo change
        # self._expanded += 1
        # triplesList = list()
        # for action in self.actions:
        #     if action.isNoOp():
        #         # action is persistence
        #         continue
        #     elif action.allPrecondsInList(state):
        #         # all the precondition of the action are in the propositions list
        #         successor = list(state)
        #         for propAdd in action.getAdd():
        #             if propAdd in state or propAdd in action.getDelete():
        #                 # propAdd is already in state or will be deleted after applying the action
        #                 continue
        #             else:
        #                 successor.append(propAdd)
        #         triplesList.append((successor, action, stepCost))
        # return triplesList

    def getCostOfActions(self, actions):
        cost = 0
        for each in actions:
            if len(each) > 1 and type(each[2]) is int:
                cost += each[2]
            else:
                cost += 1  # default not assign is to cost of 1
        return cost

    def goalStateNotInPropLayer(self, propositions):
        """
        Helper function that returns true if all the goal propositions
        are in propositions
        """
        for goal in self.goal:
            if goal not in propositions:
                return True
        return False

    def createNoOps(self):
        """
        Creates the noOps that are used to propagate propositions from one layer to the next
        """
        for prop in self.propositions:
            name = prop.name
            precon = []
            add = []
            precon.append(prop)
            add.append(prop)
            delete = []
            act = Action(name,precon,add,delete, True)
            self.actions.append(act)

def maxLevel(state, problem, includeMutexInExpand=False):
    """
  The heuristic value is the number of layers required to expand all goal propositions.
  If the goal is not reachable from the state your heuristic should return float('inf')  
  A good place to start would be:
  propLayerInit = PropositionLayer()          #create a new proposition layer
  for prop in state:
    propLayerInit.addProposition(prop)        #update the proposition layer with the propositions of the state
  pgInit = PlanGraphLevel()                   #create a new plan graph level (level is the action layer and the propositions layer)
  pgInit.setPropositionLayer(propLayerInit)   #update the new plan graph level with the the proposition layer

  includeMutexInExpand is good feetcher set in default to False forthermore explain in the readme
  """
    propLayerInit = PropositionLayer()  # create a new proposition layer
    for prop in state:
        propLayerInit.addProposition(prop)  # update the proposition layer with the propositions of the state
    pgInit = PlanGraphLevel()  # create a new plan graph level (level is the action layer and the propositions layer)
    pgInit.setPropositionLayer(propLayerInit)  # update the new plan graph level with the the proposition layer
    currentGraph = [pgInit]  # list with the "new plan graph level" as first item in the list
    numOfLevels = 0  # counter of levels for the heuristic and for iterating the levels in the while loop
    currentLevel = currentGraph[numOfLevels]
    while problem.goalStateNotInPropLayer(currentLevel.getPropositionLayer().getPropositions()):
        if isFixed(currentGraph, numOfLevels):
            return float('inf')
        pgNew = PlanGraphLevel()  # create a new plan graph level (level is the action layer and the propositions layer)
        # expanding using expand OR expandWithoutMutex functions(And this is thanks to the change added in the
        # expand function) that was implemented in planGraphLevel.py
        # includeMutexInExpand default is False for the sake of minimizing the complexity of the code so that
        # the code will be more efficient
        pgNew.expand(previousLayer=currentGraph[numOfLevels], includeMutex=includeMutexInExpand)
        currentGraph.append(pgNew)
        numOfLevels += 1
        currentLevel = currentGraph[numOfLevels]
    return numOfLevels


def levelSum(state, problem, includeMutexInExpand=False):
    """
  The heuristic value is the sum of sub-goals level they first appeared.
  If the goal is not reachable from the state your heuristic should return float('inf')
  """
    propLayerInit = PropositionLayer()  # create a new proposition layer
    for prop in state:
        propLayerInit.addProposition(prop)  # update the proposition layer with the propositions of the state
    pgInit = PlanGraphLevel()  # create a new plan graph level (level is the action layer and the propositions layer)
    pgInit.setPropositionLayer(propLayerInit)  # update the new plan graph level with the the proposition layer
    currentGraph = [pgInit]  # list with the "new plan graph level" as first item in the list
    numOfLevels = 0  # counter of levels for iterating the levels in the while loop
    currentLevel = currentGraph[numOfLevels]
    sumSubGoalsLevelFA = 0  # for the heuristic
    goalList = problem.goal + []
    while len(goalList) > 0:
        if isFixed(currentGraph, numOfLevels):
            # goal is not reachable
            return float('inf')
        propositions = currentLevel.getPropositionLayer().getPropositions()
        for goal in [p for p in goalList if p in propositions]:
            # for every goal that includes in goal propositions and in propositions
            sumSubGoalsLevelFA += numOfLevels
            goalList = [item for item in goalList if item != goal]
        pgNew = PlanGraphLevel()  # create a new plan graph level (level is the action layer and the propositions layer)
        # expanding using expand OR expandWithoutMutex functions(And this is thanks to the change added in the
        # expand function) that was implemented in planGraphLevel.py
        # includeMutexInExpand default is False for the sake of minimizing the complexity of the code so that
        # the code will be more efficient
        pgNew.expand(previousLayer=currentGraph[numOfLevels], includeMutex=includeMutexInExpand)
        # expand the planning graph, omitting the computation of mutex relations.
        currentGraph.append(pgNew)
        numOfLevels += 1
        currentLevel = currentGraph[numOfLevels]
    sumSubGoalsLevelFA += numOfLevels
    return sumSubGoalsLevelFA


def isFixed(Graph, level):
    """
  Checks if we have reached a fixed point,
  i.e. each level we'll expand would be the same, thus no point in continuing
  """
    if level == 0:
        return False
    return len(Graph[level].getPropositionLayer().getPropositions()) == len(
        Graph[level - 1].getPropositionLayer().getPropositions())


if __name__ == '__main__':
    import sys
    import time
    if len(sys.argv) != 1 and len(sys.argv) != 4:
        print("Usage: PlanningProblem.py domainName problemName heuristicName(max, sum or zero)")
        exit()
    domain = 'dwrDomain.txt'
    problem = 'dwrProblem.txt'
    heuristic = lambda x,y: 0
    if len(sys.argv) == 4:
        domain = str(sys.argv[1])
        problem = str(sys.argv[2])
        if str(sys.argv[3]) == 'max':
            heuristic = maxLevel
        elif str(sys.argv[3]) == 'sum':
            heuristic = levelSum
        elif str(sys.argv[3]) == 'zero':
            heuristic = lambda x,y: 0
        else:
            print("Usage: PlanningProblem.py domainName problemName heuristicName(max, sum or zero)")
            exit()

    prob = PlanningProblem(domain, problem)
    start = time.clock()
    plan = aStarSearch(prob, heuristic)
    elapsed = time.clock() - start
    if plan is not None:
        print("Plan found with %d actions in %.2f seconds" % (len(plan), elapsed))
    else:
        print("Could not find a plan in %.2f seconds" % elapsed)
    print("Search nodes expanded: %d" % prob._expanded)
