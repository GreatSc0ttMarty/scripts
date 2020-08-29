######################################################
# 			Folder Permissions Script				 #
# Script watches for files to be created in a folder #
# and applies the folder's permissions to all files. #
#													 #
# Set $FolderPath Var to the desired folder location #
######################################################


# Elevate Powershell Prompt

param([switch]$Elevated)

function Test-Admin {
  $currentUser = New-Object Security.Principal.WindowsPrincipal $([Security.Principal.WindowsIdentity]::GetCurrent())
  $currentUser.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
}

if ((Test-Admin) -eq $false)  {
    if ($elevated) 
    {
        # tried to elevate, did not work, aborting
    } 
    else {
        Start-Process powershell.exe -Verb RunAs -ArgumentList ('-noprofile -noexit -file "{0}" -elevated' -f ($myinvocation.MyCommand.Definition))
}

exit
}

Write-Host '**running with full privileges**'
Write-Host '**DO NOT CLOSE THIS WINDOW**'

$FolderPath = "{PATH}"
$watcher = New-Object System.IO.FileSystemWatcher
$watcher.IncludeSubdirectories = $true
$watcher.Path = $FolderPath
$watcher.EnableRaisingEvents = $true
$action =
{
    $path = $event.SourceEventArgs.FullPath
    $changetype = $event.SourceEventArgs.ChangeType
    $file = Split-Path -Path $path -Leaf -Resolve
	$Path_Resolve = Split-Path -Path $path 
	get-acl $Path_Resolve | set-acl $path
	Write-Host "Security Permissions Updated on $file"
}
Register-ObjectEvent $watcher 'Created' -Action $action

# To remove all event watchers run Get-EventSubscriber | Unregister-Event