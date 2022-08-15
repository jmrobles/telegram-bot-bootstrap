import enum

class FSM():

    def __init__(self, states: enum.Enum, transitions, start_state, actions=None):

        self.states = states
        self.transitions = transitions
        self.current_state = start_state
        self.actions = actions

    def step(self, event: int):
        """
        Step the FSM forward one step.
        """
        if event in self.transitions[self.current_state]:
            self.current_state, action = self.transitions[self.current_state][event]
            if action:
                action()
    
    def bind_actions(self, actions):
        """
        Bind actions to the FSM.
        """
        self.actions = actions
