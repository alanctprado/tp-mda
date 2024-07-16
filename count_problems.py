
def map_rating(rating: str) -> int | None:
    try:
        return int(int(rating) / 100) - 8
    except:
        return None


def get_max_ratings():
    users = open("output.csv")
    next(users)

    max_ratings = {}
    for line in users:
        fields = line.split("\t")
        handle = fields[0]
        max_rating = fields[13]
        try:
            max_ratings[handle] = int(max_rating)
        except:
            pass

    return max_ratings


def main():
    max_ratings = get_max_ratings()
    file = open("submissions.csv")
    next(file)
    
    solved = {}
    for line in file:
        fields = line.split("\t")
        handle = fields[0]

        if not handle in max_ratings:
            continue

        problem = fields[1] + fields[2]
        index = map_rating(fields[4])
        ok = fields[8][:-1] == "OK"

        if not handle in solved:
            solved[handle] = {}
        
        if index is None or not ok:
            continue

        solved[handle][problem] = index


    handles = {}
    for handle, s in solved.items():
        if not handle in handles:
            handles[handle] = [0] * 28

        for problem, index in s.items():
            handles[handle][index] += 1
    
    print("handle,", end="")
    for i in range(800, 3600, 100):
        print(str(i) + ",", end="")
    print("max_rating")

    for handle, solved in handles.items():
        if not handle in max_ratings:
            continue

        print(handle + ",", end="")
        for count in solved:
            print(str(count) + ",", end="")
        print(max_ratings[handle])



if __name__ == "__main__":
    main()
