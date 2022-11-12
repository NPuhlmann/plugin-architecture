from typing import List


class IPluginRegistry(type):
    plugins: List[type] = []

    # bases and attr are unuese here, but required for metaclass magic!
    def __init__(cls, name, bases, attr):
        super().__init__(cls)
        if name != "PluginCore":
            IPluginRegistry.plugins.append(cls)
