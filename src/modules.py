# manages applications
import importlib
from os import path listdir

settings = {'ModulePath': "../modules"}

def build_app_index():
    if path.isdir(settings['ModulePath']):
        # get all python modules in ModulePath
        app_index = []
        for path in listdir(settings['ModulePath'])
            if ".py" in path:
                module = importlib.import_module(path)
                module_info = {
                    'name': module.__name__
                    'triggers': module.canHandle()

                }
                app_index.append()
                