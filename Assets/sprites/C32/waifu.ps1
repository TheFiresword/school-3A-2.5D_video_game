
$varCheminRepertoireScript = [System.IO.Path]::GetDirectoryName($MyInvocation.MyCommand.Definition) #On rÃ©cupÃ¨re le chemin du rÃ©pertoire contenant ce script

$NomExe = "C:\Users\Alban Waxin\Downloads\waifu2x-ncnn-vulkan-20220728-windows\waifu2x-ncnn-vulkan.exe"

$MonFolder = Get-ChildItem -Path $varCheminRepertoireScript -File | Where-Object {$_.Name -match 'png$'} #On rÃ©cupÃ¨re la liste des fichiers de ce rÃ©pertoire
foreach ($MyFile in $MonFolder)
{
    start-process -FilePath $NomExe -ArgumentList "-i $MyFile -o $MyFile -n 2 s 2" -workingdirectory $varCheminRepertoireScript -NoNewWindow -Wait
    Write-Host "$($MyFile.name) / $($MyFile.FullName)"
}

