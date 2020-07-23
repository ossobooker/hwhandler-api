from transitions import Machine


class FSM(object):
    # define states
    states = ['halted', 'engaged', 'synchronized', 'configured', 'running', ]

    def __init__(self, name):
        self.name = name
        self.machine = Machine(
            model=self, states=self.states, initial='halted')
        self.machine.add_transition(
            trigger='engage', source='halted', dest='engaged')
        self.machine.add_transition(
            trigger='synchronize_links', source='engaged', dest='synchronized')
        self.machine.add_transition(
            trigger='configure', source='synchronized', dest='configured')
        self.machine.add_transition(
            trigger='start', source='configured', dest='running')
        self.machine.add_transition(
            trigger='stop', source='running', dest='synchronized')

        self.machine.add_transition('reset', '*', 'halted')

    def start(self):
        print("Starting...")


if __name__ == '__main__':
    test_fsm = fsm("test_fsm")
    print(test_fsm.state)
    test_fsm.engage()
    print(test_fsm.state)

