import frontier
import state
from tabulate import tabulate

def search(s, funct):
    print("Initial state:")
    s.print_board()
    f = frontier.create(s, funct)
    while not frontier.is_empty(f):
        s = frontier.remove(f)
        print()
        print("Current state:")
        s.print_board()

        if s.is_goal():
            print("Reached the goal!")
            return [s, f["total pushed items"]]
        ns = s.expand()
        print("Next states:")
        for i in ns:
            print("  ", i.constraints)
        print("Expanding:", len(ns), "states")
        for i in ns:
            frontier.insert(f, i)
    print("No solution")
    return [0, f["total pushed items"]]

def testChocolate():
    # Define your search functions here
    f = {lambda stat: stat.path_len() : "UCS", lambda stat: stat.hdistance() : "Greedy",
       lambda stat: stat.hdistance()+stat.path_len() : "A*"}

    runTimes = 100
    succMaze = [0] * len(f)
    succChecks = [0] * len(f)
    failChecks = [0] * len(f)
    succLen = [0] * len(f)

    for j in range(runTimes):
        s = state.ChocolateBoard()  # Initialize the initial state of the game
        # Set up initial constraints here if needed

        for i, k in zip(f.keys(), range(len(f))):
            res = search(s, i)
            if res[0]:
                succMaze[k] += 1
                succChecks[k] += res[1]
                succLen[k] += len(res[0].board)
            else:
                failChecks[k] += res[1]

    table_data = []
    headers = ["Algorithm", "Success Rate (%)", "Avg Success Length", "Avg Success Checks", "Avg Failure Checks"]

    for i, j in zip(f.values(), range(len(f))):
        avgSuccChecks = 0
        avgSuccLen = 0
        if succMaze[j] != 0:
            avgSuccChecks = round(succChecks[j] / succMaze[j], 2)
            avgSuccLen = round(succLen[j] / succMaze[j], 2)
        avgFailChecks = 0
        if runTimes - succMaze[j] != 0:
            avgFailChecks = round(failChecks[j] / (runTimes - succMaze[j]), 2)

        row_data = [
            i,
            round((succMaze[j] / runTimes) * 100, 2),
            avgSuccLen,
            avgSuccChecks,
            avgFailChecks
        ]
        table_data.append(row_data)

    print(tabulate(table_data, headers=headers, tablefmt="grid"))

if __name__ == '__main__':
    testChocolate()






