$ErrorActionPreference='SilentlyContinue'
$sig='[DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow(); [DllImport("user32.dll")] public static extern int GetWindowThreadProcessId(IntPtr h, out int p); [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, System.Text.StringBuilder s, int n); [StructLayout(LayoutKind.Sequential)] public struct LII { public uint cbSize; public uint dwTime; } [DllImport("user32.dll")] public static extern bool GetLastInputInfo(ref LII l);'
Add-Type -Namespace PB -Name W -MemberDefinition $sig
$h=[PB.W]::GetForegroundWindow(); $id=0; [void][PB.W]::GetWindowThreadProcessId($h,[ref]$id)
$sb=New-Object Text.StringBuilder 512; [void][PB.W]::GetWindowText($h,$sb,512); $t=$sb.ToString(); $p=(Get-Process -Id $id).ProcessName
$l=New-Object PB.W+LII; $l.cbSize=8; [void][PB.W]::GetLastInputInfo([ref]$l)
$now=[BitConverter]::ToUInt32([BitConverter]::GetBytes([Environment]::TickCount),0); $d=[double]$now-[double]$l.dwTime; if($d -lt 0){$d+=4294967296}; $idle=$d/1000
$tl=($t -replace '^\(\d+\)\s*','') -replace ' - (Opera|Google Chrome|Brave|Mozilla Firefox|Personal - Microsoft.*Edge)$',''
if($idle -gt 180){$i=0x1F4A4;$v='Away from the PC';$app='Away';$tl=('idle for {0} min' -f [math]::Floor($idle/60))}
elseif($t -match 'YouTube'){$i=0x1F4FA;$v='Watching';$app='YouTube';$tl=$tl -replace ' - YouTube$',''}
elseif($p -match '^(cs2|FC2\d|FC2\d_Trial)$'){$i=0x1F3AE;$v='Playing';$app='Gaming'}
elseif($p -eq 'Discord'){$i=0x1F4AC;$v='On Discord';$app='Discord'}
elseif($t -match 'WhatsApp'){$i=0x1F4AC;$v='On WhatsApp';$app='WhatsApp'}
elseif($p -eq 'Spotify'){$i=0x1F3A7;$v='On Spotify';$app='Spotify'}
elseif($p -match '^(claude|Code|WindowsTerminal|powershell|pwsh)$'){$i=0x1F4BB;$v='Working with AI / code';$app='Coding & AI'}
elseif($p -match '^(WINWORD|EXCEL|POWERPNT|Acrobat|AcroRd32|Notion|Obsidian)$'){$i=0x1F4DA;$v='Studying';$app='Study apps'}
elseif($p -match '^(opera|chrome|msedge|brave|firefox)$'){$i=0x1F310;$v='Browsing';$app='Browsing'}
elseif($p -eq 'explorer'){$i=0x1F5C2;$v='In File Explorer';$app='Other'}
else{$i=0x1F5A5;$v=('Using '+$p);$app=$p}
if($tl.Length -gt 70){$tl=$tl.Substring(0,67)+'...'}
($([char]::ConvertFromUtf32($i))+' '+$v); $tl
if($app -ne 'Away'){$dir=Join-Path $env:LOCALAPPDATA 'PhoneBox\activity'; New-Item -ItemType Directory -Force $dir | Out-Null; Add-Content -Path (Join-Path $dir ((Get-Date -Format 'yyyy-MM-dd')+'.csv')) -Value ((Get-Date -Format 'HH:mm')+','+$app) -Encoding UTF8}
