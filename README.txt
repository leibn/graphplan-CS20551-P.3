208271775
*****


def independentPair(a1, a2):
        We will define limitations of action to be the union of:
            1: list of the precondition propositions
            2: list of the propositions that will be added after applying the action
        And then we will check for each of the limits whether the proposition prop
            is a negative effect of the other action


def haveCompetingNeeds(a1, a2, mutexProps):
    Checks if there are 2 preconditions(one from a1 and second from a2) that have competing needs.

def mutexPropositions(prop1, prop2, mutexActions):
    same idea as def haveCompetingNeeds exclude that:
        this func is for all the possible actions in the layer that have the self object is in their add list


def updateActionLayer(self, previousPropositionLayer):
    For any non-contradictory action:
        If:
            1. not all the prerequisites for the action are in the previous bidding layer(not fire continue)
            2. The action is not yet on the batch (not fire continue)
        will add the action


def updateMutexActions(self, previousLayerMutexProposition):
    for all two different actions from self.actionLayer.getActions()
        if the pair already in this layer mutex, so we don't need to check this pair, so we will continue
        elif the pair is mutex in previous layer, so we will add the pair to this layer mutex actions

def updatePropositionLayer(self):
    using dict for keep track on the propositions that had checked already.
    and then checks for every proposition:
     (that will be added after applying action (iterates every action in the layer actions))
        if the proposition not initialise yet in the dict
            then adding proposition name to dict (initializing the key in dict)
        anyway will add every producer's as propositions in the current layer
            (For now will add only to the newPropositionsDict )
    and then we will convert the newPropositionsDict to the self object type in the layer




def updateMutexProposition(self):
    for all two different Proposition from currentLayerPropositions:
        if the pair already in this layer Proposition mutex, so we don't need to check this pair, and we will continue
        elif prop1 and prop2 are mutex in the current layer, so we will add the pair to this layer mutex list


def expand(self, previousLayer):
	An obvious implementation of the previous questions



I edit dwrProblem.txt (saved in dwr1) such that it can be achieved within at least 8 actions (without noOps)
the change of the Goal state made such that each robot need to be at the location he was in the initial state.
dwr1 will be :
    Initial state: r1 q2 a1 b2 ur uq
    Goal state: r1 q2 a2 b1


I edit dwrProblem.txt (saved in dwr2) such that the goal state will be a not achievable state.
The goal state declared to be "literals mutex" so the robot's(r&q) will need to be in both locating(1&2).
My code not seceded in solving the problem I set in dwr2, so... apparently the problem in dwr2 and my code was successful, which means My code seceded in solving the problem ?!?! (Logical cynicism)
dwr2 will be :
    Initial state: r1 q2 a1 b2 ur uq
    Goal state: r1 r2 q1 q2

class PlanningProblem():
    def __init__(self, domain, problem):
        no change made.

    def getStartState(self):
        # An obvious implementation

    def isGoalState(self, state):
        Just the negation of self.goalStateNotInPropLayer(state)

    def getSuccessors(self, state, stepCost=1):
        will iterate every action(that not persist) checking if
        all the precondition of the action are in the propositions list:
            copy state to new list for successors mange
            so for every prop where propAdd is not already in state or will be deleted after applying the action will
            be added to successors
            such that finely wil be added to the returned triplesList

def maxLevel(state, problem, includeMutexInExpand=False):
    the variable "includeMutexInExpand" default is False for the sake of minimizing the complexity of the code so that
    the code will be more efficient.
    returns heuristic value is the number of layers required to expand all goal propositions.
    If the goal is not reachable from the state the return heuristic will be float('inf')
    The function will expand the levels in the order of creation as long as we have not reached a fixed state
    expanding was implement using expand OR expandWithoutMutex functions(And this is thanks to the change added in the
    expand function) that was implemented in planGraphLevel.py


def levelSum(state, problem, includeMutexInExpand=False):
    the variable "includeMutexInExpand" default is False for the sake of minimizing the complexity of the code so that
        the code will be more efficient.
    the variable "sumSubGoalsLevelFA" stands for the heuristic value that in other name
        is the sum of sub-goals level they first appeared.
    returned heuristic value is sumSubGoalsLevelFA.
        If the goal is not reachable from the state the return heuristic will be float('inf')
        The function will expand the levels in the order of creation as long as we have not reached a fixed state
        expanding was implement using expand OR expandWithoutMutex functions(And this is thanks to the change added in the
        expand function) that was implemented in planGraphLevel.py

hanoi.py(q13-14)
    the syntax is described bellow and ass well in the code.
    The sign -|  means:
        left side is the "thing that actually changes" and the
        right side is "the previous or remaining" (depending on the context of the action marker)
        the letter at the end of the string indicates the peg


    conector = '-'  : For make sure not pddl typo errors
    singleSpace = ' ' : Indicates end or beginning of the statement / literal etc.
    allNumbersSetString = "allNumbersSet " : Indicates that currently all numbers are in one of the pegs (i.e. you can perform a get operation at the moment)
    nothingString = "nothing" : Just as it sounds in his context. For example if there is nothing above a then nothing above 'a', but it should be noted that as in set theory nothing belongs to any peg.
    belongString = "belongTo" : Indicates location
    aboveString = "above" Specifies the base of the number / nothing
    actionString = "-|" : means:
                            left side is the "thing that actually changes" and the
                            right side is "the previous or remaining" (depending on the context of the action marker)
                            the letter at the end of the string indicates the peg

    notBelongsAnyString = "-notBelongsAnyPeg" : means that number is after get action and so that it not Belongs Any peg

    getString = "get" : declare get action
    setString = "set" : declare set action

    This is the format given in the task description
    InitialStateDeclareString = 'Initial state: ' :This is the format given in the task description
    GoalStateDeclareString = 'Goal state: ' : This is the format given in the task description
    propositionsString = "Propositions:" + lineSpace : This is the format given in the task description
    nameString = "Name: " : This is the format given in the task description
    preString = "pre: " : This is the format given in the task description
    addString = "add: " : This is the format given in the task description
    deleteSting = "delete: " : This is the format given in the task description


    alphaBetStartPlaceInAsci = 96 : for the char method

