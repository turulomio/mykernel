from argparse import ArgumentParser
from datetime import datetime
from multiprocessing import cpu_count
from mykernel.mykernel_initramfs import initramfs
from mykernel.myconfigparser import MyConfigParser
from mykernel.cpupower import sys_set_cpu_max_scaling_freq, sys_get_cpu_min_freq, sys_get_cpu_max_scaling_freq
from mykernel.objects.command import command
from os import chdir

def main():
    start=datetime.now()
    parser=ArgumentParser("Initramfs generator for luks root partition")
    parser.add_argument('-e', '--encrypted', help='Where encrypted device is', default='/dev/nvme0n1p2')
    args=parser.parse_args()
    print(args)
    config=MyConfigParser('/etc/mykernel/mykernel.ini')
    
    cpu_hz_before=sys_get_cpu_max_scaling_freq()
    cpu_hz=config.get('cpupower','cpu_hz',  str(sys_get_cpu_min_freq()))
    
    efi_directory=config.get("grub", 'efi_directory', '/boot')
    efi_target=config.get('grub', 'efi_target', 'x86_64-efi')
    efi_partition=config.get('grub', 'efi_partition',  '/dev/sda1')
    
    encrypted_root_partition=config.get("initramfs", 'encrypted_root_partition', '')
    
    sys_set_cpu_max_scaling_freq(int(cpu_hz))

    chdir("/usr/src/linux")
    if encrypted_root_partition!="":
        initramfs(encrypted_root_partition, start, efi_directory)
    command("make -j{}".format(cpu_count()))
    command("make modules_install")
    command("make install")
    command("emerge @module-rebuild --keep-going")

    command("grub-install --efi-directory={} --target={} {}".format(efi_directory, efi_target, efi_partition))
    command("grub-mkconfig -o {}/grub/grub.cfg".format(efi_directory))
    
    sys_set_cpu_max_scaling_freq(cpu_hz_before)
    config.save()
    print("Compilation with {} processors took {}".format(datetime.now()-start,  cpu_count()))
##!/bin/bash
#if [ $# -ne 0 ]
#then
#  echo "Programa que ayuda a la compilación de un nuevo kernel en Gentoo"
#  echo "Se debe copiar el .config en el nuevo directorio y hacer # make oldconfig"
#  echo "Después se debe ejecutar: # compile.kernel"
#  echo "Si la particion boot no es la sda1 y la luks la sda4, debes cambiar este script"
#fi


