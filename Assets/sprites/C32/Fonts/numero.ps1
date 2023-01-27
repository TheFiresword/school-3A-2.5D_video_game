$varCheminRepertoireScript = [System.IO.Path]::GetDirectoryName($MyInvocation.MyCommand.Definition) #On rÃ©cupÃ¨re le chemin du rÃ©pertoire contenant ce script

$Count = 0
$MonFolder = Get-ChildItem -Path $varCheminRepertoireScript -File | Where-Object {$_.Name -match 'png$'} #On rÃ©cupÃ¨re la liste des fichiers de ce rÃ©pertoire
foreach ($MyFile in $MonFolder)
{   
    $Count = $Count +1
    Rename-Item -Path $($MyFile.FullName) -NewName "$Count.png"
}
