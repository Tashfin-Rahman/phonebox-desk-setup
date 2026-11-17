$f=Join-Path $env:LOCALAPPDATA ('PhoneBox\activity\'+(Get-Date -Format 'yyyy-MM-dd')+'.csv')
if(-not (Test-Path $f)){'Nothing tracked yet today.'; 'Keep the Home or Live page on screen.'; return}
$rows=Get-Content $f -Encoding UTF8 | Where-Object {$_ -match ','} | ForEach-Object { $a=$_.Split(',',2); [pscustomobject]@{m=$a[0];a=$a[1]} }
$mins=$rows | Group-Object m | ForEach-Object { ($_.Group | Group-Object a | Sort-Object Count -Descending | Select-Object -First 1).Name }
$fmt={param($n) $h=[math]::Floor($n/60); $m=$n%60; if($h){'{0} h {1:D2} m' -f $h,$m}else{'{0} m' -f $m}}
$mins | Group-Object | Sort-Object Count -Descending | Select-Object -First 7 | ForEach-Object { '{0,-12} {1}' -f $_.Name, (& $fmt $_.Count) }
'----'; 'Tracked today: '+(& $fmt @($mins).Count)
