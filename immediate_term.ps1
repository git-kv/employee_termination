# Scheduled to check a folder every minute to see if there is an
# immediate termination waiting to be processed.
$root_path = "C:\Users\KVoelker\repos\immediate_account_disablement\"

while ($true) {
    $ShouldSync = Test-Path "$root_path*"

    if ($ShouldSync) {
        Get-ChildItem -Path $root_path | ForEach-Object {
            $user_to_be_disabled = $_.BaseName
            Write-Host $user_to_be_disabled
            # Disable-ADAccount -Identity $user_to_be_disabled
            # New-Item "\\eocservices\apps$\programs\scripts\active_directory\needsync\sync_plz"
            Remove-Item $_
        }
    }
    Start-Sleep -Seconds 60
}