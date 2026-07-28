$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$vendor = Join-Path $root "vendor\ffmpeg"
New-Item -ItemType Directory -Force -Path $vendor | Out-Null

if ((Test-Path (Join-Path $vendor "ffmpeg.exe")) -and (Test-Path (Join-Path $vendor "ffprobe.exe"))) {
    Write-Host "ffmpeg ya esta en vendor\ffmpeg"
    exit 0
}

$zip = Join-Path $env:TEMP "ffmpeg-essentials.zip"
$dest = Join-Path $env:TEMP "ffmpeg-essentials"
Write-Host "Descargando ffmpeg essentials..."
Invoke-WebRequest -Uri "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip" -OutFile $zip -UseBasicParsing
if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
Expand-Archive -Path $zip -DestinationPath $dest -Force
$bin = Get-ChildItem -Path $dest -Recurse -Directory -Filter "bin" | Select-Object -First 1
Copy-Item (Join-Path $bin.FullName "ffmpeg.exe") (Join-Path $vendor "ffmpeg.exe") -Force
Copy-Item (Join-Path $bin.FullName "ffprobe.exe") (Join-Path $vendor "ffprobe.exe") -Force
Write-Host "Listo: $vendor"
