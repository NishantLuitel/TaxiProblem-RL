# This is the implementation of Taxi problem in Reinforcement Learning using,
# Every Visit, on-policy, Monte-Carlo method
import random
from copy import deepcopy


class Grid:
    def __init__(self, size: int = 5, walls: list = []):
        self.size = size
        self.walls = walls

    def check_if_bounded(self, p: tuple):
        # Checks if the position of taxi is within the grid

        if (p[0] >= 0 and p[0] <= self.size-1) and (p[1] >= 0 and p[1] <= self.size-1):
            check = True
        else:
            check = False
        return check

    def put_walls(self, wall_prob: float = 0.2):
        # wall locations is a list consisting of 3 order tuples
        # The first two coordinates give the location of wall and third coordinate gives the direction of wall
        i = 0
        while (len(self.walls) != 2*int(wall_prob*self.size*self.size)):
            # print(i)
            # i += 1
            # up(0) or down(1) or left(2) or right(3)
            wall_direction = random.randint(0, 3)
            location_x = random.randint(0, self.size-1)
            location_y = random.randint(0, self.size-1)
            if (location_x == 0 and wall_direction == 2) or (location_x == self.size-1 and wall_direction == 3):
                continue
            if (location_y == 0 and wall_direction == 1) or (location_y == self.size-1 and wall_direction == 0):
                continue
            self.walls.append((location_x, location_y, wall_direction))

            # append symmetric walls to the list
            # for example if the right of a cell:(x,y) is walled then so is the left of the cell:(x+1,y)
            if wall_direction == 2:
                self.walls.append((location_x-1, location_y, 3))
            if wall_direction == 3:
                self.walls.append((location_x+1, location_y, 2))
            if wall_direction == 0:
                self.walls.append((location_x, location_y+1, 1))
            if wall_direction == 1:
                self.walls.append((location_x, location_y-1, 0))

        return self.walls


class TaxiProblem:

    # The possible action that taxi can take is move left,right,up,down or
    #  pick and drop the passenger
    actions = ['L', 'R', 'U', 'D', 'P', 'Dr']

    class State:
        def __init__(self, taxi_p, passenger_p, destination, current_passenger=-1):

            assert len(destination) == len(
                passenger_p), "Every passenger should have a destination\
                and vice-versa"

            self.taxi_p = taxi_p
            self.passenger_p = passenger_p
            self.destination = destination
            self.current_passenger = current_passenger
            # self.walls = walls

        def return_tuple(self):
            # return state as a tuple of positions
            return (self.taxi_p, self.passenger_p, self.destination, self.current_passenger)

        def __str__(self):
            assert len(self.destination) == len(
                self.passenger_p), "Every passenger should have a destination\
                and vice-versa"

            return f'{self.taxi_p, self.passenger_p, self.destination,self.current_passenger}'

    def __init__(self, grid: Grid, taxi_p: tuple, passengers_p: list,
                 destination: list):

        self.grid = grid

        # Check if passenger, taxi and destination locations are within the grid
        if self.check_taxi_position(taxi_p):
            if self.check_passenger_position(passengers_p) and self.check_passenger_position(destination):

                self.current_state = self.State(taxi_p,
                                                passengers_p, destination)

        self.episode = [deepcopy(self.current_state)]
        self.policy_dict = {}

    def get_actions(self, s: State):
        taxi_p, passengers, destination, current_passenger = s.return_tuple()

        # a = ['L', 'R', 'U', 'D']
        # if taxi_p in passengers:
        #     a += ['P']
        # if current_passenger != -1 and taxi_p == destination[current_passenger]:
        #     a += ['Dr']
        # return a

        return self.actions

    def action(self, a: str):

        s = self.current_state
        taxi_p, passengers, destination, current_passenger = s.return_tuple()
        walls = self.grid.walls

        possible_actions = self.get_actions(s)

        assert a in possible_actions, "action not possible in current state"

        self.episode.append(a)
        reward = 0
        if a in ['L', 'R', 'U', 'D'] and self.check_if_action_hits_wall_or_boundry(taxi_p, a, walls):
            self.current_state = deepcopy(self.current_state)
            reward = -10

        if a in ['L', 'R', 'U', 'D'] and not self.check_if_action_hits_wall_or_boundry(taxi_p, a, walls):
            reward = -4

            if a == 'L':
                p = (taxi_p[0]-1, taxi_p[1])
            if a == 'R':
                p = (taxi_p[0]+1, taxi_p[1])
            if a == 'D':
                p = (taxi_p[0], taxi_p[1]-1)
            if a == 'U':
                p = (taxi_p[0], taxi_p[1]+1)
            self.current_state = self.State(
                p, passengers, destination, current_passenger)

        if a in ['P'] and taxi_p not in passengers:
            self.current_state = deepcopy(self.current_state)
            reward = -10

        if a in ['P'] and taxi_p in passengers:
            passenger_id = passengers.index(taxi_p)
            self.current_state = self.State(
                taxi_p, passengers, destination, passenger_id)
            reward = -10

        if a in ['Dr'] and (current_passenger == -1):
            reward = -10
            self.current_state = deepcopy(self.current_state)

        if a in ['Dr'] and (current_passenger != -1) and taxi_p != destination[current_passenger]:
            reward = -10
            self.current_state = deepcopy(self.current_state)

            # passengers_ = passengers[:current_passenger] + \
            #     passengers[current_passenger+1:]
            # destination_ = destination[:current_passenger] + \
            #     destination[current_passenger+1:]
            # self.current_state = self.State(
            #     taxi_p, passengers_, destination_, -1)

        if a in ['Dr'] and current_passenger != -1 and taxi_p == destination[current_passenger]:
            reward = 25
            passengers_ = passengers[:current_passenger] + \
                passengers[current_passenger+1:]
            destination_ = destination[:current_passenger] + \
                destination[current_passenger+1:]
            self.current_state = self.State(
                taxi_p, passengers_, destination_, -1)

        self.episode.append(reward)
        self.episode.append(deepcopy(self.current_state))

        return reward

    def is_terminal(self):
        # Returns True if in terminal state
        s = self.current_state
        taxi_p, passengers, destination, current_passenger = s.return_tuple()

        if len(passengers) == 0:
            return True
        return False

    def check_if_action_hits_wall_or_boundry(self, taxi_p: tuple, a: str, walls: list):
        action_to_direction = {
            'L': 2,
            'R': 3,
            'U': 0,
            'D': 1
        }
        if a == 'L':
            p = (taxi_p[0]-1, taxi_p[1])
        if a == 'R':
            p = (taxi_p[0]+1, taxi_p[1])
        if a == 'D':
            p = (taxi_p[0], taxi_p[1]-1)
        if a == 'U':
            p = (taxi_p[0], taxi_p[1]+1)
        if (taxi_p[0], taxi_p[1], action_to_direction[a]) in walls or not self.check_taxi_position(p):
            # print("Entered")
            return True
        return False

    def check_taxi_position(self, p: tuple):
        assert len(p) == 2, "Two coordinates required"

        return self.grid.check_if_bounded(p)

    def check_passenger_position(self, passengers_p: tuple):
        '''
        Check for every passengers if they lie within the grid
        '''

        for p_p in passengers_p:
            assert len(p_p) == 2, "Two coordinates required"
            check = self.grid.check_if_bounded(p_p)
            if not check:
                return False
        return True


class Policy:
    def __init__(self, policy_dict: dict = {}):
        self.policy_dict = policy_dict

    def policy_to_action(self, s: TaxiProblem.State, p=20):
        # Returns which action to perform while on a given state
        if str(s) not in self.policy_dict.keys():
            rand = random.randint(0, len(TaxiProblem.actions)-1)
            self.policy_dict[str(s)] = TaxiProblem.actions[rand]
            # return TaxiProblem.actions[rand]

        # print(self.policy_dict)
        p_d = random.randint(0, 99)
        if p_d <= p-1:
            rand = random.randint(0, len(TaxiProblem.actions)-1)
            return TaxiProblem.actions[rand]
        else:
            return self.policy_dict[str(s)]

    def update_policy(self, s: TaxiProblem.State, a: str):
        # Change the dictionary value to 'a' for given state
        self.policy_to_action(str(s))
        self.policy_dict[str(s)] = a


class ActionValue:
    def __init__(self, actionValue_dict: dict = {}):
        self.actionValue_dict = actionValue_dict

    def value(self, s: TaxiProblem.State, a: str):
        # Returns which action to perform while on a given state
        if (str(s), a) not in self.actionValue_dict:
            rand_reward = random.randint(-0, 1)
            self.actionValue_dict[(str(s), a)] = rand_reward

        return self.actionValue_dict[(str(s), a)]

    def update_actionValue(self, s: TaxiProblem.State, a: str, avg: float):
        # Change the dictionary value to 'a' for given state

        v = self.value(str(s), a)
        self.actionValue_dict[(str(s), a)] = avg


class Returns:
    def __init__(self, returns_dict: dict = {}):
        self.returns_dict = returns_dict

    def returns_list(self, s: TaxiProblem.State, a: str):
        # Returns which action to perform while on a given state
        if (str(s), a) not in self.returns_dict:
            self.returns_dict[(str(s), a)] = [0, 0]

        return self.returns_dict[(str(s), a)]

    def update(self, s: TaxiProblem.State, a: str, ret: float):
        # Change the dictionary value to 'a' for given state
        self.returns_list(str(s), a)
        self.returns_dict[(str(s), a)][0] += ret
        self.returns_dict[(str(s), a)][1] += 1

    def empty_return_dict(self):
        self.returns_dict = {}

    def return_avg(self, s: TaxiProblem.State, a: str):
        self.returns_list(str(s), a)
        if self.returns_dict[(str(s), a)] == [0, 0]:
            return 0
        else:
            return self.returns_dict[(str(s), a)][0]/self.returns_dict[(str(s), a)][1]

    #  [(3, 4, 2), (2, 4, 3), (2, 1, 2), (1, 1, 3), (3, 4, 2), (2, 4, 3), (2, 1, 3), (3, 1, 2), (3, 2, 0), (3, 3, 1)]
