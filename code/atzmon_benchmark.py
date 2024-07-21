'''
This file contains the code to run the benchmark specified by Dr. Atzmon. The benchmark will consist of running the algorithm
on a set of instances with 4, 8, 12, 16, and 20 agents. The instances will be generated using the functions in the instances
module. The benchmark can be run on empty instances or instances with 10% of the cells blocked.

Functions
---------
do_benchmark()
    Run the benchmark specified by Dr. Atzmon.

Notes
-----
The benchmark will be run on regular CBS with one of the following splitting strategies:
- Standard
- Disjoint
- Tuvya Splitting

The following metrics will be recorded for each instance:
- HL Nodes expanded
- HL Nodes generated
- LL Nodes expanded
- LL Nodes generated
- Total runtime
- Solution cost
'''

import argparse
import time
import os

from run_experiments import import_mapf_instance
from cbs_basic import CBSSolver
from single_agent_planner import get_sum_of_cost

def do_benchmark(args):
    '''
    Run the benchmark specified by Dr. Atzmon. Saves the output to a file.

    Parameters
    ----------
    args : argparse.Namespace
        The arguments to the script.

    Returns
    -------
    None
    '''

    # Get the files to run the benchmark on
    files = get_benchmark_files(args.instance_type)

    # Run each file through the algorithm specified, and track the metrics
    metrics = []
    for file in files:
        instance_metrics = benchmark_algorithm_on_instance(file, args.splitting_strategy)
        metrics.append(instance_metrics)

    # Log the metrics to a file
    log_metrics(metrics, args.output_directory)

def get_benchmark_files(instance_type):
    '''
    Get the files to run the benchmark on.

    Parameters
    ----------
    instance_type : str
        The type of instances to use. Can be "empty" or "10-percent".

    Returns
    -------
    list
        The files to run the benchmark on.
    '''

    if not instance_type in ['empty', '10-percent']:
        raise ValueError('Invalid instance type. Must be "empty" or "10-percent".')
    
    if instance_type == 'empty':
        instance_type = 'empty-grid'
    
    files = []
    for num_agents in [4, 8, 12, 16, 20]:
        for i in range(25):
            file = f'instances/atzmon_benchmark/{instance_type}/{i + 1}-{num_agents}-agents.txt'
            files.append(file)

    return files

def benchmark_algorithm_on_instance(file, splitting_strategy):
    '''
    Run the algorithm on the given file and track the metrics. The following metrics will be recorded:
    - HL Nodes expanded
    - HL Nodes generated
    - LL Nodes expanded
    - LL Nodes generated
    - Total runtime
    - Solution cost

    Parameters
    ----------
    file : str
        The file to run the algorithm on.
    splitting_strategy : str
        The splitting strategy to use.

    Returns
    -------
    dict
        The metrics for the instance.
    '''

    # Import the instance
    map, starts, goals = import_mapf_instance(file)

    # Run the algorithm
    cbs = CBSSolver(map, starts, goals, timeout=args.timeout)

    disjoint, tuvya_splitting = False, False
    if splitting_strategy == 'disjoint':
        disjoint = True
    elif splitting_strategy == 'tuvya_splitting':
        tuvya_splitting = True

    start_time = time.time()
    paths, _, _ = cbs.find_solution(disjoint=disjoint, do_tuvya_splitting=tuvya_splitting)
    end_time = time.time()

    # Collect the metrics
    metrics = {
        'HL Nodes expanded': cbs.num_of_expanded,
        'HL Nodes generated': cbs.num_of_generated,
        'LL Nodes expanded': cbs.ll_num_of_expanded,
        'LL Nodes generated': cbs.ll_num_of_generated,
        'Total runtime': end_time - start_time,
        'Solution cost': get_sum_of_cost(paths)
    }

    return metrics

def log_metrics(metrics, output_directory):
    '''
    Log the metrics to a file.

    Parameters
    ----------
    metrics : list
        The metrics to log.
    output_directory : str
        The directory to save the output to.

    Returns
    -------
    None
    '''

    # Attempt to create the output directory if it doesn't exist
    try:
        os.makedirs(output_directory)
    except FileExistsError:
        pass

    # Define the filename based on the date and time
    date_time = time.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'{output_directory}/{date_time}.txt'

    # Write the metrics to the file
    with open(filename, 'w') as f:
        for metric in metrics:
            f.write(str(metric) + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Atzmon benchmark.')

    parser.add_argument('--splitting_strategy', type=str, default="standard", help='The splitting strategy to use.')
    parser.add_argument('--instance_type', type=str, default="empty", help='The type of instances to use. Can be "empty" or "10-percent".')
    parser.add_argument('--output_directory', '-o', type=str, default='atzmon_benchmark_results', help='The directory to save the output to.')
    parser.add_argument('--timeout', '-t', type=int, default=60, help='The timeout for each instance in seconds.')

    args = parser.parse_args()

    do_benchmark(args)