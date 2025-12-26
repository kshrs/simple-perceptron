import numpy as np
import matplotlib.pyplot as plt
import math
import time

class Aunit:
    id = 0
    def __init__(self, x, y):
        Aunit.id += 1
        self.id = Aunit.id
        
        self.x = x
        self.y = y

        self.x_conns = {}
        self.y_conns = {}

        self.status = 0
        self.value = 1 + (np.random.random() * 0.02)

        self.e = 0
        self.i = 0


    def display_connection_info(self):
        print("X conns: ", self.x_conns)
        print("Y conns: ", self.y_conns)

    def compute(self, image, threshold):
        for pos in self.x_conns.values():
            if image[pos[0]][pos[1]] == 1:
                self.e += 1
        for pos in self.y_conns.values():
            if image[pos[0]][pos[1]] == 1:
                self.i += 1
        
        if ((self.e - self.i) >= threshold):
            self.status = 1

        self.e = 0
        self.i = 0


class SourceSet:
    id = 0
    def __init__(self, Aunits):
        SourceSet.id += 1
        self.id = SourceSet.id

        self.Aunits = Aunits

        self.type = "default"

class Stimuli:
    def __init__(self, dims):
        self.dims = dims # means dims x dims {square stimuli}
        self.gen_stimuli()

    def clear_stimuli(self):
        self.image = np.zeros((self.dims, self.dims), dtype=int)

    def gen_stimuli(self, type="default"):
        start = np.random.randint(self.dims)

        self.clear_stimuli()


        if (type == "default"):
            type = np.random.choice(["vline", "hline"])


        if (type == "vline"):
            self.image[0:self.dims, start] = 1
        if (type == "hline"):
            self.image[start, 0:self.dims] = 1

        if (type == "vline-nf"):
            self.image[start:self.dims, start] = 1
        if (type == "hline-nf"):
            self.image[start, start:self.dims] = 1

    def show_stimuli(self):
        print(self.image)

    def gen_and_show_stimuli(self, type="default"):
        self.gen_stimuli(type)
        print(self.image)

    def __add__(self, other):
        possible_connections = [(i,j) for i in range(self.dims) for j in range(self.dims)]
        if isinstance(other, SourceSet):
            Aunits = other.Aunits
            x = Aunits[0].x
            y = Aunits[0].y

            n = len(Aunits)

            pos_x = 0
            pos_y = 0

            if (other.type == "hline") or (other.type == "hline-nf"):
                for Aunit in Aunits:
                    for e in range(x):
                        if (pos_x >= len(possible_connections)):
                            pos_x = 0
                        Aunit.x_conns[e] = possible_connections[pos_x]
                        pos_x += 1
                    step = 0

                    for i in range(y):
                        if (pos_y >= len(possible_connections)):
                            step += 1
                            pos_y = 0 + step
                        Aunit.y_conns[i] = possible_connections[pos_y]
                        pos_y += self.dims
            else:
                # vline
                for Aunit in Aunits:
                    step = 0
                    for e in range(x):
                        if (pos_x >= len(possible_connections)):
                            step += 1
                            pos_x = 0 + step
                        Aunit.x_conns[e] = possible_connections[pos_x]
                        pos_x += self.dims

                    for i in range(y):
                        if (pos_y >= len(possible_connections)):
                            pos_y = 0
                        Aunit.y_conns[i] = possible_connections[pos_y]
                        pos_y += 1


    def create_training_set(self, n):
        x_data = []
        y_data = []
        for i in range(math.floor(n/2)):
            val = 1 
            self.gen_stimuli("vline-nf")
            x_data.append(self.image.copy())
            y_data.append(val)
        for i in range(math.floor(n/2), n):
            val = 2 
            self.gen_stimuli("hline-nf")
            x_data.append(self.image.copy())
            y_data.append(val)
        tup = list(zip(x_data, y_data))
        np.random.shuffle(tup)

        x_data, y_data = zip(*tup)
        return (x_data, y_data)


class Response:
    id = 0
    def __init__(self, sourceset):
        Response.id += 1
        self.id = Response.id

        self.status = 0
        self.SourceSet = sourceset

        self.sum = 0


    def compute_sum(self):
        for Aunit in self.SourceSet.Aunits:
            self.sum += Aunit.value * Aunit.status
    def compute_mean(self):
        count = 0
        for Aunit in self.SourceSet.Aunits:
            if Aunit.status == 1:
                count += 1
                self.sum += Aunit.value

        if count > 0:
            self.sum = self.sum / count
            count = 0

class Perceptron:
    def __init__(self):
        print("The Old Perceptron is back")

        self.Aunits = []
        self.SourceSets = []
        self.ResponseUnits = []
        self.Stimuli = 0

        self.threshold = 0

        self.response_result = 0


    def show_info_of_response(self, response_id):
        for ResponseUnit in self.ResponseUnits:
            if (response_id == ResponseUnit.id):
                print("Source Set ID: ", end="")
                print(ResponseUnit.SourceSet.id)

                print("Active A units: ", [(Aunit.id,Aunit.value) if Aunit.status == 1 else None for Aunit in ResponseUnit.SourceSet.Aunits])
                return


    def refresh(self):
        for ResponseUnit in self.ResponseUnits:
            ResponseUnit.status = 0
            ResponseUnit.sum = 0
            for Aunit in ResponseUnit.SourceSet.Aunits:
                Aunit.status = 0
        self.response_result = 0

    def plot(self, ax=None):
        if ax is None:
            plt.imshow(self.Stimuli.image, cmap="Greys")
            title = "Response " + str(self.response_result) + " | " + ("Vertical" if self.response_result == 1 else "Horizontal")
            print(title)
            plt.title(title)
            plt.show()
        else:
            ax.imshow(self.Stimuli.image, cmap="Greys")
            title = "Response " + str(self.response_result) + " | " + ("Vertical" if self.response_result == 1 else "Horizontal")
            print(title)
            ax.set_title(title)
            

    def compute(self, image=None):
        if image is None:
            image = self.Stimuli.image
        else:
            self.Stimuli.image = image
        response_sum_pair = {}
        for Aunit in self.Aunits:
            Aunit.compute(image, self.threshold)
        for ResponseUnit in self.ResponseUnits:
            ResponseUnit.compute_mean()
            response_sum_pair[ResponseUnit.id] = ResponseUnit.sum

        result_id = max(response_sum_pair, key = response_sum_pair.get)
        print(max(response_sum_pair, key = response_sum_pair.get))
        self.response_result = result_id
        max_value = response_sum_pair[result_id]
        print(response_sum_pair)

        self.show_info_of_response(result_id)
        print(f"Response: {result_id} Value: {max_value}")
        pretty_result = "Response " + str(self.response_result) + " | " + ("Vertical" if self.response_result == 1 else "Horizontal")
        print(pretty_result)
        print("------------------------")
        print()

    def reinforce(self, id):
        if id == self.response_result:
            print("Correct Response")
            # if correct response
            # # Reward the active A units in the source set and 
            for ResponseUnit in self.ResponseUnits:
                if self.response_result == ResponseUnit.id:
                    for Aunit in ResponseUnit.SourceSet.Aunits:
                        if Aunit.status == 1:
                            Aunit.value += 1
                else:
                    for Aunit in ResponseUnit.SourceSet.Aunits:
                        if Aunit.status == 1:
                            Aunit.value -= 1
        else:
            print("Wrong Response")
            for ResponseUnit in self.ResponseUnits:
                if self.response_result == ResponseUnit.id:
                    for Aunit in ResponseUnit.SourceSet.Aunits:
                        if Aunit.status == 1:
                            Aunit.value -= 1
                else:
                    for Aunit in ResponseUnit.SourceSet.Aunits:
                        if Aunit.status == 1:
                            Aunit.value += 1
    def forget_weights(self):
        for Aunit in self.Aunits:
            Aunit.value = 0

