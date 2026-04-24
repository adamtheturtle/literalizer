$ErrorActionPreference = 'Stop'
$stream = [Console]::OpenStandardInput()
$buffer = New-Object System.IO.MemoryStream
$stream.CopyTo($buffer)
$paths = [System.Text.Encoding]::UTF8.GetString($buffer.ToArray()) -split "`0" |
    Where-Object { $_ }
$failed = $false
foreach ($p in $paths) {
    try {
        $block = [scriptblock]::Create((Get-Content -Raw -LiteralPath $p))
        & $block
    } catch {
        [Console]::Error.WriteLine("FAIL ${p}: $($_.Exception.Message)")
        $failed = $true
    }
}
if ($failed) { exit 1 }
