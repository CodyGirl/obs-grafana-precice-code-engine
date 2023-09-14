from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
from dependencyExtraction import createDependencyFile
from createTree import getTree, filter_tree_data
from branchInfo import get_default_branch_states
import json

app = Flask(__name__)
CORS(app)

@app.route("/createDependencyList", methods = ["GET"])
@cross_origin(origin = '*')
def createDependencyList():
    repo_list = createDependencyFile()
    return Response(json.dumps(repo_list), mimetype = 'application/json')

@app.route("/getDependencyTree", methods = ["GET"])
@cross_origin(origin = '*')
def getDependencyTree():
    repo = request.args.get('node')
    tree = getTree()
    if repo != 'All' or repo == '':
        tree = filter_tree_data(repo, tree)
    return Response(json.dumps(tree), mimetype = 'application/json')

@app.route("/getBranchStates", methods = ["GET"])
@cross_origin(origin = '*')
def getGitHubBranchStates():
    branch_states = get_default_branch_states()
    return Response(json.dumps(branch_states), mimetype = 'application/json')

@app.route("/nodes", methods = ["GET"])
@cross_origin(origin = '*')
def getNodeList():
    tree = getTree()
    return Response(json.dumps([node['id'] for node in tree['nodes']]), mimetype = 'application/json')

if __name__ == '__main__':
    app.run(debug = True, host = "0.0.0.0")