from argparse import ArgumentParser
from datetime import datetime
from multiprocessing import cpu_count
from mykernel.mykernel_initramfs import initramfs
from mykernel.myconfigparser import MyConfigParser
from mykernel.cpupower import sys_set_cpu_max_scaling_freq, sys_get_cpu_max_freq, sys_get_cpu_max_scaling_freq, is_cpufreq_configured
from mykernel.objects.command import command
from mykernel.version import __version__, __versiondate__
from mykernel.gettext import _
from os import environ, system
from sys import exit

def main():
    start=datetime.now()
    parser=ArgumentParser(description=_("My method to compile the Linux kernel"))
    parser.add_argument('--version', action='version', version="{} ({})".format(__version__, __versiondate__))
    parser.add_argument('--config', help=_("Write a config file in /etc/mykernel/mykernel.ini"),  action='store_true',  default=False)
    parser.add_argument('--ccache', help=_("Use ccache to compile"),  action='store_true',  default=False)
    parser.add_argument('--ccache_stats', help=_("Shows ccache statistics"),  action='store_true',  default=False)
    args=parser.parse_args()
    config=MyConfigParser('/etc/mykernel/mykernel.ini')
    
    if is_cpufreq_configured():
        cpu_hz_before=sys_get_cpu_max_scaling_freq()
        cpu_hz=config.get('cpupower','cpu_hz',  str(sys_get_cpu_max_freq()))
        sys_set_cpu_max_scaling_freq(int(cpu_hz))
        
    if args.ccache==True or args.ccache_stats==True:
        environ["PATH"]="/usr/lib/ccache/bin:" + environ["PATH"]
        environ["CCACHE_DIR"]="/var/cache/ccache_mykernel" #Different path of portage due to it has different user permissions
        if args.ccache_stats==True:
            system("ccache -s")
            exit(0)

    efi=config.get("grub", "efi", "True")
    boot_directory =config.get("grub", 'boot_directory', '/boot')
    efi_target=config.get("grub", 'efi_target', 'x86_64-efi')
    efi_partition=config.get("grub", 'efi_partition',  '/dev/sda1')
    mbr_device=config.get("grub", "mbr_device", "")
    
    encrypted_root_partition=config.get("initramfs", 'encrypted_root_partition', '')
    
    if args.config==True: #Writes a config file
        config.save()
        print("You must set your settings in /etc/mykernel/mykernel.ini. Use man mykernel for help.")
        exit(0)

    if encrypted_root_partition!="":
        initramfs(encrypted_root_partition, start, boot_directory)
    command("make -j{}".format(cpu_count()))
    command("make modules_install")
    command("make install")
    command("emerge @module-rebuild --keep-going")

    if efi=="True":#Gpt partition with efi
        command("grub-install --efi-directory={} --target={} {}".format(boot_directory, efi_target, efi_partition))
        command("grub-mkconfig -o {}/grub/grub.cfg".format(boot_directory))
    else:#Dos partition with mbr
        command("grub-install {}".format(mbr_device))
        command("grub-mkconfig -o {}/grub/grub.cfg".format(boot_directory))
    
    if is_cpufreq_configured():
        sys_set_cpu_max_scaling_freq(cpu_hz_before)
    config.save()
    print("Compilation with {} processors took {}".format(datetime.now()-start,  cpu_count()))
