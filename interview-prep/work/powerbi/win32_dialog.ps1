<#
Win32 fallback for common dialogs whose controls expose no UIA patterns.
Checks that every hwnd belongs to the expected PID before sending anything.

  -ExpectPid 65436 -EditHwnd 918798 -Text "C:\x\y.pbit"      (WM_SETTEXT)
  -ExpectPid 65436 -ButtonHwnd 3215620                        (BM_CLICK)
  -ExpectPid 65436 -ReadHwnd 918798                           (WM_GETTEXT)
#>
param([int]$ExpectPid, [long]$EditHwnd = 0, [string]$Text = "", [long]$ButtonHwnd = 0, [long]$ReadHwnd = 0)
Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Text;
public static class W32D {
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern IntPtr SendMessage(IntPtr h, uint m, IntPtr w, string l);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern IntPtr SendMessage(IntPtr h, uint m, IntPtr w, StringBuilder l);
  [DllImport("user32.dll")] public static extern IntPtr SendMessage(IntPtr h, uint m, IntPtr w, IntPtr l);
  [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr h, uint m, IntPtr w, IntPtr l);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll")] public static extern bool IsWindow(IntPtr h);
}
"@
function Check-Owner([long]$h) {
  if (-not [W32D]::IsWindow([IntPtr]$h)) { Write-Output "hwnd $h is not a window"; exit 1 }
  $p = 0; [void][W32D]::GetWindowThreadProcessId([IntPtr]$h, [ref]$p)
  if ($p -ne $ExpectPid) { Write-Output "hwnd $h belongs to PID $p, not ${ExpectPid}; refusing"; exit 1 }
}
if ($EditHwnd) {
  Check-Owner $EditHwnd
  [void][W32D]::SendMessage([IntPtr]$EditHwnd, 0x000C, [IntPtr]::Zero, $Text)
  $sb = New-Object System.Text.StringBuilder 1024
  [void][W32D]::SendMessage([IntPtr]$EditHwnd, 0x000D, [IntPtr]1024, $sb)
  Write-Output "edit now '$($sb.ToString())'"
}
if ($ReadHwnd) {
  Check-Owner $ReadHwnd
  $sb = New-Object System.Text.StringBuilder 1024
  [void][W32D]::SendMessage([IntPtr]$ReadHwnd, 0x000D, [IntPtr]1024, $sb)
  Write-Output "text '$($sb.ToString())'"
}
if ($ButtonHwnd) {
  Check-Owner $ButtonHwnd
  # BM_CLICK posted so a modal follow-up cannot block this script
  [void][W32D]::PostMessage([IntPtr]$ButtonHwnd, 0x00F5, [IntPtr]::Zero, [IntPtr]::Zero)
  Write-Output "BM_CLICK posted to $ButtonHwnd"
}
