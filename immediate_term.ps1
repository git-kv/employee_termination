# Scheduled to check a folder every minute to see if there is an
# immediate termination waiting to be processed.
$root_path = "C:\Users\KVoelker\repos\immediate_account_disablement\"
$smtp_server = "exnode2.dartadvantage.com"
$from = "ImmediateTerm@dart.net"


while ($true) {
    $ShouldSync = Test-Path "$root_path*"

    if ($ShouldSync) {
        Get-ChildItem -Path $root_path | ForEach-Object {
            $user_to_be_disabled = $_.BaseName
            $vip_subject = "A separation request was submitted to immediately disable $user_to_be_disabled"
            $vip_body = "A separation request was submitted to immediately disable $user_to_be_disabled.`n`nSince this is a VIP account it will need to be disabled manually if immediate disablement is desired."
            $vip_recipients = "kvoelker@dart.net"
            $default_subject = "Account Disabled $user_to_be_disabled"
            $default_body = "$user_to_be_disabled's account has been disabled."
            $default_recipients = "kvoelker@dart.net"

            Get-ADPrincipalGroupMembership $user_to_be_disabled | Select-Object Name | ForEach-Object {
                if (($_.Name -eq "T2_Admins") -or ($_.Name -like "T2_VIP") -or ($_.Name -like "T1*") -or ($_.Name -like "T0*") -or ($_.Name -like "*Domain Admins")) {
                    Send-MailMessage -Subject $vip_subject -Body $vip_body -To $vip_recipients -From $from -SmtpServer $smtp_server
                }
                else {
                    Disable-ADAccount -Identity $user_to_be_disabled
                    New-Item "\\eocservices\apps$\programs\scripts\active_directory\needsync\sync_plz"
                    Send-MailMessage -Subject $default_subject -Body $default_body -To $default_recipients -From $from -SmtpServer $smtp_server
                }
            }
            Remove-Item $_
        }
    }
    Start-Sleep -Seconds 60
}