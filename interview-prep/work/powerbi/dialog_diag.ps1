param([long]$Hwnd, [string]$Id = "")
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$AE = [System.Windows.Automation.AutomationElement]
$dlg = $AE::FromHandle([IntPtr]$Hwnd)
$all = $dlg.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.Condition]::TrueCondition)
foreach ($e in $all) {
  $c = $e.Current
  if ($Id -and $c.AutomationId -ne $Id -and $c.ClassName -notlike "*$Id*") { continue }
  $pats = ($e.GetSupportedPatterns() | ForEach-Object { $_.ProgrammaticName -replace 'Identifiers.Pattern','' }) -join ','
  Write-Output ("id={0} class={1} ctype={2} hwnd={3} name='{4}' pats={5}" -f $c.AutomationId, $c.ClassName, $c.ControlType.Id, $c.NativeWindowHandle, $c.Name, $pats)
}
