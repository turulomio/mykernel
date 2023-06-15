
from mangenerator import Man
from mykernel.reusing.file_functions import replace_in_file
from mykernel.reusing.github import download_from_github
from datetime import date
from mykernel.version import __version__
from os import system
from sys import argv
from mykernel.gettext import _



def release():
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

def translate():
        system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o locale/mykernel.pot mykernel/*.py mykernel/objects/*.py")
        system("msgmerge -N --no-wrap -U locale/es.po locale/mykernel.pot")
        system("msgmerge -N --no-wrap -U locale/fr.po locale/mykernel.pot")
        system("msgfmt -cv -o mykernel/locale/es/LC_MESSAGES/mykernel.mo locale/es.po")
        system("msgfmt -cv -o mykernel/locale/fr/LC_MESSAGES/mykernel.mo locale/fr.po")


def mangenerator():
        """
            Create man pages for parameter language
        """
        for language in ["en", "es", "fr"]:
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
            man.paragraph("[cpupower]", 1, True)
            man.paragraph("cpu_hz", 2,  True)
            man.paragraph(_("Number of CPU scaling frequency. Default is maximum scaling frequency. Leave at it is if you don't know what are you doing."), 3)

            man.paragraph("[initramfs]", 1, True)
            man.paragraph("encrypted_root_partition", 2,  True)
            man.paragraph(_("Encrypted partition device name. Empty if there isn't encription in our system."), 3)

            man.paragraph("[grub]", 1, True)
            man.paragraph("efi", 2,  True)
            man.paragraph(_("True if it uses and EFI system with gpt partition table. False if system uses dos partiton with mbr block."), 3)
            
            man.paragraph("boot_directory", 2,  True)
            man.paragraph(_("Path to boot directory. By default /boot."), 3)

            man.paragraph("efi_target", 2,  True)
            man.paragraph(_("Can be one of grub targets for efi. x86_64-efi, i386-pc..."), 3)
            
            man.paragraph("efi_partition", 2,  True)
            man.paragraph(_("Partition name where EFI directory is."), 3)

            man.paragraph("mbr_device", 2,  True)
            man.paragraph(_("Device name where mbr is going to be installed. Only works for none EFI systems."), 3)
            
            
            man.save()

def reusing():
    """
        Actualiza directorio reusing
        poe reusing
        poe reusing --local
    """
    local=False
    if len(argv)==2 and argv[1]=="--local":
        local=True
        print("Update code in local without downloading was selected with --local")
    if local is False:
        download_from_github('turulomio','reusingcode','python/myconfigparser.py', 'mykernel/reusing/')
        download_from_github('turulomio','reusingcode','python/github.py', 'mykernel/reusing/')
        download_from_github('turulomio','reusingcode','python/cpupower.py', 'mykernel/reusing/')
        download_from_github('turulomio','reusingcode','python/datetime_functions.py', 'mykernel/reusing/')
        download_from_github('turulomio','reusingcode','python/casts.py', 'mykernel/reusing/')

    replace_in_file("mykernel/reusing/myconfigparser.py",  "from casts",  "from .casts")
    replace_in_file("mykernel/reusing/myconfigparser.py",  "from datetime_functions",  "from .datetime_functions")
