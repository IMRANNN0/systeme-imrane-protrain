# Use the installed Windows PATH in this process; never edit the global PATH.
$workspacePath = Split-Path -Parent $PSScriptRoot
$persistedMachinePath = [Environment]::GetEnvironmentVariable('Path', 'Machine')
$persistedUserPath = [Environment]::GetEnvironmentVariable('Path', 'User')
$env:Path = $env:Path + ';' + $persistedMachinePath + ';' + $persistedUserPath
& python -X utf8 (Join-Path $PSScriptRoot 'systeme-imrane\scripts\imrane.py') @args --workspace $workspacePath
exit $LASTEXITCODE
