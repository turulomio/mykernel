from argparse import ArgumentParser
from datetime import datetime
from multiprocessing import cpu_count
from mykernel.mykernel_initramfs import initramfs
from mykernel.config import ConfigFile
from pycpufreq import sys_set_cpu_max_scaling_freq, sys_get_cpu_max_scaling_freq, is_cpufreq_configured
from mykernel.commons import kernel_version, _
from mykernel.version import __version__, __versiondate__
from os import environ, chdir
from sys import exit
import subprocess


def main():
    start=datetime.now()
    parser=ArgumentParser(description=_("My method to compile the Linux kernel"))
    parser.add_argument('--version', action='version', version="{} ({})".format(__version__, __versiondate__))
    parser.add_argument('--config', help=_("Write a config file in /etc/mykernel/mykernel.ini"),  action='store_true',  default=False)
    parser.add_argument('--ccache_stats', help=_("Shows ccache statistics"),  action='store_true',  default=False)
    args=parser.parse_args()
    config=ConfigFile('/etc/mykernel/mykernel.ini')
    
    
    environ["PATH"]="/usr/lib/ccache/bin:" + environ["PATH"]
    environ["CCACHE_DIR"]="/var/cache/ccache_mykernel" #Different path of portage due to it has different user permissions
    
    if args.ccache_stats==True:
        subprocess.run(["ccache", "-s"])
        exit(0)

    if is_cpufreq_configured():
        cpu_hz_before=sys_get_cpu_max_scaling_freq()
        print(_("Setting CPU max scaling frequency to: {} Hz").format(config.cpu_hz))
        sys_set_cpu_max_scaling_freq(int(config.cpu_hz))
        

    if args.config==True: #Writes a config file
        if not config.created:
            config.save()
            print(_("You must set your settings in {}. See README for help.").format(config.filename))
        exit(3)
        
        
    var_kernel_version=kernel_version()
    print (_("Version detected: {0}").format(var_kernel_version))
    
    config.check()

    if config.mykernel_generate is True:
        if config.mykernel_encrypted_root_partition!="":
            initramfs(config.mykernel_encrypted_root_partition, start, config.boot_directory)
            
    if config.dracut_generate is True:
        subprocess.run(["dracut", "--kver", str(var_kernel_version)], check=True)


    chdir("/usr/src/linux")

    subprocess.run(["make", f"-j{cpu_count()}"], check=True)
    subprocess.run(["make", "modules_install"], check=True)
    subprocess.run(["make", "install"], check=True)
    environ["CCACHE_DIR"]="/var/cache/ccache" #Emerge needs portage CCACHE_DIR
    subprocess.run(["emerge", "@module-rebuild", "--keep-going"], check=True)

    if config.efi=="True":#Gpt partition with efi
        subprocess.run(["grub-install", f"--efi-directory={config.boot_directory}", f"--target={config.efi_target}", str(config.efi_partition)], check=True)
        subprocess.run(["grub-mkconfig", "-o", f"{config.boot_directory}/grub/grub.cfg"], check=True)
    else:#Dos partition with mbr
        subprocess.run(["grub-install", str(config.mbr_device)], check=True)
        subprocess.run(["grub-mkconfig", "-o", f"{config.boot_directory}/grub/grub.cfg"], check=True)
    
    if is_cpufreq_configured():
        print(_("Restoring CPU max scaling frequency to: {} Hz").format(cpu_hz_before))
        sys_set_cpu_max_scaling_freq(cpu_hz_before)
    config.save()
    print("Compilation with {} processors took {}".format(datetime.now()-start,  cpu_count()))
