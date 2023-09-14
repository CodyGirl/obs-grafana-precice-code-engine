from tree import Tree
import pandas as pd
from getConfigs import Configuration

config_file_path = ".config"
config = Configuration(config_file_path)

ORG = config.org
tree = Tree([],[])

def extract_edges():
    df = readFile("dependencyFile.json")
    for item in df.itertuples():
        repo = item[1]
        createNode(repo, True, "")
        for dep in item[2]:
            edge = {}
            depName = dep['depName'].split('/')[-1]
            createNode(depName, False, dep['sourceUrl'])
            edge['id'] = repo + depName
            edge['source'] = repo
            edge['target'] = depName
            createEdge(edge)

def readFile(filename):
    df = pd.read_json(filename)
    return df

def createNode(repo, isPreciceRepo, url):
    global tree
    if isPreciceRepo:
        url = "https://github.com/"+ ORG + '/' + repo
    node = {'id': repo, 'title': repo, 'url': url}
    if node_present(node) == False:
        tree.add_node(node)

def node_present(node):
    present = False
    global tree
    for tree_node in tree.get_nodes():
        if node['id'] == tree_node['id']:
            present = True
            break
    return present

def createEdge(edge):
    global tree
    if edge_present(edge) == False:
        tree.add_edge(edge)

def edge_present(edge):
    present = False
    global tree
    for tree_edge in tree.get_edges():
        if edge['source'] == tree_edge['source'] and edge['target'] == tree_edge['target']:
            present = True
            break
    return present

def calcNodeDegree():
    global tree
    nodes = tree.get_nodes()
    edges = tree.get_edges()
    for node in nodes:
        node['degree'] = 0
        for edge in edges:
            if (node['id'] == edge['source'] or node['id'] == edge['target']) and node['degree'] < 30:
                node['degree'] += 1
    tree.set_nodes(nodes)

def getCategories():
    global tree
    categories = []
    nodes = tree.get_nodes()
    for node in nodes:
        if node['degree'] == 0:
            node['color'] = '#ffbb33'
            categories.append({'name': 'No Dependency'})
        elif node['degree'] <= 5:
            node['color'] = '#99ccff'
            categories.append({'name': 'Less than 5 dependencies'})
        elif node['degree'] <= 10:
            node['color'] = '#ff8080'
            categories.append({'name': '5 to 10 dependencies'})
        elif node['degree'] <= 20:
            node['color'] = '#86c89b'
            categories.append({'name': '10 to 20 dependencies'})
        elif node['degree'] > 20:
            node['color'] = '#71669e'
            categories.append({'name': 'More than 20 dependencies'})
    tree.set_nodes(nodes)
    return categories

def filter_edges(repo, edges):
    filtered_edges = []
    for item in edges:
        if item['source'] == repo or item['target'] == repo:
            filtered_edges.append(item)
    edges = filtered_edges
    return edges

def filter_nodes(repo, tree):
    filtered_nodes = []
    for item in tree['nodes']:
        if any(edge['source'] == item['id'] or edge['target'] == item['id'] for edge in tree['edges']):
            filtered_nodes.append(item)
        if len(tree['edges']) == 0 and item['id'] == repo:
            filtered_nodes.append(item)
    return filtered_nodes

def filter_tree_data(repo, input_tree):
    input_tree['edges'] = filter_edges(repo, input_tree['edges'])
    input_tree['nodes'] = filter_nodes(repo, input_tree)
    if len(input_tree['edges']) == 0:
        input_tree['edges'].append({'id': 'default', 'source': 'default', 'target': 'default'})
    return input_tree

def getTree():
    extract_edges()
    calcNodeDegree()
    categories = getCategories()
    global tree
    tree_object = {}
    tree_object['nodes'] = tree.get_nodes()
    tree_object['edges'] = tree.get_edges()
    tree_object['categories'] = categories
    return tree_object