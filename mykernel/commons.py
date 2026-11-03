from gettext import translation
from pathlib import Path
from importlib.resources import files
from sys import exit

def _(s):
    t=translation('mykernel', files("mykernel") /"locale")
    return t.gettext(s)

def kernel_version():
    makefile = Path("/usr/src/linux/Makefile")
    if makefile.exists():
        with open(makefile) as f:
            f.readline()
            version=f.readline().split(" = ")[1].strip()
            subversion=f.readline().split(" = ")[1].strip()
            subsubversion=f.readline().split(" = ")[1].strip()
            subsubsubversion=f.readline().split(" = ")[1].strip()
            s="{}.{}.{}{}".format(version,subversion,subsubversion,subsubsubversion)
    else:
        print ("Version not detected")
        exit(255)
    return s


