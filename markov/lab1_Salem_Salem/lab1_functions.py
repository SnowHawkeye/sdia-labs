import numpy as np

def ehrenfest(K, n_max, rng):
    """Generates a trajectory of n_max points using Ehrenfest's model starting from state 0.

    Args:
        K (int): Number of particles in Ehrenfest's model.
        n_max (int): Number of steps of the Markov chain.
        rng (numpy.random.Generator): Random generator.

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