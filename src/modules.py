# manages applications
import importlib
import json
from os import path, listdir

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

        with open(settings['indexPath'], 'w') as fd:
            fd.write(json.dumps(app_index))

if __name__ == '__main__':
    build_app_index()