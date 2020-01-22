from gettext import translation
from pkg_resources import resource_filename

def _(s):
    t=translation('mykernel', resource_filename("mykernel","locale"))
    return t.gettext(s)
