import os
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path
from pydicts.casts import dtnaive2str
from mykernel.commons import kernel_version, _


def initramfs(encrypted_root_partition, start, efi_directory):
    dt = dtnaive2str(start, "%Y%m%d%H%M")

    with tempfile.TemporaryDirectory(prefix=f"myinit-{dt}-") as temp_dir:
        output_path = Path(temp_dir)
        output = str(output_path)

        saved = {"/bin/sh", "/bin/echo", "/bin/mount", "/bin/umount", "/sbin/cryptsetup", "/sbin/fsck.ext4", "/sbin/switch_root", "/bin/ls"}
        saved.add("/lib64/ld-linux-x86-64.so.2")  # Si falla command unknown será por este

        var_kernel_version = kernel_version()
        print(_("Version detected: {0}").format(var_kernel_version))
        lastsetcount = 0

        initfile = """#!/bin/sh

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

        # Make dirs
        for d in ["bin", "dev", "etc", "lib64", "newroot", "proc", "sbin", "sys", "usr/bin", "usr/lib64", "run/cryptsetup", "lib", "usr/lib"]:
            target_dir = output_path / d
            print(f"mkdir -p {target_dir}")
            target_dir.mkdir(parents=True, exist_ok=True)

        # Symlinks: link lib -> lib64 safely inside output and output/usr if not already existing
        for symlink_dir in [output_path, output_path / "usr"]:
            link_target = symlink_dir / "lib"
            print(f"ln -s lib64 {link_target}")
            if link_target.exists() or link_target.is_symlink():
                if link_target.is_dir() and not link_target.is_symlink():
                    link_target.rmdir()
                else:
                    link_target.unlink()
            link_target.symlink_to("lib64")

        # Copy devices into output/dev/ safely
        devices_to_copy = ["/dev/null", "/dev/console", "/dev/tty"]
        if encrypted_root_partition:
            devices_to_copy.append(encrypted_root_partition)
        print("cp -a {} {}/dev/".format(" ".join(devices_to_copy), output))
        subprocess.run(["cp", "-a", *devices_to_copy, f"{output}/dev/"], check=True)

        # Create init file with safe executable permissions (0755)
        init_path = output_path / "init"
        init_path.write_text(initfile)
        print(f"chmod 755 {init_path}")
        init_path.chmod(stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

        # Search recursively dependencies
        print(_("Searching dependencies..."))
        env_c = {**os.environ, "LC_ALL": "C"}
        while lastsetcount != len(saved):
            tmp = set(saved)
            lastsetcount = len(saved)
            for program in tmp:
                if not Path(program).exists():
                    continue
                proc = subprocess.run(["ldd", "-v", program], capture_output=True, text=True, check=False, env=env_c)
                for line in proc.stdout.splitlines():
                    if "not a dynamic executable" in line or "no es un ejecutable" in line:
                        break
                    if "Version information" in line:
                        continue
                    if ":" in line:
                        dep = line.strip().split(":")[0]
                        if dep not in saved and Path(dep).exists():
                            saved.add(dep)

        # Copy files
        for f in saved:
            src_path = Path(f)
            if src_path.exists():
                dest = Path(f"{output}{f}")
                dest.parent.mkdir(parents=True, exist_ok=True)
                print(f"cp {f} {dest}")
                shutil.copy2(src_path, dest)

        gcc_proc = subprocess.run(["gcc", "-dumpversion"], capture_output=True, text=True, check=False)
        gccversion = gcc_proc.stdout.strip()
        if gccversion:
            gcc_lib = Path(f"/usr/lib/gcc/x86_64-pc-linux-gnu/{gccversion}/libgcc_s.so.1")
            if gcc_lib.exists():
                print(f"cp {gcc_lib} {output_path}/lib/libgcc_s.so")
                shutil.copy2(gcc_lib, output_path / "lib/libgcc_s.so")
                print(f"cp {gcc_lib} {output_path}/lib/libgcc_s.so.1")
                shutil.copy2(gcc_lib, output_path / "lib/libgcc_s.so.1")

        # Create timestamp file
        timestamp_file = output_path / f"{dt}.txt"
        print(f"touch {timestamp_file}")
        timestamp_file.touch()

        # Genera el fichero cpio usando un archivo temporal seguro
        dest_img = Path(efi_directory) / f"initramfs-{var_kernel_version}.img"
        print(f"Generating initramfs: {dest_img}")
        with tempfile.NamedTemporaryFile(prefix="myinit-", suffix=".cpio", delete=False) as cpio_tmp_file:
            cpio_tmp_path = Path(cpio_tmp_file.name)

        try:
            find_proc = subprocess.Popen(["find", ".", "-print0"], cwd=output, stdout=subprocess.PIPE)
            with open(cpio_tmp_path, "wb") as cpio_out:
                subprocess.run(["cpio", "--null", "-o", "--format=newc"], cwd=output, stdin=find_proc.stdout, stdout=cpio_out, check=True)
            if find_proc.stdout:
                find_proc.stdout.close()

            shutil.copyfile(cpio_tmp_path, dest_img)
        finally:
            if cpio_tmp_path.exists():
                cpio_tmp_path.unlink()

    os.chdir("/usr/src/linux")



