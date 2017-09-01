import numpy as np
import matplotlib.pyplot as plt

num_data_files = 1

data = [[0 for _ in range(11)] for _ in range(11)]
for i in range(1, num_data_files + 1):
    with open("data" + str(i) + ".txt") as f:
        temp = f.readlines()
        for line in temp:
            alpha, gamma, *fed = map(int, line.split())
            data[alpha][gamma] += fed[2] / num_data_files

print(data)

plt.imshow(data, extent=[-0.5, 10.5,-0.5,10.5], origin='lower', 
           interpolation='nearest', cmap='Blues') #BrBG
           
plt.title("QLearning Parameters vs. Fed")
plt.xlabel("Discount Rate")
plt.ylabel("Learning Rate")

plt.colorbar()
plt.tight_layout()
plt.show()