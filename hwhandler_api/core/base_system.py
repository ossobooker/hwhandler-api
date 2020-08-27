import logging
import yaml
import os
from types import SimpleNamespace

from .system_fsm import FSM

class BaseSystem:
    """Base for a system configuration."""

    def __init__(self, config_file):
        self.config_file = config_file
        self.config = {}
        self.fsm = FSM()

        # system status and error message
        # STATUS == 0 ==> OK
        self.set_system_status(status_code=0, error_message="")

        # setup system
        self.configure()

        # setup fsm
        if self.system_status.status_code == 0:
            self.fsm_config = self.config["fsm"]
            # print(self.fsm_config)
            self.fsm = FSM(
                name="system_fsm",
                states=self.fsm_config["states"],
                transitions=self.fsm_config["transitions"],
                initial_state=self.fsm_config["initial_state"],
                transitions_commands=self.fsm_config["transitions_commands"],
            )

    def set_system_status(self, status_code=0, error_message=""):
        """Set global system status."""
        self.system_status = SimpleNamespace(
            **{"status_code": status_code, "error_message": error_message}
        )

    def configure(self):
        logging.info(
            f"Configuring Hardware Handler. Configuration file: {self.config_file}"
        )

        try:
            # load system config
            with open(self.config_file, "r") as f:
                self.config = yaml.safe_load(f)

            # load commands config
            with open("config_setup/commands/config_commands.yaml", "r") as f:
                self.config.update(yaml.safe_load(f))

            # load monitorables config
            with open("config_setup/monitorables/config_monitorables.yaml", "r") as f:
                self.config.update(yaml.safe_load(f))

            # load fsm config
            with open("config_setup/fsm/config_fsm.yaml", "r") as f:
                self.config.update(yaml.safe_load(f))

        except:
            logging.error(f"Configuration file not found.")
            self.set_system_status(
                status_code=1, error_message="Configuration file not found."
            )
