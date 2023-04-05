import os
import inspect
import importlib

info = {
    "module" : "backend.cache.basecache",
    "fullname" : "Cache"

}
mod = importlib.import_module(info["module"])
if "." in info["fullname"]:
    objname, attrname = info["fullname"].split(".")
    obj = getattr(mod, objname)
    try:
        obj = getattr(obj, attrname)
    except AttributeError:
        print('euu3')
else:
    obj = getattr(mod, info["fullname"])

print(obj)
try:
    file = inspect.getsourcefile(obj)
    lines = inspect.getsourcelines(obj)
    file = os.path.relpath(file, os.path.abspath(".."))
    print(file)
    print(type(file))
    file = file.replace("Terms-and-condition-simplifier/", "")
except TypeError:
    # e.g. object is a typing.Union
    print('euu4')
start, end = lines[1], lines[1] + len(lines[0]) - 1

ff =  f"https://github.com/QuirkyDevil/Terms-and-condition-simplifier/blob/main/{file}#L{start}-L{end}"
print(ff)