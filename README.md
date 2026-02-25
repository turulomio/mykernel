# mykernel - Linux Kernel Compilation Tool for Gentoo

## Descripción

`mykernel` is a Python-based tool designed to simplify and automate the Linux kernel compilation process, specifically tailored for **Gentoo Linux** systems. It handles various compilation aspects, including `ccache` configuration, CPU frequency scaling, initramfs generation (both custom and with Dracut), kernel compilation, module installation, and GRUB configuration for both EFI and MBR systems.

## Usage

To run `mykernel`, use the following command:

```bash
mykernel [OPCIONES]
```

### Opciones

*   `--version`: Muestra el número de versión del programa y sale.
*   `--config`: Escribe un archivo de configuración por defecto en `/etc/mykernel/mykernel.ini`.
    *   **Nota:** Después de ejecutar con `--config`, debes editar `/etc/mykernel/mykernel.ini` para establecer tus configuraciones deseadas. Usa `man mykernel` para obtener ayuda detallada sobre las opciones de configuración.
*   `--ccache_stats`: Muestra las estadísticas de `ccache`.

## Ayuda de Configuración de `mykernel.ini`

La herramienta `mykernel` utiliza un archivo de configuración ubicado en `/etc/mykernel/mykernel.ini`. A continuación se detallan las secciones y parámetros disponibles:

### `[cpupower]`

*   **`cpu_hz`**
    *   **Descripción:** Número de la frecuencia de escalado de la CPU. El valor por defecto es la frecuencia de escalado máxima detectada. Déjalo como está si no sabes lo que estás haciendo, ya que una configuración incorrecta puede afectar el rendimiento.

### `[mykernel_initramfs]`

*   **`encrypted_root_partition`**
    *   **Descripción:** El nombre del dispositivo de la partición raíz cifrada (por ejemplo, `/dev/sda2`). Déjalo vacío si no hay cifrado en tu sistema.
*   **`generate`**
    *   **Descripción:** Establece a `True` para generar un initramfs personalizado utilizando la lógica interna de `mykernel`. Establece a `False` para deshabilitar. No puede ser `True` si `dracut_initramfs`'s `generate` también es `True`.

### `[dracut_initramfs]`

*   **`generate`**
    *   **Descripción:** Establece a `True` para generar un initramfs utilizando Dracut. Establece a `False` para deshabilitar. No puede ser `True` si `mykernel_initramfs`'s `generate` también es `True`.

### `[grub]`

*   **`efi`**
    *   **Descripción:** Establece a `True` si tu sistema utiliza un sistema EFI con una tabla de particiones GPT. Establece a `False` si tu sistema utiliza una tabla de particiones DOS con un bloque MBR.
*   **`boot_directory`**
    *   **Descripción:** La ruta al directorio de arranque. Por defecto, es `/boot`.
*   **`efi_target`**
    *   **Descripción:** Especifica el objetivo de GRUB para sistemas EFI. Ejemplos incluyen `x86_64-efi`, `i386-pc`.
*   **`efi_partition`**
    *   **Descripción:** El nombre de la partición donde se encuentra el directorio EFI (por ejemplo, `/dev/sda1`).
*   **`mbr_device`**
    *   **Descripción:** El nombre del dispositivo donde se instalará el MBR (por ejemplo, `/dev/sda`). Este parámetro solo es aplicable para sistemas no EFI.

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
