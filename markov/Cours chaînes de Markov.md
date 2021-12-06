# CHAîNES DE MARKOV ET FILES D'ATTENTE

Utilitaires :

- [Symboles LaTeX](http://detexify.kirelabs.org/classify.html)

- [Fonction supportées par KaTeX](https://katex.org/docs/supported.html#special-notation)

- [Mermaid flowcharts](https://mermaid-js.github.io/mermaid/#/flowchart)

## Sommaire

- [Chaînes de Markov à temps discret](#cha-nes-de-markov---temps-discret)
  * [Cadre](#cadre)
    + [Définition : Chaîne de Markov](#d-finition---cha-ne-de-markov)
  * [Matrice de transition d'une chaîne de Markov](#matrice-de-transition-d-une-cha-ne-de-markov)
    + [Définition : Chaîne de Markov homogène](#d-finition---cha-ne-de-markov-homog-ne)
    + [Propriétés élémentaires de la matrice de transition](#propri-t-s--l-mentaires-de-la-matrice-de-transition)
    + [Graphe associé à une chaîne de Markov](#graphe-associ----une-cha-ne-de-markov)
    + [Définition : Chemin](#d-finition---chemin)
  * [Classes d'équivalence](#classes-d--quivalence)
    + [Définition : Classe de communication (CdC)](#d-finition---classe-de-communication--cdc-)
    + [Définition : Chaîne de Markov irréductible](#d-finition---cha-ne-de-markov-irr-ductible)
    + [Définition : Classe de communication fermée](#d-finition---classe-de-communication-ferm-e)
    + [Propriété : Restriction d'une CDM à une CdC fermée](#propri-t----restriction-d-une-cdm---une-cdc-ferm-e)
    + [Définition : Etat absorbant](#d-finition---etat-absorbant)
  * [Etats récurrents et transitoires](#etats-r-currents-et-transitoires)
    + [Définition : Temps d'atteinte](#d-finition---temps-d-atteinte)
    + [Définition : Etats récurrents et transitoires](#d-finition---etats-r-currents-et-transitoires)
    + [Théorème : Caractérisation des états récurrents et transitoires](#th-or-me---caract-risation-des--tats-r-currents-et-transitoires)
    + [Corollaire : Classes de communication récurrentes et transitoires](#corollaire---classes-de-communication-r-currentes-et-transitoires)
    + [Proposition : Classes récurrentes et classes fermées](#proposition---classes-r-currentes-et-classes-ferm-es)
- [Limite d'une chaîne de Markov](#limite-d-une-cha-ne-de-markov)
  * [Notion de périodicité d'une chaîne de Markov](#notion-de-p-riodicit--d-une-cha-ne-de-markov)
    + [Définition : Chaîne de Markov périodique](#d-finition---cha-ne-de-markov-p-riodique)
  * [Mesures invariantes](#mesures-invariantes)
    + [Définition : Mesure invariante](#d-finition---mesure-invariante)
    + [Cas particulier important : chaînes de Markov réversibles](#cas-particulier-important---cha-nes-de-markov-r-versibles)
  * [Théorèmes limites pour une chaîne de Markov](#th-or-mes-limites-pour-une-cha-ne-de-markov)
    + [Théorème : Existence d'une mesure invariante](#th-or-me---existence-d-une-mesure-invariante)
    + [Théorème ergodique](#th-or-me-ergodique)

---

## Chaînes de Markov à temps discret

### Cadre

On se donne $(\Omega, \mathcal{F}, \mathbb{P})$ un espace probabilisé, et $\mathcal{S}$ un enemble **d'états** fini (discret ou dénombrable). 

On note $n \in \mathbb{N}$ le **temps** et on se donne une suite $(X_n)$ de variables aléatoires à valeurs dans $\mathcal{S}$.

#### Définition : Chaîne de Markov

$X_n$ est une **chaîne de Markov à temps discret** si :

$$
\mathbb{P}(X_n = i_n | X_{n-1} = i_{n-1}, \ldots, X_0 = i_0) = \mathbb{P}(X_n = i_n | X_{n-1})
$$

### Matrice de transition d'une chaîne de Markov

On définit la matrice $P^{(n)}$ qui permet de passer de $X_n$ à $X_{n+1}$ telle que : 

$$
p_{i,j}^{(n)} \equiv \mathbb{P}(X_{n+1} = j | X_{n} = i) \\
\scriptsize\forall (i,j) \in \mathcal{S} \times \mathcal{S}
$$

Matriciellement, c'est la probabilité d'aller en `colonne` sachant qu'on est en `ligne`.

#### Définition : Chaîne de Markov homogène

On dit qu'une chaîne de Markov est **homogène** si pour tout $n \in \mathbb{N}$ :

$$
P^{n} = P
$$

C'est-à-dire que la matrice de transition est la même à chaque étape. Dans la suite du cours, on ne considère que des chaînes de Markov (CDM) homogènes.

#### Propriétés élémentaires de la matrice de transition

- Ses coefficients sont toujours positifs ou nuls, et inférieurs à 1.

- C'est une matrice **stochastique** (la somme des éléments d'une ligne vaut 1) :

$$
\sum_{j \in \mathcal{S}} p_{i,j} = 1 \\
\scriptsize\forall i \in \mathcal{S}
$$

- La loi d'un élément de la suite peut s'obtenir avec cette matrice. Soit par exemple $\Phi$ la loi de $X_0$, alors la loi de $X_1$ vaut :

$$
(\mathbb{P}(X_1 = j))_{j \in \mathcal{S}} 
= (\sum_{i \in \mathcal{S}} \mathbb{P}(X_1 = j | X_0 = i)\mathbb{P}(X_0=i))_{j \in \mathcal{S}}
= \Phi P
$$

#### Graphe associé à une chaîne de Markov

Les états (éléments de $\mathcal{S}$ sont les sommets du graphe). On dessine une arrête entre $i$ et $j$ si $p_{i,j} > 0$. Par exemple :

```mermaid
flowchart TD

    A((A)) -->|0.5| B((B))
    A -->|0.5| A
    C((C)) -- 1 --> C
```

#### Définition : Chemin

Il existe un chemin entre $i$ et $j$ $(i, j) \in \mathcal{S}$ s'il existe un entier $m$ et une suite d'éléments 

$$
i_0=1, i_1, \ldots, i_{m-1}, i_{m} = j
$$

tels que $\forall k \in \llbracket 1,m \rrbracket$

$$
p_{i_k, i_{k+1}} > 0
$$

Autrement dit,

$$
\exist n \in \mathbb{N} / (P^{(n)})_{i,j} > 0
$$

En français : on peut aller de $i$ à $j$ avec une probabilité non nulle.

### Classes d'équivalence

#### Définition : Classe de communication (CdC)

Il y a **équivalence** entre $i$ et $j$ s'il existe un chemin allant de $i$ à $j$ et vice-versa. On note alors $i \sim j$. C'est une relation d'équivalence (réflexive, transitive, symétrique), et on peut donc exhiber une partition de $\mathcal{S}$ entre classes d'équivalence.

On appelle ces classes d'équivalence des **classes de communication**.

#### Définition : Chaîne de Markov irréductible

On dit d'une CDM qu'elle est **irréductible** si elle admet une seule classe d'équivalence.

Autrement dit, on peut toujours trouver un chemin entre tout $i$ et tout $j$ :

$$
\forall (i, j) \in \mathcal{S \times S}, 
\exists m \in \mathbb{N} / P^m_{i,j} > 0
$$

#### Définition : Classe de communication fermée

Une classe de communication $\mathcal{C}$ est dite **fermée** si :

$$
\sum_{j \in \mathcal{C}} p_{i,j} = 1
$$

(On somme sur une partie des éléments d'une ligne)

Autrement dit, lorsqu'on atteint un état de $\mathcal{C}$, on reste toujours dans $\mathcal{C}$.

#### Propriété : Restriction d'une CDM à une CdC fermée

La restriction d'une CDM à une classe de communication fermée est encore une CDM.

#### Définition : Etat absorbant

Un état $i \in \mathcal{S}$ est dit **absorbant** s'il vérifie :

$$
\text{Si } X_0 = i \text{ alors } X_n = i {\text{ pour tout }} n \in \mathbb{N}
$$

### Etats récurrents et transitoires

#### Définition : Temps d'atteinte

On note $T_{i_0}^i$ le **temps d'atteinte** de l'état $i$ en partant de $i_0$ :

$$
T_{i_0}^i = \inf 
\text{\textbraceleft} 
n \in \mathbb{N} / X^n=i | X^0 = i_0
 \text{\textbraceright}
$$

Le temps d'atteinte est une variable aléatoire à valeurs dans $\mathbb{N}^* \cup \text{\textbraceleft} +\infty \text{\textbraceright}$.

Si $i$ et $j$ sont dans la même classe de communication, alors le temps d'atteinte a une probabilité non nulle d'être fini :

$$
\mathbb{P}(T^i_j < + \infty) > 0
$$

#### Définition : Etats récurrents et transitoires

Un état $i$ est dit **récurrent** si le temps d'atteinte de $i$ partant de $i$ est presque sûrement fini :

$$
\mathbb{P}(T^i_i < + \infty) = 1
$$

Sinon, on dit que l'état est **transitoire**.

Un état $i$ est dit **récurrent positif** s'il est récurrent et si de plus :

$$
\mathbb{E}(T_i^i) < + \infty
$$

Sinon, il est dit **récurrent nul**.

#### Théorème : Caractérisation des états récurrents et transitoires

1. Un état $i$ est récurrent si, et seulement si, partant de $i$, on reviendra presque sûrement en $i$ une infinité de fois  :

$$
i \text{ récurrent } 
\iff \mathbb{P}(\#\{ n/X_n=i|X_0=i\} = + \infty) = 1 \\ 
\\ \text{ } \\
\text{i.e.} \sum_n p^n_{i,i} = + \infty

$$

2. On prouve un théorème similaire pour les états transitoires :

$$
i \text{ transitoire } 
\iff \mathbb{P}(\#\{ n/X_n=i|X_0=i\} = + \infty) = 0 \\ 
\\ \text{ } \\ 
\text{i.e.} \sum_n p^n_{i,i} < + \infty
$$

#### Corollaire : Classes de communication récurrentes et transitoires

Au sein d'une classe de communication, les états sont soit tous récurrents, soit tous transitoires. On dira alors de la classe de communication elle-même qu'elle est **récurrente** ou **transitoire**.

#### Proposition : Classes récurrentes et classes fermées

Une classe de communication $\mathcal{C}$ est récurrente <u>ssi</u> elle est fermée.

## Limite d'une chaîne de Markov

On note $\mu_n$ la loi de $X_n$. On a alors $\mu_n = \mu_0 P^n$.

Dans cette section, on s'intéresse à la limite de $\mu_n$ lorsque $n \rightarrow + \infty$.

### Notion de périodicité d'une chaîne de Markov

#### Définition : Chaîne de Markov périodique

Supposons qu'on ait une partition de $\mathcal{S}$ : $E_1, E_2, \ldots , E_K$ telle que :

$$
\forall k \in \llbracket 1,K \rrbracket, 
\forall i \in E_k, \sum_{j \in E_{k+1}}p_{i,j} = 1
$$

Avec la convention $K+1 = 1$ (on écrit les $k$ modulo $K$).

Le plus petit $K$ vérifiant la relation ci-dessus est appelé la **période** de la CDM.

En français : si on est dans un état de $E_k$, on est certain d'être dans un état de $E_{k+1}$ à l'étape suivante. 

Si la partition ne contient que $\mathcal{S}$, alors la chaîne est dite **apériodique**.

### Mesures invariantes

#### Définition : Mesure invariante

Une mesure $\mu$ est dite **invariante** si, pour une matrice de transition $P$ :

$$
\begin{cases}
\mu P = \mu \\
\mu \geq 0
\end{cases}
$$

Si de plus on peut choisir $\mu$ telle que $\sum_{k \in \mathcal{S}} \mu_k=1$, on dit de $\mu$ que c'est une **probabilité invariante**.

<u>Remarque</u> : Les limites éventuelles des lois d'une CDM $(X_n)$ sont de telles mesures. On peut penser à des "vecteurs propres à gauche de P associés à la valeur propre 1".

#### Cas particulier important : chaînes de Markov réversibles

Une chaîne de Markov est dite **réversible** si il existe une mesure $\mu$ telle que :

$$
\forall i,j \in \mathcal{S}, \mu_{i} \times p_{ij} = \mu_{j} \times p_{ji}
$$

On prouve qu'<u>une mesure réversible est invariante</u>.

### Théorèmes limites pour une chaîne de Markov

#### Théorème : Existence d'une mesure invariante

Soit $X_n$ une chaîne de Markov <u>irréductible</u> et <u>récurrente</u>.

Alors, modulo multiplication par $t>0$, il existe une **unique mesure invariante** $\mu$.

#### Théorème ergodique

Soit $X_n$ une chaîne de Markov <u>irréductible</u>. On introduit les notations suivantes :

$$
T^i = \inf \{ n \geq 1 / X_n = i | X_0 = i \}
$$

est le premier temps de retour à $i$ partant de $i$, et

$$
\forall i \in \mathcal{S}, \pi_i = \frac{1}{\mathbb{E}(T^i)}
$$

Avec la convention $\pi_i = 0$ si $i$ est un état transitoire ou réccurent nul.

Alors, on a le résultat de convergence en loi suivant :

$$
\frac{1}{n} \sum_{k=1}^n X_k \xrightarrow \mathcal{L} \pi
$$

En particulier, si $X_n$ est <u>apériodique</u>, 

$$
\mu_i^n = \mathbb{P}(X_n = i) \xrightarrow {n \rightarrow + \infty} \pi_i
$$

avec $\pi_i$ défini comme plus haut, et $\mu$ est l'unique mesure invariante de $X_n$.



## Méthodes de Monte-Carlo fondées sur les chaînes de Markov

### Condition de Doeblin

#### Définition : Condition de Doeblin

Soit $X_n$ une CDM de matrice de transition $P$. La **condition de Doeblin** est vérifiée s'il existe une probabilité $\pi$ et une constante $C > 0$ telles que :

$$
p_{ij} \geq C \pi_j
$$

On peut montrer l'équivalence avec une condition plus faible : 

$$
\exists l \in \mathbb Z / (P^l)_{ij} \geq c \pi_j
$$



#### Théorème : Existence d'une probabilité invariante

Si la CDM $X_n$ vérifie la condition de Doeblin, alors elle admet une unique probabilité invariante.



### Algorithme de Metropolis-Hastings

L'objectif est d'approcher (d'échantilloner selon) une mesure de probabilité inconnue $\pi$ sur un ensemble d'états $\mathcal S$ fini (de cardinal grand).

On suppose connue une mesure invariante $f = \kappa \pi$ où $\kappa$ est un réel inconnu.

Pour l'algorithme, on a besoin de définir une matrice de transition permettant de visiter les différents sites (états). Cette matrice notée $Q$ vérifie :

$$
q_{ij} > 0 \iff q_{ji} >0
$$

En pratique, on choisit $Q$ symétrique.

On définit également une relation d'équivalence : $i$ et $j$ sont dits voisins si $q_{ij} > 0$.

En supposant $f$ donnée, on pose :

$$
\alpha_{ij} = \min \left( 1,\frac{f_j q_{ji}}{f_i q_{ij}} \right)
$$

et on peut alors assembler une matrice stochastique $P$ : 

$$
\begin{cases}
p_{ij} = \alpha_{ij} q_{ij} & \text{si $i$ et $j$ sont voisins} \\
p_{ii} = 1 - \sum_{j \neq i} p_{ij} & \text{sinon}
\end{cases}
$$



#### Propositions : Résultats de convergence

Avec les notations ci-dessus : 

- La CDM $X_n$ associée à $P$ admet $\pi$ comme probabilité invariante.

- Si $Q$ vérifie la condition de Doeblin, alors $P$ vérifie également cette condition.



#### Algorithme : Metropolis-Hastings

L'algorithme est le suivant : 

- On initialise $X_n$ à un état $i$ donné.

- A chaque itération, on choisit aléatoirement un état $j$ candidat pour $X_{n+1}$ à partir de la distribution $q_{ij}$. On tire alors un nombre uniformément aléatoire $v \in [0,1]$ et on calcule le **taux d'acceptation** $\alpha_{ij}$. Alors : 

$$
\begin{cases}
\text{si } v \leq \alpha_{ij} & X_{n+1} = j \\
\text{si } v >    \alpha_{ij} & X_{n+1} = i \\
\end{cases}
$$

Pour $Q$ symétrique, le rapport $\frac{f_j q_{ji}}{f_i q_{ij}}$ devient simplement $\frac{\pi_j}{\pi_i}$.  Le calcul de ce rapport ne nécessite pas nécessairement la connaissance des valeurs des $\pi_i$.



### Algorithme du recuit simulé

On considère un paramètre $\theta$ ("température") qui permet de faire évoluer l'état du système.

L'algorithme consiste à appliquer l'algorithme de Metropolis-Hastings à température constante pendant un certain nombre d'étapes, puis à faire diminuer la température. 

La mesure utilisée est la mesure de Gibbs : 

$$
\mu_{\theta}(j) = \frac{1}{Z_{\theta}} \exp \left(- \frac{\mathcal H(j)}{\theta} \right)
$$

Avec :

- $\mathcal H$ une fonction de $\mathcal S$ (fini) dans $\mathbb R$ appelée **énergie**.

-  $Z_{\theta}$ est une constante de normalisation appelée <u>fonction de partition</u>.

On peut prouver qu'on a bien convergence lorsque $n \rightarrow +\infty$ et $\theta \rightarrow 0^+$.

En particulier :

$$
\mu_{\theta} \xrightarrow{\theta \rightarrow 0} \frac{1}{\#\mathcal M}
$$

où $\mathcal M$ est le nombre de minimiseurs de $\mathcal H$.

On utilise 

$$
\theta_n = \frac{\text{cste}}{n}
$$
