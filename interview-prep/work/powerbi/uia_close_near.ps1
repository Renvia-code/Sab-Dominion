param([int]$ProcId, [string]$Text, [string]$Button = "Close")
# Click the button named $Button that sits in the same container as the text element named $Text
# (for teaching bubbles), searching only the windows of process $ProcId.
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$AE = [System.Windows.Automation.AutomationElement]
$walker = [System.Windows.Automation.TreeWalker]::ControlViewWalker
$pidCond = New-Object System.Windows.Automation.PropertyCondition($AE::ProcessIdProperty, $ProcId)
$wins = $AE::RootElement.FindAll([System.Windows.Automation.TreeScope]::Children, $pidCond)
$nameCond = New-Object System.Windows.Automation.PropertyCondition($AE::NameProperty, $Text)
foreach ($w in $wins) {
  $hits = $w.FindAll([System.Windows.Automation.TreeScope]::Descendants, $nameCond)
  foreach ($t in $hits) {
    $parent = $walker.GetParent($t)
    for ($up = 0; $up -lt 3 -and $parent; $up++) {
      $btnCond = New-Object System.Windows.Automation.AndCondition(
        (New-Object System.Windows.Automation.PropertyCondition($AE::NameProperty, $Button)),
        (New-Object System.Windows.Automation.PropertyCondition($AE::ControlTypeProperty, [System.Windows.Automation.ControlType]::Button)))
      $b = $parent.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $btnCond)
      if ($b) {
        $p = $null
        if ($b.TryGetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern, [ref]$p)) { $p.Invoke(); Write-Output "closed near '$Text' (up $up)"; exit 0 }
      }
      $parent = $walker.GetParent($parent)
    }
  }
}
Write-Output "nothing closed near '$Text'"; exit 1
