from configparser_rb.core import ConfigParserRB
from mykernel.reusing.cpupower import sys_get_cpu_max_freq, is_cpufreq_configured
from mykernel.commons import _
from sys import exit


from os.path import exists


class ConfigFile(ConfigParserRB):
    """
    Class to manage /etc/mykernel/mykernel.ini configuration file
    """
    def __init__(self, filename="/etc/mykernel/mykernel.ini"):
        self.created = not exists(filename)
        super().__init__(filename)
        self.load()
        if self.created:
            self.save()
            print(_("WARNING: Configuration file created in {}. You must set your settings. See README for help.").format(self.filename))

    def load(self):
        # cpupower
        if is_cpufreq_configured():
            self.cpu_hz = self.get('cpupower', 'cpu_hz', str(sys_get_cpu_max_freq()))
        else:
            self.cpu_hz = self.get('cpupower', 'cpu_hz', str(sys_get_cpu_max_freq()))

        # grub
        self.efi = self.get("grub", "efi", "True")
        self.boot_directory = self.get("grub", "boot_directory", "/boot")
        self.efi_target = self.get("grub", "efi_target", "x86_64-efi")
        self.efi_partition = self.get("grub", "efi_partition", "/dev/sda1")
        self.mbr_device = self.get("grub", "mbr_device", "")

        # dracut_initramfs
        self.dracut_generate = self.getBoolean("dracut_initramfs", "generate", "True")

        # mykernel_initramfs
        self.mykernel_encrypted_root_partition = self.get("mykernel_initramfs", "encrypted_root_partition", "")
        self.mykernel_generate = self.getBoolean("mykernel_initramfs", "generate", False)

    def check(self):
        if self.mykernel_generate is True and self.dracut_generate is True:
            print(_("Mykernel and Dracut initramfs generation is selected at the same time. Please fix it in /etc/mykernel/mykernel.ini"))
            exit(2)
