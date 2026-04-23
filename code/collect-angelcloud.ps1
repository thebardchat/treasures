[CmdletBinding()]
param(
  [string]$DestProject = "$env:USERPROFILE\Desktop\angel-cloud-main",
  [string]$ScanDir     = "",   # leave blank to auto-pick newest angel-cloud-scan-* on Desktop
  [switch]$DryRun
)

function Get-LatestScanDir {
  $root = "$env:USERPROFILE\Desktop"
  if (-not (Test-Path $root)) { return $null }
  Get-ChildItem -Path $root -Directory -Filter 'angel-cloud-scan-*' |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
}

# Resolve scan dir
if (-not $ScanDir -or -not (Test-Path $ScanDir)) {
  $latest = Get-LatestScanDir
  if (-not $latest) { throw "Could not find an 'angel-cloud-scan-*' folder on Desktop. Run scan-angelcloud.ps1 first." }
  $ScanDir = $latest.FullName
}

# Inputs from scan
$autoList = Join-Path $ScanDir 'automation-dirs.txt'
$pkgList  = Join-Path $ScanDir 'package-json-files.txt'
$miscList = Join-Path $ScanDir 'angel-cloud-paths.txt'

if (-not (Test-Path $DestProject)) { throw "Destination project not found: $DestProject" }

# Prepare ingest folder
$stamp   = Get-Date -Format 'yyyyMMdd_HHmm'
$ingest  = Join-Path $DestProject ("archive\ingest-{0}" -f $stamp)
$ingAuto = Join-Path $ingest 'automation'
$ingProj = Join-Path $ingest 'projects'
$ingMisc = Join-Path $ingest 'misc'

foreach ($d in @($ingest,$ingAuto,$ingProj,$ingMisc)) {
  if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d | Out-Null }
}

Write-Host "Scan dir: $ScanDir" -ForegroundColor Cyan
Write-Host "Ingest to: $ingest" -ForegroundColor Cyan
if ($DryRun) { Write-Host "(Dry run - nothing will be copied)" -ForegroundColor DarkYellow }

# Helper: copy a tree with robocopy, skipping heavy folders
function Copy-Tree {
  param([string]$Source,[string]$Dest)
  if (-not (Test-Path $Source)) { return }
  if (-not (Test-Path $Dest))   { New-Item -ItemType Directory -Path $Dest | Out-Null }

  $args = @(
    $Source, $Dest,
    '/E','/NFL','/NDL','/NJH','/NJS','/NP',
    '/XD','node_modules','.git','dist','build','.next','.turbo','.cache','coverage','bin','obj',
    '/XF','package-lock.json','yarn.lock','pnpm-lock.yaml','.DS_Store','Thumbs.db'
  )

  if ($DryRun) {
    Write-Host ("robocopy {0}" -f ($args -join ' ')) -ForegroundColor DarkGray
  } else {
    & robocopy @args | Out-Null
  }
}

$manifest = [System.Collections.Generic.List[object]]::new()

# 1) Automation directories
if (Test-Path $autoList) {
  $srcs = Get-Content -Path $autoList | Where-Object { $_ -and (Test-Path $_) }
  foreach ($src in $srcs) {
    try {
      $name = Split-Path $src -Leaf
      $dest = Join-Path $ingAuto $name
      Write-Host "Automation -> $dest" -ForegroundColor Green
      Copy-Tree -Source $src -Dest $dest
      $manifest.Add([pscustomobject]@{ kind='automation'; source=$src; dest=$dest })
    } catch { }
  }
}

# 2) Node projects (by package.json)
if (Test-Path $pkgList) {
  $pkgFiles = Get-Content -Path $pkgList | Where-Object { $_ -and (Test-Path $_) }
  $roots = $pkgFiles | ForEach-Object { Split-Path $_ -Parent } | Sort-Object -Unique
  foreach ($root in $roots) {
    try {
      $name = Split-Path $root -Leaf
      $dest = Join-Path $ingProj $name
      Write-Host "Project -> $dest" -ForegroundColor Green
      Copy-Tree -Source $root -Dest $dest
      $manifest.Add([pscustomobject]@{ kind='project'; source=$root; dest=$dest })
    } catch { }
  }
}

# 3) Misc angel-cloud files (single files)
if (Test-Path $miscList) {
  $files = Get-Content -Path $miscList | Where-Object { $_ -and (Test-Path $_) }
  foreach ($f in $files) {
    try {
      if ((Get-Item $f).PSIsContainer) { continue }
      $dest = Join-Path $ingMisc (Split-Path $f -Leaf)
      Write-Host "File -> $dest" -ForegroundColor Green
      if (-not $DryRun) { Copy-Item -LiteralPath $f -Destination $dest -Force }
      $manifest.Add([pscustomobject]@{ kind='file'; source=$f; dest=$dest })
    } catch { }
  }
}

# Write manifest + summary
$manJson = Join-Path $ingest 'MANIFEST.json'
$sumTxt  = Join-Path $ingest 'SUMMARY.txt'
$manifest | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 -Path $manJson

$lines = @(
  "Ingest folder: $ingest",
  "Date: $(Get-Date)",
  "",
  "Counts:",
  ("  Automation dirs: {0}" -f (($manifest | Where-Object { $_.kind -eq 'automation' }).Count)),
  ("  Projects       : {0}" -f (($manifest | Where-Object { $_.kind -eq 'project'   }).Count)),
  ("  Misc files     : {0}" -f (($manifest | Where-Object { $_.kind -eq 'file'      }).Count)),
  "",
  "Next:",
  "  - Review 'projects' and decide what belongs in backend/frontend.",
  "  - Merge useful bits into $DestProject (keep ingest as archive).",
  "  - Run 'npm i' inside any project you adopt (node_modules were skipped)."
)
$lines | Set-Content -Encoding UTF8 -Path $sumTxt

Write-Host ""
Write-Host "Done. Ingest summary:" -ForegroundColor Cyan
Get-Content $sumTxt | ForEach-Object { Write-Host $_ }
Write-Host ""

if (-not $DryRun) { try { Invoke-Item $ingest } catch { } }
