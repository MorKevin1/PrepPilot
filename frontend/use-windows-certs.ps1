# Node does not use the Windows cert store. Run this in the same terminal
# before npm / npx / vite so HTTPS to the registry works on this network.
$env:NODE_EXTRA_CA_CERTS = Join-Path $PSScriptRoot ".certs\windows-ca-bundle.pem"
Write-Host "NODE_EXTRA_CA_CERTS=$env:NODE_EXTRA_CA_CERTS"
