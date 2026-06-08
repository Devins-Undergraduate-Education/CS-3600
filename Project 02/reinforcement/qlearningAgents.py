# qlearningAgents.py͏󠄂͏️͏󠄌͏󠄎͏︄͏︊͏󠄅
# ------------------͏󠄂͏️͏󠄌͏󠄎͏︄͏︊͏󠄅
# Licensing Information:  You are free to use or extend these projects for͏󠄂͏️͏󠄌͏󠄎͏︄͏︊͏󠄅
# educational purposes provided that (1) you do not distribute or publish͏󠄂͏️͏󠄌͏󠄎͏︄͏︊͏󠄅
# solutions, (2) you retain this notice, and (3) you provide clear͏󠄂͏️͏󠄌͏󠄎͏︄͏︊͏󠄅
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.͏󠄂͏️͏󠄌͏󠄎͏︄͏︊͏󠄅
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.͏󠄂͏️͏󠄌͏󠄎͏︄͏︊͏󠄅
# The core projects and autograders were primarily created by John DeNero͏󠄂͏️͏󠄌͏󠄎͏︄͏︊͏󠄅
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).͏󠄂͏️͏󠄌͏󠄎͏︄͏︊͏󠄅
# Student side autograding was added by Brad Miller, Nick Hay, and͏󠄂͏️͏󠄌͏󠄎͏︄͏︊͏󠄅
# Pieter Abbeel (pabbeel@cs.berkeley.edu).͏󠄂͏️͏󠄌͏󠄎͏︄͏︊͏󠄅


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.qVals = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        return self.qVals[(state, action)]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"

        # get available actions
        legalActions = self.computeActionFromQValues(state)

        # if no legal moves, OOPSIE
        if not legalActions:
            return 0.0
        
        # let's use the method we will write :)
        return self.getQValue(state, legalActions)

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"

        # get actions we can do
        legalActions = self.getLegalActions(state)

        # no moves available... uh oh.
        if not legalActions:
            return None
        
        # initialize best action and val
        bestAction = [legalActions[0]]
        bestValue = float('-inf')

        # iterate and find action with highest qvalue
        for action in legalActions: 

            # find curr qvalue
            qvalue = self.getQValue(state, action)  

            # update everything if a higher qvalue is found
            if qvalue > bestValue:
                bestValue = qvalue
                bestAction = [action]
            elif qvalue == bestValue:
                bestAction.append(action)

        # randomly choose an optimal action
        return random.choice(bestAction)


    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action͏󠄂͏️͏󠄌͏󠄎͏︄͏︊͏󠄅
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
    
        # if no legal actions, go home and watch TV
        if not legalActions:
            return action
        
        # let a coin decide our fate...
        if util.flipCoin(self.epsilon):
            return random.choice(legalActions)
        
        # fate says pick the best policy
        return self.computeActionFromQValues(state)

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"

        # compute curr qvalue
        qCurState = self.getQValue(state, action)

        # compute next qvalue (qvalue')
        qNextState = self.computeValueFromQValues(nextState)

        # do some funky calculation that is in the slideshow
        qval = qCurState + self.alpha * (reward + self.discount * qNextState - qCurState)

        # set the calculated value to the current qvalue
        self.qVals[(state, action)] = qval

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        features = self.featExtractor.getFeatures(state, action)
        "*** YOUR CODE HERE ***"

        # initialize result
        qvalue = 0

        # compute qvalue as sum of weights
        for feature, value in features.items():
            qvalue += self.weights[feature] * value

        # return qvalue
        return qvalue

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        features = self.featExtractor.getFeatures(state, action)
        "*** YOUR CODE HERE ***"

        # compute correction term
        correction = reward + self.discount * self.getValue(nextState) - self.getQValue(state, action)

        # update weights
        for feature, value in features.items():
            self.weights[feature] += self.alpha * correction * value

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method͏󠄂͏️͏󠄌͏󠄎͏︄͏︊͏󠄅
        PacmanQAgent.final(self, state)

        # did we finish training?͏󠄂͏️͏󠄌͏󠄎͏︄͏︊͏󠄅
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging͏󠄂͏️͏󠄌͏󠄎͏︄͏︊͏󠄅
            "*** YOUR CODE HERE ***"
            # print("Here are some funky values", self.weights, sep = " ")
            pass
