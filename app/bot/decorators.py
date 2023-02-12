class CommandMapper(dict):
    def __init__(self, command, name):
        self.action = command
        self[name] = self.action.__name__

    def _map(self, name, func):
        assert name not in self, (
            "Command '%s' has already been mapped to '.%s'." % (name, self[name]))
        assert func.__name__ != self.action.__name__, (
            "Command mapping does not behave like the property decorator. You "
            "cannot use the same command name for each mapping declaration.")

        self[name] = func.__name__

        return func


def bot_command(name: str, description: str, **kwargs):

    def decorator(func):
        func.mapping = CommandMapper(func, name)
        func.name = name
        func.description = description
        func.kwargs = kwargs
        return func

    return decorator
