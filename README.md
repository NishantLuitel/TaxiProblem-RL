# TaxiProblem-RL
Here, I have trained an agent to solve taxi problem in Reinforcement Learning using Every Visit, Off-policy Monte Carlo Method

# Files
--`taxi_problem.py`: This file contains implementation of data structures and classes used for this problem.
--`monte.py`: This file contains the learning algorithm used. Run this file to run the algorithm.
--`run_random.py`: This file contains code to run the taxi problem with random position of taxi.
--`gui.py`: This file runs a GUI to visualize how the learned policy is performing. You can set the location of taxi from the interface.

The policy files present are the learned policy from the algorithms from my experiments. You can use those or train you own policy as explained next.


# How to Run?

## Run monte.py to learn about policy
The command line code should be of the following format: `python monte.py {filename to save the policy} {number of episodes}`.
Following is the code to run 500 episodes and save the model in policy4.pt file.
```{python}
python run monte.py policy4.pt 500
```
## Run run_random.py to test the policy in random experiments
The command line code should be of the following format: `python monte.py {filename of policy} {number of random experiments}`.
The code is to run 12 experiments and save the model in policy4.pt file is:
```{python}
python run run_random.py policy4.pt 12
```

## Run gui.py 
The command line code should be of the following format: `python monte.py {filename to save the model}`. Enter the input the x and y 
coordinates of the taxi for given two fields. The coordinate system used has its origin at the left top box.
The code is to run gui to test the policy4 is:
```{python}
python run gui.py policy4.pt 
```


# Reference

Sutton, R. S., & Barto, A. G. (2018). Reinforcement learning: An introduction. Cambridge (Mass.): The MIT Press. Taken from the Stanford Archives.




# References
