import json

import click

from dialogue_script_reverser.data import Choice, Node
from dialogue_script_reverser.schema import NodeSchema


@click.command()
@click.argument('file_path')
@click.option(
    '-n', 
    '--start-node', 
    required=True, 
    type=int, 
    help='The starting dialogue node.'
)
def reverser(file_path, start_node):
    with open(file_path, 'r') as file_obj:
        graph_data = json.load(file_obj)
    
    node_schema = NodeSchema(many=True)
    nodes_by_id = {n.id: n for n in node_schema.load(graph_data)}
    
    

if __name__ == '__main__':
    reverser()

