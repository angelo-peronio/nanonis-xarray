<#
    .SYNOPSIS
    Bootstrap a development environment.
#>

#Requires -Version 7.4
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

&"$PSScriptRoot\New-PythonVenv.ps1"
# Do not update pre-commit hooks on bootstrap, since cffconvert fails to update.
# &"$PSScriptRoot\Update-PreCommitHooks.ps1"
&"$PSScriptRoot\Install-PreCommitHooks.ps1"
