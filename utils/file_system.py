import os.path


class FileSystem:

    @staticmethod
    def get_base_dir() -> str:
        """
        Find the base dir of the project (we asume it's always only one step upwards)
        :return: base dir
        """
        path = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(path, '..')

    @staticmethod
    def get_plugins_directory() -> str:
        base_dir = FileSystem.get_base_dir()
        return os.path.join(base_dir, 'plugins')