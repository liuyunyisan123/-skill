param(
    [string]$SkillsDirectory = ''
)

$ErrorActionPreference = 'Stop'
$sourceDirectory = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot 'skills')).TrimEnd('\', '/')
$skillNames = @('research-writing', 'research-figures', 'academic-ppt')

if ([string]::IsNullOrWhiteSpace($SkillsDirectory)) {
    $codexDirectory = $env:CODEX_HOME
    if ([string]::IsNullOrWhiteSpace($codexDirectory)) {
        $codexDirectory = Join-Path ([Environment]::GetFolderPath('UserProfile')) '.codex'
    }
    $SkillsDirectory = Join-Path $codexDirectory 'skills'
}
$SkillsDirectory = [IO.Path]::GetFullPath($SkillsDirectory).TrimEnd('\', '/')
$comparison = [StringComparison]::OrdinalIgnoreCase
if ($SkillsDirectory.Equals($sourceDirectory, $comparison) -or
    $SkillsDirectory.StartsWith($sourceDirectory + [IO.Path]::DirectorySeparatorChar, $comparison) -or
    $sourceDirectory.StartsWith($SkillsDirectory + [IO.Path]::DirectorySeparatorChar, $comparison)) {
    throw '安装目录不能与源目录相同，也不能互相包含。'
}

foreach ($skillName in $skillNames) {
    if (-not (Test-Path -LiteralPath (Join-Path $sourceDirectory "$skillName/SKILL.md") -PathType Leaf)) {
        throw "更新包不完整，缺少技能入口：$skillName"
    }
}

$backupDirectory = Join-Path (Split-Path -Parent $SkillsDirectory) ('skill-backups/research-skills-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [guid]::NewGuid().ToString('N').Substring(0, 6))
New-Item -ItemType Directory -Path $SkillsDirectory -Force | Out-Null
New-Item -ItemType Directory -Path $backupDirectory -Force | Out-Null

# 写入前先备份三个同名技能，不修改其他技能。
foreach ($skillName in $skillNames) {
    $existingDirectory = Join-Path $SkillsDirectory $skillName
    if (Test-Path -LiteralPath $existingDirectory) {
        Copy-Item -LiteralPath $existingDirectory -Destination $backupDirectory -Recurse
    }
}

foreach ($skillName in $skillNames) {
    $sourceSkill = Join-Path $sourceDirectory $skillName
    $destinationSkill = Join-Path $SkillsDirectory $skillName
    foreach ($sourceFile in Get-ChildItem -LiteralPath $sourceSkill -Recurse -File) {
        $relativePath = $sourceFile.FullName.Substring($sourceSkill.Length).TrimStart('\', '/')
        $destinationFile = Join-Path $destinationSkill $relativePath
        New-Item -ItemType Directory -Path (Split-Path -Parent $destinationFile) -Force | Out-Null
        Copy-Item -LiteralPath $sourceFile.FullName -Destination $destinationFile -Force
        if ((Get-FileHash -LiteralPath $sourceFile.FullName -Algorithm SHA256).Hash -ne (Get-FileHash -LiteralPath $destinationFile -Algorithm SHA256).Hash) {
            throw "复制后校验失败：$skillName/$relativePath。原版本保存在 $backupDirectory"
        }
    }
}

Write-Output '已更新科研写作、科研附图、科研汇报PPT三个技能，并逐文件核对成功。'
Write-Output "技能目录：$SkillsDirectory"
Write-Output "原版本备份：$backupDirectory"
