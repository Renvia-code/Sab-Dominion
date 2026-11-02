<#
Drive one Windows "Save As" / "Open" common dialog by its hwnd (UI Automation): list its controls,
set the file name, optionally pick a file type, and press Save/Open. Scoped to that hwnd only.

  powershell -File save_dialog.ps1 -Hwnd 394092 -List
  powershell -File save_dialog.ps1 -Hwnd 394092 -FileName "C:\x\y.pbit" [-TypeName "..."] -Press "Save"
#>
param([long]$Hwnd, [switch]$List, [string]$FileName = "", [string]$TypeName = "", [string]$Press = "")
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$AE = [System.Windows.Automation.AutomationElement]
$dlg = $AE::FromHandle([IntPtr]$Hwnd)
$all = $dlg.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.Condition]::TrueCondition)
if ($List) {
  foreach ($e in $all) { if ($e.Current.Name) { Write-Output "[$($e.Current.ControlType.ProgrammaticName -replace 'ControlType\.','')] '$($e.Current.Name)' id=$($e.Current.AutomationId)" } }
  exit 0
}
if ($TypeName) {
  $cb = $null
  foreach ($e in $all) { if ($e.Current.ControlType -eq [System.Windows.Automation.ControlType]::ComboBox -and $e.Current.AutomationId -eq "FileTypeControlHost") { $cb = $e } }
  if ($cb) {
    $p = $null
    if ($cb.TryGetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern, [ref]$p)) { $p.Expand(); Start-Sleep -Milliseconds 700 }
    $items = $cb.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.Condition]::TrueCondition)
    foreach ($i in $items) {
      if ($i.Current.Name) { Write-Output "  type option '$($i.Current.Name)'" }
      if ($i.Current.Name -eq $TypeName) { $sp = $null; if ($i.TryGetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern, [ref]$sp)) { $sp.Select(); Write-Output "picked type '$TypeName'" } }
    }
    try { $p.Collapse() } catch {}
  } else { Write-Output "no file-type combo" }
}
if ($FileName) {
  # the file-name box lives under the pane whose AutomationId is FileNameControlHost
  $host_ = $null
  foreach ($e in $all) { if ($e.Current.AutomationId -eq "FileNameControlHost") { $host_ = $e; break } }
  $cands = @()
  if ($host_) {
    $vp0 = $null
    if ($host_.TryGetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern, [ref]$vp0)) { $cands += $host_ }
    $cands += @($host_.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.Condition]::TrueCondition))
  }
  $done = $false
  foreach ($c in $cands) {
    $vp = $null
    if ($c.TryGetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern, [ref]$vp)) {
      $vp.SetValue($FileName); Start-Sleep -Milliseconds 300
      Write-Output "file name set on id=$($c.Current.AutomationId) now '$($vp.Current.Value)'"; $done = $true; break
    }
  }
  if (-not $done) { Write-Output "no file name edit with ValuePattern"; exit 2 }
}
if ($Press) {
  $all = $dlg.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.Condition]::TrueCondition)
  foreach ($e in $all) {
    if ($e.Current.Name -eq $Press -and ($e.Current.AutomationId -eq "1" -or $e.Current.AutomationId -eq "2" -or $e.Current.ClassName -eq "Button")) {
      $ip = $null
      if ($e.TryGetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern, [ref]$ip)) { $ip.Invoke(); Write-Output "pressed '$Press' (id=$($e.Current.AutomationId))"; exit 0 }
      $lp = $null
      if ($e.TryGetCurrentPattern([System.Windows.Automation.LegacyIAccessiblePattern]::Pattern, [ref]$lp)) { $lp.DoDefaultAction(); Write-Output "pressed '$Press' via legacy"; exit 0 }
    }
  }
  Write-Output "button '$Press' not found"; exit 3
}
