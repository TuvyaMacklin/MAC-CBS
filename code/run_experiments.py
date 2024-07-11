#!/usr/bin/python
import argparse
import glob
from pathlib import Path
from cbs_basic import CBSSolver # original cbs with standard/disjoint splitting

# cbs with different improvements
from icbs_cardinal_bypass import ICBS_CB_Solver # only cardinal dectection and bypass
from icbs_complete import ICBS_Solver # all improvements including MA-CBS


from independent import IndependentSolver
from prioritized import PrioritizedPlanningSolver
from visualize import Animation
from single_agent_planner import get_sum_of_cost

HLSOLVER = "CBS"

LLSOLVER = "a_star"

def print_mapf_instance(my_map, starts, goals):
    print('Start locations')
    print_locations(my_map, starts)
    print('Goal locations')
    print_locations(my_map, goals)


def print_locations(my_map, locations):
    starts_map = [[-1 for _ in range(len(my_map[0]))] for _ in range(len(my_map))]
    for i in range(len(locations)):
        starts_map[locations[i][0]][locations[i][1]] = i
    to_print = ''
    for x in range(len(my_map)):
        for y in range(len(my_map[0])):
            if starts_map[x][y] >= 0:
                to_print += str(starts_map[x][y]) + ' '
            elif my_map[x][y]:
                to_print += '@ '
            else:
                to_print += '. '
        to_print += '\n'
    print(to_print)


def import_mapf_instance(filename):
    f = Path(filename)
    if not f.is_file():
        raise BaseException(filename + " does not exist.")
    f = open(filename, 'r')
    # first line: #rows #columns
    line = f.readline()
    rows, columns = [int(x) for x in line.split(' ')]
    rows = int(rows)
    columns = int(columns)
    # #rows lines with the map
    my_map = []
    for r in range(rows):
        line = f.readline()
        my_map.append([])
        for cell in line:
            if cell == '@':
                my_map[-1].append(True)
            elif cell == '.':
                my_map[-1].append(False)
    # #agents
    line = f.readline()
    num_agents = int(line)
    # #agents lines with the start/goal positions
    starts = []
    goals = []
    for a in range(num_agents):
        line = f.readline()
        sx, sy, gx, gy = [int(x) for x in line.split(' ')]
        starts.append((sx, sy))
        goals.append((gx, gy))
    f.close()
    return my_map, starts, goals

def run_all_tests(args):
    '''
    This command runs all the tests in the instances folder and prints out a summary of the results.
    It is useful for checking completeness in the solvers.

    Parameters:
        args: The arguments from the command line
    '''

    # Iterate over files test_1.txt to test_57.txt
    files = ["instances/test_{}.txt".format(i) for i in range(1, 58)]

    actual = get_actual_results("instances/min-sum-of-cost.csv")

    successes = 0

    for file in files:
        try:
            if run_test(file, args, actual[file]):
                successes += 1
        except BaseException as e:
            print("Test failed for file {}. Error: {}".format(file, e))

    print("Tests passed: {}/57".format(successes))

def get_actual_results(filename):
    '''
    This function reads the actual results from the min-sum-of-cost.csv file.

    Parameters:
        filename: The name of the file to read from

    Returns:
        A dictionary mapping the filename to the sum of costs
    '''

    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    actual = {}

    for line in lines:
        parts = line.split(',')
        actual[parts[0]] = int(parts[1])

    return actual

def run_test(file, args, actual):
    '''
    This function runs a single test and compares the result to the expected result.

    Parameters:
        file: The name of the file to run
        args: The arguments from the command line
        actual: The actual result of the test

    Returns:
        True if the test passed, False otherwise
    '''

    my_map, starts, goals = import_mapf_instance(file)

    if args.hlsolver == "CBS":
        cbs = CBSSolver(my_map, starts, goals)
    elif args.hlsolver == "ICBS":
        cbs = ICBS_Solver(my_map, starts, goals)
    else:
        raise RuntimeError("Unknown solver!")
    
    paths, _, _ = cbs.find_solution(args.disjoint)

    if paths is None:
        raise BaseException('No solutions')
    
    cost = get_sum_of_cost(paths)
    
    if cost == actual:
        print("Test passed for file {}. Cost: {}".format(file, cost))
        return True
    else:
        print("Test failed for file {}. Expected: {}, Actual: {}".format(file, actual, cost))
        return False
    

def benchmark_instance(file, args, print_results=False):
    '''
    This function runs a single instance through the solver without disjoing splitting and compares it to that with disjoint splitting.
    It prints out the amount of nodes generated and expanded for both cases.

    Parameters:
        file: The name of the file to run
        args: The arguments from the command line
    '''

    # Assert that the solver is CBS
    if not args.hlsolver == "CBS":
        raise Exception("Benchmarking only works with CBS")

    # Set up the results dictionary
    results = {
        "standard_splitting": {},
        "disjoint_splitting": {},
        "tuvya_splitting": {}
    }

    # Load the instance
    my_map, starts, goals = import_mapf_instance(file)

    # Run with standard splitting
    cbs = CBSSolver(my_map, starts, goals)
    paths, results["standard_splitting"]["nodes_gen"], results["standard_splitting"]["nodes_exp"] = cbs.find_solution(False)

    if paths is None:
        raise BaseException('No solutions')

    # Run with disjoint splitting
    cbs = CBSSolver(my_map, starts, goals)
    paths, results["disjoint_splitting"]["nodes_gen"], results["disjoint_splitting"]["nodes_exp"] = cbs.find_solution(True)

    if paths is None:
        raise BaseException('No solutions')
    
    # Run with Tuvya splitting
    cbs = CBSSolver(my_map, starts, goals)
    paths, results["tuvya_splitting"]["nodes_gen"], results["tuvya_splitting"]["nodes_exp"] = cbs.find_solution(True)

    if paths is None:
        raise BaseException('No solutions')
    
    if print_results:
        # Print the result as a table. The columns should be num_exp and num_gen and the rows should be standard and disjoint
        print("Method\tNodes Expanded\tNodes Generated")
        print("Standard\t{}\t{}".format(results["standard_splitting"]["nodes_exp"], results["standard_splitting"]["nodes_gen"]))
        print("Disjoint\t{}\t{}".format(results["disjoint_splitting"]["nodes_exp"], results["disjoint_splitting"]["nodes_gen"]))
        print("Tuvya\t\t{}\t{}".format(results["tuvya_splitting"]["nodes_exp"], results["tuvya_splitting"]["nodes_gen"]))

    return results

def benchmark_all_instances(args):
    '''
    This function runs all instances through the solver without disjoing splitting and compares it to that with disjoint splitting.
    It prints out the amount of nodes generated and expanded for both cases.

    Parameters:
        args: The arguments from the command line
    '''

    # Assert that the solver is CBS
    if not args.hlsolver == "CBS":
        raise Exception("Benchmarking only works with CBS")

    # Set up the results dictionary
    results = {}

    # Iterate over files test_1.txt to test_57.txt
    files = ["instances/test_{}.txt".format(i) for i in range(1, 10)]

    for file in files:
        try:
            results[file] = benchmark_instance(file, args)
        except BaseException as e:
            print("Benchmark failed for file {}. Error: {}".format(file, e))

    # Print the results in the following format:
    # File, Standard Nodes Expanded, Standard Nodes Generated, Disjoint Nodes Expanded, Disjoint Nodes Generated, Tuvya Nodes Expanded, Tuvya Nodes Generated
    # print("File, Standard Nodes Expanded, Standard Nodes Generated, Disjoint Nodes Expanded, Disjoint Nodes Generated, Tuvya Nodes Expanded, Tuvya Nodes Generated")
    # for file in results:
    #     print("{}, {}, {}, {}, {}, {}, {}".format(file, results[file]["standard_splitting"]["nodes_exp"], results[file]["standard_splitting"]["nodes_gen"], results[file]["disjoint_splitting"]["nodes_exp"], results[file]["disjoint_splitting"]["nodes_gen"], results[file]["tuvya_splitting"]["nodes_exp"], results[file]["tuvya_splitting"]["nodes_gen"]))

    print("Results")
    print("File\tMethod\tNodes Expanded\tNodes Generated")
    for file in results:
        for method in results[file]:
            print("{}\t{}\t{}\t{}".format(file, method, results[file][method]["nodes_exp"], results[file][method]["nodes_gen"]))

    
    
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs various MAPF algorithms')
    parser.add_argument('--instance', type=str, default=None,
                        help='The name of the instance file(s)')
    parser.add_argument('--batch', action='store_true', default=False,
                        help='Use batch output instead of animation')
    parser.add_argument('--disjoint', action='store_true', default=False,
                        help='Use the disjoint splitting')
    parser.add_argument('--tuvya_splitting', action='store_true', default=False,
                        help='Use Tuvya splitting')
    parser.add_argument('--hlsolver', type=str, default=HLSOLVER,
                        help='The solver to use (one of: {CBS,ICBS_CB,ICBS}), defaults to ' + str(HLSOLVER))
    parser.add_argument('--run_all_tests', action='store_true', default=False,
                        help='Run all tests in the instances folder. Used for checking completeness of the solvers.')
    parser.add_argument('--benchmark_instance', action='store_true', default=False,
                        help='Run a single instance through the solver without disjoint splitting and compare it to that with disjoint splitting.')
    parser.add_argument('--benchmark_all_instances', action='store_true', default=False,
                        help='Run all instances through the solver without disjoint splitting and compare it to that with disjoint splitting.')
    # parser.add_argument('--llsolver', type=str, default=LLSOLVER,
    #                     help='The solver to use (one of: {a_star,pea_star,epea_star}), defaults to ' + str(LLSOLVER))
    args = parser.parse_args()

    if args.run_all_tests:
        run_all_tests(args)
        exit()

    if args.benchmark_instance:
        benchmark_instance(args.instance, args, True)
        exit()

    if args.benchmark_all_instances:
        benchmark_all_instances(args)
        exit()

    result_file = open("results.csv", "w", buffering=1)

    # node_results_file = open("nodes-cleaned.csv", "w", buffering=1)

    nodes_gen_file = open("nodes-gen-cleaned.csv", "w", buffering=1)
    nodes_exp_file = open("nodes-exp-cleaned.csv", "w", buffering=1)


    if args.batch:
        
        input_instance = sorted(glob.glob("instances/test*"))
    else:
        input_instance = sorted(glob.glob(args.instance))

    for file in input_instance:

        print("***Import an instance***")

        
        print(file)
        my_map, starts, goals = import_mapf_instance(file)
        print_mapf_instance(my_map, starts, goals)

        if args.hlsolver == "CBS":
            print("***Run CBS***")
            cbs = CBSSolver(my_map, starts, goals)
            # solution = cbs.find_solution(args.disjoint)

            # if solution is not None:
            #     # print(solution)
            #     paths, nodes_gen, nodes_exp = [solution[i] for i in range(3)]
            #     if paths is None:
            #         raise BaseException('No solutions')  
            # else:
            #     raise BaseException('No solutions')

        elif args.hlsolver == "ICBS_CB":
            print("***Run ICBS with CB***")
            cbs = ICBS_CB_Solver(my_map, starts, goals)
 

        elif args.hlsolver == "ICBS":
            print("***Run ICBS***")
            cbs = ICBS_Solver(my_map, starts, goals)
            # solution = cbs.find_solution(args.disjoint)

            # if solution is not None:
            #     # print(solution)
            #     paths, nodes_gen, nodes_exp = [solution[i] for i in range(3)]
            #     if paths is None:
            #         raise BaseException('No solutions')  
            # else:
            #     raise BaseException('No solutions')



        # elif args.solver == "Independent":
        #     print("***Run Independent***")
        #     solver = IndependentSolver(my_map, starts, goals)
        #     paths, nodes_gen, nodes_exp = solver.find_solution()
        # elif args.solver == "Prioritized":
        #     print("***Run Prioritized***")
        #     solver = PrioritizedPlanningSolver(my_map, starts, goals)
        #     paths, nodes_gen, nodes_exp = solver.find_solution()

        else:
            raise RuntimeError("Unknown solver!")



        solution = cbs.find_solution(args.disjoint, print_results=True)

        if solution is not None:
            # print(solution)
            paths, nodes_gen, nodes_exp = [solution[i] for i in range(3)]
            if paths is None:
                raise BaseException('No solutions')  
        else:
            raise BaseException('No solutions')

        cost = get_sum_of_cost(paths)
        result_file.write("{},{}\n".format(file, cost))

        nodes_gen_file.write("{},{}\n".format(file, nodes_gen))
        nodes_exp_file.write("{},{}\n".format(file, nodes_exp))



        if not args.batch:
            print("***Test paths on a simulation***")
            animation = Animation(my_map, starts, goals, paths)
            # animation.save("output.mp4", 1.0)
            animation.show()
            # animation.save('demo/fig.gif', 1)

    result_file.close()
