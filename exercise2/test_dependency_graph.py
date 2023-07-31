import pytest
import os
from exercise2.dependency_graph import DependencyGraph, build_graph


# Define a fixture to setup and teardown test json files
@pytest.fixture(params=[
    ('{"pkg1": ["pkg2", "pkg3"], "pkg2": ["pkg3"], "pkg3": []}', 
     [("pkg1", ["pkg2", "pkg3"]), ("pkg2", ["pkg3"]), ("pkg3", [])]),
    ('{"pkg1": ["pkg2"], "pkg2": ["pkg3"], "pkg3": ["pkg1"]}', 
     [("pkg1", ["pkg2"]), ("pkg2", ["pkg3"]), ("pkg3", ["pkg1"])]),
    ('{"pkg1": [], "pkg2": [], "pkg3": []}', 
     [("pkg1", []), ("pkg2", []), ("pkg3", [])]),
])
def test_file(request):
    filename = '/tmp/test_deps.json'
    content, edges = request.param
    
    with open(filename, 'w') as file:
        file.write(content)

    yield filename, edges  # Test starts here

    os.remove(filename)  # Remove the created test json files after end of test


def test_build_graph(test_file):
    filename, expected_edges = test_file

    # Build the expected graph
    expected = DependencyGraph()
    for pkg, deps in expected_edges:
        expected.add_edge(pkg, deps)

    # Call the function under test
    actual = build_graph(filename)

    # Assert that the actual and expected graphs are the same
    assert actual.graph == expected.graph
