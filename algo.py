class Node:
    state=0;
    nextStatesByWeight= {};

    def __init__(self, state):
        self.state = state


    def __repr__(self):
        '''
        Override to string method to get some meaningful debug messages
        :return:
        '''

        return 'State : %s, weights : %s \n' % (self.state, self.nextStatesByWeight)

    def addStateWithWeight(self, nextState, nextStateWeight):
        self.nextStatesByWeight[nextState] = nextStateWeight


def createGoToFunction(keywords):
    newstate = 0
    for keyword in keywords:
        processKeyword(keyword)

    allkeys = ''.join(set(''.join(keywords)))
    for i in range(len(allkeys)):
        if g.get((0, allkeys[i]), fail) == fail:
            g[(0, allkeys[i])] = 0


g = {}
output = {}
failure = {}
newstate = 0
fail = None


def processKeyword(keyword):
    global newstate
    state = 0
    j = 0
    while g.get((state, keyword[j]), fail) != fail:
        state = g[(state, keyword[j])] #we are sure the key exists
        j = j + 1

    for p in range(j, len(keyword)) :
        newstate = newstate + 1
        g[(state, keyword[p])] = newstate
        state = newstate

    updateOutput(state, keyword)

    return keyword

def updateOutput(state, keyword) :
    if state in output.keys():
        #this scenario will be triggered by updates from create failure
        if isinstance(keyword, list):
            output[state].extend(keyword)
        else:
            output[state].append(keyword)
    else:
        output[state] = [keyword]


def createFailueFunction():
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


def findInString(inputString):
    state = 0
    for i in range(len(inputString)) :

        while g.get((state, inputString[i]), fail) == fail and state != 0:
            #print ('STATE = ', state)
            state = failure[state]
        state = g.get((state, inputString[i]), state)
        if output.get(state, None ) != None :
            print('i = %s , output = %s , actual : %s' % (i, output[state], inputString[:i + 1]))

keywords = ['he', 'she', 'his', 'hers']
text = 'ushers'

keywords = ['pattern',	'tree',	'state','prove','the','it']
with open('input', 'r') as myfile:
    text=myfile.read().replace('\n', '')

createGoToFunction(keywords)
createFailueFunction()
print( 'G = %s \n Ouput %s \nFailure %s' % (g, output, failure))

findInString(text)
