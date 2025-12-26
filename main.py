import numpy as np
import matplotlib.pyplot as plt
import math
import time
from perceptron import Perceptron, Stimuli, Aunit, SourceSet, Response



### Setup of the connections and variables


# Stimuli of 5x5 grid
stimuli = Stimuli(5)

# Aunit setup.
# Array of 50 with x = 5 and y = 1
aunits = [Aunit(5, 1) for i in range(50)]


## Two source set as it is a binary classifier
# Use vline, hline for full length and vline-nf,hline-nf for irregular length
s1 = SourceSet(aunits[:25])
s1.type = "vline"
s2 = SourceSet(aunits[25:])
s2.type = "hline"


# Connect each Aunit to appropriate stimuli cell
### Modified the code base purely for line separator.
stimuli+s1
stimuli+s2


# Connection of source set to the appropriate response
r1 = Response(s1)
r2 = Response(s2)


# Init of perceptron and set up of instances 
perceptron = Perceptron()
perceptron.Aunits = aunits
perceptron.SourceSets = [s1, s2]
perceptron.ResponseUnits = [r1, r2]
perceptron.Stimuli = stimuli
# threshold to fire a Aunit
perceptron.threshold = 2


# stimuli.show_stimuli()
# perceptron.compute(default=self.Stimuli.image)
# perceptron.refresh()
# perceptron.plot(default=ax)
# perceptron.forget_weights()


# Creation of training sets
x_train, y_train = stimuli.create_training_set(100)
x_test, y_test = stimuli.create_training_set(16)



# This is how training occurs
for i in range(len(x_train)):
    perceptron.compute(x_train[i])
    perceptron.reinforce(y_train[i])
    perceptron.refresh()


correct = 0
wrong = 0
total = len(x_test)

# Testing phase and plot the results
### Modify the appropirate subplots values to display the result of array n
fig, ax = plt.subplots(4, 4)
ax_flat = ax.flat
for i in range(len(x_test)):
    perceptron.compute(x_test[i])
    ax = next(ax_flat)
    if perceptron.response_result == y_test[i]:
        correct += 1
    else:
        wrong += 1
    perceptron.plot(ax)
    perceptron.refresh()
plt.title(f"Accuracy: {correct/total}")
plt.show()


## This is the test phase code. pure test to plots
# for i in range(len(x_test)):
#     print(x_test[i])
#     perceptron.compute(x_test[i])
#     if perceptron.response_result == y_test[i]:
#         correct += 1
#     else:
#         wrong += 1
#     perceptron.refresh()


## Display of results
print("Total: ", len(x_test))
print("Correct: ", correct)
print("Wrong: ", wrong)
print("Correct / Total: ", correct/total)


### Stress test and analysis code. (Use only for testing)
#
# accuracy = []
# n_values = []
#
# n = 1
# while (n <= 1000):
#     perceptron.forget_weights()
#     x_train, y_train = stimuli.create_training_set(n*2)
#     x_test, y_test = stimuli.create_training_set(100)
#
#
#     for i in range(len(x_train)):
#         perceptron.compute(x_train[i])
#         perceptron.reinforce(y_train[i])
#         perceptron.refresh()
#
#     correct = 0
#     wrong = 0
#     total = len(x_test)
#     for i in range(len(x_test)):
#         print(x_test[i])
#         perceptron.compute(x_test[i])
#         if perceptron.response_result == y_test[i]:
#             correct += 1
#         else:
#             wrong += 1
#         perceptron.refresh()
#
#
#     n_values.append(n)
#     accuracy.append(correct/total)
#
#     if n<100:
#         n+=10
#     else:
#         n+=100
#
# plt.plot(n_values, accuracy, color="blue")
# plt.xlabel("Number of samples per stimuli")
# plt.ylabel("Accuracy (per 100 samples tested)")
# plt.title("HLine Vs VLine Separator (irregular length)")
# plt.show()
#


### Info of the Perceptron
# print(perceptron.Aunits)
# print(perceptron.SourceSets)
# print(perceptron.ResponseUnits)
# print(perceptron.response_result)
# print(perceptron.Stimuli)
# print(perceptron.threshold)
