# MyKernel
## Gentoo kernel with root luks example

We create luks partition with `cryptsetup`

With `blkid` we can see created partitions UUID
```
/dev/nvme0n1p1: UUID="51F2-B573" BLOCK_SIZE="512" TYPE="vfat" PARTUUID="3bb72034-0028-4b4b-a022-86dcf77991bf"
/dev/nvme0n1p2: UUID="e3905174-0bfc-406c-8958-8004cfec6528" TYPE="crypto_LUKS" PARTUUID="01037e81-d022-c041-a85e-6e872cbcb791"
/dev/mapper/root: UUID="ebc859bc-a777-4953-9c92-178c89b52222" BLOCK_SIZE="4096" TYPE="ext4"
```
Gentoo package install-kernel must have dracut USE


We edit /etc/dracut.conf
```
add_dracutmodules+=" crypt dm rootfs-block "
kernel_cmdline+=" root=UUID=ebc859bc-a777-4953-9c92-178c89b52222 rd.luks.uuid=e3905174-0bfc-406c-8958-8004cfec6528 "
```

We edit /etc/default/grub
```
GRUB_CMDLINE_LINUX_DEFAULT="crypt_root=nvme0n1p2"
```

## Changelog
### 1.0.0 (2025-04-13)
- Migrated to poetry>2.0.0
- Security bugs

### 0.11.0 (2024-01-28)
- Added dracut support. See /etc/mykernel/mykernel.ini 

### 0.10.0 (2023-06-15)
- Migrated to poetry project

### 0.9.0
- Added gcc library to initramfs, needed in some environments.

### 0.8.0
- Ccache is used by default.
- Removed --ccache argument.
- Portage CCACHE_DIR is used emerging kernel modules.

### 0.7.0
- Ccache directory is now /var/cache/ccache_mykernel.

### 0.6.0
- Added ccache support with --ccache parameter.

### 0.5.0
- Fixed bug when cpufreq isn't configured in kernel.

### 0.4.0
- Added suppor for MBR disk installations.
- Added man documentation.
- Improved spanish translations.

### 0.3.0
- Solved critical bug due to a bad return

### 0.2.0
- Converted to a python module
- You can set your parameters in /etc/mykernel/mykernel.ini

### 0.1.0
- Imported from old scripts
