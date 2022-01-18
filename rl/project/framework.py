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
    """An environment contains a set of arms. It lets a user pull any arm and exposes the history of rewards observed when doing so.
    """
    def __init__(self, arms):
        """Creates an environment with the given list of arms.

        Args:
            arms (list(Arm)): The list of arms to initialize the environment with. They must all have the same variance.

        Raises:
            ValueError: If all arms do not have the same variance.
        """
        # Ensure that all arms have the same known variance
        for a in arms :
            if a.std != arms[0].std : raise ValueError("All arms within the environment must have the same variance.")
        
        self.arms = arms
        self.std = self.arms[0].std
        self.reward_history = [ [] for _ in range(len(self.arms)) ] # Contains the observed rewards
        
    def pull_arm(self, arm_number):
        """Pull the requested arm.

        Args:
            arm_number (int): The arm to pull.

        Returns:
            float: The reward obtained by pulling the arm.
        """
        reward = self.arms[arm_number].pull()
        self.reward_history[arm_number].append(reward)
        return reward

    def reset_history(self):
        """Resets the environment's history.
        """
        self.reward_history = [ [] for _ in range(len(self.arms)) ]
    
################# AGENTS #################

class Agent(metaclass=abc.ABCMeta):
    """Abstract class representing an arm-pulling agent.
    """
    @abc.abstractmethod
    def play(self, steps, confidence, env):
        """The agent plays in the given environment and returns the relevant results.

        Args:
            steps (int): The number of steps to play.
            confidence (float): The confidence level (between 0 and 1).
            env (Environment): The environment to play in.
            
        Returns:
            PlayResults: The results obtained at the end of the session.
        """
        pass
  
class ETC_Agent(Agent):
    """An arm-pulling agent using the Explore-Then-Commit strategy.
    """
    
    def play(self, steps, confidence, env):
        if len(env.arms) != 2 : raise ValueError("This agent requires exactly two arms to play.")
        if steps < 3 : raise ValueError("The number of steps must be at least 3.")
        
        # Initialization
        env.reset_history()
        n = 2
        chosen_arms = [0, 1]
        rewards_obtained = []
        rewards_obtained.append(env.pull_arm(0))
        rewards_obtained.append(env.pull_arm(1))
        
        # Exploration loop
        while abs(np.mean(env.reward_history[0]) - np.mean(env.reward_history[1])) < np.sqrt((4*(env.std**2)/n)*np.log((np.log(n))**2/confidence)) and n < steps:
            rewards_obtained.append(env.pull_arm(0))
            rewards_obtained.append(env.pull_arm(1))
            chosen_arms.append(0)
            chosen_arms.append(1)
            n += 2
        
        decision_time = n # The desired confidence has been reached
        
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
                
        return PlayResults(chosen_arms, rewards_obtained, decision_time, env)
    
################# RESULTS #################
    
class PlayResults():
    def __init__(self, chosen_arms, rewards_obtained, decision_time, env):
        self.chosen_arms = np.array(chosen_arms)
        self.rewards_obtained = np.array(rewards_obtained)
        self.env = env
        
        self.regret = self.__compute_regret()
        self.decision_time = decision_time
        self.decision_regret = self.__compute_regret(until=self.decision_time)
        
    def __compute_regret(self, until = None):
        T = len(self.chosen_arms)
        if until == None: until = T
        
        max_reward = np.max([arm.mean for arm in self.env.arms])
        cumulative_rewards = np.sum(self.rewards_obtained)
        return T * max_reward - cumulative_rewards

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

