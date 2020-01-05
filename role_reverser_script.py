from datetime import datetime
import json
from typing import List, Mapping

import click

from dialogue_script_role_reverser.base64 import base64_gen
from dialogue_script_role_reverser.data import Choice, Node
from dialogue_script_role_reverser.schema import NodeSchema


def node_contains_valid_choices(node: Node):
    return node.choices and any(choice.target for choice in node.choices)


def print_options(node: Node, nodes: Mapping[str, Node]):
    print(f'Given that the player has said "{node.npc}\n"')
    print('Which of the following would you like the NPC to say?\n')
    
    for number, choice in enumerate(node.choices, 1):
        if choice.target:
            target_node = nodes[choice.target]
            print(
                f'{number}. "{choice.player}" ' 
                f'to which the player replies "{target_node.npc}"\n'
            )
    

def prompt_option(node: Node) -> Choice:
    while True:
        number_input = input('Enter a number or the word "done" to finish.\n')
        
        if number_input.lower() == 'done':
            return None

        try:
            return node.choices[int(number_input) - 1]
        except ValueError:
            print(f'Error: {number_input} is not a valid integer.')
        except IndexError:
            print(f'Error: {number_input} doesn\'t identify a choice.')


def reverse_roles(starting_choice: Choice, nodes: Mapping[str, Node]) -> List[Node]:
    id_generator = base64_gen()

    target_node = nodes[starting_choice.target]
    next_id = next(id_generator)

    while target_node.choices and any(c.target for c in target_node.choices):
        print_options(target_node, nodes)
        choice = prompt_option(target_node)
        if choice is None:
            break
            
        target_node = nodes[choice.target]
        new_node = Node(npc=choice.player, id=next_id, choices=[])
        next_id = next(id_generator)
        new_node.choices = [Choice(player=target_node.npc, target=next_id)]
        yield new_node
    
    print('The chosen node has no choices. Finishing up...')


@click.command()
@click.argument('file_path')
@click.option(
    '-n', 
    '--start-node-id', 
    required=True, 
    type=str, 
    help='The starting dialogue node.'
)
@click.option(
    '-c', 
    '--start-choice-num', 
    required=True, 
    type=int, 
    help=(
        'The dialogue choice from the starting node. '
        'This becomes the NPC text of the first node in the derived script.'
    )
)
def reverser(file_path, start_node_id, start_choice_num):
    with open(file_path, 'r') as file_handle:
        graph_data = json.load(file_handle)
    
    node_schema = NodeSchema(many=True)
    nodes_by_id = {n.id: n for n in node_schema.load(graph_data)}
    
    starting_choice = nodes_by_id[start_node_id].choices[start_choice_num]
    derived_nodes = list(reverse_roles(starting_choice, nodes_by_id))

    now = datetime.now().strftime('%Y-%m-%d_%H%M')
    new_file_path = f'{file_path}_role-reversed_{now}.json'
    print(f'Saving derived graph to {new_file_path}...')
    with open(new_file_path, 'w') as file_handle:
        file_handle.write(node_schema.dumps(derived_nodes))
        

if __name__ == '__main__':
    reverser()

