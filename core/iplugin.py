
from logging import Logger
from typing import Optional

from core.iplugin_registry import IPluginRegistry
from models.meta import Meta


class IPlugin(object, metaclass=IPluginRegistry):

    meta = Optional[Meta]

    def __init__(self, logger: Logger):
        self.logger = logger

    def invoke(self, **args) -> str:
        pass
