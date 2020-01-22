from setuptools import setup, Command
import gettext
import os
import site
from platform import system as platform_system

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
        if platform_system()=="Linux":
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

        for language in ["en", "es", "fr"]:
            self.mangenerator(language)

    def mangenerator(self, language):
        """
            Create man pages for parameter language
        """
        from mangenerator import Man
        from datetime import date
        if language=="en":
            lang1=gettext.install('mykernel', 'badlocale')
            man=Man("man/man1/mykernel")
        else:
            lang1=gettext.translation('mykernel', 'mykernel/locale', languages=[language])
            lang1.install()
            man=Man("man/{}/man1/mykernel".format(language))
        print("  - DESCRIPTION in {} is {}".format(language, _("DESCRIPTION")))

        man.setMetadata("mykernel",  1,   date.today(), "Mariano Muñoz", _("Change files and directories owner and permissions recursively."))
        man.setSynopsis("""usage: mykernel [-h] [--version] [--config]""")
        man.header(_("DESCRIPTION"), 1)
        man.paragraph(_("This app has the following mandatory parameters:"), 1)
        man.paragraph("--config", 2, True)
        man.paragraph(_("It writes a config file in /etc/mykernel/mykernel.ini"), 3)
        
        man.header(_("MYKERNEL.INI CONFIGURATION HELP"), 1)
        man.paragraph(_("[cpupower]"), 1, True)
        man.paragraph(_("cpu_hz"), 2,  True)
        man.paragraph(_("Number of CPU scaling frequency. Default is maximum scaling frequency. Leave at it is if you don't know what are you doing."), 3)

        man.paragraph(_("[initramfs]"), 1, True)
        man.paragraph(_("encrypted_root_partition"), 2,  True)
        man.paragraph(_("Encrypted partition device name. Empty if there isn't encription in our system."), 3)

        man.paragraph(_("[grub]"), 1, True)
        man.paragraph(_("efi"), 2,  True)
        man.paragraph(_("True if it uses and EFI system with gpt partition table. False if system uses dos partiton with mbr block."), 3)
        
        man.paragraph(_("boot_directory"), 2,  True)
        man.paragraph(_("Path to boot directory. By default /boot."), 3)
        
        
        man.paragraph(_("efi_target"), 2,  True)
        man.paragraph(_("Can be one of grub targets for efi. x86_64-efi, i386-pc..."), 3)
        
        man.paragraph(_("efi_partition"), 2,  True)
        man.paragraph(_("Partition name where EFI directory is."), 3)

        man.paragraph(_("mbr_device"), 2,  True)
        man.paragraph(_("Device name where mbr is going to be installed. Only works for none EFI systems."), 3)
        
        
        man.save()

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

if platform_system()=="Linux":
    data_files=[('/usr/share/man/man1/', ['man/man1/mykernel.1']), 
                ('/usr/share/man/es/man1/', ['man/es/man1/mykernel.1'])
               ]
else:
    data_files=[]
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
                                        'mykernel=mykernel.mykernel_compile:main',
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
    data_files=data_files,
    include_package_data=True
    )

_=gettext.gettext#To avoid warnings
