from gettext import translation
from os import path, system
from pkg_resources import resource_filename

def _(s):
    t=translation('mykernel', resource_filename("mykernel","locale"))
    return t.gettext(s)

def kernel_version():
    if path.exists("/usr/src/linux/Makefile"):
       f=open("/usr/src/linux/Makefile")
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
    
def command(s):
    print (s)
    system(s)
