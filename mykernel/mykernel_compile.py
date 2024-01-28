from argparse import ArgumentParser
from datetime import datetime
from multiprocessing import cpu_count
from mykernel.mykernel_initramfs import initramfs
from mykernel.reusing.myconfigparser import MyConfigParser
from mykernel.reusing.cpupower import sys_set_cpu_max_scaling_freq, sys_get_cpu_max_freq, sys_get_cpu_max_scaling_freq, is_cpufreq_configured
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
    config=MyConfigParser('/etc/mykernel/mykernel.ini')
    
    
    environ["PATH"]="/usr/lib/ccache/bin:" + environ["PATH"]
    environ["CCACHE_DIR"]="/var/cache/ccache_mykernel" #Different path of portage due to it has different user permissions
    
    if args.ccache_stats==True:
        system("ccache -s")
        exit(0)

    if is_cpufreq_configured():
        cpu_hz_before=sys_get_cpu_max_scaling_freq()
        cpu_hz=config.get('cpupower','cpu_hz',  str(sys_get_cpu_max_freq()))
        sys_set_cpu_max_scaling_freq(int(cpu_hz))
        


    efi=config.get("grub", "efi", "True")
    boot_directory =config.get("grub", 'boot_directory', '/boot')
    efi_target=config.get("grub", 'efi_target', 'x86_64-efi')
    efi_partition=config.get("grub", 'efi_partition',  '/dev/sda1')
    mbr_device=config.get("grub", "mbr_device", "")
    
    dracut_generate=config.getBoolean("dracut_initramfs", 'generate', 'True')
    
    
    mykernel_encrypted_root_partition=config.get("mykernel_initramfs", 'encrypted_root_partition', '')
    mykernel_generate=config.getBoolean("mykernel_initramfs", 'generate', False)
    
    if args.config==True: #Writes a config file
        config.save()
        print("You must set your settings in /etc/mykernel/mykernel.ini. Use man mykernel for help.")
        exit(3)
        
        
    var_kernel_version=kernel_version()
    print (_("Version detected: {0}").format(var_kernel_version))
    

    if mykernel_generate is True and dracut_generate is True:
        print(_("Mykernel and Dracut initramfs generation is selected at the same time. Please fix it in /etc/mykernel/mykernel.ini"))
        exit(2)

    if mykernel_generate is True:
        if mykernel_encrypted_root_partition!="":
            initramfs(mykernel_encrypted_root_partition, start, boot_directory)
            
    if dracut_generate is True:
        command(f"dracut --kver {var_kernel_version}")


    chdir("/usr/src/linux")

    command("make -j{}".format(cpu_count()))
    command("make modules_install")
    command("make install")
    environ["CCACHE_DIR"]="/var/cache/ccache" #Emerge needs portage CCACHE_DIR
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
