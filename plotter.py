import matplotlib.pyplot as plt
import numpy as np
from constants import NB_ITERATIONS
import main


def depth_analysis():
    with open("res.txt", "r") as f:
        data = f.readlines()
        data = [d.split(":") for d in data]
        data = [[int(d[0]), float(d[1]), float(d[2]), float(d[3]), float(d[4])] for d in data]

    x = [i for i in range(len(data))]
    y_total_times = [data[i][1] for i in range(len(data))]
    y_each_times = [data[i][3] for i in range(len(data))]

    fig, axis = plt.subplots(2)
    axis[0].set_title("Total game time")
    axis[1].set_title("Each black play time")
    axis[0].plot(x, y_total_times, label="Total game time")
    axis[1].plot(x, y_each_times, label="Each black play time")
    
    axis[0].legend()
    axis[1].legend()
    plt.legend()
    plt.show()


def plot(mean_results: list, results: list):
    x = [i for i in range(NB_ITERATIONS)]
    y_total_times = [results[i][0] for i in range(NB_ITERATIONS)]  
    y_each_times = [results[i][3] for i in range(NB_ITERATIONS)]

    fig, axis = plt.subplots(2)
    axis[0].set_title("Total game time")
    axis[1].set_title("Each black play time")
    axis[0].plot(x, y_total_times, label="Total game time")
    axis[0].axhline(y=mean_results[0], color='r', linestyle='-', label="Mean")
    axis[1].plot(x, y_each_times, label="Each black play time")
    axis[1].axhline(y=mean_results[3], color='r', linestyle='-', label="Mean")
    
    axis[0].legend()
    axis[1].legend()
    plt.show()



if __name__ == "__main__":
    inp = input("Do you want to run the game? (y/n) ")
    if inp == "y":
        mean_results, results = main.run()
        plot(mean_results, results)
    
    depth_analysis()