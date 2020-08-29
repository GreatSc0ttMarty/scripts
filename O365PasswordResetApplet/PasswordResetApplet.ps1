# Hide PowerShell Console
Add-Type -Name Window -Namespace Console -MemberDefinition '
[DllImport("Kernel32.dll")]
public static extern IntPtr GetConsoleWindow();
[DllImport("user32.dll")]
public static extern bool ShowWindow(IntPtr hWnd, Int32 nCmdShow);
'
$consolePtr = [Console.Window]::GetConsoleWindow()
[Console.Window]::ShowWindow($consolePtr, 0)

$username = "{USERNAME}"
$password = ConvertTo-SecureString "{PASSWORD}" -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential -ArgumentList ($username, $password)

#Add-Type -assembly System.Windows.Forms
#$WaitWindow = New-Object System.Windows.Forms.Form
#$WaitWindow.Text ='Office 365 Password Reset Applet'
#$WaitWindow.Width = 375
#$WaitWindow.Height = 35
#$WaitWindow.AutoSize = $true
#
#$WaitLabel = New-Object System.Windows.Forms.Label
#$WaitLabel.Text = "Installing required modules and connecting to Office 365. Please wait..."
#$WaitLabel.Location  = New-Object System.Drawing.Point(10,10)
#$WaitLabel.Size = New-Object System.Drawing.Size(80,100)
#$WaitLabel.AutoSize = $true
#$WaitWindow.Controls.Add($WaitLabel)
#$WaitWindow.ShowDialog()

Install-Module MSOnline
Import-Module MSOnline

$Session = New-PSSession -ConfigurationName Microsoft.Exchange -ConnectionUri https://ps.outlook.com/powershell/ -Credential $Cred -Authentication Basic -AllowRedirection
try {
    Import-PSSession $Session -DisableNameChecking
}
catch {
    Write-Host "PSSESSION has already been imported."
}

Import-Module MSOnline
Connect-MsolService -Credential $Cred
$E1Users = get-MSOLUser -All | where {$_.isLicensed -eq "TRUE" -and $_.Licenses.AccountSKUID -eq "kodiakroofing:EXCHANGESTANDARD"}
$UserPrincipalName = get-MSOLUser -All | where {$_.isLicensed -eq "TRUE" -and $_.Licenses.AccountSKUID -eq "kodiakroofing:EXCHANGESTANDARD"} | Sort-Object -Property @{Expression = "Status"; Descending = $True}, @{Expression = "DisplayName"; Descending = $False} | Select UserPrincipalName | ft -HideTableHeaders | Out-String

Add-Type -assembly System.Windows.Forms
$main_form = New-Object System.Windows.Forms.Form
$main_form.Text ='Office 365 Password Reset Applet'
$main_form.Width = 375
$main_form.Height = 200
$main_form.AutoSize = $true

$Label = New-Object System.Windows.Forms.Label
$Label.Text = "E1 Office 365 Users:"
$Label.Location  = New-Object System.Drawing.Point(10,10)
$Label.AutoSize = $true
$main_form.Controls.Add($Label)

$ComboBox = New-Object System.Windows.Forms.ComboBox
$ComboBox.Width = 200
Foreach ($r in $UserPrincipalName -split '(?<=.com)'){If ($r -ne "") {$ComboBox.Items.Add($r.trim().ToLower())}}
$ComboBox.Location  = New-Object System.Drawing.Point(130,10)
$main_form.Controls.Add($ComboBox)

$PassLabel = New-Object System.Windows.Forms.Label
$PassLabel.Text = "Enter New Password:"
$PassLabel.Location  = New-Object System.Drawing.Point(10,52)
$PassLabel.AutoSize = $true
$main_form.Controls.Add($PassLabel)

$TextBox = New-Object System.Windows.Forms.TextBox
$TextBox.Location = New-Object System.Drawing.Size(130,50)
$TextBox.Size = New-Object System.Drawing.Size(200,23)
$main_form.Controls.Add($TextBox)

$Button = New-Object System.Windows.Forms.Button
$Button.Location = New-Object System.Drawing.Size(120,100)
$Button.Size = New-Object System.Drawing.Size(120,23)
$Button.Text = "OK"
$main_form.Controls.Add($Button)

$Label3 = New-Object System.Windows.Forms.Label
$Label3.Text = ""
$Label3.Location  = New-Object System.Drawing.Point(15, 80)
$Label3.AutoSize = $true
$main_form.Controls.Add($Label3)

$Button.Add_Click(
    {
        try {
            $Label3.Refresh()
            Set-MsolUserPassword -UserPrincipalName $ComboBox.selectedItem -NewPassword $TextBox.Text
            $Label3.Text =  $ComboBox.selectedItem + "'s password has been reset."
        }
        catch {
            $Label3.Refresh()
            $Label3.Text =  "Error Resetting" + $ComboBox.selectedItem + " Password. `nPlease try again or contact TEAMSOS."
        }
    }
)


$main_form.ShowDialog()

remove-pssession *