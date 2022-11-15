import os, glob

all_list = list()
for f in glob.glob(os.path.dirname(__file__)+"/*.py"):
    name = os.path.basename(f)[:-3]
    if os.path.isfile(f):
        if ('disabled.' in name) or (os.path.basename(f).startswith('__')):
            continue

        all_list.append(name)
        
__all__ = all_list  