import tkinter as tk
from taxi_problem import Grid, TaxiProblem, Policy, ActionValue, Returns
import time
import pickle
import sys
num_passengers = 1
grid_size = 5


class TaxiEnvironment(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Taxi Problem")
        self.geometry("400x500")

        self.grid_size = grid_size
        self.cell_size = 80
        self.canvas = tk.Canvas(
            self, width=400, height=400, borderwidth=0, highlightthickness=0)
        self.canvas.pack()
        self.create_grid()
        self.position_set = False
        # Obstacles format: (x, y, direction)
        self.obstacles = walls
        self.create_obstacles()

        self.x_entry = tk.Entry(self)
        self.x_entry.pack()
        self.y_entry = tk.Entry(self)
        self.y_entry.pack()
        self.set_position_button = tk.Button(
            self, text="Set Initial Position", command=self.set_initial_position)
        self.set_position_button.pack()

    def create_grid(self):
        for i in range(self.grid_size):
            self.canvas.create_line(0, i*self.cell_size, 400, i*self.cell_size)
            self.canvas.create_line(i*self.cell_size, 0, i*self.cell_size, 400)

    def create_objects(self, passenger_position, destination_position):
        for p in passenger_position:
            if self.TP.current_state.current_passenger == -1:
                self.passenger = self.canvas.create_text((p[0]+0.8)*self.cell_size,
                                                         (p[1] + 0.8) *
                                                         self.cell_size,
                                                         text="P", font=("Helvetica", 10))

        for d in destination_position:
            self.destination = self.canvas.create_text((d[0]+0.8)*self.cell_size,
                                                       (d[1] +
                                                        0.8)*self.cell_size,
                                                       text="D", font=("Helvetica", 10))

    def create_obstacles(self):
        for obstacle in self.obstacles:
            x, y, direction = obstacle
            if direction == 0:
                self.canvas.create_rectangle(x*self.cell_size, (y+1)*self.cell_size-5,
                                             (x+1)*self.cell_size, (y+1)*self.cell_size, fill="black")

            elif direction == 1:
                self.canvas.create_rectangle(x*self.cell_size, y*self.cell_size,
                                             (x+1)*self.cell_size, y*self.cell_size+5, fill="black")

            elif direction == 2:
                self.canvas.create_rectangle(x*self.cell_size, y*self.cell_size,
                                             x*self.cell_size+5, (y+1)*self.cell_size, fill="black")
            elif direction == 3:
                self.canvas.create_rectangle((x+1)*self.cell_size-5, y*self.cell_size,
                                             (x+1)*self.cell_size, (y+1)*self.cell_size, fill="black")

    def set_initial_position(self):
        if not self.position_set:
            # self.bind("<Button-1>", self.on_click)
            self.position_set = True
        self.on_click()

    def on_click(self):
        x = int(self.x_entry.get())
        y = int(self.y_entry.get())

        self.TP = TaxiProblem(grid, (x, y), passengers, destination)
        self.canvas.delete('all')
        self.create_grid()
        self.create_obstacles()
        self.create_objects(self.TP.current_state.passenger_p,
                            self.TP.current_state.destination)
        self.taxi = self.canvas.create_rectangle(x*self.cell_size + (self.cell_size/2-10), y*self.cell_size+(self.cell_size/2-10),
                                                 (x)*self.cell_size+(self.cell_size/2+10), (y)*self.cell_size+(self.cell_size/2+10), fill="yellow")
        self.taxi_label = self.canvas.create_text(x*self.cell_size + (self.cell_size/2),
                                                  y*self.cell_size +
                                                  (self.cell_size/2),
                                                  text="T", font=("Helvetica", 10))
        self.after(100, self.run)

    def update_position(self):
        x = self.TP.current_state.taxi_p[0]
        y = self.TP.current_state.taxi_p[1]
        self.create_grid()
        self.create_obstacles()
        self.create_objects(self.TP.current_state.passenger_p,
                            self.TP.current_state.destination)
        self.taxi = self.canvas.create_rectangle(x*self.cell_size + (self.cell_size/2-10), y*self.cell_size+(self.cell_size/2-10),
                                                 (x)*self.cell_size+(self.cell_size/2+10), (y)*self.cell_size+(self.cell_size/2+10), fill="yellow")
        self.taxi_label = self.canvas.create_text(x*self.cell_size + (self.cell_size/2),
                                                  y*self.cell_size +
                                                  (self.cell_size/2),
                                                  text="T", font=("Helvetica", 10))
        self.update()

    def run(self):
        # Create a list of actions
        while not self.TP.is_terminal():
            self.update_position()
            self.canvas.delete('all')
            time.sleep(1)
            a = policy.policy_to_action(self.TP.current_state, p=1)
            self.TP.action(a)
        self.update_position()


if __name__ == "__main__":

    assert len(sys.argv) == 2, "Provide the model to be loaded"
    with open(sys.argv[1], 'rb') as f:
        pd, avd, rd, passengers, destination, walls = pickle.load(f)
    grid = Grid(grid_size, walls=walls)

    policy = Policy(pd)
    actionValue = ActionValue(avd)
    returns = Returns(rd)

    app = TaxiEnvironment()
    app.mainloop()
