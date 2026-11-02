param([string]$OutDir, [string]$PageList, [int]$Wait = 12, [int]$Start = 1)
# -PageList is one string, pages separated by "|" (powershell -File does not split arrays)
$Pages = $PageList -split '\|'
# Click through report pages of the Power BI Desktop instance started by pbi_open_and_shoot.ps1
# (PID from $OutDir\started_pids.txt) and save a window shot of each page as pbi_pNN.png.
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$ids = Get-Content (Join-Path $OutDir "started_pids.txt") | Where-Object { $_ -match '^\d+$' } | ForEach-Object { [int]$_ }
$p = Get-Process -Id $ids -ErrorAction SilentlyContinue | Where-Object ProcessName -eq 'PBIDesktop' | Select-Object -First 1
if (-not $p) { Write-Output "PBIDesktop not running"; exit 1 }
$i = $Start
foreach ($page in $Pages) {
  $r = & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $here "pbi_uia.ps1") -ProcId $p.Id -ControlType TabItem -Click $page
  Start-Sleep -Seconds $Wait
  $tag = "p{0:D2}" -f $i
  $s = & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $here "pbi_open_and_shoot.ps1") -ShootOnly -OutDir $OutDir -Tag $tag
  Write-Output "$tag '$page': $(($r | Select-Object -Last 1)) | $s"
  $i++
}
