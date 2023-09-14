import requests
import json
from getConfigs import Configuration

config_file_path = ".config"
config = Configuration(config_file_path)

URL = config.github_graphql_api
ORG = config.org
GTOKEN = config.gtoken

def callGitHubAPI(body):
    response = requests.post(url=URL, json={"query": body}, headers={"Authorization":"Bearer " + GTOKEN,"Accept":"application/vnd.github.hawkgirl-preview+json"})
    if response.status_code == 200:
        return response.json()
    return None

def getRepoList():
    body = """
    {
        repositoryOwner(login:"""+"\"" +ORG+"\"" +"""){
            repositories(first: 100) {
                totalCount
                nodes {
                name
                repo_url: url
                }
            }
        }
    }
    """
    repoList = callGitHubAPI(body)
    return repoList

def getDependencyList(repo):
    body = """
    {
        repository(owner:\"""" + ORG + """\", name:\"""" + repo + """\") {
            dependencyGraphManifests {
            totalCount
            nodes {
                filename
                dependencies{
                totalCount
                nodes{
                    packageName
                    repository{
                    url
                    name
                    }
                }
                }
            }
            }
        }
    }"""
    dependencyList =  callGitHubAPI(body)
    return dependencyList

def extractFlatDependencyList(dependencyList):
    flatDepList = []
    for node in dependencyList['data']['repository']['dependencyGraphManifests']['nodes']:
        dataSource = node['filename']
        for dep in node['dependencies']['nodes']:
            depName = dep['packageName']
            sourceUrl = dep['repository']['url'] if dep['repository'] is not None else ""
            flatDepList.append({'dataSource': dataSource, 'depName': depName, 'sourceUrl': sourceUrl})
    return flatDepList

def createDependencyFile():
    open('dependencyFile.json','w').close()
    fileHandler = open('dependencyFile.json','a+')
    fileHandler.write('[')
    repoList = getRepoList()['data']['repositoryOwner']['repositories']['nodes']
    sizeRepoList = len(repoList)
    separatorIndex = 0
    for repo in repoList:
        separatorIndex += 1
        fileHandler.write('{')
        depList = extractFlatDependencyList(getDependencyList(repo['name']))
        fileHandler.write('"repo": ' + json.dumps(repo['name'], indent = 4) + ',')
        fileHandler.write('"deps": ' + json.dumps(depList, indent = 4))
        fileHandler.write('}')
        if separatorIndex != len(repoList):
            fileHandler.write(',')
    
    fileHandler.write(']')
    fileHandler.close()
    return repoList