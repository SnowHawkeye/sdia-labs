# SECURITE DE L'INFORMATION

## Notions de base

Un scénario de sécurité se définit par : 

- Les objectifs de l'adversaire.

- Les connaissances de l'adversaire.

- Les moyens de l'adversaire.

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
> 
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



#### Interprétation géométrique du tatouage

$\mathcal D(m,k)$ : région utilisée pour coder / décoder $m$, paramétrisée par $k$, dans laquelle se trouve $y$.

- Distortion : $|w|$

- Robustesse (*e.g.* ajout de bruit) : distance entre et $y$ et la frontière de  $\mathcal D(m,k)$

- Sécurité : capacité pour l'adversaire à estimer $\mathcal D(m,k)$

Si l'adversaire veut enlever le tatouage, il doit "faire sortir" $y$ de la région de codage / décodage.



### Exemple du tatouage par étalement de spectre

- $x_i, X_i \sim \mathcal N(0, \sigma^2_x)$ i.i.d de dimension $N_v$

- $m \in \{0,1\}$ 1 bit inséré 

- $k$  vecteur de dimension $N_v$, généré pseudo-aléatoireement en utilisant un germe <u>secret</u>. $k$ sera centré : $\mathbb E[k] = 0$ et $|k| = 1$.

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











