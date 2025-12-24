import numpy as np
import math

class Aunit:
    id = 0
    def __init__(self, x, y):
        Aunit.id += 1
        self.id = Aunit.id
        
        self.x = x
        self.y = y

        self.x_conns = {}
        self.y_conns = {}
    def display_connection_info(self):
        print("X conns: ", self.x_conns)
        print("Y conns: ", self.y_conns)
        

class SourceSet:
    id = 0
    def __init__(self, Aunits):
        SourceSet.id += 1
        self.id = SourceSet.id

        self.Aunits = Aunits


class Stimuli:
    def __init__(self, dims):
        self.dims = dims # means dims x dims {square stimuli}
        self.gen_stimuli()

    def clear_stimuli(self):
        self.image = np.zeros((self.dims, self.dims), dtype=int)

    def gen_stimuli(self, type="default"):
        start_stop = np.random.randint(self.dims, size=(1, 2))

        self.clear_stimuli()

        start = start_stop[0][0]
        stop = start_stop[0][1]
        if (start > stop): 
            temp = start
            start = stop
            stop = temp

        if (type == "default"):
            type = np.random.choice(["square", "line"])

        if (type == "square"):
            self.image[start:stop+1, start:stop+1] = 1
        if (type == "line"):
            self.image[start, start:stop+1] = 1

    def show_stimuli(self):
        print(self.image)

    def gen_and_show_stimuli(self, type="default"):
        self.gen_stimuli(type)
        print(self.image)

    def __add__(self, other):
        possible_connections = [(i,j) for i in range(self.dims) for j in range(self.dims)]
        random_connections = np.random.permutation(possible_connections)
        if isinstance(other, SourceSet):
            Aunits = other.Aunits
            x = Aunits[0].x
            y = Aunits[0].y

            n = len(Aunits)

            pos_x = 0
            pos_y = 0
            for Aunit in Aunits:
                for e in range(x):
                    if (pos_x == len(possible_connections)):
                        pos_x = 0
                    Aunit.x_conns[e] = random_connections[pos_x]
                    pos_x += 1
                for i in range(y):
                    if (pos_y == len(possible_connections)):
                        pos_y = 0
                    Aunit.y_conns[i] = random_connections[pos_y]
                    pos_y += 1






stimuli = Stimuli(3)

a1 = Aunit(3,2)
a2 = Aunit(3,2)
a3 = Aunit(3,2)
a4 = Aunit(3,2)

s1 = SourceSet([a1, a2])
s2 = SourceSet([a3, a4])

stimuli+s1
stimuli+s2

print("Source Set ID: ", s1.id)
for Aunit in s1.Aunits:
    print("A unit ID: ", Aunit.id)
    Aunit.display_connection_info()

print()

print("Source Set ID: ", s2.id)
for Aunit in s2.Aunits:
    print("A unit ID: ", Aunit.id)
    Aunit.display_connection_info()
