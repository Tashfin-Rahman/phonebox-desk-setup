Get-Process | Where-Object { $_.MainWindowTitle } | Sort-Object CPU -Descending | Select-Object -First 6 | ForEach-Object { '{0}: {1}' -f $_.ProcessName, $_.MainWindowTitle }
