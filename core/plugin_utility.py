import os
import subprocess
import sys
import yaml
from logging import Logger
from typing import List, Optional
from dacite import from_dict, ForwardReferenceError, UnexpectedDataError, WrongTypeError, MissingValueError
import pkg_resources
from pkg_resources import Distribution

from utils.file_system import FileSystem
from models.dependency_module import DependencyModule
from models.plugin_config import PluginConfig


class PluginUtility:
    __IGNORE_LIST = ['__pycache__']
    _logger: Logger

    def __init__(self, logger: Logger) -> None:
        super().__init__()
        self._logger = logger

    @staticmethod
    def __filter_unwanted_directories(name: str) -> bool:
        return name not in PluginUtility.__IGNORE_LIST

    @staticmethod
    def filter_plugins_paths(plugin_package) -> List[str]:
        """Filters out a list of untwanted directories
        :param plugins_package:
        :return: list of directories
        """
        return list(filter(PluginUtility.__filter_unwanted_directories, os.listdir(plugin_package)))

    @staticmethod
    def __get_missing_packages(installed: List[Distribution], required: Optional[List[DependencyModule]]) -> List[
        DependencyModule]:
        missing = list()
        if required is not None:
            installed_packages: List[str] = [pkg.project_name for pkg in installed]
            for required_pkg in required:
                if not installed_packages.__contains__(required_pkg.name):
                    missing.append(required_pkg)
        return missing

    @staticmethod
    def __load_configuration(name: str = 'configuration.yaml', config_directory: Optional[str] = None) -> dict:
        if config_directory is None:
            #search settings one level up (packages are mostly only one level deep)
            base_dir = FileSystem.get_base_dir()
            config_directory = os.path.join(base_dir, 'settings')
        with open(os.path.join(config_directory, name), encoding='UTF-8') as file:
            input_data = yaml.safe_load(file)
        return input_data

    def __manage_requirements(self, package_name: str, plugin_config: PluginConfig) -> None:
        installed_packages: List[Distribution] = list(
            filter(
                lambda pkg: isinstance(pkg, Distribution), pkg_resources.working_set
            )
        )
        missing_packages = self.__get_missing_packages(installed_packages, plugin_config.requirements)
        for missing in missing_packages:
            self._logger.info(f'Preparing installation of module: {missing} for package: {package_name}')
            try:
                python = sys.executable
                exit_code = subprocess.check_call(
                    [python, '-m', 'pip', 'install', missing.__str__()],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self._logger.info(f'installation of module: {missing} for package: {package_name} returned exit code: {exit_code}')
            except subprocess.CalledProcessError as e:
                self._logger.error(f'Installation of {missing} failed', e)

    def __read_config(self, module_path) -> Optional[PluginConfig]:
        try:
            plugin_config_data = self.__load_configuration('config.yaml', module_path)
            plugin_config = from_dict(data_class = PluginConfig, data=plugin_config_data)
            return plugin_config
        except FileNotFoundError as fnfe:
            self._logger.error('Unable to read Configuration File', fnfe)
        except (NameError, ForwardReferenceError, UnexpectedDataError, WrongTypeError, MissingValueError) as e:
            self._logger.error('Unable to parse Plugin Config to data class', e)
        return None

    def setup_plugin_configuration(self, package_name, module_name) -> Optional[str]:
        """
        Handles configuration of a given package and module
        :param package_name: package of the plugin
        :param module_name: module of the plugin
        :return: a module name to import
        """
        module_path = os.path.join(FileSystem.get_plugins_directory(), module_name)
        if os.path.isdir(module_path):
            self._logger.debug(f'Checking configuration file exists for module: {module_name}')
            plugin_config: Optional[PluginConfig] = self.__read_config(module_path)
            if plugin_config is not None:
                self.__manage_requirements(package_name, plugin_config)
                return plugin_config.runtime.main
            else:
                self._logger.debug(f'No configuration found for module: {module_name}')
        self._logger.debug(f'Module: {module_name} is not a directory, skipping scanning phase')
        return None
