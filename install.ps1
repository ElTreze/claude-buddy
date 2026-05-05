# Claude Buddy - Windows installer
# Run: .\install.ps1
# Uninstall: .\install.ps1 -Uninstall

param([switch]$Uninstall)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$installPy = Join-Path $scriptDir "scripts\install.py"

if ($Uninstall) {
    python $installPy --uninstall
} else {
    python $installPy
}
