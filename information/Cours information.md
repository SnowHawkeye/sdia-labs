# SECURITE DE L'INFORMATION

## Notions de base

Un scénario de sécurité se définit par : 

- Les objectifs de l'adversaire.

- Les connaissances de l'adversaire.

- Les moyens de l'adversaire.

Le **principe de Kerckhoffs** dit que pour faire une analyse de sécurité, on a toutes les connaissances du processus (*e.g.* algorithmes utilisés) à l'exception d'une clé secrète.

### Mesures informationnelles en sécurité de l'information

#### Objectif : Trouver une clé secrète $k$

Mesurer la difficulté :

$$
\text{entropie de la clé = taille de la clé (en bits) si utilisation uniforme}
$$

> *Exemple* : Clé de 128 bits. On a $|K| = 2^{128}$ clés possibles. Alors, la probabilité de trouver la clé en tirant une clé uniformément est : $\mathbb P (\text{Trouver une clé secrète}) = \frac{1}{2^{128}}$
> 
> Montrons que c'est un "grand" nombre. On se place dans un scénario d'attaque où l'adversaire a une "très grosse" grille de calcul : on recouvre la terre de processeurs de la taille d'un grain de sable ($1 \text{ mm}^2$) travaillant tous à la vitesse de la lumière (1 test correspond au temps qu'il faut à la lumière pour passer à travers le processeur, *i.e.* que le processeur peut faire $3.10^{11}$  tests à la seconde, soit $310 \text{ GHz}$). 
> 
> A raison d'une surface de $5.10^8 \text{ mm}^2$, et de $1,5.10^{33}$ tests par seconde, il faudrait alors 4756 ans pour estimer la clé secrète.

#### Objectif : Détecter une intrusion dans un réseau, détecter une information cachée (stéganalyse)

On note :

- $P_n$ la distribution d'un flux (IP) sur le réseau (toutes les données liées à l'échange de données sur un réseau).

- $P_a$ la distribution d'un flux anormal sur le réseau.

L'intrusion n'est pas détectable si la divergence de Küllback-Leibler $D_{KL}$ vérifie :

$$
D_{KL}(P_N, P_A) = \sum_x P_N(x) \log \frac{P_N(x)}{P_A(x)} = 0
$$



#### Objectif : Estimer une clé à partir d'observations bruitées de cette clé

On définit la **fuite d'information** :

$$
I(\underbrace{K}_{\text{clé}}, 
\underbrace{O_1,\ldots, O_{N_o}}_{N_o \text{ observations}}) = 
H(K) - H(K|O_1,\ldots, O_{N_o})
$$

Il n'y a pas de fuite d'information si : 

$$
I(K, O_1, \ldots, O_{N_o}) = 0
$$

> *Exemple* : $O_1 = k + u$ version bruitée de la clé $k$. On considère la loi uniforme $U$ entre -3 et 4.
> 
> $$
> I(K, O_1) = H(K) - \underbrace{H(K | O_1)}_{H(U) = \text{ 3 bits}}
> $$
> 
> Pour $H(K) = 128 \text{ bits}$ on trouve $I(K, O_1) = 125 \text{ bits}$. Autrement dit, 125 bits d'information sont déjà connus.
> 
> *Autres exemples* : ondes électromagnétiques (pour trouver une image affichée sur un écran), consommation d'un CPU (pour trouver une clé secrète), mouvement d'un bras (pour trouver un code PIN).

## Le *watermarking* (filigrane, tatouage)

### Définition

Le ***watermarking*** correspond à l'insertion d'une marque (ou d'un message) qui est à la fois <u>imperceptible</u> et <u>indélébile</u> dans un contenu (image, son vidéo, *etc.*).

Mathématiquement, on écrit :

$$
y = x + w
$$

où :

- $y$ est le contenu tatoué

- $x$ est le contenu original

- $w$ est le tatouage (*watermark*)

L'**imperceptibilité** se traduit par : 

$$
|w| \ll |x|
$$

Être **indélébile** signifie que l'adversaire ne doit pas être capable d'enlever la signature. C'est lié à la notion de **robustesse** : la marque doit pouvoir être détectée / lue après des opérations telle que :

- la compression JPEG

- l'impression et le scan

- des rotations et redimensionnements

Le *watermarking* a plusieurs applications, parmi lesquelles : 

- la protection des droits d'auteurs

- le "traçage de traitres"

### Généralités en tatouage

#### Notations

- Contenu original $C$ (*e.g.* toute l'image)

- Composantes du contenu $x \in \mathcal X$ de taille $N_v$ (*e.g.* certains pixels de l'image)

- Clé secrète $k$

- Composantes tatouées $y$ de taille $N_v$

- Tatouage $w$ de taille $N_v$

- Contenu tatoué $C_w$

- Message à insérer $m$ ($N_m$ bits). C'est une constante (marque). L'objectif est de détecter et non de décoder.

<img src="file:///C:/Users/Shadr/AppData/Roaming/marktext/images/2021-12-15-13-18-08-image.png" title="" alt="" data-align="center">

#### Interprétation géométrique du tatouage

$\mathcal D(m,k)$ : région utilisée pour coder / décoder $m$, paramétrisée par $k$, dans laquelle se trouve $y$.

- Distortion : $|w|$

- Robustesse (*e.g.* ajout de bruit) : distance entre et $y$ et la frontière de  $\mathcal D(m,k)$

- Sécurité : capacité pour l'adversaire à estimer $\mathcal D(m,k)$

Si l'adversaire veut enlever le tatouage, il doit "faire sortir" $y$ de la région de codage / décodage.

### Exemple du tatouage par étalement de spectre

- $x_i, X_i \sim \mathcal N(0, \sigma^2_x)$ i.i.d de dimension $N_v$

- $m \in \{0,1\}$ 1 bit inséré 

- $k$  vecteur de dimension $N_v$, généré pseudo-aléatoirement en utilisant un germe <u>secret</u>. $k$ sera centré : $\mathbb E[k] = 0$ et $|k| = 1$.

On pose alors :

$$
w(m, k) = \pm \alpha k = -(-1)^m \alpha k
$$

Avec le paramètre $\alpha$ :

$$
|w| = \alpha = \mathbb E(|w|)
$$

On décale les contenus dans la direction $\alpha k$ quand $m=1$ et dans la direction $-\alpha k$ quand $m=0$. On a donc deux sous-régions de (dé)codage selon la valeur de $m$.

L'estimation du $m$ décodé $\hat m$ vaut : 

$$
\hat m = \frac{\text{sign} \langle y, k \rangle + 1}{2}
$$



#### Robustesse

- Bruit $n_i \sim \mathcal N(0, \sigma^2_N)$

- $z = y + n$ où $z$ est le contenu bruité ("attaqué" mais ici l'attaque peut être naïve)

- Décodage avec bruit : 
  
  $$
  \hat m = \frac{\text{sign} \langle z, k \rangle + 1}{2}
  $$

- Probabilité d'erreur : 
  
  $$
  \mathbb P(\hat m = 1 | m = 0) = \mathbb P(\hat m = 0 | m = 1)
  $$

On a : 

$$
\begin{cases}
\langle X, K \rangle \sim \mathcal N(0, \sigma^2_X) \\
\langle N, K \rangle \sim \mathcal N(0, \sigma^2_N) \\
\langle Y, K | m=1 \rangle \sim \mathcal N(\alpha, \sigma^2_X) \\
\end{cases}
$$

D'où, si $m=1$, par somme :

$$
\langle Z, K \rangle \sim \mathcal N(\alpha, \sigma^2_X + \sigma^2_N)
$$

Si $m=2$ (2 bits), on a $k_1$ et $k_2$ avec $\langle k_1, k_2 \rangle = 0$.

Et alors 

$$
y = x + w_1 + w_2
$$

avec

$$
w_i = \begin{cases}
\alpha k_i & \text{si } m = 1 \\
- \alpha k_i & \text{si } m = 0 \\
\end{cases}
$$

#### Scénario de sécurité n°1

- On suppose le principe de Kerckhoffs : le schéma ($m$) est connu (cadre supervisé).

- $|m|=1 \text{ bit}$

- L'adversaire observe un nombre de messages $N_o$ contenus tatoués et il connaît les $N_o$ messages (bits) insérés (chacun de 1 bit).

- Objectif : estimer la clé secrète $k$.

Si on suppose $m_1 = 1$

$$
\hat k_1 = \frac{1}{\alpha N_o} \sum y_i
$$

Solution générale : 

$$
\hat k_1 = \frac{1}{\alpha N_o} \sum -(-1^m)y_i
$$

#### Scénario de sécurité n°2

- Même scénario que 1 mais $m$ est inconnu (cadre non supervisé).

- $|m| = 1 \text{ bit}$

On sait qu'il y a deux clusters :

- On peut faire du **clustering** (*e.g.* K-means mais ne fonctionne pas bien en grande dimension).

- La variance est la plus importante dans la direction de la clé secrète $k$ selon laquelle on fait la translation. On peut donc faire une **analyse en composantes principales** (PCA).



#### Scénario de sécurité n°3

- Comme le scénario 2 mais on insère 2 bits par contenu (et on a donc deux clés $k_1$ et $k_2$). 

On peut encore penser au clustering, mais on a toujours le même problème en grande dimension. La PCA ne fonctionne pas forcément non plus car dans certains cas les clusters sont tels que la variance est la même dans toutes les directions.

Par définition, les tirages $m_1$ et $m_2$ sont indépendants. On peut donc utiliser une **analyse en composantes indépendantes** (*cf.* TP et fast ICA).



## Stéganographie et stéganalyse

### Introduction

La **stéganographie** est l'insertion d'un message <u>indéctable</u> dans un contenu. Elle sert à cacher des informations sensibles. La principe différence avec le *watermarking* est la contrainte d'intédectabilité. 

La **stéganalyse** est la détection de ces messages cachés. Elle est principalement utilisée par des agences de sécurité.

Une bonne méthode de stéganographie donne une probabilité d'erreur de 50% (on ne détecte pas mieux que le hasard).

L'image qui sert à cacher l'information est appelée ***cover***.

On évaluera la sécurité de méthodes de stéganalyse d'après le principe de Kerckhoffs, càd que le stéganalyste connaît : 

- L'algorithme d'insertion.

- La taille du message inséré.

- La façon dont les *cover* sont générés (*e.g.* quel type d'appareil photo a créé l'image).



### Stéganographie

#### Stéganographie par substitution de bit de poids faible

Le bit de poids faible (LSB pour *Least Significant Bit*) correspond au bit de parité dans la représentation binaire d'un nombre (càd le dernier bit, vaut 0 si le nombre est pair).

##### Insertion

Entrées : 

- message $m$ de taille $N_m$

- clé $K$

- image *cover* de taille $N_I$ codée en niveaux de gris sur 8 bits

Sortie :

- image "stégo"

##### Définition : Taux d'insertion

On définit le **taux d'insertion** $\alpha$, d'unité le <u>bit par pixel</u> (bpp) comme : 

$$
\alpha = \frac{N_m}{N_I}
$$

##### Algorithme

La clé sélectionne les $N_m$ pixels qui coderont le message (vecteur $p$).

> En pratique, on peut mélanger (permuter) les pixels de l'image avec une *seed* qui constitue la clé secrète. On choisit alors les $N_m$ premiers pixels, on insère le message, et on effectue la permutation inverse.

Le message est substitué aux LSB des $N_m$ pixels sélectionnés : si on veut insérer un 0, les chiffres pairs restent pairs et les chiffres impairs deviennent pairs (inversement, pour insérer un 1 les chiffres impairs restent impairs).

##### Décodage

La connaissance de la clé permet de récupérer les $N_m$ pixels d'intérêt. Il suffit ensuite de lire les LSB sur ces pixels.

##### Détection

Dans le cas "facile" où $\alpha = 1$, 50% des pixels sont modifiés en moyenne (puisque certains restent les mêmes). Dans l'image stégo, il y a alors apparition de "marches" dans l'histogramme des valeurs (*e.g.* il y a la même proportion de 128 et 129, de 130 et 131, *etc.*).

De façon générale, pour d'autres valeurs de $\alpha$ on aura le même type de phénomène.

##### Variante un peu plus sûre : stéganographie $\pm 1$

Pour pallier au problème précédent, on peut associer $\pm 1$ lorsqu'on change la parité d'un nombre, avec une probabilité 0.5 pour chaque.

Sur le même principe, on peut faire une stéganographie JPEG en modifiant les coefficients DCT (utilisés pour la compression) plutôt que les pixels.

##### Stéganographie adaptive

Le défaut des méthodes précédentes est qu'elles sont détectables si des pixels sont modifiés dans des zones uniformes. La stéganographie adaptive privilégie l'insertion dans les textures de l'image.



### Stéganalyse

L'objectif est d'extraire des caractéristiques ou apprendre des classifieurs sensibles à l'insertion stéganographique.

On peut également extraire des caractéristiques ou apprendre des régresseurs sensibles au taux d'insertion. On parle alors de stéganalyse quantitative.

Remarques : 

- On peut générer des images de classe stégo "à volonté" à partir d'images *cover*.

- Il est facile de labelliser les images.

- On peut effectuer un apprentissage par "paires" (*cover*, stégo).



#### Exemple 1 : Caractéristiques pour la stéganalyse (SPAM)

En résumé, les caractéristiques sont les *bin* d'un histogramme multivarié (au lieu de considérer chaque pixel, on considère un certain nombre $n$ d'échantillons voisins).

Puisqu'on a un histogramme en dimension $n$, on a deux problèmes : 

- Malédiction de la dimension.
  
  - S'il y a des variations sur $m$ valeurs, il y a alors $m^n$ bins par caractéristique. Il faut donc veiller à ce que $m$ et $n$ soient faibles.

- L'information sur le signal stégo réside dans les variations fines de l'image.
  
  - Solution : calculer des dérivées premières pour capter les variations.

##### Algorithme

- Soit un $p$-uplet de $n+1$ pixels voisins $[p_1, \ldots, p_{n+1}]$.

- On calcule les "dérivées premières" ($d_1 = p_1 - p_2$, *etc.*). On peut le faire dans les huit directions de parcours.

- Pour diminuer $m$, on va "tronquer" les dérivées : 

$$
\begin{cases}
d_i \leftarrow T & \text{si } d_i \ge T \\
d_i \leftarrow -T & \text{si } d_i < T
\end{cases}
$$

- Les caractéristiques correspondent à un histogramme construit en observant $[d_1, \ldots, d_n]$ pour chaque pixel de l'image. On a $(2T+1)^n$ caractéristiques.

- On peut moyenner les histogrammes donnés par les différents parcours : gauche/droit et haut/bas vont ensemble, les directions diagonales forment un deuxième groupe, et on concatène (on sépare car les distances entre deux pixels sont différentes dans les deux cas). Au total, on a donc $2 \times (2T+1)^n$ caractéristiques.


