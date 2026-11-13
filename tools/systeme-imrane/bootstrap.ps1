# Run from a trusted clone. No ExecutionPolicy change and no remote shell script.
[CmdletBinding()]
param([string]$Workspace, [ValidateSet('core','complete')][string]$Profile='complete', [switch]$Apply)
$ErrorActionPreference = 'Stop'
if (-not $Workspace) { throw 'Pass -Workspace with a new or reviewed workspace path.' }
$pythonCommand = $null
foreach ($candidateName in @('python3','python','py')) {
  foreach ($candidate in @(Get-Command $candidateName -All -CommandType Application -ErrorAction SilentlyContinue)) {
    if ($candidate.Source -match '[\\/]Microsoft[\\/]WindowsApps[\\/]') { continue }
    $candidateWorks = $false
    try {
      $probeOutput = & $candidate.Source -c 'import sys; sys.exit(0 if sys.version_info >= (3,11) else 1)' 2>&1
      $candidateWorks = ($LASTEXITCODE -eq 0)
    } catch {
      # A stale manager shim must not stop discovery of another working Python.
      $candidateWorks = $false
    }
    if ($candidateWorks) { $pythonCommand = $candidate.Source; break }
  }
  if ($pythonCommand) { break }
}
if (-not $pythonCommand) {
  Write-Output 'Missing working Python >=3.11. Plan: winget install --id Python.Python.3.12 --exact --source winget'
  if ($Apply) {
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) { throw 'Install Microsoft App Installer (winget) first.' }
    & winget install --id Python.Python.3.12 --exact --source winget
    if ($LASTEXITCODE -ne 0) { throw 'Python installation failed.' }
    Write-Output 'Reopen your terminal and rerun this command to use the installed Python.'
  }
  exit 1
}
$applyArgs = @()
if ($Apply) { $applyArgs += '--apply' }
& $pythonCommand "$PSScriptRoot/scripts/imrane.py" deps --workspace $Workspace --profile $Profile @applyArgs
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $pythonCommand "$PSScriptRoot/scripts/imrane.py" init --workspace $Workspace @applyArgs
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
if ($Profile -eq 'complete') {
  & $pythonCommand "$PSScriptRoot/scripts/skills.py" install --workspace $Workspace --all @applyArgs
  exit $LASTEXITCODE
}
Write-Output 'Core profile: no optional skills installed. Use complete or install chosen GitHub skills individually.'
exit 0
