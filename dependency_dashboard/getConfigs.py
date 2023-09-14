import configparser
import os

class Configuration():
    def __init__(self, configfilepath):
        config = configparser.ConfigParser()
        config.read(configfilepath)

        try:
            self.github_rest_api = config['GITHUB']['github_rest_api']
            self.github_graphql_api = config['GITHUB']['github_graphql_api']
            self.org = config['GITHUB']['org']
            self.gtoken = os.environ.get('GTOKEN')
            self.workflow_filename = config['GITHUB']['workflow_filename']
        
        except:
            print("Configurations could not be fetched properly!")
            raise
