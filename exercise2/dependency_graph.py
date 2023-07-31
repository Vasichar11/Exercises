import json
from collections import defaultdict


# 2.2) Reconstruct full dependency graph
class DependencyGraph:
    def __init__(self):
        # Will automatically create new lists for the keys that are not yet of the dictionary
        self.graph = defaultdict(list)

    # Function to add edge for package's dependencies
    def add_edge(self, pkg, deps):
        # If package not in graph, a new list is automatically created with the dependencies
        self.graph[pkg].extend(deps)

    # Function to print graph to console
    def display_graph(self, pkg, indent=0):
        # Required whitespaces plus package print
        print('  ' * indent + '- ' + pkg)
        for dep in self.graph[pkg]:
            # Recursively print next dependencies with increased indentation
            self.display_graph(dep, indent + 1)


def build_graph(filename):

    # 2.1) Read json data
    with open(filename, 'r') as file:
        data = json.load(file)

    # Create instance of a Dependency Graph (DG)
    DG = DependencyGraph()

    for pkg, deps in data.items():
        DG.add_edge(pkg, deps)

    return DG


def main():

    # Fixed location in the filesystem
    filename = '/tmp/deps.json'

    # 2.3) Function that takes a filename and returns an object representing the fully resolved graph
    DG = build_graph(filename)

    # 2.4) Display graph when executed
    for pkg in DG.graph:
        DG.display_graph(pkg)
