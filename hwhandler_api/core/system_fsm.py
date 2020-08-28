from transitions import Machine

# import importlib


class FSM:
    def __init__(
        self,
        name="",
        states=["no_state"],
        transitions=[],
        initial_state="no_state",
        transitions_commands=[],
    ):
        self.name = name

        # define states and transitions
        self.states = states
        self.transitions = transitions
        self.initial_state = initial_state

        # define state machine
        self.machine = Machine(
            model=self,
            states=self.states,
            transitions=self.transitions,
            initial=self.initial_state,
            ignore_invalid_triggers=True,
            auto_transitions=False,
        )

        # set transition commands
        # self.do_dummy = config_setup.fsm.do_dummy.do_dummy

        # if self.state != "no_state":
        #     for tc in transitions_commands:
        #         command_module = importlib.import_module(f"config_setup.fsm.{tc}")
        #         command_obj = getattr(command_module, tc)
        #         setattr(self, tc, command_obj)
        #     # self.do_dummy().exec_command()
        # # print(dir(self))
        # # print(self.machine.get_triggers(self.state))

    def available_transitions(self):
        """Return the available transitions for the current state."""
        return self.machine.get_triggers(self.state)


if __name__ == "__main__":
    test_fsm = FSM(name="test_fsm")
    print(test_fsm.state)
