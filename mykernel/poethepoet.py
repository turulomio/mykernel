from mangenerator import Man
from mykernel.reusing.github import download_from_github
from datetime import date
from mykernel.version import __version__
from os import system
from sys import argv
from mykernel.commons import _

def release():
    print("""Nueva versión:
  * Crear un nuevo issue en github con el nombre myemerge-NUEVAVERSION
  * Copiar el codigo de github para cambiar de versión y pegarlo en la consola
  * Cambiar la version en pyproject.toml
  * Cambiar la versión y la fecha en version.py
  * Vuelve a ejecutar poe release
  * Modificar el Changelog README.md
  * poe translate
  * mcedit locale/es.po
  * poe translate
  * git commit -a -m 'mykernel-{0}'
  * git push
  * Hacer un pull request con los cambios a master
  * Hacer un nuevo tag en GitHub
  * git checkout master
  * git pull
  * poetry build
  * poetry publish
  * Crea un nuevo ebuild en Gentoo con la nueva versión
  * Subelo al repositorio myportage
""".format(__version__))

def translate():
        system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o mykernel/locale/mykernel.pot mykernel/*.py")
        system("msgmerge -N --no-wrap -U mykernel/locale/es.po mykernel/locale/mykernel.pot")
        system("msgmerge -N --no-wrap -U mykernel/locale/fr.po mykernel/locale/mykernel.pot")
        system("msgfmt -cv -o mykernel/locale/es/LC_MESSAGES/mykernel.mo mykernel/locale/es.po")
        system("msgfmt -cv -o mykernel/locale/fr/LC_MESSAGES/mykernel.mo mykernel/locale/fr.po")

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

