
from math import exp, sqrt
import matplotlib.pyplot as plt


NUM_FEATURES = 28

class Model:
    def __init__(self, baseline, limit, gain):
        self.baseline = baseline
        self.limit = limit
        self.gain = gain
    
    def eval(self, x):
        result = self.baseline
        for i in range(NUM_FEATURES):
            partial = self.limit[i] * (1 - exp(-self.gain[i] * x[i]))
            result += partial
        return result
    
    def calculate_error(self, x, y):
        diff = y - self.eval(x)
        return diff * diff
        

best_model = Model(
    836.926,
    [20.783, 1.18272, 1.12132, 90.2824, 43.4044, 40.383, 86.4512, 3.20236, 58.8065, 110.989, 138.202, 59.3391, 70.5712, 160.648, 25.0045, 60.4748, 189.337, 256.089, 113.842, 60.33, 101.986, 170.006, 45.5957, 48.3872, 62.8992, 89.594, 42.3275, 49.3362],
    [0.574126, 0.0183221, 0.0150065, 1.41466, 1.74711, 1.12801, 0.73062, 0.0244584, 1.92629, 0.646292, 0.455038, 0.50509, 0.320186, 0.0534544, 0.0268589, 0.792542, 0.229015, 0.0382293, 0.0269923, 0.027888, 0.0359261, 0.0350064, 0.0417141, 0.0426146, 0.0372959, 0.0665829, 0.0393887, 0.0332444]    
)


def separate_by_category(entries):
    separated = {}
    for x, y in entries.values():
        category = (y // 100) * 100
        if category not in separated:
            separated[category] = []
        separated[category].append((x, y))
    return separated


def error_by_category(categories):
    errors = {}
    for category, entries in categories.items():
        error = 0
        for x, y in entries:
            error += best_model.calculate_error(x, y)
        errors[category] = sqrt(error / len(entries))
    return errors


def main():
    plt.bar([str(i) for i in range(800, 3600, 100)], best_model.limit)
    plt.xlabel("Rating")
    plt.ylabel("Limite")
    plt.title("Limite de cada problema")
    plt.show()

    plt.bar([str(i) for i in range(800, 3600, 100)], best_model.gain)
    plt.xlabel("Rating")
    plt.ylabel("Ganho")
    plt.title("Ganho de cada problema")
    plt.show()


    file = open("problems_solved.csv")
    next(file)

    entries = {}
    for line in file:
        fields = line.split(",")

        handle = fields[0]
        x = []
        for i in range(1, 29):
            x.append(int(fields[i]))
        y = int(fields[-1])

        total_solved = sum(x)
        if total_solved < 20 or y < 700:
            continue

        entries[handle] = (x, y)


    categories = separate_by_category(entries)
    errors = error_by_category(categories)

    y = [0 for i in range(700, 4000, 100)]
    for key, error in errors.items():
        y[key // 100 - 7] = error

    plt.bar([str(i) for i in range(700, 4000, 100)], y)
    plt.xlabel("Rating")
    plt.ylabel("Erro")
    plt.title("Erro por faixa de rating")
    plt.show()


            
        


if __name__ == "__main__":
    main()

