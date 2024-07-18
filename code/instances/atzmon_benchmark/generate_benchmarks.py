def generate_benchmarks(scen_file, output_name, num_agents):
    '''
    Generate benchmarks from a scenario file. The instance will be an empty 8x8 grid
    with the agents taken from the specified scenario file. The output will be written
    to a file with the specified name.

    Parameters
    ----------
    scen_file : str
        The path to the scenario file.
    output_name : str
        The name of the output file.
    num_agents : int
        The number of agents to include in the instance.

    Returns
    -------
    None
    '''

    # Read the contents of the scenario file.
    lines = None
    with open(scen_file, 'r') as f:
        lines = f.readlines()

    lines = lines[1:]

    # Remove all agents beyond the specified number.
    lines = lines[:num_agents]

    # Convert each line to an agent's start and goal locations.
    agents = [parse_scen_line(line) for line in lines]

    # Write the instance to the output file.
    map = get_empty_map()
    write_instance(map, agents, output_name)

def parse_scen_line(line: str) -> str:
    '''
    Parse a line from a scenario file and return a string representing the agent's start and goal locations.

    Parameters
    ----------
    line : str
        The line to parse.

    Returns
    -------
    str
        A string representing the agent's start and goal locations.
    '''

    tokens = line.split()
    start_x = int(tokens[5])
    start_y = int(tokens[4])
    goal_x = int(tokens[7])
    goal_y = int(tokens[6])

    agent_string = "{0} {1} {2} {3}".format(start_x, start_y, goal_x, goal_y)

    return agent_string

def get_empty_map() -> str:
    '''
    Return a string representing an empty 8x8 grid with the dimensions at the beginning.

    Returns
    -------
    str
        A string representing an empty 8x8 grid.
    '''

    height = 8
    width = 8

    map_data = ['.' * width for _ in range(height)]

    map = '\n'.join(map_data)

    return f'{height} {width}\n{map}'

def write_instance(map: str, agents: list, output_name: str):
    '''
    Write an instance to a file with the specified name.

    Parameters
    ----------
    map : str
        A string representing the map.
    agents : list
        A list of strings representing the agents' start and goal locations.
    output_name : str
        The name of the output file.

    Returns
    -------
    None
    '''

    num_agents = len(agents)

    agent_string = '\n'.join(agents)

    output_string = f'{map}\n{num_agents}\n{agent_string}'

    with open(output_name, 'w') as f:
        f.write(output_string)

def generate_empty_instances():
    '''
    Generate empty instances for the Atzmon benchmark with 4, 8, 12, 16, and 20 agents.

    Returns
    -------
    None
    '''

    amounts_of_agents = [4, 8, 12, 16, 20]

    num_of_source_files = 25

    # amounts_of_agents = [4]
    # num_of_source_files = 1

    for num_agents in amounts_of_agents:
        for i in range(num_of_source_files):
            scen_file = f'instances/atzmon_benchmark/source/empty-8-8-random-{i + 1}.scen'
            output_name = f'instances/atzmon_benchmark/empty-grid/{i + 1}-{num_agents}-agents.txt'
            generate_benchmarks(scen_file, output_name, num_agents)

if __name__ == "__main__":
    generate_empty_instances()