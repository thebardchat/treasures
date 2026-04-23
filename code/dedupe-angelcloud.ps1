[CmdletBinding()]
param(
  [string]$DestProject = "$env:USERPROFILE\Desktop\angel-cloud-main",
  [string]$ScanDir,      # leave blank to auto-pick the newest scan folder on Desktop
  [switch]$Apply         # add -Apply to actually copy; default is report-only
)

function Get-LatestScanDir {
  $root = "$env:USERPROFILE\Desktop"
  if (-not (Test-Path $root)) { return $null }
  $d = Get-ChildItem -Path $root -Directory -Filter 'angel-cloud-scan-*' |
       Sort-Object LastWriteTime -Descending |
       Select-Object -First 1
  return $d
}

# Resolve ScanDir (PowerShell 5.1 friendly – no ??)
if (-not $ScanDir -or -not (Test-Path $ScanDir)) {
  $latest = Get-LatestScanDir
  if ($latest) { $ScanDir = $latest.FullName }
  else { throw "Could not find an 'angel-cloud-scan-*' directory on your Desktop. Run scan-angelcloud.ps1 first." }
}

# Input list created by the scan
$memListPath = Join-Path $ScanDir 'memory-system-files.txt'
if (-not (Test-Path $memListPath)) {
  throw "Not found: $memListPath. Run scan-angelcloud.ps1 first."
}

# Collect candidates
$memPaths = @()
try { $memPaths = Get-Content -Path $memListPath | Where-Object { $_ -and (Test-Path $_) } } catch {}

if (-not $memPaths -or $memPaths.Count -eq 0) {
  Write-Host "No memory-system.js files listed in $memListPath" -ForegroundColor Yellow
  return
}

# Build inventory with hashes
$rows = @()
foreach ($p in $memPaths) {
  try {
    $fi = Get-Item -LiteralPath $p -ErrorAction Stop
    $h  = Get-FileHash -LiteralPath $p -Algorithm SHA256 -ErrorAction Stop
    $rows += [pscustomobject]@{
      Path          = $fi.FullName
      Directory     = $fi.DirectoryName
      Name          = $fi.Name
      Length        = $fi.Length
      LastWriteTime = $fi.LastWriteTime
      SHA256        = $h.Hash
      InProject     = ($fi.FullName -like (Join-Path $DestProject '*'))
    }
  } catch { }
}

if (-not $rows -or $rows.Count -eq 0) {
  Write-Host "No readable memory-system.js files found." -ForegroundColor Yellow
  return
}

# Group identical files by content hash, pick freshest per hash
$byHash = $rows | Group-Object SHA256
$BestPerHash = @()
foreach ($g in $byHash) {
  $BestPerHash += ($g.Group | Sort-Object LastWriteTime -Descending | Select-Object -First 1)
}

# Choose global best:
# prefer one already inside DestProject if present, otherwise newest overall
$best = $null
$bestInProject = $BestPerHash | Where-Object { $_.InProject } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($bestInProject) { $best = $bestInProject }
else { $best = ($BestPerHash | Sort-Object LastWriteTime -Descending | Select-Object -First 1) }

# Write a detailed report
$reportCsv = Join-Path $ScanDir 'memory-system-report.csv'
$rows | Sort-Object SHA256, LastWriteTime -Descending |
  Export-Csv -Path $reportCsv -NoTypeInformation -Encoding UTF8

Write-Host ""
Write-Host "Report written:" -ForegroundColor Green
Write-Host "  $reportCsv" -ForegroundColor Yellow
Write-Host ""

Write-Host "Selected best candidate:" -ForegroundColor Cyan
$best | Format-List Path, Length, LastWriteTime, SHA256, InProject

if (-not $Apply) {
  Write-Host ""
  Write-Host "Preview mode only. Re-run with -Apply to copy into your project." -ForegroundColor DarkYellow
  return
}

# Apply: copy into DestProject\automation\memory-system.js (with backup if different)
$destAutomation = Join-Path $DestProject 'automation'
$destFile       = Join-Path $destAutomation 'memory-system.js'
$archiveDir     = Join-Path $DestProject 'archive\memory-system'

# Ensure dirs exist
try { New-Item -ItemType Directory -Path $destAutomation -Force -ErrorAction SilentlyContinue | Out-Null } catch {}
try { New-Item -ItemType Directory -Path $archiveDir     -Force -ErrorAction SilentlyContinue | Out-Null } catch {}

# Determine if copy is needed
$needCopy = $true
if (Test-Path $destFile) {
  try {
    $destHash = (Get-FileHash -LiteralPath $destFile -Algorithm SHA256).Hash
    if ($destHash -eq $best.SHA256) { $needCopy = $false }
  } catch { }
}

if (-not $needCopy) {
  Write-Host ""
  Write-Host "Destination already has the same memory-system.js. No changes made." -ForegroundColor Green
  return
}

# Backup existing if present and different
if (Test-Path $destFile) {
  $stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
  $backupPath = Join-Path $archiveDir ("memory-system-$stamp.js")
  Copy-Item -LiteralPath $destFile -Destination $backupPath -Force
  Write-Host ("Backed up existing file to: {0}" -f $backupPath) -ForegroundColor DarkCyan
}

# Copy the chosen best file
Copy-Item -LiteralPath $best.Path -Destination $destFile -Force
Write-Host ("Updated: {0}" -f $destFile) -ForegroundColor Green
