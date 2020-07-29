import logging
import yaml
import requests
import os
from types import SimpleNamespace

from .system_fsm import FSM


class BaseSystem():
    '''Base for a system configuration.'''

    def __init__(self, config_file):
        self.config_file = config_file
        self.config = {}
        self.fsm = FSM()

        # system status (0 is OK) and error message
        self.set_system_status(status_code=0, error_message='')

        # setup system
        self.configure()

        # setup fsm 
        if self.system_status.status_code == 0:
          self.fsm_config = self.config['fsm']
          # print(self.fsm_config)
          self.fsm = FSM(
            name = 'system_fsm', 
            states = self.fsm_config['states'],
            transitions = self.fsm_config['transitions'],
            initial_state = self.fsm_config['initial_state'],
            transitions_commands=self.fsm_config['transitions_commands']
          )

    def set_system_status(self, status_code=0, error_message=''):
      '''Set global system status.'''
      self.system_status = SimpleNamespace(**{'status_code': status_code, 'error_message': error_message})
         

    def download_setup_files(self):
        '''Download setup file for system configuration.'''
        logging.info(f"Downloading setup files from {self.config['git_repository']}")
        os.system("rm -rf config_setup ; mkdir config_setup")
        download_url = f"{self.config['git_repository']}/{self.config['repo_project_name']}/-/jobs/artifacts/{self.config['repo_branch_name']}/raw/config_setup.tar.gz?job=build"
        # download_url = f"https://gitlab.cern.ch/rpcos4ph2setups/{self.config['repo_project_name']}/-/jobs/artifacts/{self.config['repo_branch_name']}/raw/config_setup.tar.gz?job=build"
        r = requests.get(download_url, allow_redirects=True, timeout=30)
        open('config_setup/config_setup.tar.gz', 'wb').write(r.content)
        os.system("cd config_setup/ ; tar -zxf config_setup.tar.gz ; rm -rf config_setup.tar.gz")

    def configure(self):
        logging.info(f'Configuring Hardware Handler. Configuration file: {self.config_file}')
        request_config_file = requests.get(self.config_file, timeout=10)
        if request_config_file.status_code == 200:
            # load system config
            self.config = yaml.safe_load(request_config_file.text)
            self.download_setup_files()
            # load commands config
            with open('config_setup/commands/config_commands.yaml', 'r') as f:
              self.config.update(yaml.safe_load(f))
            # load monitorables config
            with open('config_setup/monitorables/config_monitorables.yaml', 'r') as f:
              self.config.update(yaml.safe_load(f))
            # load fsm config
            with open('config_setup/fsm/config_fsm.yaml', 'r') as f:
              self.config.update(yaml.safe_load(f))
        else:
            logging.error(f'Configuration file not found.')
            self.set_system_status(status_code=1, error_message='Configuration file not found.')
            