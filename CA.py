from copy import copy


class TimePortal(object):
    def __init__(t_enter, t_exit, x1, x2, w):
        self.t_enter


class CA:
    def __init__(self):
        
        
        rule_30 = [0, 0, 0, 1, 1, 1, 1, 0]  # An initial rule system
        rule_110 = [0,1,1,0,1,1,1,0]
        self.rules = rule_110  # List that stores the ruleset, i.e. 0,1,1,0,1,1,0,1
        self.scl = 5  # How many pixels wide/high is each cell?
        self.num_cells = int(width / self.scl)
        self.num_gens = int(height / self.scl)
        self.active_generations = [0]
        
        self.universe = []
        self.restart()  # Sets generations to [0], only middle cell to 1

        # time portal
        self.t_enter = 80
        self.t_exit = 40
        self.x_enter = self.num_cells / 2 + 5
        self.x_exit = self.num_cells / 2 + 5
        self.w = 32
        self.history = set()  # store what's gone through portal
        self.trips = 0

    # Set the rules of the CA
    def setRules(self, r):
        self.rules = r

    # Make a random ruleset
    def randomize(self):
        
        # TODO only use Class 4 roles
        for i in range(8):
            self.rules[i] = int(random(2))

    # Reset to generation 0
    def restart(self):
        self.universe = []
        for _ in range(self.num_gens):
            self.universe.append([0] * self.num_cells)
        self.active_generations = [0]
        
        # We arbitrarily start with just the middle cell having a state of "1"
        self.universe[0][self.num_cells -40 ] = 1
        
    def generate(self):
        
        self.active_generations = [t for t in self.active_generations if t < self.num_gens -1]
        
        for i in range(len(self.active_generations)):
            # ASSUMPTION: two active generations are never right next to each other
            t = self.active_generations[i]
            self.generate_row(t)
            self.active_generations[i] += 1

    # The process of creating the new generation
    def generate_row(self, t):
        # First we create an empty array for the new values
        nextgen = [0] * self.num_cells
        # For every spot, determine new state by examing current state,
        # and neighbor states
        # Ignore edges that only have one neighor
        for i in range(1, self.num_cells - 1):
            left = self.universe[t][i - 1]  # Left neighbor state
            me = self.universe[t][i]  # Current state
            right = self.universe[t][i + 1]  # Right neighbor state
            # Compute next generation state based on ruleset
            nextgen[i] = self.executeRules(left, me, right)

        # Copy the array into universe
        self.universe[t+1] = copy(nextgen)

        # did we enter the portal?
        if t == self.t_enter:
            # reset time
            self.active_generations.append(self.t_exit)

            # copy the portal back
            portal = copy(self.universe[t+1][self.x_enter : self.x_enter + self.w])
            self.universe[self.t_exit][self.x_exit : self.x_exit + self.w] = portal
            
            # save
            self.trips += 1
            t_portal = tuple(portal)
            if t_portal in self.history:
                print("time loop!")
            self.history.add(tuple(portal))
            print("trips: {} history: {}".format(self.trips, len(self.history)))

    # This is the easy part, just draw the cells,
    # fill 255 for '1', fill 0 for'0'
    def render(self):
        # for t in range(self.num_gens):
        for t in self.active_generations:
            self.render_row(t)
            
        # draw exit portal
        fill(255, 0, 0)
        scl = self.scl
        rect(self.x_exit * scl, self.t_exit * scl, self.w * scl, scl/5)
        
        # draw enter portal
        fill(0, 255, 0)
        rect(self.x_enter * scl, (self.t_enter + 1) * scl, self.w * scl, scl/5)
    
    def render_row(self, t):
        scl = self.scl
        for i in range(self.num_cells):
            if self.universe[t][i] == 1:
                fill(255)
            else:
                fill(0)

            noStroke()
            rect(i * scl, t * scl, scl, scl)


    # Implementing the Wolfram rules
    # Could be improved and made more concise, but here we can
    # explicitly see what is going on for each case
    def executeRules(self, a, b, c):
        if a == 1 and b == 1 and c == 1:
            return self.rules[0]
        if a == 1 and b == 1 and c == 0:
            return self.rules[1]
        if a == 1 and b == 0 and c == 1:
            return self.rules[2]
        if a == 1 and b == 0 and c == 0:
            return self.rules[3]
        if a == 0 and b == 1 and c == 1:
            return self.rules[4]
        if a == 0 and b == 1 and c == 0:
            return self.rules[5]
        if a == 0 and b == 0 and c == 1:
            return self.rules[6]
        if a == 0 and b == 0 and c == 0:
            return self.rules[7]
        return 0

    # The CA is done if it reaches the bottom of the screen
    def finished(self):
        return False
        # if (self.num_gens - 1) in self.active_generations:
        #     return True
        # else:
        #     return False
