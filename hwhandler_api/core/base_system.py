import logging
import yaml
import requests
import os

from hwhandler_api.fsm import FSM


class BaseSystem():
    '''Base for a system configuration.'''

    def __init__(self, config_file):
        self.config_file = config_file
        self.config = {}
        self.fsm = None

        # setup system
        self.configure()
        

    def download_setup_files(self):
        '''Download setup file for system configuration.'''
        logging.info(f"Downloading setup files from {self.config['git_repository']}")
        os.system("rm -rf config_setup ; mkdir config_setup")
        download_url = f"{self.config['git_repository']}/{self.config['repo_project_name']}/-/jobs/artifacts/{self.config['repo_branch_name']}/raw/config_setup.tar.gz?job=build"
        # download_url = f"https://gitlab.cern.ch/rpcos4ph2setups/{self.config['repo_project_name']}/-/jobs/artifacts/{self.config['repo_branch_name']}/raw/config_setup.tar.gz?job=build"
        r = requests.get(download_url, allow_redirects=True)
        open('config_setup/config_setup.tar.gz', 'wb').write(r.content)
        os.system("cd config_setup/ ; tar -zxf config_setup.tar.gz ; rm -rf config_setup.tar.gz")

    def configure(self):
        logging.info(f'Configuring Hardware Handler. Configuration file: {self.config_file}')
        request_config_file = requests.get(self.config_file)
        if request_config_file.status_code == 200:
            self.config = yaml.safe_load(request_config_file.text)
            self.download_setup_files()
        else:
            logging.error(f'Configuration file not found.')
            exit()
            