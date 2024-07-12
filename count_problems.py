
def map_rating(rating: str) -> int | None:
    try:
        return int(int(rating) / 100) - 8
    except:
        return None


def main():
    file = open("submissions.csv")
    next(file)

    handles = {}
    for line in file:
        fields = line.split(";")
        handle = fields[0]
        index = map_rating(fields[4])

        if not handle in handles:
            handles[handle] = [0] * 28

        if index is None:
            continue
        
        handles[handle][index] += 1
    
    print("handle,", end="")
    for i in range(800, 3500, 100):
        print(str(i) + ",", end="")
    print("3500")

    for handle, solved in handles.items():
        print(handle + ",", end="")
        for count in solved[:-1]:
            print(str(count) + ",", end="")
        print(str(solved[-1]))
        


if __name__ == "__main__":
    main()
