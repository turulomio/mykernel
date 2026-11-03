from configparser_rb.core import ConfigParserRB
from pycpufreq import sys_get_cpu_max_freq, is_cpufreq_configured
from mykernel.commons import _
from sys import exit
from pathlib import Path


class ConfigFile(ConfigParserRB):
    """
    Class to manage /etc/mykernel/mykernel.ini configuration file
    """
    def __init__(self, filename="/etc/mykernel/mykernel.ini"):
        self.created = not Path(filename).exists()
        super().__init__(filename)
        self.load()
        if self.created:
            self.save()
            print(_("WARNING: Configuration file created in {}. You must set your settings. See README for help.").format(self.filename))

    def _sync(self):
        """
        Detects missing or obsolete keys/sections according to expected schema and updates config.
        """
        expected_schema = {
            'ccache': {
                'ccache': 'False',
            },
            'cpupower': {
                'cpu_hz': str(sys_get_cpu_max_freq()),
            },
            'grub': {
                'efi': 'True',
                'boot_directory': '/boot',
                'efi_target': 'x86_64-efi',
                'efi_partition': '/dev/sda1',
                'mbr_device': '',
            },
            'dracut_initramfs': {
                'generate': 'True',
            },
            'mykernel_initramfs': {
                'encrypted_root_partition': '',
                'generate': 'False',
            },
        }

        changed = False

        # Remove extra sections
        for section in list(self.config.sections()):
            if section not in expected_schema:
                self.config.remove_section(section)
                changed = True
            else:
                # Remove extra options
                for option in list(self.config.options(section)):
                    if option not in expected_schema[section]:
                        self.config.remove_option(section, option)
                        changed = True

        # Add missing sections and options
        for section, options in expected_schema.items():
            if not self.config.has_section(section):
                self.config.add_section(section)
                changed = True
            for option, default_val in options.items():
                if not self.config.has_option(section, option):
                    self.set(section, option, default_val)
                    changed = True

        if changed and not self.created:
            self.save()
            print(_("Configuration file {} updated with missing/obsolete keys.").format(self.filename))

    def load(self):
        self._sync()

        # ccache
        self.ccache = self.getBoolean("ccache", "ccache", False)
        self.ccache_dir = Path("/var/cache/ccache_mykernel")

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

    def save(self):
        super().save()
        try:
            cfg_path = Path(self.filename)
            if cfg_path.exists():
                cfg_path.chmod(0o644)
        except OSError:
            pass

    def check(self):
        try:
            hz = int(self.cpu_hz)
            if hz <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            print(_("Invalid cpu_hz value '{}' in /etc/mykernel/mykernel.ini. Must be a positive integer.").format(self.cpu_hz))
            exit(2)

        if self.mykernel_generate is True and self.dracut_generate is True:
            print(_("Mykernel and Dracut initramfs generation is selected at the same time. Please fix it in /etc/mykernel/mykernel.ini"))
            exit(2)

        if self.efi == "True":
            if not self.efi_partition:
                print(_("grub efi_partition cannot be empty when efi is True."))
                exit(2)
        else:
            if not self.mbr_device:
                print(_("grub mbr_device cannot be empty when efi is False."))
                exit(2)


