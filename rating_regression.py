
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
from math import exp, log


class Data:
    def __init__(self, solved, max_rating):
        self.solved = solved
        self.max_rating = max_rating


def main():
    file = open("problems_solved.csv")
    next(file)

    x = []
    y = []

    users = {}
    for line in file:
        data = line.split(",")

        handle = data[0]
        solved = []
        for i in range(1, 29):
            solved.append(int(data[i]))
        max_rating = int(data[29])

        total_solved = sum(solved)
        if total_solved < 20:
            continue

        users[handle] = Data(solved, max_rating)
        x.append(solved)
        # y.append(exp(max_rating / 500))
        y.append(max_rating)
    
    plt.hist(y)
    plt.show()

    model = LinearRegression()
    model.fit(x, y)

    print(f'Coefficients: {model.coef_}')
    print(f'Intercept: {model.intercept_}')

    print(model.predict([users["theNewSon"].solved])[0])
    # print(log(model.predict([users["theNewSon"].solved])[0]) * 500)





if __name__ == "__main__":
    main()
    