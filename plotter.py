import matplotlib.pyplot as plt
import main


def plot(x:list, y:list):
    plt.plot(x, y)
    plt.show()



if __name__ == "__main__":
    params = main.run()

    print(params)