from mangenerator import Man
from mykernel.version import __version__
from glob import glob
import subprocess

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
    py_files = glob("mykernel/*.py")
    subprocess.run(["xgettext", "-L", "Python", "--no-wrap", "--no-location", "--from-code=UTF-8", "-o", "mykernel/locale/mykernel.pot", *py_files], check=True)
    subprocess.run(["msgmerge", "-N", "--no-wrap", "-U", "mykernel/locale/es.po", "mykernel/locale/mykernel.pot"], check=True)
    subprocess.run(["msgmerge", "-N", "--no-wrap", "-U", "mykernel/locale/fr.po", "mykernel/locale/mykernel.pot"], check=True)
    subprocess.run(["msgfmt", "-cv", "-o", "mykernel/locale/es/LC_MESSAGES/mykernel.mo", "mykernel/locale/es.po"], check=True)
    subprocess.run(["msgfmt", "-cv", "-o", "mykernel/locale/fr/LC_MESSAGES/mykernel.mo", "mykernel/locale/fr.po"], check=True)



