<#
Find a push button by name inside one window (by hwnd) with MSAA (oleacc) and run its default
action. Used for the HTML dialogs Power BI Desktop hosts in an embedded browser control, which
UI Automation does not expose. Scoped to the given hwnd only.

  powershell -NoProfile -ExecutionPolicy Bypass -File msaa_click.ps1 -Hwnd 464956 -Name OK [-ListOnly]
#>
param([long]$Hwnd, [string]$Name = "OK", [switch]$ListOnly)
Add-Type -Language CSharp -TypeDefinition @"
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using Accessibility;
public static class Msaa {
  [DllImport("oleacc.dll")] static extern int AccessibleObjectFromWindow(IntPtr hwnd, uint id, ref Guid iid, [MarshalAs(UnmanagedType.IUnknown)] out object obj);
  [DllImport("oleacc.dll")] static extern int AccessibleChildren(IAccessible acc, int start, int count, [Out] object[] children, out int obtained);
  public static List<string> Log = new List<string>();
  static IAccessible Root(IntPtr h) {
    Guid g = new Guid("618736E0-3C3D-11CF-810C-00AA00389B71"); object o;
    AccessibleObjectFromWindow(h, 0xFFFFFFFC, ref g, out o); return o as IAccessible; }
  public static bool Walk(IntPtr h, string name, bool listOnly) { return Visit(Root(h), name, listOnly, 0); }
  static bool Visit(IAccessible acc, string name, bool listOnly, int depth) {
    if (acc == null || depth > 25) return false;
    int n = 0; try { n = acc.accChildCount; } catch { return false; }
    if (n == 0) return false;
    object[] kids = new object[n]; int got;
    if (AccessibleChildren(acc, 0, n, kids, out got) != 0) return false;
    for (int i = 0; i < got; i++) {
      IAccessible c = kids[i] as IAccessible;
      if (c != null) {
        string nm = null; object role = null;
        try { nm = c.get_accName(0); role = c.get_accRole(0); } catch {}
        if (!string.IsNullOrEmpty(nm)) Log.Add(new string(' ', depth * 2) + role + " | " + nm);
        if (!listOnly && nm != null && nm.Trim() == name && role is int && ((int)role == 43 || (int)role == 44)) {
          c.accDoDefaultAction(0); Log.Add("DID default action on '" + nm + "'"); return true; }
        if (Visit(c, name, listOnly, depth + 1)) return true;
      } else if (kids[i] is int) {
        string nm = null; object role = null;
        try { nm = acc.get_accName(kids[i]); role = acc.get_accRole(kids[i]); } catch {}
        if (!string.IsNullOrEmpty(nm)) Log.Add(new string(' ', depth * 2) + role + " | " + nm + " (simple)");
        if (!listOnly && nm != null && nm.Trim() == name && role is int && ((int)role == 43 || (int)role == 44)) {
          acc.accDoDefaultAction(kids[i]); Log.Add("DID default action on '" + nm + "' (simple)"); return true; }
      }
    }
    return false;
  }
}
"@ -ReferencedAssemblies "Accessibility"
$ok = [Msaa]::Walk([IntPtr]$Hwnd, $Name, [bool]$ListOnly)
[Msaa]::Log | Select-Object -First 80 | ForEach-Object { Write-Output $_ }
Write-Output "result: $ok"
