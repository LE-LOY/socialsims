import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def visualize(runs=10):
    for run in range(1, runs + 1):
        data = [[], [], [], []]
        time = []
        
        print('data/dist/' + str(run) + 'run.txt')
        with open('data/dist/' + str(run) + 'run.txt') as f:
            print(f.readlines())
            for line in f.readlines():
                a, b, c, d = map(int, line.split())
                time.append(len(time) + 1)
                data[0].append(a)
                data[1].append(b)
                data[2].append(c)
                data[3].append(d)
        
        print(time)

if __name__ == '__main__':
    visualize()