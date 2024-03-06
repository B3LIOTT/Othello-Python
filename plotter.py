import matplotlib.pyplot as plt
import numpy as np
from constants import NB_ITERATIONS, ANALYSE
import pylab
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


def time_analysis():
    """
    https://fr.moonbooks.org/Articles/Diagramme-en-b%C3%A2tons-avec-Matplotlib/#myGallery
    """
    with open("res.txt", "r") as f:
        data = f.readlines()
        data = [d.split(":") for d in data]
        data = [[float(d[1]), float(d[3]), float(d[4])] for d in data]

    x = [data[i][0] for i in range(len(data))]
    y_total_times = [data[i][1] for i in range(len(data))]
    y_each_times_black = [data[i][3] for i in range(len(data))]
    y_each_times_white = [data[i][4] for i in range(len(data))]

    fig = plt.figure()
    x = [1,2]
    width = 0.05
    BarNames = ['a','b']

    plt.bar(x, y_each_times_black, width, color=(0.65098041296005249, 0.80784314870834351, 0.89019608497619629, 1.0) )
    plt.scatter([i+width/2.0 for i in x],y_each_times_black,color='k',s=40)

    plt.xlim(0,11)
    plt.ylim(0,14)
    plt.grid()

    plt.ylabel('Counts')
    plt.title('Diagramme en Batons !')

    pylab.xticks(x, BarNames, rotation=40)

    plt.savefig('SimpleBar.png')
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
    
    inp = int(input("What type of results do you want?\n\t1. Time/Depth analysis\n\t2. Time analysis\n\nYour choice:"))
    if inp == 1:
        depth_analysis()
    elif inp == 2:
        time_analysis()
