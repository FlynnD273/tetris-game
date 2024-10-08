class InputHandler:
    def __init__(self):
        self.hooks = []

    def add_hook(self, hook):
        self.hooks.append(hook)

    def update(self, states):
        for hook in self.hooks:
            hook.do_action(states[hook.key])


class InputHook:
    def __init__(self, key):
        self.key = key

    def do_action(self, state):
        raise NotImplementedError


class OnPressRequireResetHook(InputHook):
    def __init__(self, key, action):
        super().__init__(key)
        self.action = action
        self.checked = False

    def do_action(self, state):
        # If key is down and has not been checked already
        if state and not self.checked:
            self.action()
            self.checked = True

        # If key is released and has been checked
        if not state and self.checked:
            self.checked = False


class OnPressRepeatingHook(InputHook):
    def __init__(self, key, action):
        super().__init__(key)
        self.action = action

    def do_action(self, state):
        if state:
            self.action()


class OnPressRepeatDelayedHook(InputHook):
    def __init__(self, key, action, cycles):
        super().__init__(key)
        self.action = action
        self.delay = cycles
        self.check_count = 0

    def do_action(self, state):
        if state and (self.check_count == 0 or self.check_count > self.delay):
            self.action()
            self.check_count = self.check_count + 1
        elif state:
            self.check_count = self.check_count + 1

        if not state:
            self.check_count = 0
