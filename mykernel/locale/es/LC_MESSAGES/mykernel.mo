��          �      l      �  )   �  3        ?     \      y  :   �     �  P   �  O   2  5   �     �  %   �     �  {     &   �  )   �     �  0   �  j   !  1   �  j  �  0   )  8   Z  $   �      �  %   �  G   �     G  c   T  W   �  B   	  ,   S	  +   �	     �	  �   �	  5   J
  +   �
     �
  ?   �
  �     ?   �                                                    	                   
                             * Change version and date in version.py   * Create a new gentoo ebuild with the new version   * Edit Changelog in README   * Make a new tag in github   * Upload to portage repository Can be one of grub targets for efi. x86_64-efi, i386-pc... DESCRIPTION Device name where mbr is going to be installed. Only works for none EFI systems. Encrypted partition device name. Empty if there isn't encription in our system. It writes a config file in /etc/mykernel/mykernel.ini MYKERNEL.INI CONFIGURATION HELP My method to compile the Linux kernel New Release: Number of CPU scaling frequency. Default is maximum scaling frequency. Leave at it is if you don't know what are you doing. Partition name where EFI directory is. Path to boot directory. By default /boot. Shows ccache statistics This app has the following mandatory parameters: True if it uses and EFI system with gpt partition table. False if system uses dos partiton with mbr block. Write a config file in /etc/mykernel/mykernel.ini Project-Id-Version: mykernel
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2020-04-13 21:21+0200
Last-Translator: Turulomio <turulomio@yahoo.es>
Language-Team: Spanish <kde-i18n-doc@kde.org>
Language: es
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=(n != 1);
X-Generator: Lokalize 19.12.3
   * Cambiar la versión y la fecha en version.py   * Crea un nuevo ebuild de Gentoo con la nueva versión   * Modificar el Changelog en README   * Hacer un nuevo tag en GitHub   * Subelo al repositorio del portage Puede ser uno de los objetivos de grub para efi. x86_64-efi, i386-pc... DESCRIPCIÓN Nombre del dispositivo donde el mbr va a ser instalado. Solo funciona para sistemas que no son EFI. Nombre del dispostivo de la partición cifrada. Vacío si no hay cifrado en tu sistema. Escribe un fichero de configuración en /etc/mykernel/mykernel.ini AYUDA PARA LA CONFIGURACIÓN DE MYKERNEL.INI Mi método para compilar el kernel de Linux Nueva versión: Número de la frequencia de escalado de la CPU. El valor por defecto es su valor máximo. Déjalo como está si no sabes que estás haciendo. Nombre de la partición donde está el directorio EFI Ruta al directorio boot. Por defecto /boot. Muestra estadísticas de ccache Esta aplicación tiene los siguientes parámetros obligatorios: Verdadero si tienes un sistema EFE con una tabla de particiones gpt. False si el sistema usa una partición dos con un bloque mbr. Escribe un fichero de configuración /etc/mykernel/mykernel.ini 