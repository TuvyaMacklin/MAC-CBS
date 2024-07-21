import random


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

def generate_10_percent_instances(amounts_of_agents: str = [4, 8, 12, 16, 20], obstacle_density: float = 0.1,
                                  amount_of_maps: int = 25):
    '''
    Generates instances for the Atzmon benchmark with a 10% random obstacle density.
    The instances will have 4, 8, 12, 16, and 20 agents by default.

    The start and goal locations of the agents will be taken from the source files in the
    instances/atzmon_benchmark/source directory. The obstacles will be randomly generated
    with the specified density.

    Parameters
    ----------
    amounts_of_agents : str
        The number of agents to include in the instances. Default is [4, 8, 12, 16, 20].
    obstacle_density : float
        The obstacle density of the instances. Default is 0.1.
    amount_of_maps : int
        The number of maps to generate. Default is 25.

    Returns
    -------
    None
    '''

    # Get the name of the source file with the start and goal locations of the agents.
    source_files = [f'instances/atzmon_benchmark/source/empty-8-8-random-{i + 1}.scen' for i in range(amount_of_maps)]

    # Generate instances for each number of agents.
    for num_agents in amounts_of_agents:
        for i, source_file in enumerate(source_files):
            output_name = f'instances/atzmon_benchmark/10-percent/{i + 1}-{num_agents}-agents.txt'
            generate_10_percent_instance(source_file, output_name, num_agents, obstacle_density)

def generate_10_percent_instance(scen_file: str, output_name: str, num_agents: int, obstacle_density: float):
    '''
    Generate an instance for the Atzmon benchmark with a 10% random obstacle density.

    The instance will be an 8x8 grid with the specified number of agents and the obstacles
    randomly generated with the specified density.

    Parameters
    ----------
    scen_file : str
        The path to the scenario file.
    output_name : str
        The name of the output file.
    num_agents : int
        The number of agents to include in the instance.
    obstacle_density : float
        The obstacle density of the instance.

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

    # Generate the map with the specified obstacle density.
    map_string = generate_filled_map(obstacle_density, agents)

    # Write the instance to the output file.
    write_instance(map_string, agents, output_name)

def generate_filled_map(obstacle_density: float, agents: list) -> str:
    '''
    Generate a map with the specified obstacle density.

    Parameters
    ----------
    obstacle_density : float
        The obstacle density of the map.
    agents : list
        A list of strings representing the agents' start and goal locations.

    Returns
    -------
    str
        A string representing the map.
    '''
    # Get the open locations in the map.
    open_locations = get_open_locations(agents)

    # Shuffle the possible locations.
    random.shuffle(open_locations)

    # Calculate the number of obstacles to place on the map.
    num_obstacles = int(obstacle_density * 64)
    
    # Place the obstacles on the map.
    map_data = [['.' for _ in range(8)] for _ in range(8)]
    for i in range(num_obstacles):
        y, x = open_locations[i]
        map_data[y][x] = '@'

    # Convert the map to a string.
    map_data = [''.join(row) for row in map_data]
    map_string = '\n'.join(map_data)

    return f'8 8\n{map_string}'

def get_open_locations(agents: list) -> list:
    '''
    Get the open locations on the map.

    Parameters
    ----------
    agents : list
        A list of strings representing the agents' start and goal locations. Each string should contain
        four integers separated by spaces. The first two integers represent the agent's start y and x,
        and the last two integers represent the agent's goal y and x.

    Returns
    -------
    list
        A list of tuples representing the open locations on the map. Each tuple should contain two integers
        representing the y and x coordinates of the open location.
    '''

    # Parse the agents' start and goal locations into lists of ints.
    agent_locations = [list(map(int, location.split())) for location in agents]

    # Split them into start and goal locations and store them in one list.
    start_locations = [location[:2] for location in agent_locations]
    goal_locations = [location[2:] for location in agent_locations]
    taken_locations = start_locations + goal_locations

    # Enumerate all the possible locations on the map. Then remove the agent locations.
    all_possible_locations = [(y, x) for y in range(8) for x in range(8)]

    open_locations = [location for location in all_possible_locations if not location_taken(location, taken_locations)]

    return open_locations

def location_taken(location: tuple, taken_locations: list) -> bool:
    '''
    Check if a location is taken by an agent.

    Parameters
    ----------
    location : tuple
        A tuple containing two integers representing the y and x coordinates of the location.
    taken_locations : list
        A list of tuples representing the locations taken by agents.

    Returns
    -------
    bool
        True if the location is taken, False otherwise.
    '''

    for taken_location in taken_locations:
        if location[0] == taken_location[0] and location[1] == taken_location[1]:
            return True
        
    return False

if __name__ == "__main__":
    generate_10_percent_instances()