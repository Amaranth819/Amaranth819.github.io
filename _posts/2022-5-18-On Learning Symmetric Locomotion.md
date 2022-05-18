# On Learning Symmetric Locomotion

Paper link: [[link]](https://www.cs.ubc.ca/~van/papers/2019-MIG-symmetry/index.html)

## 1. Motivation

1. Exploiting the motion symmetry in DRL-based locomotion tasks can (1) learn more realistic locomotion patterns, (2) result in 2x faster learning speedup.





## 2. Contribution

Four methods of incorporating symmetry into the learning process:

1. **DUP**: duplicating tuples with their symmetric counterparts (the learning data)
2. **LOSS**: Adding a symmetry auxiliary loss (the learning loss)
3. **PHASE**: Motion phase mirroring (the learning data)
4. **NET**: Enforcing symmetry in the network itself (the policy structure)

where **DUP** and **NET** are new, **LOSS** and **PHASE** are present.





## 3. Symmetry

### 3.1 Background

**Definition**: Two trajectories are symmetry if for each state-action tuple $(s,a)$ from one trajectory, the corresponding state-action tuple from another trajectory is given by $(\mathcal{M}_s(s),\mathcal{M}_a(a))$, where $\mathcal{M}$ is a mirroring function.



**Goal**: find a symmetric policy $\pi_\theta$ following holds for all states $s \in \mathcal{S}$
$$
\pi_\theta (\mathcal{M}_s(s)) = \mathcal{M}_a(\pi_\theta(s))
$$


**Existing problems**

1. Encouraging or constraining the learned policies to be symmetric does not guarantee a symmetric gait, but instead may produce staggered poses.
2. It is possible but ineffective to directly specify gait symmetry in the reward function.



### 3.2 Duplicate Tuples (DUP)

**Idea**: Data augmentation

**Steps**:

1. Sample a trajectory $\tau = (s_1,a_1,r_1,...)$ from the environment.
2. Generate a mirrored trajectory $\tau'=(\mathcal{M}_s(s_1),\mathcal{M}_a(a_1),r_1,...)$ and add it to the rollout buffer for learning.

**Drawbacks**: 

1. The mirrored tuples are not strictly on-policy, so training by on-policy algorithms can be problematic.
2. (Not critical) At training time the policy is not guaranteed to be symmetric, therefore the probability of sampling action $\mathcal{M}_a(a_t)$ from $\pi_\theta(\mathcal{M}_s(s_t))$ could be low.



### 3.3 Auxiliary Loss (LOSS)

**Idea**: create a symmetry loss
$$
\begin{gather}
L_{sym}(\theta) = \sum^T_{i=1}||\pi_\theta(s_t) - \mathcal{M}_a(\pi_\theta(\mathcal{M}_s(s_t)))||^2 \\
\pi_\theta = \arg\min_\theta L_{PPO}(\theta) + \omega L_{sym}(\theta)
\end{gather}
$$
**Drawbacks**:

1. Although the symmetry loss improves the sample efficiency, it does not always work for training.



### 3.4 Phase-Based Mirroring (PHASE)

**Idea**: Introduce a phase variable $\phi \in [0,1)$. An alternative strategy for additional robustness is to perform a phase-reset at each foot strike. For example, set $\phi=0$ upon left-foot strike and $\phi=0.5$ upon right-foot strike.

**Formulation**: To enforce symmetry
$$
a_t = 
\left\{
    \begin{array}{lr}
        \pi_\theta(s_t) & 0 \leq \phi(s_t) < 0.5 \\
        \mathcal{M}_a(\pi_\theta(\mathcal{M}_s(s_t))) & 0.5 \leq \phi(s_t) < 1
    \end{array}
\right.
$$
**Drawbacks**:

1. In phase-reset, abrupt changes may exist at $\phi=0.5$ when the phase is strictly computed as a function of time.



### 3.5 Symmetric Network Architecture (NET)

**Idea**: Impose symmetry in network architecture in section 3.1



**Proof**:

Consider
$$
\begin{gather}
a = [a_l,a_r] \\
\mathcal{M}_a(a) = [a_r,a_l]
\end{gather}
$$
Define a symmetric policy consisting of a network $f$ as follows
$$
\pi_{side}(s) = [f(s,\mathcal{M}_s(s)),f(\mathcal{M}_s(s),s)]
$$
Then
$$
\begin{aligned}
\pi_{side}(\mathcal{M}_s(s)) 
&= \begin{bmatrix} f(\mathcal{M}_s(s),\mathcal{M}_s(\mathcal{M}_s(s))) \\ f(\mathcal{M}_s(\mathcal{M}_s(s)), \mathcal{M}_s(s)) \end{bmatrix} \\
&= \begin{bmatrix} f(\mathcal{M}_s(s),s) \\ f(s, \mathcal{M}_s(s)) \end{bmatrix} \\
&= \mathcal{M}_a \begin{bmatrix} f(s,\mathcal{M}_s(s)) \\ f( \mathcal{M}_s(s), s) \end{bmatrix} \\
&= \mathcal{M}_a(\pi_{side}(s))
\end{aligned}
$$


**Steps**:

1. Impose symmetry by $\pi_{side}(s)$ for left/right body parts, and define $\pi_{com}=h(s)+h(\mathcal{M}_s(s))$ for those body parts invariant to left/right mirroring like the torso and head.

2. Define the policy as
   $$
   \pi_\theta(s) = [\pi_{com}(s),\pi_{side}(s)]
   $$

3. 



**Drawbacks**:

1. Require knowledge about the state and action symmetry structures to define the network.
2. Highly sensitive to state and action normalization





## 4. Gait Symmetry Matrices

​	After training, it is important to evaluate how well the methods achieve gait symmetry.

(1) Robinson Symmetry Index (SI) [[Yu et al. 2018]](https://arxiv.org/abs/1801.08093)
$$
SI = \frac{2|X_R-X_L|}{X_L+X_R}\cdot 100
$$
where

- $X_R$: a scalar feature of interest, for example the duration of the stance phase for the right leg.
- $X_L$: the counterpart of the left leg.

(2) The phase-portrait [[Hsiao-Wecksler et al. 2010]](https://www.mdpi.com/2073-8994/2/2/1135)

Idea: A scatter plot drawn over a single cycle, where x and y-axes of the 2D plot correspond to the position and velocity respectively.

​	In this paper, the author proposes to use phase-portrait index (PPO) to numerically quantify the similarity between two phase-portraits.



## 5. Experiments

**Environment**: Walker2D, Walker3D, Stepper, Cassie on PyBullet

**Experiments**

1. Learning speed
2. Symmetry enforcement

