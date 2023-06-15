# Changelog
## 0.10.0 (2023-06-15)
- Migrated to poetry project

## 0.9.0
- Added gcc library to initramfs, needed in some environments.

## 0.8.0
- Ccache is used by default.
- Removed --ccache argument.
- Portage CCACHE_DIR is used emerging kernel modules.

## 0.7.0
- Ccache directory is now /var/cache/ccache_mykernel.

## 0.6.0
- Added ccache support with --ccache parameter.

## 0.5.0
- Fixed bug when cpufreq isn't configured in kernel.

## 0.4.0
- Added suppor for MBR disk installations.
- Added man documentation.
- Improved spanish translations.

## 0.3.0
- Solved critical bug due to a bad return

## 0.2.0
- Converted to a python module
- You can set your parameters in /etc/mykernel/mykernel.ini

## 0.1.0
- Imported from old scripts