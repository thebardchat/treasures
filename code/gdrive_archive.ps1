# ShaneBrain Google Drive Archive Manager
# PowerShell script for intelligent file archiving and space management

param(
    [Parameter(Position=0)]
    [string]$Action = "menu",
    
    [Parameter()]
    [string]$SourcePath = "$env:USERPROFILE",
    
    [Parameter()]
    [int]$MinSizeMB = 100,
    
    [Parameter()]
    [int]$DaysOld = 30
)

# Configuration
$Script:Config = @{
    ArchivePath = "$env:USERPROFILE\ShaneBrain_Archive"
    GDrivePath = "G:\"  # Change this to your Google Drive mount point
    LogPath = "$env:USERPROFILE\.shanebrain\archive_log.txt"
    ProtectedFolders = @(
        "ShaneBrain",
        "AngelCloud", 
        "PulsarAI",
        ".shanebrain",
        "start-shanebrain.bat"
    )
    ExcludedExtensions = @(
        ".bat", ".exe", ".dll", ".sys", ".ps1", ".cmd"
    )
}

# Ensure log directory exists
$logDir = Split-Path $Config.LogPath -Parent
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

function Write-Log {
    param($Message, $Level = "INFO")
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    
    # Write to console with color
    switch ($Level) {
        "ERROR" { Write-Host $logMessage -ForegroundColor Red }
        "WARNING" { Write-Host $logMessage -ForegroundColor Yellow }
        "SUCCESS" { Write-Host $logMessage -ForegroundColor Green }
        default { Write-Host $logMessage }
    }
    
    # Write to log file
    Add-Content -Path $Config.LogPath -Value $logMessage
}

function Get-SystemInfo {
    $disk = Get-PSDrive C
    $memory = Get-WmiObject Win32_OperatingSystem
    
    $info = @{
        DiskUsedGB = [math]::Round($disk.Used / 1GB, 2)
        DiskFreeGB = [math]::Round($disk.Free / 1GB, 2)
        DiskTotalGB = [math]::Round(($disk.Used + $disk.Free) / 1GB, 2)
        DiskPercentUsed = [math]::Round(($disk.Used / ($disk.Used + $disk.Free)) * 100, 2)
        MemoryUsedGB = [math]::Round(($memory.TotalVisibleMemorySize - $memory.FreePhysicalMemory) / 1MB, 2)
        MemoryTotalGB = [math]::Round($memory.TotalVisibleMemorySize / 1MB, 2)
        MemoryPercentUsed = [math]::Round((($memory.TotalVisibleMemorySize - $memory.FreePhysicalMemory) / $memory.TotalVisibleMemorySize) * 100, 2)
    }
    
    return $info
}

function Find-LargeFiles {
    param(
        [string]$Path = $env:USERPROFILE,
        [int]$MinSizeMB = 100
    )
    
    Write-Log "Searching for files larger than ${MinSizeMB}MB in $Path"
    
    $largeFiles = @()
    $minSize = $MinSizeMB * 1MB
    
    Get-ChildItem -Path $Path -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object { 
            $_.Length -gt $minSize -and
            $Config.ExcludedExtensions -notcontains $_.Extension -and
            $Config.ProtectedFolders -notcontains $_.Directory.Name
        } |
        ForEach-Object {
            $largeFiles += @{
                Path = $_.FullName
                SizeMB = [math]::Round($_.Length / 1MB, 2)
                Modified = $_.LastWriteTime
                Age = (Get-Date) - $_.LastWriteTime
            }
        }
    
    return $largeFiles | Sort-Object SizeMB -Descending
}

function Find-OldFiles {
    param(
        [string]$Path = $env:USERPROFILE,
        [int]$DaysOld = 30
    )
    
    Write-Log "Searching for files older than $DaysOld days in $Path"
    
    $cutoffDate = (Get-Date).AddDays(-$DaysOld)
    $oldFiles = @()
    
    Get-ChildItem -Path $Path -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object { 
            $_.LastAccessTime -lt $cutoffDate -and
            $Config.ExcludedExtensions -notcontains $_.Extension -and
            $Config.ProtectedFolders -notcontains $_.Directory.Name
        } |
        ForEach-Object {
            $oldFiles += @{
                Path = $_.FullName
                SizeMB = [math]::Round($_.Length / 1MB, 2)
                LastAccess = $_.LastAccessTime
                Age = (Get-Date) - $_.LastAccessTime
            }
        }
    
    return $oldFiles | Sort-Object LastAccess
}

function Archive-ToGoogleDrive {
    param(
        [array]$Files,
        [string]$ArchiveName = "Archive_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    )
    
    if (-not (Test-Path $Config.GDrivePath)) {
        Write-Log "Google Drive not found at $($Config.GDrivePath)" "ERROR"
        Write-Log "Please ensure Google Drive is mounted or update the path in the script" "WARNING"
        return $false
    }
    
    $archivePath = Join-Path $Config.GDrivePath "ShaneBrain_Archives\$ArchiveName"
    New-Item -ItemType Directory -Path $archivePath -Force | Out-Null
    
    Write-Log "Starting archive to: $archivePath" "INFO"
    
    $archived = 0
    $totalSize = 0
    
    foreach ($file in $Files) {
        try {
            $relativePath = $file.Path.Replace("$env:USERPROFILE\", "")
            $destPath = Join-Path $archivePath $relativePath
            $destDir = Split-Path $destPath -Parent
            
            if (-not (Test-Path $destDir)) {
                New-Item -ItemType Directory -Path $destDir -Force | Out-Null
            }
            
            Write-Host "Archiving: $($file.Path)" -ForegroundColor Cyan
            Move-Item -Path $file.Path -Destination $destPath -Force
            
            # Create a link file in the original location
            $linkContent = @"
This file has been archived to Google Drive
Archive Location: $destPath
Archive Date: $(Get-Date)
File Size: $($file.SizeMB) MB
To restore, copy the file back from Google Drive
"@
            Set-Content -Path "$($file.Path).archived.txt" -Value $linkContent
            
            $archived++
            $totalSize += $file.SizeMB
            
        } catch {
            Write-Log "Failed to archive: $($file.Path) - $_" "ERROR"
        }
    }
    
    Write-Log "Archived $archived files (Total: ${totalSize}MB)" "SUCCESS"
    return $true
}

function Restore-FromArchive {
    param(
        [string]$ArchivePath
    )
    
    if (-not (Test-Path $ArchivePath)) {
        Write-Log "Archive not found: $ArchivePath" "ERROR"
        return
    }
    
    Write-Log "Restoring from: $ArchivePath"
    
    $files = Get-ChildItem -Path $ArchivePath -Recurse -File
    $restored = 0
    
    foreach ($file in $files) {
        $relativePath = $file.FullName.Replace($ArchivePath, "").TrimStart("\")
        $destPath = Join-Path $env:USERPROFILE $relativePath
        $destDir = Split-Path $destPath -Parent
        
        if (-not (Test-Path $destDir)) {
            New-Item -ItemType Directory -Path $destDir -Force | Out-Null
        }
        
        try {
            Copy-Item -Path $file.FullName -Destination $destPath -Force
            $restored++
            Write-Host "Restored: $destPath" -ForegroundColor Green
        } catch {
            Write-Log "Failed to restore: $destPath - $_" "ERROR"
        }
    }
    
    Write-Log "Restored $restored files" "SUCCESS"
}

function Show-InteractiveMenu {
    $files = @()
    
    while ($true) {
        Clear-Host
        Write-Host "================================================================================" -ForegroundColor Cyan
        Write-Host "                     SHANEBRAIN GOOGLE DRIVE ARCHIVE MANAGER                   " -ForegroundColor Yellow
        Write-Host "================================================================================" -ForegroundColor Cyan
        
        # Show system info
        $sysInfo = Get-SystemInfo
        Write-Host ""
        Write-Host "System Status:" -ForegroundColor White
        Write-Host "  Disk: $($sysInfo.DiskFreeGB) GB free of $($sysInfo.DiskTotalGB) GB ($($sysInfo.DiskPercentUsed)% used)" -ForegroundColor Gray
        Write-Host "  Memory: $($sysInfo.MemoryUsedGB) GB of $($sysInfo.MemoryTotalGB) GB ($($sysInfo.MemoryPercentUsed)% used)" -ForegroundColor Gray
        Write-Host ""
        
        if ($files.Count -gt 0) {
            Write-Host "Files ready for archive: $($files.Count) files" -ForegroundColor Green
        }
        
        Write-Host "================================================================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "  [1] Find Large Files (>100MB)" -ForegroundColor White
        Write-Host "  [2] Find Old Files (>30 days)" -ForegroundColor White
        Write-Host "  [3] Custom Search" -ForegroundColor White
        Write-Host "  [4] Archive Selected Files to Google Drive" -ForegroundColor Yellow
        Write-Host "  [5] View Archive History" -ForegroundColor White
        Write-Host "  [6] Restore from Archive" -ForegroundColor White
        Write-Host "  [7] Configure Settings" -ForegroundColor White
        Write-Host "  [8] Quick Space Recovery" -ForegroundColor Red
        Write-Host "  [0] Exit" -ForegroundColor Gray
        Write-Host ""
        Write-Host "================================================================================" -ForegroundColor Cyan
        
        $choice = Read-Host "Enter your choice"
        
        switch ($choice) {
            "1" {
                $files = Find-LargeFiles
                Write-Host ""
                Write-Host "Found $($files.Count) large files:" -ForegroundColor Green
                $files | Select-Object -First 10 | ForEach-Object {
                    Write-Host "  $([math]::Round($_.SizeMB, 1)) MB - $($_.Path)" -ForegroundColor Gray
                }
                if ($files.Count -gt 10) {
                    Write-Host "  ... and $($files.Count - 10) more files" -ForegroundColor Gray
                }
                Read-Host "Press Enter to continue"
            }
            
            "2" {
                $files = Find-OldFiles
                Write-Host ""
                Write-Host "Found $($files.Count) old files:" -ForegroundColor Green
                $files | Select-Object -First 10 | ForEach-Object {
                    Write-Host "  $($_.Age.Days) days old - $($_.Path)" -ForegroundColor Gray
                }
                if ($files.Count -gt 10) {
                    Write-Host "  ... and $($files.Count - 10) more files" -ForegroundColor Gray
                }
                Read-Host "Press Enter to continue"
            }
            
            "3" {
                $searchPath = Read-Host "Enter path to search (default: $env:USERPROFILE)"
                if ([string]::IsNullOrEmpty($searchPath)) {
                    $searchPath = $env:USERPROFILE
                }
                
                $minSize = Read-Host "Minimum file size in MB (default: 50)"
                if ([string]::IsNullOrEmpty($minSize)) {
                    $minSize = 50
                }
                
                $files = Find-LargeFiles -Path $searchPath -MinSizeMB $minSize
                Write-Host "Found $($files.Count) files" -ForegroundColor Green
                Read-Host "Press Enter to continue"
            }
            
            "4" {
                if ($files.Count -eq 0) {
                    Write-Host "No files selected for archiving. Please search for files first." -ForegroundColor Yellow
                } else {
                    Write-Host ""
                    Write-Host "Ready to archive $($files.Count) files" -ForegroundColor Yellow
                    $totalSize = ($files | Measure-Object -Property SizeMB -Sum).Sum
                    Write-Host "Total size: $([math]::Round($totalSize, 2)) MB" -ForegroundColor Yellow
                    Write-Host ""
                    
                    $confirm = Read-Host "Proceed with archiving? (Y/N)"
                    if ($confirm -eq "Y") {
                        $archiveName = Read-Host "Enter archive name (or press Enter for default)"
                        if ([string]::IsNullOrEmpty($archiveName)) {
                            $archiveName = "Archive_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
                        }
                        
                        Archive-ToGoogleDrive -Files $files -ArchiveName $archiveName
                        $files = @()  # Clear the list after archiving
                    }
                }
                Read-Host "Press Enter to continue"
            }
            
            "5" {
                Write-Host ""
                Write-Host "Archive History:" -ForegroundColor Yellow
                if (Test-Path $Config.LogPath) {
                    Get-Content $Config.LogPath -Tail 20 | ForEach-Object {
                        if ($_ -match "SUCCESS") {
                            Write-Host $_ -ForegroundColor Green
                        } elseif ($_ -match "ERROR") {
                            Write-Host $_ -ForegroundColor Red
                        } else {
                            Write-Host $_
                        }
                    }
                } else {
                    Write-Host "No archive history found" -ForegroundColor Gray
                }
                Read-Host "Press Enter to continue"
            }
            
            "6" {
                $gdriveArchives = Join-Path $Config.GDrivePath "ShaneBrain_Archives"
                if (Test-Path $gdriveArchives) {
                    $archives = Get-ChildItem -Path $gdriveArchives -Directory
                    
                    Write-Host ""
                    Write-Host "Available Archives:" -ForegroundColor Yellow
                    for ($i = 0; $i -lt $archives.Count; $i++) {
                        Write-Host "  [$i] $($archives[$i].Name)" -ForegroundColor Gray
                    }
                    
                    $selection = Read-Host "Select archive number to restore"
                    if ($selection -match '^\d+$' -and [int]$selection -lt $archives.Count) {
                        Restore-FromArchive -ArchivePath $archives[[int]$selection].FullName
                    }
                } else {
                    Write-Host "No archives found" -ForegroundColor Yellow
                }
                Read-Host "Press Enter to continue"
            }
            
            "7" {
                Write-Host ""
                Write-Host "Current Configuration:" -ForegroundColor Yellow
                Write-Host "  Google Drive Path: $($Config.GDrivePath)" -ForegroundColor Gray
                Write-Host "  Archive Path: $($Config.ArchivePath)" -ForegroundColor Gray
                Write-Host "  Protected Folders: $($Config.ProtectedFolders -join ', ')" -ForegroundColor Gray
                Write-Host ""
                
                $newPath = Read-Host "Enter new Google Drive path (or press Enter to skip)"
                if (-not [string]::IsNullOrEmpty($newPath)) {
                    $Config.GDrivePath = $newPath
                    Write-Host "Google Drive path updated" -ForegroundColor Green
                }
                
                Read-Host "Press Enter to continue"
            }
            
            "8" {
                Write-Host ""
                Write-Host "QUICK SPACE RECOVERY" -ForegroundColor Red
                Write-Host "This will automatically archive large, old files" -ForegroundColor Yellow
                
                $confirm = Read-Host "Continue? (Y/N)"
                if ($confirm -eq "Y") {
                    Write-Host "Finding candidates for archiving..." -ForegroundColor Yellow
                    
                    $largeOldFiles = Find-LargeFiles -MinSizeMB 50 |
                        Where-Object { $_.Age.TotalDays -gt 14 } |
                        Select-Object -First 50
                    
                    if ($largeOldFiles.Count -gt 0) {
                        $totalSize = ($largeOldFiles | Measure-Object -Property SizeMB -Sum).Sum
                        Write-Host "Found $($largeOldFiles.Count) files totaling $([math]::Round($totalSize, 2)) MB" -ForegroundColor Green
                        
                        Archive-ToGoogleDrive -Files $largeOldFiles -ArchiveName "QuickRecovery_$(Get-Date -Format 'yyyyMMdd')"
                        
                        Write-Host ""
                        Write-Host "Space recovered: $([math]::Round($totalSize, 2)) MB" -ForegroundColor Green
                    } else {
                        Write-Host "No suitable files found for quick recovery" -ForegroundColor Yellow
                    }
                }
                Read-Host "Press Enter to continue"
            }
            
            "0" {
                Write-Host ""
                Write-Host "Thank you for using ShaneBrain Archive Manager!" -ForegroundColor Green
                Write-Host "Building the future, one byte at a time." -ForegroundColor Cyan
                return
            }
            
            default {
                Write-Host "Invalid choice. Please try again." -ForegroundColor Red
                Start-Sleep -Seconds 2
            }
        }
    }
}

# Main execution
if ($Action -eq "menu") {
    Show-InteractiveMenu
} elseif ($Action -eq "find-large") {
    $files = Find-LargeFiles -Path $SourcePath -MinSizeMB $MinSizeMB
    $files | Format-Table -AutoSize
} elseif ($Action -eq "find-old") {
    $files = Find-OldFiles -Path $SourcePath -DaysOld $DaysOld
    $files | Format-Table -AutoSize
} elseif ($Action -eq "quick-archive") {
    Write-Log "Starting quick archive process"
    $files = Find-LargeFiles -Path $SourcePath -MinSizeMB $MinSizeMB
    if ($files.Count -gt 0) {
        Archive-ToGoogleDrive -Files $files
    } else {
        Write-Log "No files found matching criteria" "WARNING"
    }
}
