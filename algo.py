
#Global variables
g = {} #this dictionary represents go to function and holds as keys tuples (state, weight) and the value is the next state
output = {} #this dictionary maps states to a list of unique keywords found
failure = {} # this dictionary maps each state with the next state
caseSensitive = False # when this parameter is set to false, we match strings with letter case difference


fail = None # global constant with a meaningful name which is the output of the graph f when the weight(letter) is not part of the graph
newstate = 0 #global variable used to propagate the state index cross kewords iterations

def initializeGlobalParameters():
    ''''
    This method makes sure that all global parameters are properly reset
    '''
    global g
    global output
    global failure
    global newstate
    g = {}
    output = {}
    failure = {}
    newstate = 0

def createStateMachine(keywords):
    ''''
    This method initializes global parameters, creates the go to, failure and output functions
    '''
    initializeGlobalParameters()
    createGoToFunction(keywords)
    createFailueFunction()


def createGoToFunction(keywords):
    '''

    :param keywords: list of strings based on which we create the automata
    :return: go to function
    '''

    newstate = 0 # start with state 0
    for keyword in keywords:
        processKeyword(keyword)

    # For all letters which are not mapped to the 0 root state, create references to state 0
    # For efficiency concatenate all keywords and remove duplicated letters
    allkeys = ''.join(set(''.join(keywords)))
    for i in range(len(allkeys)):
        if g.get((0, allkeys[i]), fail) == fail:
            g[(0, allkeys[i])] = 0
    return g


def processKeyword(keyword):
    '''
    For each letter in keyword, if it is already present in our graph g at current state,
    update current state to the value of the next state
    otherwise add a new node to the graph mapping the current state + 1 with the current letter
    :param keyword:
    :return:
    '''
    global newstate
    state = 0
    j = 0
    while g.get((state, keyword[j]), fail) != fail: #state already defined
        state = g[(state, keyword[j])] #we are sure the key exists
        j = j + 1

    for p in range(j, len(keyword)) :
        newstate = newstate + 1
        g[(state, keyword[p])] = newstate
        state = newstate

    updateOutput(state, keyword)


def updateOutput(state, keyword) :
    '''
    This method updates output dictionary with value keyword at key state.
    Because we can find multiple keywords at the same index, output maintains a list of
    keywords.
    For this reason, if input keyword is a string and the key doest't exist, I create an array
    with given value, otherwise I add keyword to existing array.
    This method is called by processKeyword and createFailure function and in the latter case
    it may pass a list of values (the payload of another output node, for this reason
    I check the instance type and do an array extends.
    '''
    if state in output.keys():
        #this scenario will be triggered by updates from create failure
        if isinstance(keyword, list):
            output[state].extend(keyword)
        else:
            output[state].append(keyword)
    else:
        output[state] = [keyword]


def createFailueFunction():
    '''
    This method iterates through all letters of keywords payload (set method guarantees
    distinct output) and uses a queue to manange states.
    '''
    queue = []
    allkeys = ''.join(set(''.join(keywords)))
    for i in range(len(allkeys)):
        s = g.get((0, allkeys[i]), fail)
        if  s != 0:
            queue.append(s)
            failure[s] = 0

    while len(queue) != 0 :
        r = queue[0]
        queue.remove(queue[0])

        for i in range(len(allkeys)):
            s = g.get((r, allkeys[i]), fail)
            if s!= fail :
                queue.append(s)
                state = failure[r]
                while g.get((state, allkeys[i]), fail) == fail :
                    state = failure[state]
                failure[s] = g[(state, allkeys[i])]
                if failure[s] in output.keys():
                    newOutputValue = output[failure[s]]
                    updateOutput(s, newOutputValue)


def findInString(inputString, outputFileName):
    '''
    Find all occurences of keywords in given inputString
    This method has to be called after createStateMachine
    '''
    state = 0
    outputFile = open( outputFileName, 'w')
    for i in range(len(inputString)) :
        #failure function doesn't have a value for state 0 therefor make sure the
        #this loop doesn't execute the very first time
        while g.get((state, inputString[i]), fail) == fail and state != 0:
            state = failure[state]
        #update state only when the tuple state, inputString[i] exists in go to graph, otherwise keep existing state
        state = g.get((state, inputString[i]), state)
        if output.get(state, None ) != None :
            print('\nIndex : %s , Output keywords %s \nActual text : %s' % (i, output[state], inputString[:i + 1]))
            outputFile.write('Index: %s %s \n' % (i, output[state]))


def readTextFromFile(filename):
    '''
    Return string payload of input filename.

    There might be differences in the output index results due to extra characters passed
    along during the copy paste to the input file.
    '''
    with open(filename, 'r') as myfile:
        text = myfile.read()
        if not caseSensitive :
            return text.lower()
        return text



keywords = ['he', 'she', 'his', 'hers']
text = 'ushers'

keywords = ['pattern',	'tree',	'state','prove','the','it']
if caseSensitive :
    keywords = [x.lower() for x in keywords]

text = readTextFromFile('input')

createStateMachine(keywords)
print( '>Go To Graph : %s \n>Ouput function : %s \n>Failure function : %s' % (g, output, failure))


findInString(text, 'output')
