from argparse import ArgumentParser
from datetime import datetime
from multiprocessing import cpu_count
from mykernel.mykernel_initramfs import initramfs
from mykernel.configfile import ConfigFile
from mykernel.reusing.cpupower import sys_set_cpu_max_scaling_freq, sys_get_cpu_max_scaling_freq, is_cpufreq_configured
from mykernel.commons import command,  kernel_version, _
from mykernel.version import __version__, __versiondate__
from os import environ, system, chdir
from sys import exit


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
        system("ccache -s")
        exit(0)

    if is_cpufreq_configured():
        cpu_hz_before=sys_get_cpu_max_scaling_freq()
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
        command(f"dracut --kver {var_kernel_version}")


    chdir("/usr/src/linux")

    command("make -j{}".format(cpu_count()))
    command("make modules_install")
    command("make install")
    environ["CCACHE_DIR"]="/var/cache/ccache" #Emerge needs portage CCACHE_DIR
    command("emerge @module-rebuild --keep-going")

    if config.efi=="True":#Gpt partition with efi
        command("grub-install --efi-directory={} --target={} {}".format(config.boot_directory, config.efi_target, config.efi_partition))
        command("grub-mkconfig -o {}/grub/grub.cfg".format(config.boot_directory))
    else:#Dos partition with mbr
        command("grub-install {}".format(config.mbr_device))
        command("grub-mkconfig -o {}/grub/grub.cfg".format(config.boot_directory))
    
    if is_cpufreq_configured():
        sys_set_cpu_max_scaling_freq(cpu_hz_before)
    config.save()
    print("Compilation with {} processors took {}".format(datetime.now()-start,  cpu_count()))
