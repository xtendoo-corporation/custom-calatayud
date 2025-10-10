from importlib import import_module as _import_module

for _mod in ("product_attribute", "product_template"):
    _import_module('.' + _mod, __package__)
