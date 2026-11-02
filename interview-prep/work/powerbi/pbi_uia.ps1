<#
UI Automation helper scoped to ONE Power BI Desktop process (by PID): list the named buttons
and tabs in its windows, or invoke one by name. Never touches other applications.

  powershell -NoProfile -ExecutionPolicy Bypass -File pbi_uia.ps1 -ProcId 60944 -List
  powershell -NoProfile -ExecutionPolicy Bypass -File pbi_uia.ps1 -ProcId 60944 -Click "OK"
#>
param([int]$ProcId, [switch]$List, [string]$Click, [string]$ControlType = "Button")
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$root = [System.Windows.Automation.AutomationElement]::RootElement
$pidCond = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ProcessIdProperty, $ProcId)
$wins = $root.FindAll([System.Windows.Automation.TreeScope]::Children, $pidCond)
Write-Output "top-level windows for ${ProcId}: $($wins.Count)"
$ct = switch ($ControlType) {
  "Button" { [System.Windows.Automation.ControlType]::Button }
  "TabItem" { [System.Windows.Automation.ControlType]::TabItem }
  "ListItem" { [System.Windows.Automation.ControlType]::ListItem }
  default { [System.Windows.Automation.ControlType]::Button }
}
$typeCond = New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ControlTypeProperty, $ct)
foreach ($w in $wins) {
  Write-Output "window: '$($w.Current.Name)'"
  $items = $w.FindAll([System.Windows.Automation.TreeScope]::Descendants, $typeCond)
  foreach ($b in $items) {
    $n = $b.Current.Name
    if ($List -and $n) { Write-Output "  [$ControlType] '$n'" }
    if ($Click -and $n -eq $Click) {
      $p = $null
      if ($b.TryGetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern, [ref]$p)) {
        $p.Invoke(); Write-Output "  invoked '$n'"; exit 0
      } elseif ($b.TryGetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern, [ref]$p)) {
        $p.Select(); Write-Output "  selected '$n'"; exit 0
      }
    }
  }
}
if ($Click) { Write-Output "no '$Click' found"; exit 1 }
