from myemerge.objects.command import command
from myemerge.myconfigparser import MyConfigParser
from myemerge.cpupower import sys_set_cpu_max_scaling_freq, sys_get_cpu_min_freq, sys_get_cpu_max_freq
from os import makedirs

def main():
    config=MyConfigParser('/etc/myemerge/myemerge.ini')
    if config.get('cpupower','limit_to_min_cpu_freq', "True")=="True":
         sys_set_cpu_max_scaling_freq(sys_get_cpu_min_freq())

    command("emaint cleanresume -f")
    command("emerge -ev world --keep-going y")
    command("emerge @preserved-rebuild")
    command("revdep-rebuild -i -- --keep-going y")

    if config.get('cpupower','limit_to_min_cpu_freq')=="True":
         sys_set_cpu_max_scaling_freq(sys_get_cpu_max_freq())

    config.save()


