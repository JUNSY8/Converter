

# 🎵 Descargador de Canciones

### App de escritorio para buscar y descargar música con estilo

[Python](https://www.python.org/)
[License](LICENSE)
[Windows](https://github.com/JUNSY8/Converter/releases/latest)
[yt-dlp](https://github.com/yt-dlp/yt-dlp)

**Busca por nombre y autor · Descarga en MP3 o MP4 · Elige la calidad**



---



## 💻 Descarga para Windows

1. Ve a **[Releases](https://github.com/JUNSY8/Converter/releases/latest)**
2. Descarga `DescargadorCanciones.exe`
3. Ejecuta el `.exe` (doble clic)
4. Acepta los **términos y condiciones** (solo la primera vez)

**No necesitas instalar nada más**: el `.exe` ya incluye **ffmpeg** embebido.

> Windows puede mostrar un aviso de SmartScreen al ser un ejecutable no firmado: *Más información* → *Ejecutar de todas formas*.

---



## ✨ Características


|                           |                                                          |
| ------------------------- | -------------------------------------------------------- |
| 🔍 **Búsqueda flexible**  | Título + autor, o solo el título — una canción por línea |
| 🎧 **Formatos**           | Exporta a **MP3** (audio) o **MP4** (video)              |
| 🎚️ **Calidad**           | Elige bitrate / resolución según el formato              |
| 🎲 **Modo aleatorio**     | Descarga la cola en orden mezclado                       |
| 📁 **Carpeta a tu gusto** | Elige dónde guardar; nombres `Autor - Título.ext`        |
| 🛡️ **Cola robusta**      | Si una pista falla, el resto sigue descargándose         |
| 🎬 **ffmpeg incluido**    | En el `.exe` no hace falta instalarlo por separado       |


---



## 🧰 Requisitos


| Requisito      | Detalle                                                                 |
| -------------- | ----------------------------------------------------------------------- |
| 🪟 **Windows** | Descarga el `.exe` y úsalo tal cual (ffmpeg ya va dentro)               |
| 🐍 **Código**  | Si corres desde fuente: Python 3.10+ y ffmpeg en `vendor/ffmpeg` o PATH |


<details>
<summary><b>📦 ffmpeg solo si ejecutas desde código</b></summary>

<br/>

Con el `.exe` de Releases **no aplica**. Si desarrollas o corres `python app.py`:

**Opción A — vendor local (recomendado para empaquetar)**

```bash
powershell -File scripts/fetch_ffmpeg.ps1
```

Queda en `vendor/ffmpeg/` (`ffmpeg.exe` + `ffprobe.exe`).

**Opción B — winget (PATH del sistema)**

```bash
winget install ffmpeg
```

</details>

---



## 🚀 Instalación desde código

```bash
cd convert
pip install -r requirements.txt
powershell -File scripts/fetch_ffmpeg.ps1
python app.py
```

Dependencias principales: `customtkinter` · `yt-dlp` · ffmpeg (vendor o PATH)

### Empaquetar el `.exe` (desarrolladores)

```bash
build_windows.bat
```

O manualmente:

```bash
powershell -File scripts/fetch_ffmpeg.ps1
pip install pyinstaller
python -m PyInstaller --noconfirm --clean --onefile --windowed --name "DescargadorCanciones" --collect-all customtkinter --collect-all yt_dlp --add-binary "vendor\ffmpeg\ffmpeg.exe;ffmpeg" --add-binary "vendor\ffmpeg\ffprobe.exe;ffmpeg" app.py
```

El ejecutable queda en `dist/DescargadorCanciones.exe` (con ffmpeg embebido).

---



## ▶️ Uso

1. Escribe o pega la lista (una canción por línea), por ejemplo:
  - `Bohemian Rhapsody - Queen`
  - `Blinding Lights, The Weeknd`
  - `Imagine` *(solo título)*
2. Elige formato (**MP3** o **MP4**) y calidad.
3. *(Opcional)* Activa **Aleatorio** para mezclar el orden.
4. Selecciona la carpeta de destino.
5. Pulsa **Descargar** y listo 🎉

> 💾 Los archivos se guardan como `Autor - Título.ext`

---



## ⚖️ Aviso legal

La búsqueda se realiza mediante YouTube con **yt-dlp**.  
Al abrir la app debes aceptar los términos y condiciones.  
Usa esta app **solo** con contenido al que tengas derecho a descargar.

---



## 📄 Licencia

Este proyecto se distribuye bajo la licencia **[MIT](LICENSE)**.

```
Copyright (c) 2026 JUNSY8
```

Libre de usar, modificar y distribuir — consulta el archivo `[LICENSE](LICENSE)` para el texto completo.

---

