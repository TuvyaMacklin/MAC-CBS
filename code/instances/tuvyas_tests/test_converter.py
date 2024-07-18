'''
This module contains a function used to convert the test data from the format
used in the CBSH2-RTC repo to the format used in this repo.
'''

import argparse

def convert_test_data(map_file : str = None, scen_file : str = None, output_file : str = None):
    '''
    Convert the test data from the format used in the CBSH2-RTC repo to the
    format used in this repo.

    Parameters:
        map_file (str): The path to the file containing the map data.
        scen_file (str): The path to the file containing the scenario data (aka
            the data for the agents and their goals).
        output_file (str): The path to the file to write the converted test data
            to. If None, the converted test data will be printed to the console
            so it can be piped to a file.

        - Either map_file and scen_file must be provided. Both can be provided.

    Returns:
        Str: the contents of the files in the new format.
    '''

    # Assert that at least one of map_file and scen_file is provided.
    if (map_file is None) and (scen_file is None):
        raise ValueError('Either map_file or scen_file must be provided.')
    
    # Assert that both files exist.
    if not map_file is None:
        with open(map_file, 'r') as f:
            pass
    if not scen_file is None:
        with open(scen_file, 'r') as f:
            pass

    # Assert that the map file ends in '.map' and the scenario file ends in '.scen'.
    if not map_file is None:
        if not map_file.endswith('.map'):
            raise ValueError('The map file must end in ".map".')
    if not scen_file is None:
        if not scen_file.endswith('.scen'):
            raise ValueError('The scenario file must end in ".scen".')
    
    output_string = ''
    
    # Parse the map file.
    if not map_file is None:
        with open(map_file, 'r') as f:
            map_data = f.readlines()

        # Get the dimensions of the map. They are the second tokens on the first two lines.
        height = int(map_data[1].split()[1])
        width = int(map_data[2].split()[1])

        # Get the map data. It starts on the fifth line.
        map_data = map_data[4:]

        # Go through each line of the map data and insert a space between each character.
        for i in range(len(map_data)):
            # Split the line into a list of characters.
            line = list(map_data[i])

            # If the line ends with a newline character, remove it.
            if line[-1] == '\n':
                line = line[:-1]

            # Insert a space between each character.
            line = ' '.join(line)
            # Replace the line in the map data with the new line.
            map_data[i] = line

        # Convert the map data to a single string separated by newlines.
        map = '\n'.join(map_data)

        output_string += f'{height} {width}\n{map}\n'

    # Parse the scenario file.
    if not scen_file is None:
        with open(scen_file, 'r') as f:
            scen_data = f.readlines()

        # Skip the first line.
        scen_data = scen_data[1:]

        agent_data = []

        # Extract the start and goal locations for each agent.
        # The start and goal locations are the 5th, 6th, 7th, and 8th tokens on each line.
        for line in scen_data:
            tokens = line.split()
            start_x = int(tokens[5])
            start_y = int(tokens[4])
            goal_x = int(tokens[7])
            goal_y = int(tokens[6])

            single_agent_string = f'{start_x} {start_y} {goal_x} {goal_y}'
            agent_data.append(single_agent_string)


        # Convert the agent data to a single string separated by newlines.
        agent_string = '\n'.join(agent_data)

        num_agents = len(agent_data)

        output_string += f'{num_agents}\n{agent_string}\n'

    # Write the output to the file or return it.
    if not (output_file is None):
        with open(output_file, 'w') as f:
            f.write(output_string)

    return output_string

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert test data from the format used in the CBSH2-RTC repo to the format used in this repo.')
    parser.add_argument('map_file', type=str, help='The path to the file containing the map data.')
    parser.add_argument('scen_file', type=str, help='The path to the file containing the scenario data (aka the data for the agents and their goals).')
    parser.add_argument('--output_file', type=str, help='The path to the file to write the converted test data to.')
    args = parser.parse_args()

    # Check if output_file is None. If it is, print the output to the console.
    if args.output_file is None:
        print(convert_test_data(args.map_file, args.scen_file))
    else:
        convert_test_data(args.map_file, args.scen_file, args.output_file)