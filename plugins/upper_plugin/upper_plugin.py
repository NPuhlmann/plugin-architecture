from logging import Logger
from typing import Optional

from core.iplugin import IPlugin
from models.meta import Meta


class UpperPlugin(IPlugin):

    def __init__(self, logger: Logger) -> None:
        super().__init__(logger)
        self.meta = Meta(
            name="Allianz Plugin",
            description="Analysiert die Dokumente der Allianz Versicherung",
            version="0.1"
        )

    def invoke(self, plugin_name: str, text: str) -> Optional[str]:
        if plugin_name == 'upper':
            self.logger.debug(f'{self.meta}: Got following text: {text}')
            return text.upper()
