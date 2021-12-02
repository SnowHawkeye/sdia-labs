import numpy as np

def ehrenfest(K, n_max, rng):
    """Generates a trajectory of n_max points using Ehrenfest's model starting from state 0.

    Args:
        K (int): Number of particles in Ehrenfest's model.
        n_max (int): Number of steps of the Markov chain.
        rng (numpy.random.Generator): Random number generator.

    Returns:
        numpy.array: Array containing the successive states taken at each step of the simulation.
        int: First time of return to the initial state.
    """
    X = np.zeros(n_max) # Tableau qui contient les états successifs de la simulation
    is_T_found = False
    T = 0

    # On choisit comme distribution initiale un Dirac centré en 0
    for k in range(1, n_max): # X[0] est donc défini, on démarre la boucle à X[1]

        # On commence par les deux cas particuliers : quand on se trouve dans l'état 0 ou dans l'état K
        if X[k-1] == 0 : 
            X[k] = 1
        elif X[k-1] == K : X[k] = K-1
            
        # Dans le cas général
        else :
            rand = rng.binomial(1, X[k-1]/K) # Simulation d'un tirage aléatoire avec une loi de Bernoulli
            if rand == 1 : X[k] = X[k-1] - 1
            else : X[k] = X[k-1] + 1
                
        if not is_T_found and X[k] == 0: 
                T = k
                is_T_found = True
    return X, T


def simulate_dthmc(P, mu, n_max, rng):
    """Simulates the trajectory of a Markov chain for a given number of time steps.

    Args:
        P (numpy.array): Transition matrix of the Markov chain.
        mu (numpy.array): Initial distribution.
        n_max (int): Number of steps of the Markov chain.
        rng (numpy.random.Generator): Random number generator.
        
    Returns:
        numpy.array: Array containing the successive states taken at each step of the simulation.  
    """
    
    n_state = len(mu)

    X = np.zeros(n_max).astype(int) # Tableau qui contient les états successifs de la simulation
    
    X[0] = rng.choice(np.arange(n_state), p=mu) # On initialise l'état initial selon mu
    
    for k in range(1, n_max):
        X[k] = rng.choice(np.arange(n_state), p=P[X[k-1], :]) # On passe à l'état suivant selon les probabilités de la matrice de transition
        
    return X


def simulate_dthmc_until_return(P, mu, rng):
    """Simulates the trajectory of a Markov chain until it returns to its initial state.

    Args:
        P (numpy.array): Transition matrix of the Markov chain.
        mu (numpy.array): Initial distribution.
        rng (numpy.random.Generator): Random number generator.
        
    Returns:
        numpy.array: Array containing the successive states taken at each step of the simulation.  
        int: Return time to initial state.
    """
    
    n_state = len(mu)

    X = [] # Liste qui contient les états successifs de la simulation
    # Comme on ne sait pas combien d'étapes il y aura, on ne peut pas utiliser un array
    
    initial_state = rng.choice(np.arange(n_state), p=mu) # On initialise l'état initial selon mu
    X.append(initial_state) 
    
    k = 1
    
    while True : # Il faut rentrer une première fois dans la boucle
        next_state = rng.choice(np.arange(n_state), p=P[X[k-1], :])
        X.append(next_state) # On passe à l'état suivant selon les probabilités de la matrice de transition
        if(next_state == initial_state): break # Si on est retourné à l'état initial, on arrête la simulation
        k += 1
        
    return np.array(X), k
    
    