<div align="center">

# 🎵 Descargador de Canciones

### App de escritorio para buscar y descargar música con estilo

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Windows](https://img.shields.io/badge/Windows-.exe-0078D4?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/JUNSY8/Converter/releases/latest)
[![yt-dlp](https://img.shields.io/badge/Powered%20by-yt--dlp-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)

**Busca por nombre y autor · Descarga en MP3 o MP4 · Elige la calidad**

<br/>

![demo](https://img.shields.io/badge/✨_Lista_inteligente-8B5CF6?style=flat-square)
![demo](https://img.shields.io/badge/🎧_MP3_&_MP4-EC4899?style=flat-square)
![demo](https://img.shields.io/badge/🎚️_Calidad_ajustable-F59E0B?style=flat-square)
![demo](https://img.shields.io/badge/🎲_Modo_aleatorio-10B981?style=flat-square)

</div>

---

## 💻 Descarga para Windows

1. Ve a [**Releases**](https://github.com/JUNSY8/Converter/releases/latest)
2. Descarga **`DescargadorCanciones.exe`**
3. Ten **ffmpeg** instalado y en el `PATH` (ver más abajo)
4. Ejecuta el `.exe` (doble clic)

> Windows puede mostrar un aviso de SmartScreen al ser un ejecutable no firmado: *Más información* → *Ejecutar de todas formas*.

---

## ✨ Características

| | |
|:--|:--|
| 🔍 **Búsqueda flexible** | Título + autor, o solo el título — una canción por línea |
| 🎧 **Formatos** | Exporta a **MP3** (audio) o **MP4** (video) |
| 🎚️ **Calidad** | Elige bitrate / resolución según el formato |
| 🎲 **Modo aleatorio** | Descarga la cola en orden mezclado |
| 📁 **Carpeta a tu gusto** | Elige dónde guardar; nombres `Autor - Título.ext` |
| 🛡️ **Cola robusta** | Si una pista falla, el resto sigue descargándose |

---

## 🧰 Requisitos

| Requisito | Detalle |
|:----------|:--------|
| 🪟 **Windows** | `.exe` listo (o Python 3.10+ si corres desde código) |
| 🎬 **ffmpeg** | Debe estar en el `PATH` (conversión audio/video) |

<details>
<summary><b>📦 Instalar ffmpeg en Windows</b></summary>

<br/>

**Opción A — winget**

```bash
winget install ffmpeg
```

**Opción B — manual**

1. Descarga desde [ffmpeg.org](https://ffmpeg.org/download.html)
2. Agrega la carpeta `bin` al `PATH`
3. Reinicia la terminal y verifica:

```bash
ffmpeg -version
```

</details>

---

## 🚀 Instalación desde código

```bash
cd convert
pip install -r requirements.txt
python app.py
```

Dependencias principales: `customtkinter` · `yt-dlp`

### Empaquetar el `.exe` (desarrolladores)

```bash
pip install pyinstaller
python -m PyInstaller --noconfirm --clean --onefile --windowed --name "DescargadorCanciones" --collect-all customtkinter --collect-all yt_dlp app.py
```

El ejecutable queda en `dist/DescargadorCanciones.exe`.

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
Usa esta app **solo** con contenido al que tengas derecho a descargar.

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **[MIT](LICENSE)**.

```
Copyright (c) 2026 JUNSY8
```

Libre de usar, modificar y distribuir — consulta el archivo [`LICENSE`](LICENSE) para el texto completo.

---

<div align="center">

**Hecho con 💜 · Python · CustomTkinter · yt-dlp**

</div>
