# Multi-Agent Constraint CBS
BS"D

MAC-CBS introduces a novel splitting method for MAPF algorithms that constrains all agents involved in a conflict. This approach aims to improve the efficiency and effectiveness of conflict resolution compared to traditional methods. For more detailed information, please refer to the abstract provided in this repository.

## Usage
This repository is designed to be used with a Python virtual environment (venv). It is recommended to create the virtual environment within the repository directory to keep dependencies isolated. After setting up the venv, install the required packages using the `requirements.txt` file to ensure that all necessary dependencies are properly configured.

To use the `run_experiments.py` script, run it with `python run_experiments.py --instance <INSTANCE_NAME>`, replacing `<INSTANCE_NAME>` with your desired instance file. You can run all tests with `--run_all_tests` or benchmark a single instance using `--benchmark_instance`. Additionally, set a timeout for the solver with `--timeout <SECONDS>`. To select the splitting strategy, use `--tuvya_splitting` for Tuvya Splitting, which implements MAC-CBS, or `--imbalanced_tuvya_splitting` for its imbalanced variant. Disjoint Splitting is also an option with the `--disjoint` flag.

### Atzmon Benchmark
This benchmark was specified by Dr. Dor Atzmon, the faculty advisor on this project, and follows best practices for evaluating MAPF algorithms.

To run the Atzmon benchmark, use the `atzmon_benchmark.py` script. You can specify the splitting strategy with `--splitting_strategy`, choosing from "standard", "disjoint", "tuvya_splitting", or "tuvya_splitting_imbalanced". For instance types, use `--instance_type` with options like "empty", "10-percent", or "all". Set an output directory with `--output_directory` (default is "atzmon_benchmark_results") and a timeout for each instance with `--timeout <SECONDS>`. To run the full benchmark which tests all splitting strategies across both empty and 10-percent instances, use the `--run_full_benchmark` flag.

## Reference
This project is based on the [MAPF-ICBS](https://github.com/gloriyo/MAPF-ICBS) repository. The modifications focus on implementing and experimenting with Tuvya Splitting (MAC-CBS) and a variant called Imbalanced Splitting.

