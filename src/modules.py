# manages applications
import importlib
import json
from os import path, listdir, makedirs

active_module = None
settings = {'modulePath': "applications",
            'indexPath': "tmp/appIndex.json"
}

def build_app_index():
    
    if path.isdir(settings['modulePath']):
        # get all python modules in ModulePath
        app_index = []
        for fName in listdir(settings['modulePath']):
            if ".py" in fName:
                module_name = "applications." + fName.strip(".py")
                module = importlib.import_module(module_name)
                module_info = {
                    'name': module.__name__,
                    'triggers': module.canHandle()
                }
                app_index.append(module_info)
                del module

        if not path.exists(path.dirname(settings['indexPath'])):
            makedirs(path.dirname(settings['indexPath']))

        with open(settings['indexPath'], 'w') as fd:
            fd.write(json.dumps(app_index))

def run_module(name, request):

    module = importlib.import_module(name)
    active_module = module
    res = module.handle(request)
    return res

def provide_input(request):
    active_module.handle(request)

def has_active():
    return active_module != None:

def close_module()
    del module

if __name__ == '__main__':
    build_app_index()