from copy import deepcopy #makes a copy of the puzzle so we can test actions
from colorama import Fore, Back, Style
from collections import deque #queue for BFS
import heapq #priority queue for UCS
import time

#all possible agent directions(actions)
DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}

#goal state
END = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

#UNICODE characters for drawing the puzzle in the terminal
left_down_angle = '\u2514'
right_down_angle = '\u2518'
right_up_angle = '\u2510'
left_up_angle = '\u250C'
middle_junction = '\u253C'
top_junction = '\u252C'
bottom_junction = '\u2534'
right_junction = '\u2524'
left_junction = '\u251C'


bar = Style.BRIGHT + Fore.CYAN + '\u2502' + Fore.RESET + Style.RESET_ALL
dash = '\u2500'

#puzzle box creation
first_line = Style.BRIGHT + Fore.CYAN + left_up_angle + dash + dash + dash + top_junction + dash + dash + dash + top_junction + dash + dash + dash + right_up_angle + Fore.RESET + Style.RESET_ALL
middle_line = Style.BRIGHT + Fore.CYAN + left_junction + dash + dash + dash + middle_junction + dash + dash + dash + middle_junction + dash + dash + dash + right_junction + Fore.RESET + Style.RESET_ALL
last_line = Style.BRIGHT + Fore.CYAN + left_down_angle + dash + dash + dash + bottom_junction + dash + dash + dash + bottom_junction + dash + dash + dash + right_down_angle + Fore.RESET + Style.RESET_ALL


def print_puzzle(array):
    print(first_line)
    for a in range(len(array)):
        for i in array[a]:
            if i == 0:
                print(bar, Back.RED + ' ' + Back.RESET, end=' ')
            else:
                print(bar, i, end=' ')
        print(bar)
        if a == 2:
            print(last_line)
        else:
            print(middle_line)

#state space
class Node:
    def __init__(self, current_node, previous_node, direction, cost=0):
        self.current_node = current_node
        self.previous_node = previous_node
        self.direction = direction
        self.cost = cost  # for UCS

    def __lt__(self, other):
        return self.cost < other.cost


def get_pos(current_state, element): #position of blank
    for row in range(len(current_state)):
        if element in current_state[row]:
            return (row, current_state[row].index(element))


def get_adjacent_nodes(node): #all possible states depending on possible actions
    listNode = []
    empty_pos = get_pos(node.current_node, 0)

    for dir in DIRECTIONS.keys():
        new_pos = (empty_pos[0] + DIRECTIONS[dir][0], empty_pos[1] + DIRECTIONS[dir][1])
        if 0 <= new_pos[0] < len(node.current_node) and 0 <= new_pos[1] < len(node.current_node[0]):
            new_state = deepcopy(node.current_node)
            new_state[empty_pos[0]][empty_pos[1]] = node.current_node[new_pos[0]][new_pos[1]]
            new_state[new_pos[0]][new_pos[1]] = 0
            listNode.append(Node(new_state, node.current_node, dir))

    return listNode

#traces back the steps
def build_path(closed_set):
    node = closed_set[tuple(tuple(row) for row in END)]  # Use tuple representation
    branch = []

    while node.direction:
        branch.append({
            'dir': node.direction,
            'node': node.current_node
        })
        node = closed_set[tuple(tuple(row) for row in node.previous_node)]
    branch.append({
        'dir': '',
        'node': node.current_node
    })
    branch.reverse()

    return branch

#BFS
def bfs(puzzle):
    queue = deque([Node(puzzle, None, "")])
    closed_set = {}
    visited = set()

    while queue:
        test_node = queue.popleft() #pops first in
        state_tuple = tuple(tuple(row) for row in test_node.current_node)

        if state_tuple in visited:
            continue #skips visited
        visited.add(state_tuple)

        closed_set[state_tuple] = test_node

        if test_node.current_node == END:
            return build_path(closed_set)

        adj_nodes = get_adjacent_nodes(test_node)
        for node in adj_nodes:
            node_tuple = tuple(tuple(row) for row in node.current_node)
            if node_tuple not in visited:
                queue.append(node)

    print("No solution found.")
    return []

#DFS
def dfs(puzzle):
    stack = [Node(puzzle, None, "")]
    closed_set = {}
    visited = set()

    while stack:
        test_node = stack.pop() #pops last in
        state_tuple = tuple(tuple(row) for row in test_node.current_node)  # Use tuple representation

        #visited
        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        closed_set[state_tuple] = test_node

        if test_node.current_node == END:
            return build_path(closed_set)

        adj_nodes = get_adjacent_nodes(test_node)
        for node in adj_nodes:
            node_tuple = tuple(tuple(row) for row in node.current_node)
            if node_tuple not in visited:
                stack.append(node)

    print("No solution found.")
    return []

#UCS
def ucs(puzzle):
    open_set = []
    heapq.heappush(open_set, (0, Node(puzzle, None, "", 0))) #pops lowest cost
    closed_set = {}
    visited = set()

    #total_cost = 0  # Track total cost

    while open_set:
        cost, test_node = heapq.heappop(open_set)
        #total_cost += cost  # Add the cost of the node to the total

        state_tuple = tuple(tuple(row) for row in test_node.current_node)

        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        closed_set[state_tuple] = test_node

        if test_node.current_node == END:
            return build_path(closed_set),cost

        adj_nodes = get_adjacent_nodes(test_node)
        for node in adj_nodes:
            node_tuple = tuple(tuple(row) for row in node.current_node)
            if node_tuple not in visited:
                heapq.heappush(open_set, (cost + 1, node))

    print("No solution found.")
    return []

def input_puzzle():
    print("Enter the puzzle matrix (3x3) row by row, with space between numbers:")
    puzzle = []
    for i in range(3):
        while True:
            try:
                row = list(map(int, input(f"Enter row {i + 1}: ").split()))
                if len(row) != 3:
                    print("Each row must contain exactly 3 numbers.")
                    continue
                puzzle.append(row)
                break
            except ValueError:
                print("Invalid input. Please enter integers separated by spaces.")
    return puzzle

def main():
    puzzle = input_puzzle()
    while True:
        print("---------------------WELCOME TO 8 PUZZLE SOLVER--------------------\nChoose an algorithm:")
        print("1. BFS")
        print("2. DFS")
        print("3. UCS")
        print("4. Exit")
        choice = input("Enter the number of the algorithm you want to use: ")

        if choice == '4':
            print("Exiting the program.")
            break

        #puzzle = input_puzzle()  # Get user input for the puzzle

        start_time = time.time()

        if choice == '1':
            print("Using BFS...")
            solution = bfs(puzzle)
            total_cost = len(solution)
        elif choice == '2':
            print("Using DFS...")
            solution = dfs(puzzle)
            total_cost = len(solution)
        elif choice == '3':
            print("Using UCS...")
            solution, total_cost =ucs(puzzle)
        else:
            print("Invalid choice!")
            continue

        end_time = time.time()
        execution_time = end_time - start_time

        if solution:
            print('Total steps:', len(solution) - 1)
            print()
            print(dash + dash + right_junction, "INPUT", left_junction + dash + dash)
            for b in solution:
                if b['dir'] != '':
                    letter = ''
                    if b['dir'] == 'U':
                        letter = 'UP'
                    elif b['dir'] == 'R':
                        letter = "RIGHT"
                    elif b['dir'] == 'L':
                        letter = 'LEFT'
                    elif b['dir'] == 'D':
                        letter = 'DOWN'
                    print(dash + dash + right_junction, letter, left_junction + dash + dash)
                print_puzzle(b['node'])
                print()

            print(dash + dash + right_junction, 'ABOVE IS THE OUTPUT', left_junction + dash + dash)

        print(f"Execution Time: {execution_time:.4f} seconds.")
        print(f"Total Cost: {total_cost}")

        continue_choice = input("Do you want to try another algorithm or exit? (yes to continue, any key to exit): ")
        if continue_choice != 'yes':
            print("Exiting the program.")
            break

if __name__ == "__main__":
    main()