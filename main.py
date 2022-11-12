from logging import DEBUG, Logger

from fastapi import FastAPI

from core.plugin_use_case_service import PluginUseCaseService
from utils.file_system import FileSystem
from models.request_body import RequestBody

app = FastAPI()

logger = Logger("MainApp")

options = {'directory': f'{FileSystem.get_plugins_directory()}'}

service = PluginUseCaseService(options)

service.discover_plugins()

instance_plugins = [service.register_plugin(module, logger) for module in service.modules]


def call_plugins(name: str, text: str) -> str:
    for module in instance_plugins:
        result = module.invoke(plugin_name=name, text=text)
        if result is not None:
            return result


@app.get("/")
async def main():
    return {"Hello World!"}


@app.post("/lower")
async def make_lower(body: RequestBody):
    return call_plugins("lower", body.text)


@app.post("/upper")
async def make_upper(body: RequestBody):
    return call_plugins("upper", body.text)
