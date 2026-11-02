<#
General UI Automation helper scoped to ONE process (by PID). Never touches other applications.

  List named elements (optionally filtered):   -ProcId 123 -List [-Filter "Export"] [-Window "Save As"]
  Invoke an element by exact name:             -ProcId 123 -Click "Export" [-Type MenuItem] [-Window ...] [-Index 0]
  Set the text of an edit box:                 -ProcId 123 -SetText "C:\x\y.pbit" -Name "File name:" [-Window "Save As"]
  Expand a combo box and pick an item:         -ProcId 123 -Combo "Save as type:" -Pick "Power BI template files (*.pbit)"

Invoke order: InvokePattern, SelectionItemPattern, TogglePattern, ExpandCollapsePattern,
LegacyIAccessible DoDefaultAction.
#>
param([int]$ProcId, [switch]$List, [string]$Filter = "", [string]$Window = "", [string]$Click = "",
      [string]$Type = "", [int]$Index = 0, [string]$SetText = "", [string]$Name = "", [string]$Combo = "",
      [string]$Pick = "")
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$AE = [System.Windows.Automation.AutomationElement]
$root = $AE::RootElement
$pidCond = New-Object System.Windows.Automation.PropertyCondition($AE::ProcessIdProperty, $ProcId)
$wins = $root.FindAll([System.Windows.Automation.TreeScope]::Children, $pidCond)
$targets = @()
foreach ($w in $wins) { if (-not $Window -or $w.Current.Name -like "*$Window*") { $targets += $w } }
if ($targets.Count -eq 0) { Write-Output "no window matching '$Window' (have: $(($wins | ForEach-Object { $_.Current.Name }) -join ' | '))"; exit 1 }

function Invoke-El($el) {
  $p = $null
  if ($el.TryGetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern, [ref]$p)) { $p.Invoke(); return "invoke" }
  if ($el.TryGetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern, [ref]$p)) { $p.Select(); return "select" }
  if ($el.TryGetCurrentPattern([System.Windows.Automation.TogglePattern]::Pattern, [ref]$p)) { $p.Toggle(); return "toggle" }
  if ($el.TryGetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern, [ref]$p)) { $p.Expand(); return "expand" }
  if ($el.TryGetCurrentPattern([System.Windows.Automation.LegacyIAccessiblePattern]::Pattern, [ref]$p)) { $p.DoDefaultAction(); return "legacy" }
  return $null
}

$all = New-Object System.Collections.ArrayList
foreach ($w in $targets) {
  $els = $w.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.Condition]::TrueCondition)
  foreach ($e in $els) { [void]$all.Add(@{ el = $e; win = $w.Current.Name }) }
}

if ($List) {
  foreach ($x in $all) {
    $n = $x.el.Current.Name; $t = $x.el.Current.ControlType.ProgrammaticName -replace 'ControlType\.', ''
    if ($n -and ($Filter -eq "" -or $n -like "*$Filter*")) { Write-Output "[$t] '$n'   (win '$($x.win)')" }
  }
  exit 0
}

if ($Click) {
  $hits = @($all | Where-Object { $_.el.Current.Name -eq $Click -and ($Type -eq "" -or $_.el.Current.ControlType.ProgrammaticName -eq "ControlType.$Type") })
  if ($hits.Count -le $Index) { Write-Output "not found: '$Click' type '$Type' (hits $($hits.Count))"; exit 2 }
  $how = Invoke-El $hits[$Index].el
  Write-Output "clicked '$Click' via $how"
  exit 0
}

if ($SetText) {
  $edits = @($all | Where-Object { $_.el.Current.ControlType.ProgrammaticName -eq "ControlType.Edit" -and ($Name -eq "" -or $_.el.Current.Name -eq $Name) })
  if ($edits.Count -eq 0) { Write-Output "no edit '$Name'"; exit 3 }
  $p = $null
  if ($edits[0].el.TryGetCurrentPattern([System.Windows.Automation.ValuePattern]::Pattern, [ref]$p)) { $p.SetValue($SetText); Write-Output "set '$Name' = '$SetText'" ; exit 0 }
  Write-Output "edit has no ValuePattern"; exit 4
}

if ($Combo) {
  $cb = @($all | Where-Object { $_.el.Current.ControlType.ProgrammaticName -eq "ControlType.ComboBox" -and $_.el.Current.Name -eq $Combo })
  if ($cb.Count -eq 0) { Write-Output "no combo '$Combo'"; exit 5 }
  $p = $null
  if ($cb[0].el.TryGetCurrentPattern([System.Windows.Automation.ExpandCollapsePattern]::Pattern, [ref]$p)) { $p.Expand(); Start-Sleep -Milliseconds 600 }
  $items = $cb[0].el.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.Condition]::TrueCondition)
  foreach ($i in $items) {
    if ($i.Current.Name) { Write-Output "  option '$($i.Current.Name)'" }
    if ($Pick -and $i.Current.Name -eq $Pick) {
      $sp = $null
      if ($i.TryGetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern, [ref]$sp)) { $sp.Select(); Write-Output "picked '$Pick'" }
    }
  }
  if ($p) { try { $p.Collapse() } catch {} }
  exit 0
}
