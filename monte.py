from taxi_problem import Grid, TaxiProblem, Policy, ActionValue, Returns
import random
import sys
import pickle
from tqdm import tqdm
# num_passengers = random.randint(2, 3)
num_passengers = 1
grid_size = 5
passengers = [(2, 4)]
destination = [(4, 1)]
discounting = 0.95


grid = Grid(grid_size, walls=[(3, 1, 3), (4, 1, 2), (2, 4, 1), (2, 3, 0),
                              (3, 1, 0), (3, 2, 1), (4, 1, 0), (4, 2, 1), (1, 0, 3), (2, 0, 2)])
# walls = grid.put_walls()
walls = [(3, 1, 3), (4, 1, 2), (2, 4, 1), (2, 3, 0),
         (3, 1, 0), (3, 2, 1), (4, 1, 0), (4, 2, 1), (1, 0, 3), (2, 0, 2)]


assert len(
    sys.argv) == 3, "Write command in form: python monte.py ${model name to save} ${num episodes to train}"


# with open('policy.pt', 'rb') as f:
#     pd, avd, rd, passengers, destination, walls = pickle.load(f)

passengers = [(2, 4)]
destination = [(4, 1)]

policy = Policy()
actionValue = ActionValue()
returns = Returns()

item = range(int(sys.argv[2]))

print("If initial iterations are slow, try rerunning few times")
pbar = tqdm(total=len(item), desc='Processing')
for i in item:

    taxi_p = (random.randint(0, grid_size-1),
              random.randint(0, grid_size-1))
    TP = TaxiProblem(grid, taxi_p, passengers, destination)

    # Exploring at the start

    rand = random.randint(0, len(TP.actions)-1)
    a = TP.actions[rand]
    r = TP.action(a)

    while not TP.is_terminal():
        a = policy.policy_to_action(TP.current_state)
        r = TP.action(a)

    # Episode until last return
    episode = TP.episode[:-1]
    G = 0
    # print("p:", p, ", ", len(episode))

    for item in episode[::-1]:
        if type(item) == str:
            a_t = item
        elif (type(item) == TaxiProblem.State):
            s_t = item.return_tuple()

            # Update Returns(St , at)
            returns.update(s_t, a_t, G)
            # avg_return = sum(returns.returns_list(s_t, a_t)) / \
            #     len(returns.returns_list(s_t, a_t))

            avg_return = returns.return_avg(s_t, a_t)

            # Update Q(St , at) function
            actionValue.update_actionValue(s_t, a_t, avg_return)

            # Update policy
            values = []
            for acts in TP.actions:
                value = values.append(actionValue.value(s_t, acts))
            max_value = max(values)
            index_of_max = values.index(max_value)
            optimal_action = TP.actions[index_of_max]

            policy.update_policy(s_t, optimal_action)

        else:
            G = discounting*G + item

    pbar.set_postfix(actions=len(episode)/3)  # Update the postfix
    pbar.update(1)
    # if i % 10 == 0:
    #     print("eposode:", i, ", actions:", len(episode)/3)


# print(len(TP.episode), TP.episode[-10:-1], policy.policy_dict)

print(policy.policy_dict)
with open(sys.argv[1], 'wb') as f:
    pickle.dump((policy.policy_dict, actionValue.actionValue_dict,
                 returns.returns_dict, passengers, destination, walls), f)

passengers = []
destination = []
