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
        instance_metrics = benchmark_algorithm_on_instance(file, args.splitting_strategy, timeout=args.timeout)
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

def benchmark_algorithm_on_instance(file, splitting_strategy, timeout=60):
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
    cbs = CBSSolver(map, starts, goals, timeout=timeout)

    disjoint, tuvya_splitting = False, False
    if splitting_strategy == 'disjoint':
        disjoint = True
    elif splitting_strategy == 'tuvya_splitting':
        tuvya_splitting = True

    start_time = time.time()
    result = cbs.find_solution(disjoint=disjoint, do_tuvya_splitting=tuvya_splitting)
    end_time = time.time()

    # Check if the algorithm timed out
    if result is None:
        metrics = {
            'File': file,
            'Splitting strategy': splitting_strategy,
            'HL Nodes expanded': cbs.num_of_expanded,
            'HL Nodes generated': cbs.num_of_generated,
            'LL Nodes expanded': cbs.ll_num_of_expanded,
            'LL Nodes generated': cbs.ll_num_of_generated,
            'Total runtime': "Timeout",
            'Solution cost': None,
            'Timeout': True
        }

        return metrics
    
    paths, _, _ = result

    # Collect the metrics
    metrics = {
        'File': file,
        'Splitting strategy': splitting_strategy,
        'HL Nodes expanded': cbs.num_of_expanded,
        'HL Nodes generated': cbs.num_of_generated,
        'LL Nodes expanded': cbs.ll_num_of_expanded,
        'LL Nodes generated': cbs.ll_num_of_generated,
        'Total runtime': end_time - start_time,
        'Solution cost': get_sum_of_cost(paths),
        'Timeout': False
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
    date_time = time.strftime('%m-%d-%Y_%H-%M-%S')
    filename = f'{output_directory}/{date_time}.csv'

    # Write the metrics to the file
    with open(filename, 'w') as f:
        # First write the header
        header = 'File,Splitting strategy,HL Nodes expanded,HL Nodes generated,LL Nodes expanded,LL Nodes generated,Total runtime,Solution cost\n'
        f.write(header)

        # Write the metrics
        for metric in metrics:
            file = metric['File']
            splitting_strategy = metric['Splitting strategy']
            hl_nodes_expanded = metric['HL Nodes expanded']
            hl_nodes_generated = metric['HL Nodes generated']
            ll_nodes_expanded = metric['LL Nodes expanded']
            ll_nodes_generated = metric['LL Nodes generated']
            total_runtime = metric['Total runtime']
            solution_cost = metric['Solution cost']

            if metric['Timeout']:
                f.write(f'{file},{splitting_strategy},{hl_nodes_expanded},{hl_nodes_generated},{ll_nodes_expanded},{ll_nodes_generated},{total_runtime},Timeout\n')
            else:
                f.write(f'{file},{splitting_strategy},{hl_nodes_expanded},{hl_nodes_generated},{ll_nodes_expanded},{ll_nodes_generated},{total_runtime},{solution_cost}\n')

def run_full_benchmark():
    '''
    Run the full benchmark specified by Dr. Atzmon. This function will run the benchmark on both empty and 10-percent instances with every splitting strategy.

    Returns
    -------
    None
    '''

    # # Run the benchmark on the standard splitting strategy
    # run_benchmark_with_these_args('standard', 'empty', 'atzmon_benchmark_results', 60)
    # run_benchmark_with_these_args('standard', '10-percent', 'atzmon_benchmark_results', 60)

    # # Run the benchmark on the disjoint splitting strategy
    # run_benchmark_with_these_args('disjoint', 'empty', 'atzmon_benchmark_results', 60)
    # run_benchmark_with_these_args('disjoint', '10-percent', 'atzmon_benchmark_results', 60)

    # # Run the benchmark on the tuvya splitting strategy
    # run_benchmark_with_these_args('tuvya_splitting', 'empty', 'atzmon_benchmark_results', 60)
    # run_benchmark_with_these_args('tuvya_splitting', '10-percent', 'atzmon_benchmark_results', 60)

    # Run the benchmark on the standard splitting strategy
    run_benchmark_with_these_args('standard', 'empty', 'atzmon_benchmark_results', 1)
    run_benchmark_with_these_args('standard', '10-percent', 'atzmon_benchmark_results', 1)

    # Run the benchmark on the disjoint splitting strategy
    run_benchmark_with_these_args('disjoint', 'empty', 'atzmon_benchmark_results', 1)
    run_benchmark_with_these_args('disjoint', '10-percent', 'atzmon_benchmark_results', 1)

    # Run the benchmark on the tuvya splitting strategy
    run_benchmark_with_these_args('tuvya_splitting', 'empty', 'atzmon_benchmark_results', 1)
    run_benchmark_with_these_args('tuvya_splitting', '10-percent', 'atzmon_benchmark_results', 1)

def run_benchmark_with_these_args(splitting_strategy, instance_type, output_directory, timeout):
    '''
    Run the benchmark with the given arguments. This method allows you to run the benchmark with the given arguments
    from a script or another function without having to use the command line.

    Parameters
    ----------
    splitting_strategy : str
        The splitting strategy to use. Can be "standard", "disjoint", or "tuvya_splitting".
    instance_type : str
        The type of instances to use. Can be "empty" or "10-percent".
    output_directory : str
        The directory to save the output to.
    timeout : int
        The timeout for each instance in seconds.

    Returns
    -------
    None
    '''

    args = argparse.Namespace(splitting_strategy=splitting_strategy, instance_type=instance_type, output_directory=output_directory, timeout=timeout)
    do_benchmark(args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Atzmon benchmark.')

    parser.add_argument('--splitting_strategy', type=str, default="standard", help='The splitting strategy to use. Can be "standard", "disjoint", or "tuvya_splitting". Default is "standard".')
    parser.add_argument('--instance_type', type=str, default="empty", help='The type of instances to use. Can be "empty" or "10-percent". Default is "empty".')
    parser.add_argument('--output_directory', '-o', type=str, default='atzmon_benchmark_results', help='The directory to save the output to. Default is "atzmon_benchmark_results".')
    parser.add_argument('--timeout', '-t', type=int, default=60, help='The timeout for each instance in seconds. Default is 60 seconds.')
    parser.add_argument('--run_full_benchmark', action='store_true', help='Run the full benchmark specified by Dr. Atzmon. This will run the benchmark on both empty and 10-percent instances with every splitting strategy.')

    args = parser.parse_args()

    if args.run_full_benchmark:
        run_full_benchmark()
        exit()

    do_benchmark(args)