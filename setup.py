from setuptools import setup, Command
import datetime
import gettext
import os
import platform
import site

gettext.install('mykernel', 'mykernel/locale')

class Procedure(Command):
    description = "Create/update doxygen documentation in doc/html"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(_("New Release:"))
        print(_("  * Change version and date in version.py"))
        print(_("  * Edit Changelog in README"))
        print("  * python setup.py doc")
        print("  * mcedit locale/es.po")
        print("  * python setup.py doc")
        print("  * python setup.py install")
        print("  * git commit -a -m 'mykernel-{}'".format(__version__))
        print("  * git push")
        print(_("  * Make a new tag in github"))
        print("  * python setup.py uninstall")
        print(_("  * Create a new gentoo ebuild with the new version"))
        print(_("  * Upload to portage repository")) 

class Uninstall(Command):
    description = "Uninstall installed files with install"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if platform.system()=="Linux":
            os.system("rm -Rf {}/mykernel*".format(site.getsitepackages()[0]))
            os.system("rm /usr/bin/mykernel*")
        else:
            print(_("Uninstall command only works in Linux"))

class Doc(Command):
    description = "Update man pages and translations"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o locale/mykernel.pot *.py mykernel/*.py mykernel/objects/*.py")
        os.system("msgmerge -N --no-wrap -U locale/es.po locale/mykernel.pot")
        os.system("msgmerge -N --no-wrap -U locale/fr.po locale/mykernel.pot")
        os.system("msgfmt -cv -o mykernel/locale/es/LC_MESSAGES/mykernel.mo locale/es.po")
        os.system("msgfmt -cv -o mykernel/locale/fr/LC_MESSAGES/mykernel.mo locale/fr.po")

class Reusing(Command):
    description = "Download modules from https://github.com/turulomio/reusingcode/"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from sys import path
        path.append("mykernel")
        from github import download_from_github
        download_from_github('turulomio','reusingcode','python/myconfigparser.py', 'mykernel')
        download_from_github('turulomio','reusingcode','python/github.py', 'mykernel')
        download_from_github('turulomio','reusingcode','python/cpupower.py', 'mykernel')
        download_from_github('turulomio','reusingcode','python/datetime_functions.py', 'mykernel')

    ########################################################################


## Version of modele captured from version to avoid problems with package dependencies
__version__= None
with open('mykernel/version.py', encoding='utf-8') as f:
    for line in f.readlines():
        if line.find("__version__ =")!=-1:
            __version__=line.split("'")[1]

setup(name='mykernel',
    version=__version__,
    description='Change files and directories permisions and owner recursivily from current directory',
    long_description="Project web page is in https://github.com/turulomio/mykernel",
    long_description_content_type='text/markdown',
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: System Administrators',
                 'Topic :: System :: Systems Administration',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Programming Language :: Python :: 3',
                ],
    keywords='change permissions ownner files directories',
    url='https://github.com/turulomio/mykernel',
    author='turulomio',
    author_email='turulomio@yahoo.es',
    license='GPL-3',
    packages=['mykernel'],
    entry_points = {'console_scripts': [
                                        'mykernel_compile=mykernel.mykernel_compile:main',
                                       ],
                   },
    install_requires=['colorama','setuptools'],
    cmdclass={
               'doc': Doc,
               'uninstall': Uninstall,
               'procedure': Procedure,
               'reusing': Reusing,
             },
    zip_safe=False,
    include_package_data=True
    )

_=gettext.gettext#To avoid warnings
