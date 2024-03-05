import matplotlib.pyplot as plt
import numpy as np
from constants import NB_ITERATIONS, ANALYSE
import main


def depth_analysis():
    with open("res.txt", "r") as f:
        data = f.readlines()
        data = [d.split(":") for d in data]
        data = [[int(d[0]), float(d[1]), float(d[2]), float(d[3]), float(d[4])] for d in data]

    x = [data[i][0] for i in range(len(data))]
    y_total_times = [data[i][1] for i in range(len(data))]
    y_each_times_black = [data[i][3] for i in range(len(data))]
    y_each_times_white = [data[i][4] for i in range(len(data))]

    fig, axis = plt.subplots(2)
    axis[0].set_title("Total game time")
    axis[1].set_title("Each black play time")
    axis[0].plot(x, y_total_times, label="Total game time")
    axis[1].plot(x, y_each_times_black, label="Black plays mean time")
    axis[1].plot(x, y_each_times_white, label="White plays mean time")
    
    axis[0].legend()
    axis[1].legend()
    plt.legend()
    plt.show()


def plot(mean_results: list, results: list):
    x = [i for i in range(1, NB_ITERATIONS+1)]
    y_total_times = [results[i][0] for i in range(NB_ITERATIONS)]  
    y_each_times_black = [results[i][3] for i in range(NB_ITERATIONS)]
    y_each_times_white = [results[i][4] for i in range(NB_ITERATIONS)]

    fig, axis = plt.subplots(2)
    axis[0].set_title("Total game time")
    axis[1].set_title("Each black play time")
    axis[0].plot(x, y_total_times, label="Total game time")
    axis[0].axhline(y=mean_results[0], color='r', linestyle='-', label="Mean")
    axis[1].plot(x, y_each_times_black, label="Black plays mean time")
    axis[1].plot(x, y_each_times_white, label="White plays mean time")
    axis[1].axhline(y=mean_results[3], color='r', linestyle='-', label="General black mean")
    axis[1].axhline(y=mean_results[4], color='b', linestyle='-', label="General white mean")
    
    axis[0].legend()
    axis[1].legend()
    plt.show()



if __name__ == "__main__":
    if not ANALYSE:
        raise ValueError("ANALYSE must be True in constants.py")
    
    inp = input("Do you want to run the game? (y/n) ")
    if inp == "y":
        mean_results, results = main.run()
        plot(mean_results, results)
    
    depth_analysis()