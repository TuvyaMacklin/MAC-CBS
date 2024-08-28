# Multi-Agent Constraint CBS
BS"D

MAC-CBS introduces a novel splitting method for MAPF algorithms that constrains all agents involved in a conflict. This approach aims to improve the efficiency and effectiveness of conflict resolution compared to traditional methods. For more detailed information, please refer to the abstract provided in this repository.

## Usage
To use the `run_experiments.py` script, run it with `python run_experiments.py --instance <INSTANCE_NAME>`, replacing `<INSTANCE_NAME>` with your desired instance file. You can run all tests with `--run_all_tests` or benchmark a single instance using `--benchmark_instance`. Additionally, set a timeout for the solver with `--timeout <SECONDS>`. To select the splitting strategy, use `--tuvya_splitting` for Tuvya Splitting, which implements MAC-CBS, or `--imbalanced_tuvya_splitting` for its imbalanced variant. Disjoint Splitting is also an option with the `--disjoint` flag.

## Reference
This project is based on the [MAPF-ICBS](https://github.com/gloriyo/MAPF-ICBS) repository. The modifications focus on implementing and experimenting with Tuvya Splitting (MAC-CBS) and a variant called Imbalanced Splitting.

