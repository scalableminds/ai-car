import pkgutil
import inspect

__all__ = []

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    try:
        module = loader.find_module(name).load_module(name)

        for name, value in inspect.getmembers(module):
            if name.startswith('__'):
                continue

            globals()[name] = value
            __all__.append(name)
    except ImportError as e:
        print("Could not import", name)
        print(e)
        pass
