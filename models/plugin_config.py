from dataclasses import dataclass
from typing import List, Optional

from models.dependency_module import DependencyModule


@dataclass
class PluginRuntimeOption(object):
    main:str
    test: Optional[List[str]]

@dataclass
class PluginConfig:
    name: str
    alias: str
    creator: str
    runtime: PluginRuntimeOption
    repository: str
    description: str
    version: str
    requirements: Optional[List[DependencyModule]]
