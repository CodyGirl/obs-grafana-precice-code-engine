import requests
import json
from requests.adapters import HTTPAdapter
import pandas as pd
import multiprocessing
import os
from getConfigs import Configuration

config_file_path = ".config"
config = Configuration(config_file_path)

URL = config.github_rest_api
ORG = config.org
GTOKEN = config.gtoken
WORKFLOW = config.workflow_filename

s = requests.Session()
s.mount('https://',HTTPAdapter(pool_connections = 50))

def get_default_branch_states():
    repo = []
    branch_states = []
    df = pd.read_json('dependencyFile.json')
    for item in df.itertuples():
        repo.append(item[1])
    with multiprocessing.Pool() as pool:
        for i, result in enumerate(pool.map(get_default_branch_state, repo)):
            state = result
            branch_states.append({'repo': repo[i], 'state': state})
    return branch_states

def get_default_branch_state(repo):
    state = None
    api = URL + ORG + '/' + repo
    response = call_github_rest_api(api)
    if response is not None:
        response = response.json()
        branch = response['default_branch']
        api = "https://github.com/" + ORG + "/" + repo + "/actions/workflows/" + WORKFLOW + "/badge.svg?branch=" + branch
        response = s.get(api)
    #     response = call_github_rest_api(api + '/commits/' + branch + '/status')
        if response.status_code == 200 and response is not None:
            response = response.text
            state = True if "passing" in response else False
    return state

def call_github_rest_api(api):
    response = s.get(api, headers = {"Authorization": "Bearer "+ GTOKEN, "Accept": "application/vnd.github+json", "X-Github-Api-Version": "2022-11-28"})
    if response.status_code == 200:
        return response
    else:
        return None

