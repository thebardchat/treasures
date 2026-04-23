[CmdletBinding()]
param(
  [string[]]$Roots = @(
    "$env:USERPROFILE\Desktop",
    "$env:USERPROFILE\Downloads",
    "$env:USERPROFILE\Documents",
    "$env:OneDrive"
  ),
  [string]$OutDir = (Join-Path (Get-Location) ("angel-cloud-scan-" + (Get-Date -Format "yyyyMMdd_HHmm")))
)

# -------- Helpers --------
function New-OutDir {
  if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir | Out-Null }
}

function Should-SkipPath {
  param([string]$FullName)
  return ($FullName -match '\\AppData\\' -or
          $FullName -match '\\node_modules\\' -or
          $FullName -match '\\\$RECYCLE\.BIN\\' -or
          $FullName -match '\\System Volume Information\\')
}

function Safe-Enumerate {
  param(
    [string]$Root,
    [switch]$Files,
    [switch]$Directories,
    [string]$Filter,
    [switch]$Recurse
  )
  if (-not (Test-Path $Root)) { return @() }

  $common = @{
    LiteralPath = $Root
    Force       = $true
    ErrorAction = 'SilentlyContinue'
  }
  if ($Files)       { $common['File']      = $true }
  if ($Directories) { $common['Directory'] = $true }
  if ($Filter)      { $common['Filter']    = $Filter }

  if ($Recurse) {
    $items = Get-ChildItem @common -Recurse
  } else {
    $items = Get-ChildItem @common
  }
  if (-not $items) { return @() }
  $items | Where-Object { -not (Should-SkipPath -FullName $_.FullName) }
}

function Write-List {
  param([string[]]$Lines, [string]$FileName)
  $dest = Join-Path $OutDir $FileName
  $Lines | Sort-Object -Unique | Set-Content -Encoding UTF8 -Path $dest
  return $dest
}

# -------- Start --------
Write-Host "► Scan starting..." -ForegroundColor Cyan
New-OutDir

# Normalize/verify roots
$Roots = $Roots | Where-Object { $_ -and (Test-Path $_) } | Sort-Object -Unique
if (-not $Roots) { throw "No valid roots to scan. Provide directories with -Roots." }

Write-Host "Roots:" -ForegroundColor DarkCyan
$Roots | ForEach-Object { Write-Host "  - $_" }

# -------- Collect --------
$angelCloud    = @()
$automationDirs= @()
$memorySystem  = @()
$googleapis    = @()
$pkgFiles      = @()

foreach ($r in $Roots) {
  Write-Host "Scanning: $r" -ForegroundColor DarkGray

  $angelCloud += Safe-Enumerate -Root $r -Recurse |
    Where-Object { $_.FullName -match 'angel-cloud' } |
    Select-Object -ExpandProperty FullName

  $automationDirs += Safe-Enumerate -Root $r -Directories -Recurse |
    Where-Object { $_.Name -match 'automation' } |
    Select-Object -ExpandProperty FullName

  $memorySystem += Safe-Enumerate -Root $r -Files -Filter 'memory-system.js' -Recurse |
    Select-Object -ExpandProperty FullName

  $googleapis += Safe-Enumerate -Root $r -Recurse |
    Where-Object { $_.FullName -match 'googleapis' } |
    Select-Object -ExpandProperty FullName

  $pkgFiles += Safe-Enumerate -Root $r -Files -Filter 'package.json' -Recurse |
    Select-Object -ExpandProperty FullName
}

# Deduplicate
$angelCloud     = $angelCloud     | Sort-Object -Unique
$automationDirs = $automationDirs | Sort-Object -Unique
$memorySystem   = $memorySystem   | Sort-Object -Unique
$googleapis     = $googleapis     | Sort-Object -Unique
$pkgFiles       = $pkgFiles       | Sort-Object -Unique

# -------- Write lists --------
$angelFile = Write-List -Lines $angelCloud -FileName 'angel-cloud-paths.txt'
$autoFile  = Write-List -Lines $automationDirs -FileName 'automation-dirs.txt'
$memFile   = Write-List -Lines $memorySystem -FileName 'memory-system-files.txt'
$gaFile    = Write-List -Lines $googleapis -FileName 'googleapis-paths.txt'
$pkgList   = Write-List -Lines $pkgFiles -FileName 'package-json-files.txt'

# Also summarize package.json name/version to CSV (PS5-safe)
$pkgRows = @()
foreach ($pkg in $pkgFiles) {
  try {
    $raw  = Get-Content -Raw -ErrorAction Stop -Path $pkg
    $meta = $null
    try {
      $meta = $raw | ConvertFrom-Json -ErrorAction Stop
    } catch {
      $meta = $null
    }

    $pkgName = ''
    $pkgVer  = ''
    if ($meta -ne $null) {
      if ($meta.PSObject.Properties['name'])    { $pkgName = [string]$meta.name }
      if ($meta.PSObject.Properties['version']) { $pkgVer  = [string]$meta.version }
    }

    $pkgRows += [pscustomobject]@{
      PackageJsonPath = $pkg
      PackageName     = $pkgName
      PackageVersion  = $pkgVer
    }
  } catch {
    $pkgRows += [pscustomobject]@{
      PackageJsonPath = $pkg
      PackageName     = ''
      PackageVersion  = ''
    }
  }
}

$pkgCsv = Join-Path $OutDir 'node-packages.csv'
$pkgRows | Export-Csv -Path $pkgCsv -NoTypeInformation -Encoding UTF8

Write-Host ""
Write-Host "✓ Done. Results saved to:" -ForegroundColor Green
Write-Host "  $OutDir" -ForegroundColor Yellow
Write-Host "  - $(Split-Path $angelFile -Leaf)"
Write-Host "  - $(Split-Path $autoFile  -Leaf)"
Write-Host "  - $(Split-Path $memFile   -Leaf)"
Write-Host "  - $(Split-Path $gaFile    -Leaf)"
Write-Host "  - $(Split-Path $pkgList   -Leaf)"
Write-Host "  - $(Split-Path $pkgCsv    -Leaf)"
Write-Host ""
Write-Host "Opening folder..." -ForegroundColor DarkCyan
Invoke-Item $OutDir
