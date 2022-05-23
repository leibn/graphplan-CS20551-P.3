# syntax appearance for representing

conector = '-'
singleSpace = ' '
lineSpace = '\n'
allNumbersSetString = "allNumbersSet "
nothingString = "nothing"
belongString = "belongTo"
aboveString = "above"
actionString = "-|"
notBelongsAnyString = "-notBelongsAnyPeg"
getString = "get"
setString = "set"
InitialStateDeclareString = 'Initial state: '
GoalStateDeclareString = 'Goal state: '
propositionsString = "Propositions:"+lineSpace
nameString = "Name: "
preString = "pre: "
addString = "add: "
deleteSting = "delete: "
alphaBetStartPlaceInAsci = 96


syntaxDict = dict(
    conector='-',
    singleSpace = ' ',
    lineSpace = '\n',
    allNumbersSetString = "allNumbersSet ",
    nothingString = "nothing",
    belongString = "belongTo",
    aboveString = "above",
    actionString = "-|",
    notBelongsAnyString = "-notBelongsAnyPeg",
    getString = "get",
    setString = "set",
    InitialStateDeclareString = 'Initial state: ',
    GoalStateDeclareString = 'Goal state: ',
    propositionsString = "Propositions:" + lineSpace,
    nameString = "Name: ",
    preString = "pre: ",
    addString = "add: ",
    deleteSting = "delete: ",
    alphaBetStartPlaceInAsci = 96
)


def warpConectors(name):
    """
    warp name with conector for valid pdll roles
    Parameters
    """
    return conector + name + conector


def belong(number, peg, pegsTransfer=None, listCheck=True):
    """
    Parameters
    ----------
    number
    peg
    pegsTransfer for valid check of the belong function.
    listCheck : bool if set to false will ignore errors check in func.

    Returns
    -------
    walid str represent belong in pdll
    """
    belongs = warpConectors(belongString)
    if listCheck:
        return IsLists(small=number, big=peg, pegsTransfer=pegsTransfer, funcItem=belong)
    else:
        return str(number) + belongs + str(peg) + singleSpace


def isRepresentNumber(number):
    """
    check if this is number in string or int etc.

    Parameters
    ----------
    number to be check

    Returns
    -------
    true if is number
    """
    try:
        res = str(number).isdigit()
        return res
    except ValueError:
        return False


def IsLists(small, big, pegsTransfer, funcItem):
    """
     func for specify input from user fails (lists,num,alphanumeric) and for nothing-above-number etc.

    Parameters
    ----------
    small : int, str, list
    big  : int, str, list
    pegsTransfer : pegs
    funcItem : validation func or list of them for each check.

    Returns
    -------
    string of func in good way.
    """
    if pegsTransfer is None: # prevents errors in the func.
        pegsTransfer = list()
    output = ""
    # input boolean checkers:
    smallList = type(small) is list
    bigList = type(big) is list
    smallDigit = isRepresentNumber(small)
    bigDigit = isRepresentNumber(big)

    # binding to category's
    if bigList and smallList:
        # booth lists will run for each of each.
        for eachB in big:
            for eachS in small:
                output += funcItem(eachS, eachB, pegsTransfer=pegsTransfer, listCheck=True)
                # list check for valid the func specific terms

    elif smallList and not bigList:
        # first is list second is not list
        for eachS in small:
            output += funcItem(eachS, big, pegsTransfer=pegsTransfer, listCheck=True)

    elif bigList and not smallList:
        # first is not list second is  list
        for eachB in big:  # expanding for each of the list (for nothing-above-number etc.)
            output += funcItem(small, eachB, pegsTransfer=pegsTransfer, listCheck=True)

    # so there is no lists check for literals.
    elif smallDigit and not bigDigit and big in ((syntaxDict.values()) + list(pegsTransfer)):
        # first is digit second is not digit
        output += funcItem(small, big, pegsTransfer=pegsTransfer, listCheck=False)

    # for eazy set the initial number on peg :
    elif not smallDigit and bigDigit and small in syntaxDict.values():  # for cases as nothing above number etc.
        # first is not digit second is digit
        output += funcItem(small, big, pegsTransfer=pegsTransfer, listCheck=False)

    elif not smallDigit and not bigDigit and \
            small in (
                syntaxDict.values() + pegsTransfer)\
            and big in (
                syntaxDict.values() + pegsTransfer):
        # for cases as nothing above number etc.
        output += funcItem(small, big, pegsTransfer=pegsTransfer, listCheck=False)
    elif smallDigit and bigDigit and -1 < int(small) < int(big):
        # first and second are digit and valid for make above func.
        output += funcItem(small, big, pegsTransfer=pegsTransfer, listCheck=False)

    # else: the case not valid in the problem rules
    return output


def above(small, big, pegsTransfer, listCheck=True):
    """
    generates pddl above string

    Parameters
    ----------
    small : any like as former functions
    big : any like as former functions
    pegsTransfer : pegs as former functions
    listCheck : validation func or list of them for each check.

    Returns
    -------
    pddl above string
    """
    aboves = warpConectors(aboveString)
    if listCheck is False:
        return small + aboves + big + singleSpace
    else:
        return IsLists(small, big, funcItem=above, pegsTransfer=pegsTransfer)


def notBelongsAnyPeg(number, setMany=False):
    """
    generates pddl notBelongsAnyPeg string

    Parameters
    ----------
    number : for the set
    setMany : true if multy assign

    Returns
    -------
    pddl notBelongsAnyPeg string
    """
    output = ""
    if not setMany:  # simple with no excepts
        return number + notBelongsAnyString + singleSpace
    for num in number:
        output += notBelongsAnyPeg(num, False)
    return output


def isValidCreate(numbers, numOfPegs):
    """
    checks that the user input is O.K.

    I give flexibility to the program souch that it can be implemented with more than 3 pegs
    I set the maximum pegs to 26 such the literals name will stay simpel (one non-capital letter for each peg)

    Parameters
    ----------
    numbers = number of numbers,most be greater than 1.
    numOfPegs = number of pegs, 2<numOfPegs<27
    """

    if numbers < 1:
        print("ohhh,"
              "sorry...\n it wil be 'a problem' gust with more then 0 numbers \n "
              "so  I will run the problem you enter but with 4 numbers ")
        numbers = 4
        numbers = list(range(numbers))  # [0,...,numbers-1]
    else:
        numbers = list(range(numbers))  # [0,...,numbers-1]
    if numOfPegs > 26:
        print("ohhh,"
              "for now I set the maximum number of pegs to be 26 such the literals name \n"
              "will stay simpel (one non-capital letter for each peg)\n"
              "sorry...\n I will run the problem you enter but with 26 pegs")
        numOfPegs = 26
    if numOfPegs < 3:
        print(
            "ohhh,"
            "Its look u have mistake( the number of pegs...)"
            "Hanoi puzzle can only be solved if there are at least 3 pegs \n"
            "So... I will run the problem you entered but with 3 pegs")
        numOfPegs = 3
    # pegs = ['a','b', 'c']
    pegs = list()
    for number in range(numOfPegs):
        pegs.append(chr(number + 1 + 96))
    numbers = [str(i) for i in numbers]
    return pegs, numbers


def propositionOutput(numbers, pegs):
    """
    arranging all the proposition pdll string, make easy understand and implement

    Parameters
    ----------
    numbers
    pegs

    Returns
    -------
    proposition pdll string
    """

    propositions = propositionsString
    propositions += allNumbersSetString
    for peg in pegs:
        propositions += above(nothingString, peg, pegsTransfer=pegs)
    for ind, number in enumerate(numbers):
        propositions += above(nothingString, number, pegsTransfer=pegs)
        propositions += notBelongsAnyPeg(number)
        for peg in pegs:
            propositions += belong(number, peg, pegsTransfer=pegs)
            propositions += above(number, peg, pegsTransfer=pegs)
        propositions += above(numbers, number, pegsTransfer=pegs)
    propositions += lineSpace
    return propositions


class Action:
    actions = list()

    def __init__(self, name, precondition, add, delete):
        """
        name: The name identifying the action
        signature: A list of tuples (name, [types]) to represent a list of
                   parameters and their type(s).
        precondition: A list of predicates that have to be true before the
                      action can be applied
        effect: An effect instance specifying the post condition of the action
        """
        self.name = name  # type str
        self.precondition = precondition  # type list
        self.add = add  # type list
        self.delete = delete  # type list
        self.actions.append(self)

    def __str__(self):
        """

        Returns
        -------
        str
        """


        output = ""
        output += (nameString + self.name + lineSpace)
        pre = ""
        for p in self.precondition:
            pre += p
        output += (preString + pre + lineSpace)
        adde = ""
        for a in self.add:
            adde += a
        output += (addString + adde + lineSpace)
        dele = ""
        for d in self.delete:
            dele += d
        output += (deleteSting + dele + lineSpace)
        return output


def getAction(small, big, base):
    if big is not None:  # check this is not case as:  get the last number in pege
        return getString + small + actionString + big + base + singleSpace
    else:
        return getString + small + actionString + base + singleSpace


def setAction(small, big, base):
    if big is not None:  # check this is not case as:  set the 1 number in pege
        return setString + small + actionString + big + base + singleSpace
    else:
        return setString + small + actionString + base + singleSpace


def actionOutput(numbers, pegs):
    """
    arranging all the Actions pdll string, make easy understand and implement

    Parameters
    ----------
    numbers
    pegs

    Returns
    -------
    Actions pdll string

    """
    output = "Actions:\n"
    for ind, small in enumerate(numbers):
        for base in pegs:
            for big in numbers[ind + 1:]:
                # cases where small-above-big is valid situation for one of pegs

                # get:
                name = getAction(small, big, base)
                precondition = [allNumbersSetString,
                                belong(small, base, pegsTransfer=pegs),
                                above(nothingString, small, pegsTransfer=pegs),
                                above(small, big, pegsTransfer=pegs)]
                add = [notBelongsAnyPeg(small), above(nothingString, big, pegsTransfer=pegs)]
                delete = precondition
                acti = Action(name, precondition, add, delete)
                output += str(acti)

                # set:
                name = setAction(small, big, base)
                precondition = [notBelongsAnyPeg(small), above(nothingString, big, pegsTransfer=pegs),
                                belong(big, base, pegsTransfer=pegs)]
                add = [allNumbersSetString, above(small, big, pegsTransfer=pegs),
                       above(nothingString, small, pegsTransfer=pegs), belong(small, base, pegsTransfer=pegs)]
                delete = [notBelongsAnyPeg(small), above(nothingString, big, pegsTransfer=pegs)]
                acti = Action(name, precondition, add, delete)
                output += str(acti)

            # cases where small is the "downiest" on peg:

            # get:
            name = getAction(small, None, base)  # is the "downiest" on peg
            precondition = [allNumbersSetString, above(small, base, pegsTransfer=pegs),
                            above(nothingString, small, pegsTransfer=pegs), belong(small, base, pegsTransfer=pegs)]
            add = [notBelongsAnyPeg(small), above(nothingString, base, pegsTransfer=pegs)]
            delete = [allNumbersSetString, above(small, base, pegsTransfer=pegs),
                      above(nothingString, small, pegsTransfer=pegs), belong(small, base, pegsTransfer=pegs)]
            acti = Action(name, precondition, add, delete)
            output += str(acti)

            # set:
            name = setAction(small, None, base)
            precondition = [notBelongsAnyPeg(small), above(nothingString, base, pegsTransfer=pegs)]
            add = [allNumbersSetString, above(small, base, pegsTransfer=pegs),
                   above(nothingString, small, pegsTransfer=pegs), belong(small, base, pegsTransfer=pegs)]
            delete = [notBelongsAnyPeg(small), above(nothingString, base, pegsTransfer=pegs)]
            acti = Action(name, precondition, add, delete)
            output += str(acti)
    return output


def createDomainFile(domainFileName, n, numOfPegs=3):
    """
    make my easier debugging

    Parameters
    ----------
    domainFileName
    n
    numOfPegs : int , extend to more then 3 pegs, this is nice to have fetcher for the creation func
    """
    pegs, numbers = isValidCreate(n, numOfPegs)
    domainFile = open(domainFileName, 'w')  #use domainFile.write(str) to write to domainFile
    domainFile.write(propositionOutput(numbers, pegs))  # function for the Propositions
    domainFile.write(actionOutput(numbers, pegs))  # function for the Actions
    domainFile.close()


def iniGoalState(numbers, pegs, start=True, pegDest=0):
    """
    this is a function for simple set state souch that all numbers are in one peg in valid order
    the default place for set the numbers is in peg 'a'

    Parameters
    ----------
    numbers
    pegs
    start : boolean where True mean this is initial start - peg 'a'
    pegDest :  stand for peg destination , in default this is set for 'a'(converted inside the func using asci,
                      the user can assign as destination or in number(int) represent index of letter from 'a')

    Returns
    -------
     str in format os given in the task that represent the Initial/Goal state
    """
    if pegDest not in pegs:
        if (not isRepresentNumber(pegDest)) or (isRepresentNumber(pegDest) and int(pegDest) != -1):
            if start:
                index = 0
            else:
                index = len(pegs)
        else:
            index = len(pegs)
        pegDest = chr(index + alphaBetStartPlaceInAsci)

    output = belong(numbers, pegDest, pegsTransfer=pegs)
    numbers2 = numbers[:]  # fast copy of numbers
    smallNum = numbers2.pop()
    bigNum = pegDest
    while numbers2:  # have more to pop
        # in similarity to algorithms of linked list:
        output += above(smallNum, bigNum, pegsTransfer=pegs)
        bigNum = smallNum
        smallNum = numbers2.pop()
    output += above(smallNum, bigNum, pegsTransfer=pegs)
    output += above(nothingString, smallNum, pegsTransfer=pegs)
    emptyPegs = pegs[:]  # fast copy of pegs
    emptyPegs.remove(pegDest)

    # the following two rows not most be on goal state,
    # but it makes the algorithms find faster mutex's, so I made this by default
    output += above(nothingString, emptyPegs, pegsTransfer=pegs)
    output += belong(nothingString, emptyPegs, pegsTransfer=pegs)
    return output


def createProblemFile(problemFileName, n, numOfPegs=3, initialIndex='a', destinationIndex=-1):
    """
    function for make problem file using the iniGoalState.
    the format was as described in the graphPlan.html
    Just like the numOfPegs/initialIndex/destinationIndex variables,
        in many things in this task I  added features (even if not required in the task) for the
        convenience and flexibility of the code.

    Parameters
    ----------
    problemFileName : name for the file
    n : number of numbers (known also in the reference 'disc')
    numOfPegs : number Of Pegs for the creating problem file(this is not course requirement)

    initialIndex : initial peg for numbers
    destinationIndex :  Goal peg for numbers
    """
    pegs, numbers = isValidCreate(n, numOfPegs)
    problemFile = open(problemFileName, 'w')  # use problem_file.write(str) to write to problem_file
    InitialState = iniGoalState(numbers=numbers, pegs=pegs, pegDest=initialIndex)
    GoalState = iniGoalState(numbers=numbers, pegs=pegs, start=False, pegDest=destinationIndex)
    problemFile.write(InitialStateDeclareString + InitialState + allNumbersSetString + lineSpace)
    problemFile.write(GoalStateDeclareString + GoalState + lineSpace)
    problemFile.close()


import sys
if __name__ == '__main__':
  if len(sys.argv) != 2:
    print('Usage: hanoi.py n')
    sys.exit(2)

  n = int(float(sys.argv[1]))  #number of disks
  domainFileName = 'hanoi' + str(n) + 'Domain.txt'
  problemFileName = 'hanoi' + str(n) + 'Problem.txt'

  createDomainFile(domainFileName, n)
  createProblemFile(problemFileName, n)
