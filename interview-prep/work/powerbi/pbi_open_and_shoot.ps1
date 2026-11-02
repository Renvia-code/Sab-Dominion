<#
Open a COPY of a .pbix in Power BI Desktop (Store build), wait for its window, and save
screenshots of that window (PrintWindow, works even when covered) and of the screen.
Records the PIDs this script started so only those are closed later.

Usage:
  powershell -NoProfile -ExecutionPolicy Bypass -File pbi_open_and_shoot.ps1 -Pbix <copy.pbix> -OutDir <dir> [-WaitSeconds 150]
  powershell -NoProfile -ExecutionPolicy Bypass -File pbi_open_and_shoot.ps1 -ShootOnly -OutDir <dir> -Tag <name>
  powershell -NoProfile -ExecutionPolicy Bypass -File pbi_open_and_shoot.ps1 -CloseStarted -OutDir <dir>
#>
param(
  [string]$Pbix,
  [string]$OutDir,
  [int]$WaitSeconds = 150,
  [switch]$ShootOnly,
  [switch]$CloseStarted,
  [string]$Tag = "open"
)
$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$pidFile = Join-Path $OutDir "started_pids.txt"

Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class Win {
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr hwnd, IntPtr hdc, uint flags);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hwnd, out RECT r);
  [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr hwnd);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr hwnd, int cmd);
  [DllImport("user32.dll")] public static extern bool SetProcessDpiAwarenessContext(IntPtr ctx);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
}
"@
# Per-monitor DPI aware (-4): window rects and PrintWindow in physical pixels, so the shot is the whole window
[Win]::SetProcessDpiAwarenessContext([IntPtr](-4)) | Out-Null

function Get-PbiProcs { Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -match '^(PBIDesktop|msmdsrv|Microsoft\.Mashup\.Container.*)$' } }

function Save-WindowShot([System.Diagnostics.Process]$p, [string]$path) {
  $h = $p.MainWindowHandle
  if ($h -eq [IntPtr]::Zero) { return $false }
  if ([Win]::IsIconic($h)) { [Win]::ShowWindow($h, 9) | Out-Null; Start-Sleep -Seconds 2 }
  $r = New-Object Win+RECT
  [Win]::GetWindowRect($h, [ref]$r) | Out-Null
  $w = $r.Right - $r.Left; $hgt = $r.Bottom - $r.Top
  if ($w -le 0 -or $hgt -le 0) { return $false }
  $bmp = New-Object System.Drawing.Bitmap $w, $hgt
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $hdc = $g.GetHdc()
  $ok = [Win]::PrintWindow($h, $hdc, 2)
  $g.ReleaseHdc($hdc); $g.Dispose()
  $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png); $bmp.Dispose()
  return $ok
}

function Save-ScreenShot([string]$path) {
  $b = [System.Windows.Forms.SystemInformation]::VirtualScreen
  $bmp = New-Object System.Drawing.Bitmap $b.Width, $b.Height
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.CopyFromScreen($b.Left, $b.Top, 0, 0, $bmp.Size)
  $g.Dispose(); $bmp.Save($path, [System.Drawing.Imaging.ImageFormat]::Png); $bmp.Dispose()
}
Add-Type -AssemblyName System.Windows.Forms

if ($CloseStarted) {
  if (-not (Test-Path $pidFile)) { Write-Output "no pid file"; exit 0 }
  $ids = Get-Content $pidFile | Where-Object { $_ -match '^\d+$' } | ForEach-Object { [int]$_ }
  foreach ($id in $ids) {
    $p = Get-Process -Id $id -ErrorAction SilentlyContinue
    if ($p) { Write-Output "closing $($p.ProcessName) $id"; Stop-Process -Id $id -Force -ErrorAction SilentlyContinue }
  }
  Start-Sleep -Seconds 3
  # children started by our PBIDesktop (msmdsrv, mashup containers) that appeared after our launch
  $after = Get-Content (Join-Path $OutDir "baseline_pids.txt") -ErrorAction SilentlyContinue | ForEach-Object { [int]$_ }
  Get-PbiProcs | Where-Object { $after -notcontains $_.Id } | ForEach-Object {
    Write-Output "closing leftover $($_.ProcessName) $($_.Id)"; Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue }
  Get-PbiProcs | Select-Object Id, ProcessName | Format-Table -AutoSize | Out-String | Write-Output
  exit 0
}

if ($ShootOnly) {
  $ids = Get-Content $pidFile | Where-Object { $_ -match '^\d+$' } | ForEach-Object { [int]$_ }
  $p = Get-Process -Id $ids -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -eq 'PBIDesktop' } | Select-Object -First 1
  if (-not $p) { Write-Output "PBIDesktop not running"; exit 1 }
  $p.Refresh()
  $ok = Save-WindowShot $p (Join-Path $OutDir "pbi_$Tag.png")
  Write-Output "window '$($p.MainWindowTitle)' shot=$ok"
  exit 0
}

# --- open ---
$baseline = @(Get-PbiProcs | ForEach-Object { $_.Id })
$baseline | Set-Content (Join-Path $OutDir "baseline_pids.txt")
$exe = Join-Path $env:LOCALAPPDATA "Microsoft\WindowsApps\PBIDesktopStore.exe"
Start-Process -FilePath $exe -ArgumentList ('"' + (Resolve-Path $Pbix).Path + '"')
$deadline = (Get-Date).AddSeconds($WaitSeconds)
$main = $null
while ((Get-Date) -lt $deadline) {
  Start-Sleep -Seconds 5
  $new = @(Get-PbiProcs | Where-Object { $baseline -notcontains $_.Id })
  $new | ForEach-Object { $_.Id } | Set-Content $pidFile
  $main = $new | Where-Object { $_.ProcessName -eq 'PBIDesktop' -and $_.MainWindowHandle -ne [IntPtr]::Zero } | Select-Object -First 1
  if ($main) { $main.Refresh(); if ($main.MainWindowTitle -match [regex]::Escape([IO.Path]::GetFileNameWithoutExtension($Pbix))) { break } }
}
if (-not $main) { Write-Output "no PBIDesktop window within $WaitSeconds s"; Save-ScreenShot (Join-Path $OutDir "screen_timeout.png"); exit 2 }
Start-Sleep -Seconds 25
$main.Refresh()
$ok = Save-WindowShot $main (Join-Path $OutDir "pbi_$Tag.png")
Save-ScreenShot (Join-Path $OutDir "screen_$Tag.png")
Write-Output "started: $(Get-Content $pidFile -Raw)"
Write-Output "window title: '$($main.MainWindowTitle)'  printwindow=$ok"
