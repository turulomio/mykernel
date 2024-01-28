from pydicts.casts import dtnaive2str
from mykernel.commons import command,  kernel_version, _
from os import  popen, chdir
from subprocess import run


###########################

def initramfs(encrypted_root_partition, start, efi_directory):
    dt=dtnaive2str(start, "%Y%m%d%H%M")
    output="/tmp/myinit-{}/".format(dt)

    saved=set(["/bin/sh", "/bin/echo", "/bin/mount", "/bin/umount","/sbin/cryptsetup", "/sbin/fsck.ext4","/sbin/switch_root", "/bin/ls"])
    saved.add("/lib64/ld-linux-x86-64.so.2")#Si falla comand unknown será por este

    var_kernel_version=kernel_version()
    print (_("Version detected: {0}").format(var_kernel_version))
    lastsetcount=0

    initfile="""#!/bin/sh

mount -t devtmpfs none /dev
mount -t proc proc /proc
mount -t sysfs sysfs /sys

echo 0 > /proc/sys/kernel/printk

ls /dev

cryptsetup luksOpen {0} root
fsck.ext4 /dev/mapper/root
mount /dev/mapper/root /newroot

umount /proc
umount /sys

if [[ -x "/newroot/sbin/init" ]] ; then
        exec switch_root /newroot /sbin/init
fi

echo "Failed to init Gentoo..."
""".format(encrypted_root_partition)

    command("rm -Rf {}".format(output))
    command("mkdir {}".format(output))

    chdir(output)

    #Make dirs
    for d in ["bin", "dev","etc", "lib64", "newroot", "proc", "sbin", "sys","usr/bin","usr/lib64","run/cryptsetup"]:
        command("mkdir -p {}/{}".format(output,d))
    command("ln -s lib64 lib")
    chdir(output+"/usr/")
    command("ln -s lib64 lib")
    chdir(output)
    command("cp -a /dev/null /dev/console /dev/tty {} {}/dev/".format(encrypted_root_partition, output))

    #Create init file
    f=open("{}/init".format(output),"w")
    f.write(initfile)
    f.close()
    command("chmod 777 init")

    #Search recursively dependencies
    while lastsetcount!=len(saved):
       tmp=set(saved)
       lastsetcount=len(saved)
       for program in tmp:
            ##Function that gets a program or lib and gets all shared dependencies.
            ##They are added to saved set
           for line in popen("ldd -v {}".format(program)):
              if line.find("no es un ejecutable")>=0:
                 break
              if line.find("Version information")>0:
                 continue
              if line.find(":")>0:
                 dep=line.strip().split(":")[0]
                 if dep not in (saved):
                    saved.add(dep)

    #Copy files
    for f in saved:
       command("cp  {0} {1}{0}".format(f, output))
       saved.add("{}".format(f))

    gccversion=run("gcc -dumpversion", shell=True, capture_output=True).stdout.decode("UTF-8")[:-1]
    ## Needed in w computer
    command (f'cp /usr/lib/gcc/x86_64-pc-linux-gnu/{gccversion}/libgcc_s.so.1 {output}/lib/libgcc_s.so')
    command (f'cp /usr/lib/gcc/x86_64-pc-linux-gnu/{gccversion}/libgcc_s.so.1 {output}/lib/libgcc_s.so.1')

    #Create timestamp
    command("touch '{}/{}.txt'".format(output, dt))

    ## Genera el fichero
    command("find . -print0 | cpio --null -o --format=newc > /tmp/myinit.cpio")#Cuidado no generarlo en el mismo sitio se grew
    command("cat /tmp/myinit.cpio > {}/initramfs-{}.img".format(efi_directory, var_kernel_version))
    chdir("/usr/src/linux")
