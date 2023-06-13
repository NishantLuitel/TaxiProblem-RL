from taxi_problem import Grid, TaxiProblem, Policy, ActionValue, Returns
import random
from copy import deepcopy
import pickle
# num_passengers = random.randint(2, 3)
num_passengers = 1
grid_size = 5
passengers = [(2, 4)]
destination = [(4, 1)]
num_episodes = 50000
discounting = 0.95


grid = Grid(grid_size, walls=[(3, 1, 3), (4, 1, 2), (2, 4, 1), (2, 3, 0),
                              (3, 1, 0), (3, 2, 1), (4, 1, 0), (4, 2, 1), (1, 0, 3), (2, 0, 2)])
# walls = grid.put_walls()
walls = [(3, 1, 3), (4, 1, 2), (2, 4, 1), (2, 3, 0),
         (3, 1, 0), (3, 2, 1), (4, 1, 0), (4, 2, 1), (1, 0, 3), (2, 0, 2)]

# policy = Policy()
# actionValue = ActionValue()
# returns = Returns()

with open('policy.pt', 'rb') as f:
    pd, avd, rd, passengers, destination, walls = pickle.load(f)

passengers = [(2, 4)]
destination = [(4, 1)]

policy = Policy(pd)
actionValue = ActionValue(avd)
returns = Returns(rd)

# # print(pd)

# for p in ([1]):
#     # returns.empty_return_dict()
#     # if p == 1:
#     #     num_episodes = 50000
#     if p == 40:
#         num_episodes = 1000
#     if p == 20:
#         num_episodes = 20000
#     if p == 10:
#         num_episodes = 200000
#     if p == 1:
#         num_episodes = 500000

#     for i in range(num_episodes):
#         #     # passengers = []
#         #     # destination = []
#         #     while (len(passengers) != num_passengers):
#         #         x = random.randint(0, grid_size-1)
#         #         y = random.randint(0, grid_size-1)

#         #         x_d = random.randint(0, grid_size-1)
#         #         y_d = random.randint(0, grid_size-1)

#         #         if (x, y) not in passengers and (x, y) != (x_d, y_d):
#         #             passengers.append((x, y))
#         #             destination.append((x_d, y_d))

#         # for i in range(num_episodes):
#         # taxi_p = (0, 0)
#         taxi_p = (random.randint(0, grid_size-1),
#                   random.randint(0, grid_size-1))
#         # passengers = [(1, 0), (0, 1)]
#         # destination = [(1, 1), (1, 2)]
#         TP = TaxiProblem(grid, taxi_p, passengers, destination)

#         # Exploring at the start

#         # rand = random.randint(0, len(TP.actions)-1)
#         # a = TP.actions[rand]
#         # r = TP.action(a)

#         while not TP.is_terminal():
#             a = policy.policy_to_action(TP.current_state, p)
#             r = TP.action(a)

#         # Episode until last return
#         episode = TP.episode[:-1]
#         G = 0
#         print("p:", p, ", ", len(episode))
#         for item in episode[::-1]:
#             if type(item) == str:
#                 a_t = item
#             elif (type(item) == TaxiProblem.State):
#                 s_t = item.return_tuple()

#                 # Update Returns(St , at)
#                 returns.update(s_t, a_t, G)
#                 # avg_return = sum(returns.returns_list(s_t, a_t)) / \
#                 #     len(returns.returns_list(s_t, a_t))

#                 avg_return = returns.return_avg(s_t, a_t)

#                 # Update Q(St , at) function
#                 actionValue.update_actionValue(s_t, a_t, avg_return)

#                 # Update policy
#                 values = []
#                 for acts in TP.actions:
#                     value = values.append(actionValue.value(s_t, acts))
#                 max_value = max(values)
#                 index_of_max = values.index(max_value)
#                 optimal_action = TP.actions[index_of_max]

#                 policy.update_policy(s_t, optimal_action)

#             else:
#                 G = discounting*G + item


# # print(len(TP.episode), TP.episode[-10:-1], policy.policy_dict)

# print(policy.policy_dict)
# with open('policy2.pt', 'wb') as f:
#     pickle.dump((policy.policy_dict, actionValue.actionValue_dict,
#                  returns.returns_dict, passengers, destination, walls), f)

# passengers = []
# destination = []

for i in range(10):
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


# for a in TP.episode[-10:]:
# print(a)

# print(TP.current_state, TP.episode[0], grid.walls)
# r = TP.action('U')
# print(r, TP.current_state.return_tuple())
# r = TP.action('R')
# print(r, TP.current_state.return_tuple())
# r = TP.action('P')
# print(r, TP.current_state.return_tuple())
# r = TP.action('U')
# print(r, TP.current_state.return_tuple())
# r = TP.action('P')
# print(r, TP.current_state.return_tuple())
# r = TP.action('R')
# print(r, TP.current_state.return_tuple())
# r = TP.action('Dr')
# print(r, TP.current_state.return_tuple())
# r = TP.action('D')
# print(r, TP.current_state.return_tuple())
# r = TP.action('D')
# print(r, TP.current_state.return_tuple())
# r = TP.action('P')
# print(r, TP.current_state.return_tuple())
# r = TP.action('Dr')
# print(r, TP.current_state.return_tuple())
# print(TP.is_terminal())
