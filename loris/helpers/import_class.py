from importlib import import_module

def import_class(qname):
    # Imports a class and returns it (the class, not an instance).
    module_name = '.'.join(qname.split('.')[:-1])
    class_name = qname.split('.')[-1]
    module = import_module(module_name)
    return getattr(module, class_name)
