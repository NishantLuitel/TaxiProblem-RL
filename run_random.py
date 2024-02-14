from taxi_problem import Grid, TaxiProblem, Policy, ActionValue, Returns
import random
import pickle
import sys

# num_passengers = random.randint(2, 3)
num_passengers = 1
grid_size = 5
passengers = [(2, 4)]
destination = [(4, 1)]
num_episodes = 50000
discounting = 0.95

assert len(
    sys.argv) == 3, "Write command in form: python run_random.py ${model name} ${number of random experiments}"
with open(sys.argv[1], 'rb') as f:
    pd, avd, rd, passengers, destination, walls = pickle.load(f)

grid = Grid(grid_size, walls=walls)

passengers = [(2, 4)]
destination = [(4, 1)]

policy = Policy(pd)
actionValue = ActionValue(avd)
returns = Returns(rd)


for i in range(int(sys.argv[2])):
    while (len(passengers) != num_passengers):
        x = random.randint(0, grid_size-1)
        y = random.randint(0, grid_size-1)

        x_d = random.randint(0, grid_size-1)
        y_d = random.randint(0, grid_size-1)

        if (x, y) not in passengers and (x, y) != (x_d, y_d):
            passengers.append((x, y))
            destination.append((x_d, y_d))
    taxi_p = (random.randint(0, grid_size-1), random.randint(0, grid_size-1))
    TP = TaxiProblem(grid, taxi_p, passengers, destination)
    final_actions = []
    while not TP.is_terminal():
        a = policy.policy_to_action(TP.current_state, p=1)
        r = TP.action(a)
        final_actions.append(a)

    print('walls:', walls)
    print('taxi_p:', taxi_p)
    print('passengers:', passengers)
    print('destination:', destination)
    print(final_actions)
    print('----------------------------------')
