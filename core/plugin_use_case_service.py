import os.path
from importlib import import_module
from logging import Logger, DEBUG
from typing import List, Dict, Any

from core.iplugin import IPlugin
from core.iplugin_registry import IPluginRegistry
from core.plugin_utility import PluginUtility


class PluginUseCaseService:
    _logger: Logger
    modules: List[type]

    def __init__(self, options: Dict) -> None:
        self._logger = Logger(self.__module__, DEBUG)
        self.plugins_package: str = options['directory']
        self.plugin_util = PluginUtility(self._logger)
        self.modules = []

    @staticmethod
    def register_plugin(module: type, logger: Logger) -> IPlugin:
        return module(logger)

    @staticmethod
    def hook_plugin(plugin: IPlugin):
        return plugin.invoke

    def __check_loaded_plugin_state(self, plugin_module: Any):
        if len(IPluginRegistry.plugins) > 0:
            latest_module = IPluginRegistry.plugins[-1]
            latest_module_name = latest_module.__module__
            current_module_name = plugin_module.__name__
            if current_module_name == latest_module_name:
                self._logger.debug('Successfully imported module `%s`', current_module_name)
                self.modules.append(latest_module)
            else:
                self._logger.error('Expected to import %s got  %s', current_module_name, latest_module_name)
            IPluginRegistry.plugins.clear()
        else:
            self._logger.error('No Plugin found in registry for module: %s', plugin_module)

    def __search_for_plugins_in(self, plugins_paths: List[str], package_name: str) -> None:
        for directory in plugins_paths:
            entry_point = self.plugin_util.setup_plugin_configuration(package_name, directory)
            if entry_point is not None:
                plugin_name, plugin_ext = os.path.splitext(entry_point)
                import_target_module = f'.{directory}.{plugin_name}'
                module = import_module(import_target_module, package_name)
                self.__check_loaded_plugin_state(module)
            else:
                self._logger.debug('No valid plugin found in %s',package_name)

    def discover_plugins(self) -> None:
        """
        Discover plugins classes, given a list of directory names to scan for.
        """
        self.modules.clear()
        IPluginRegistry.plugins.clear()
        self._logger.debug(f'Searching for plugins under: {self.plugins_package}')
        plugins_paths = PluginUtility.filter_plugins_paths(self.plugins_package)
        package_name = os.path.basename(os.path.normpath(self.plugins_package))
        self.__search_for_plugins_in(plugins_paths, package_name)
