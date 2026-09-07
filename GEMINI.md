# GEMINI.md - Directrices y Contexto del Proyecto `mykernel`

Este archivo contiene la información esencial y las directrices para que los asistentes de IA (Gemini / Antigravity) comprendan la arquitectura, propósito, convenciones y flujos de trabajo de este repositorio.

---

## 1. Descripción del Proyecto

`mykernel` es una herramienta en Python diseñada para automatizar la compilación e instalación del kernel de Linux, específicamente orientada a sistemas **Gentoo Linux**.

Gestiona de forma integral:
- Configuración de escalado de frecuencia de CPU (`cpupower`).
- Uso y estadísticas de `ccache` para optimizar tiempos de compilación.
- Compilación del kernel (`make`, `make modules_install`, `make install` en `/usr/src/linux`).
- Reconstrucción de módulos externos con Portage (`emerge @module-rebuild --keep-going`).
- Generación de `initramfs` (mediante script propio `mykernel_initramfs` o mediante `dracut`).
- Instalación y actualización de GRUB (`grub-install` y `grub-mkconfig`) tanto para particiones GPT con EFI como MBR (DOS).

---

## 2. Estructura del Código

El paquete principal se ubica en `mykernel/`:

```
mykernel/
├── __init__.py            # Exporta ConfigFile, __version__, etc.
├── commons.py             # Utilidades comunes: traducción con gettext (_), detección de versión (kernel_version), ejecución de comandos (command).
├── configfile.py          # Clase ConfigFile (hereda de ConfigParserRB): gestión, carga, validación y autocreación de /etc/mykernel/mykernel.ini.
├── mykernel_compile.py    # Punto de entrada principal (función main()). Orquesta todo el flujo de compilación y argumentos CLI.
├── mykernel_initramfs.py  # Lógica para construir initramfs personalizado (soporte LUKS cifrado, Busybox, etc.).
├── mykernel_check.py      # Comprobaciones y validaciones previas.
├── poethepoet.py          # Tareas automatizadas con PoeThePoet (traducciones, releases, sincronización de código reused).
├── version.py             # Definición de __version__ y __versiondate__.
├── locale/                # Catálogos gettext (.pot, .po y binarios .mo compilados para es y fr).
└── reusing/               # Código reutilizado/vendoreado de otros repositorios (ej. cpupower, github). Actualizado con `poe reusing`.
```

---

## 3. Archivo de Configuración (`/etc/mykernel/mykernel.ini`)

Gestionado por la clase `ConfigFile` ([mykernel/configfile.py](mykernel/configfile.py)), basada en `ConfigParserRB`.

### Secciones y claves soportadas:
- **`[cpupower]`**
  - `cpu_hz`: Frecuencia de escalado de CPU máxima deseada durante la compilación.
- **`[grub]`**
  - `efi`: `"True"` si el sistema usa arranque UEFI (GPT), `"False"` para MBR.
  - `boot_directory`: Directorio de arranque (por defecto `/boot`).
  - `efi_target`: Target EFI de GRUB (ej. `x86_64-efi`, `i386-pc`).
  - `efi_partition`: Dispositivo de la partición EFI (ej. `/dev/sda1`).
  - `mbr_device`: Dispositivo donde instalar el MBR (ej. `/dev/sda`, solo si `efi="False"`).
- **`[dracut_initramfs]`**
  - `generate`: Booleano para generar initramfs con Dracut.
- **`[mykernel_initramfs]`**
  - `generate`: Booleano para generar initramfs propio de mykernel.
  - `encrypted_root_partition`: Partición raíz cifrada si aplica (ej. `/dev/nvme0n1p2`).

### Comportamiento importante:
- Si el archivo no existe al instanciar `ConfigFile`, se crea automáticamente en disco con los valores por defecto y se emite un aviso por consola indicando al usuario que lo configure.
- `check()` valida que no estén activados simultáneamente `dracut_generate` y `mykernel_generate`.

---

## 4. Herramientas y Entorno de Desarrollo

- **Gestor de paquetes y dependencias**: `poetry` (Python `>=3.12, <4.0.0`).
  - Dependencias runtime: `colorama`, `pydicts`, `configparser-rb`.
  - Dependencias dev: `poetry`, `poethepoet`.
- **Tareas automatizadas (`poethepoet`)**:
  - `poe translate`: Regenera `.pot`, fusiona con `es.po` y `fr.po`, y compila los ficheros `.mo` (ejecutado por el usuario al hacer una release).
  - `poe reusing`: Actualiza módulos en `mykernel/reusing/` desde repositorios upstream de GitHub.
  - `poe release`: Flujo guiado para preparar una nueva versión.

---

## 5. Reglas y Pautas para el Asistente de IA

1. **Foco en lo solicitado**: Centrarse estrictamente en el código y funcionalidad que el usuario pide sin desviarse ni agregar abstracciones innecesarias.
2. **Internacionalización**: Cualquier mensaje nuevo dirigido al usuario en la CLI debe usar la función de traducción `_("...")` de `mykernel.commons`. La ejecución de `poe translate` y la edición de catálogos `.po`/`.mo` la realiza el usuario al momento de hacer una nueva release, por lo que el asistente no debe ejecutarlas ni modificarlas a menos que se le pida expresamente.
3. **Respeto a módulos reutilizados**: Los archivos dentro de `mykernel/reusing/` provienen de sincronización upstream; evitar modificarlos manualmente a menos que se solicite expresamente.
4. **Compatibilidad con Gentoo**: Tener en cuenta los comandos específicos del entorno (`emerge`, `dracut`, rutas habituales `/usr/src/linux`, permisos de `ccache`, etc.).
5. **No romper retrocompatibilidad**: Mantener la compatibilidad de opciones CLI (`--config`, `--ccache_stats`, `--version`).
