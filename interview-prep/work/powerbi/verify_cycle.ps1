param([string]$Pbit, [string]$OutDir, [int]$LoadWait = 90,
      [string]$PageList = "Summary|Scorecard|What moved|Weather|Fair comparison|Outages by county|Storms|Growth|Demand and seasons|Demand summary|Data notes")
# One verification pass: open a template COPY in Power BI Desktop, press Load in its parameter dialog,
# list any extra windows (errors), then shoot every page. Leaves Desktop open; close it with
# pbi_open_and_shoot.ps1 -CloseStarted -OutDir $OutDir.
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$ps = @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File")
& powershell @ps (Join-Path $here "pbi_open_and_shoot.ps1") -Pbix $Pbit -OutDir $OutDir -WaitSeconds 60 -Tag open | Select-Object -Last 1
$ids = Get-Content (Join-Path $OutDir "started_pids.txt") | Where-Object { $_ -match '^\d+$' } | ForEach-Object { [int]$_ }
$p = Get-Process -Id $ids -ErrorAction SilentlyContinue | Where-Object ProcessName -eq 'PBIDesktop' | Select-Object -First 1
if (-not $p) { Write-Output "no PBIDesktop"; exit 1 }
$name = [IO.Path]::GetFileNameWithoutExtension($Pbit)
$wins = & powershell @ps (Join-Path $here "list_windows.ps1") -ProcId $p.Id
$dlg = $wins | Where-Object { $_ -match [regex]::Escape("'$name'") } | Select-Object -First 1
if (-not $dlg) { Write-Output "no parameter dialog; windows:"; $wins; exit 2 }
$hwnd = [long](($dlg -split '\|')[0].Trim())
& powershell @ps (Join-Path $here "msaa_click.ps1") -Hwnd $hwnd -Name Load | Select-Object -Last 1
Start-Sleep -Seconds $LoadWait
Write-Output "windows after load:"
& powershell @ps (Join-Path $here "list_windows.ps1") -ProcId $p.Id
& powershell @ps (Join-Path $here "tour_pages.ps1") -OutDir $OutDir -Wait 9 -PageList $PageList
