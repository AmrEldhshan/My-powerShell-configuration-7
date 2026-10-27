# ==============================================
# ZeroAccess PowerShell profile entry point
# ==============================================
# The canonical, optimized profile lives at ../Profile.ps1.
# Either copy Profile.ps1 to $PROFILE, or keep this file in the
# repository and dot-source the canonical profile from here.

$canonicalProfile = Join-Path (Split-Path $PSScriptRoot -Parent) 'Profile.ps1'

if (Test-Path -LiteralPath $canonicalProfile) {
    . $canonicalProfile
} else {
    Write-Warning "Profile.ps1 was not found at '$canonicalProfile'. Copy Profile.ps1 to $PROFILE instead."
}
