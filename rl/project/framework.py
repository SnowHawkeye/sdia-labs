from argparse import ArgumentError
import numpy as np
import abc # Abstract classes


#################################### CLASSES ####################################

################# ENVIRONMENT #################

class Arm():
    def __init__(self, mean, std, sampling_function):
        """Initializes an arm for the bandit problem.

        Args:
            mean (float): Mean of the reward distribution.
            std (float): Standard deviation of the reward distribution.
            sampling_function (lambda( mean, variance, seed )): Function sampling a random variable from a given mean and variance.
        """
        self.mean = mean
        self.std = std
        self.sampling_function = sampling_function
    
    def pull(self, times=1):
        """Pull the arm a certain number of times.
        
        Args:
            times (int): Number of times the arm must be pulled.

        Returns:
            numpy.array(float): Rewards obtained by pulling the arm. If there is only one result, returns the result itself as a float (not an array)
        """
        
        results = np.zeros(times)
        for i in range(len(results)):
            results[i] = self.sampling_function(self.mean, self.std)
            
        if len(results) == 1 : return results[0]
        else : return results

class Environment():
    def __init__(self, arms):

        # Ensure that all arms have the same known variance
        for a in arms :
            if a.std != arms[0].std : raise ValueError("All arms within the environment must have the same variance.")
        
        self.arms = arms
        self.std = self.arms[0].std
        self.reward_history = [ [] for _ in range(len(self.arms)) ] # Contains the observed rewards
        self.best_arm_history = [] # Contains the list of the best arm that could have been chosen each time a pull happened
        self.best_potential_reward_history = [] # Contains the best possible reward that could have been obtained each time a pull happened
        
    def pull_arm(self, arm_number):
        # We pull every arm in order to know the best one, but only record the one that is requested
        
        rewards = np.zeros(len(self.arms))
        for i in range(len(self.arms)):
            rewards[i] = self.arms[i].pull()
        
        # Update the best potential arms
        self.best_arm_history.append(np.argmax(rewards))
        self.best_potential_reward_history.append(np.max(rewards))
        
        # Compute the reward for the requested arm
        reward = rewards[arm_number]
        self.reward_history[arm_number].append(reward)
        return reward

    def reset_history(self):
        """Resets the environment's history.
        """
        self.reward_history = [ [] for _ in range(len(self.arms)) ]
        self.best_arm_history = []
        self.best_potential_reward_history = []
    
################# AGENTS #################

class Agent(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def play(self, steps, confidence, std, env):
      pass
  
class ETC_Agent(Agent):
    # works for two arms
    # implemented as described in the article
    
    def __init__(self):
        self.is_exploring = True # if false, means that the agent is exploiting
        self.last_choice = 0 # choices are 0 or 1 for this agent
    
    def play(self, steps, confidence, env):
        if len(env.arms) != 2 : raise ValueError("This agent requires exactly two arms to play.")
        if steps < 3 : raise ValueError("The number of steps must be at least 3.")
        
        # Initialization
        env.reset_history()
        env.pull_arm(0)
        env.pull_arm(1)
        n = 2
        chosen_arms = []
        rewards_obtained = []
        
        # Exploration loop
        while abs(np.mean(env.reward_history[0]) - np.mean(env.reward_history[1])) < np.sqrt((4*(env.std**2)/n)*np.log((np.log(n))**2/confidence)) and n < steps:
            rewards_obtained.append(env.pull_arm(0))
            rewards_obtained.append(env.pull_arm(1))
            chosen_arms.append(0)
            chosen_arms.append(1)
            n += 2
        
        # Exploitation loop
        while n < steps:
            n += 1
            empirical_reward_0 = np.mean(env.reward_history[0])
            empirical_reward_1 = np.mean(env.reward_history[1])
            
            if empirical_reward_0 > empirical_reward_1:
                rewards_obtained.append(env.pull_arm(0))
                chosen_arms.append(0)
            else :
                rewards_obtained.append(env.pull_arm(1))
                chosen_arms.append(1)
                
        return chosen_arms, rewards_obtained

#################################### FUNCTIONS ####################################
    
    
def gaussian_sampling(mean, std):
    """Samples a random number from a gaussian distribution.

    Args:
            mean (float): Mean of the distribution.
            std (float): Standard deviation of the distribution.

    Returns:
        float: The generated random number.
    """
       
    rng = np.random.default_rng()
    return rng.normal(mean, std)

