import math
import random
import collections


class QLearn:
    max_states = 40

    def __init__(self, actions, temp=5, epsilon=0.1, alpha=0.5,
                 gamma=0.5):

        self.q = {}

        self.states = set()

        #  SRE => State Residual Entropy
        #  ARE => Agent Residual Entropy
        self.stat_sre = {}
        self.stat_are = 1.0
        self.dyna_sre = {}
        self.dyna_are = 1.0

        self.temp = temp

        self.epsilon = epsilon  # exploration constant
        self.alpha = alpha  # learning rate
        self.gamma = gamma  # discount rate
        self.actions = actions

    def getQ(self, state, action):
        return self.q.get((state, action), 0.0)

    def learnQ(self, state, action, reward, value):
        '''  Q-learning Formula:
            Q(s, a) += alpha * (reward(s,a) + gamma * max(Q(s')) - Q(s,a))
        '''

        oldv = self.q.get((state, action), None)
        if oldv is None:
            self.q[(state, action)] = reward
        else:
            self.q[(state, action)] = oldv + self.alpha * (value - oldv)

        self.recalc_are(state, reward)

    def recalc_are(self, state, reward):
        '''  Learning Residual Entropy
            TODO: update this to take into account diff ways of
                  measuring SRE

            update Residual Entropy of this state (stateRE) and the
                   Average Residual Entropy of the agent (aveSRE)
            (optimized using dynamic programming (DP))

            Learning Residual Entropy, 'I(S)', for a state 'S':
                       -SUM([p(S, a) * log(p(S, a)) for all a in A])
                I(S) = ---------------------------------------------
                                       log(|a|)
                where:
                    'A' is a set of actions possible in state 'S';
                    'a' is an action in set 'A';
                    'p(S, a)' is the probability of selecting
                                 action 'a' in state 'S'; and
                    '|a|' is the number of possible actions

                In an unlearned case:
                    p(S, a) = p(S, a1) = p(S, a2) = p(S, a3) = ...
                    p(S, a) = 1/|a|
                    SUM(p(S, a) * log(p(S, a))) = |a| * (1/|a|) * log(1/|a|)
                                                = - log(|a|); therefore,
                    I(S) = log(|a|) / log(|a|) = 1

                In a fully learned case:
                    p(S, a) = 1;
                    SUM( p(S, a) * log(p(S, a)) ) = SUM( 1 * log(1) )
                                                  = SUM( 1 * 0 )
                                                  = 0; therefore,
                    I(S) = 0.0 / log(|a|) = 0

                unlearned                                   fully learned
                    1  >----------------------------------------> 0

            Average of 'I(S)', 'I', in episode 'E':
                'I' is defined as follows:
                    I = SUM( [ I(S) for all S in E ] ) / |E|
                where:
                    '|E|' is the number of states included in 'E'

            In this implementation:
                stateRE[S] := I(S)
                aveSRE     := I

            Sources:
                "Automatic Adaptive Space Segmentation
                 for Reinforcement Learning"
                    Komori, Y., Notsu, A., Honda, K., & Ichihashi, H.
                "Speeding up Multi-Agent Reinforcement Learning Coarse-
                 Graining of Perception Hunter Game as an Example"
                    Ito, A. & Kanabuchi, M.
        '''

        eprobs = self.get_eprobs(state)
        new_sre = - sum([eprob * math.log(eprob) for eprob in eprobs]) / \
            math.log(len(self.actions))

        # recalc static SRE and ARE
        stat_sre_delta = new_sre - self.stat_sre.get(state, 1)
        self.stat_sre[state] = new_sre
        self.stat_are += stat_sre_delta / self.max_states

        # recalc dynamic SRE and ARE
        if state in self.states:
            dyna_sre_delta = new_sre - self.dyna_sre.get(state, 1)
            self.dyna_sre[state] = new_sre
            self.dyna_are += dyna_sre_delta / len(self.states)
        else:
            self.states.add(state)
            self.dyna_sre[state] = new_sre
            self.dyna_are = (self.dyna_are * (len(self.states) - 1) +
                             self.dyna_sre[state]) / len(self.states)

    def choose_action(self, state, method=1):
        # Greedy Epsilon
        if method in [0, 'epsilon']:
            action = 0
            if random.random() < self.epsilon:
                action = random.choice(self.actions)
            else:
                q = [self.getQ(state, a) for a in self.actions]
                maxQ = max(q)

                # In case there're several state-action max values
                # we select a random one among them
                maxCount = q.count(maxQ)
                if maxCount > 1:
                    best = [
                        i for i in range(len(self.actions))
                        if q[i] == maxQ
                    ]
                    i = random.choice(best)
                else:
                    i = q.index(maxQ)
            return action

        # Boltzmann
        elif method in [1, 'boltzmann']:
            eprobs = self.get_eprobs(state)

            ran = random.random()
            action = random.choice(self.actions)
            # print(eprobs, ran)

            for a in self.actions:
                if ran > eprobs[a]:
                    ran -= eprobs[a]
                else:
                    action = a
                    break

            # print(action, eprobs[a])
            return action

        # Mod Random
        elif method in [2, 'mod_random']:
            q = [self.getQ(state, a) for a in self.actions]
            maxQ = max(q)

            if random.random() < self.epsilon:
                # action = random.choice(self.actions)
                minQ = min(q)
                mag = max(abs(minQ), abs(maxQ))
                # add random values to all action, recalculate maxQ
                q = [
                    q[i] + random.random() * mag - 0.5 * mag
                    for i in range(len(self.actions))
                ]
                maxQ = max(q)

            # In case there're several state-action max values
            # we select a random one among them
            count = q.count(maxQ)
            if count > 1:
                best = [
                    i for i in range(len(self.actions)) if q[i] == maxQ
                ]
                i = random.choice(best)
            else:
                i = q.index(maxQ)

            action = self.actions[i]
            return action

        # random
        elif method in [3, 'random']:
            return random.choice(self.actions)

    def learn(self, state1, action1, reward, state2, print_q_after=False):
        maxqnew = max([self.getQ(state2, a) for a in self.actions])
        self.learnQ(state1,
                    action1,
                    reward,
                    reward + self.gamma * maxqnew)
        if print_q_after:
            print(self.q)

    def get_eprobs(self, state):
        ''' Probability of selecting each action on given state:
            eValue(state, action) = e ** (Q(state, action)/temp)
                                   eValue(state, action)
            eProb(state, action) = ---------------------
                                   (sum of all eValues)
        '''
        eValues = []
        for action in self.actions:
            c = getattr(self.agent, 'going_to_obstacle', None)
            if isinstance(c, collections.Callable):
                if c(action):
                    eValues.append(1)
                    continue
            eValues.append(math.exp(self.getQ(state, action) / self.temp))
        total = sum(eValues)
        return [eValue / total for eValue in eValues]


def ff(f, n):
    fs = "{:f}".format(f)
    if len(fs) < n:
        return ("{:" + n + "s}").format(fs)
    else:
        return fs[:n]
