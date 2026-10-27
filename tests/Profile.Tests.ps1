#Requires -Modules @{ ModuleName = 'Pester'; ModuleVersion = '5.0.0' }

BeforeAll {
    $script:RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
    $script:ProfilePath = Join-Path $script:RepoRoot 'Profile.ps1'
    $script:ReadmePath = Join-Path $script:RepoRoot 'README.md'
    $script:ProfileSource = Get-Content -Raw $script:ProfilePath
    $script:Readme = Get-Content -Raw $script:ReadmePath
}

Describe 'Profile.ps1 syntax' {

    It 'parses without syntax errors' {
        $tokens = $null
        $errors = $null
        $null = [System.Management.Automation.Language.Parser]::ParseFile(
            $script:ProfilePath, [ref]$tokens, [ref]$errors)

        if ($errors.Count -gt 0) {
            $detail = ($errors | ForEach-Object { "$($_.Extent.StartLineNumber): $($_.Message)" }) -join "`n"
            throw "Profile.ps1 has $($errors.Count) parse error(s):`n$detail"
        }
    }

    It 'is valid UTF-8 text' {
        $bytes = [System.IO.File]::ReadAllBytes($script:ProfilePath)
        $null = [System.Text.UTF8Encoding]::new($false, $true).GetString($bytes)
    }
}

Describe 'Profile.ps1 structure' {

    It 'defines a substantial number of functions' {
        $count = ([regex]::Matches(
            $script:ProfileSource, '(?im)^\s*function\s+[A-Za-z0-9_-]+')).Count

        $count | Should -BeGreaterThan 50 -Because 'the profile is a large toolkit'
    }

    It 'never uses Write-Host for errors' {
        $hits = [regex]::Matches(
            $script:ProfileSource, '(?im)^\s*Write-Host\s+.*-ForegroundColor\s+Red.*\$_')

        $hits.Count | Should -Be 0 -Because 'errors should go through Write-Error or throw'
    }

    It 'has no empty catch blocks that swallow failures silently' {
        $hits = [regex]::Matches($script:ProfileSource, '(?i)catch\s*\{\s*\}')

        $hits.Count | Should -Be 0 -Because 'an empty catch hides real failures'
    }

    It 'does not hardcode the author machine user profile path' {
        $hits = [regex]::Matches(
            $script:ProfileSource, '(?i)C:\\Users\\[^\\\s"]+')

        $hits.Count | Should -Be 0 -Because 'hardcoded user paths break on other machines'
    }
}

Describe 'README accuracy' {

    BeforeAll {
        $script:DefinedCommands = [regex]::Matches(
            $script:ProfileSource, '(?im)^\s*function\s+([A-Za-z0-9_-]+)') |
            ForEach-Object { $_.Groups[1].Value.ToLower() }

        $script:DefinedCommands += [regex]::Matches(
            $script:ProfileSource, '(?i)Set-Alias\s+-Name\s+([A-Za-z0-9_-]+)') |
            ForEach-Object { $_.Groups[1].Value.ToLower() }
    }

    It 'only advertises a function count the profile can back' {
        $match = [regex]::Match($script:Readme, '(\d+)\+?\s*Custom Functions')
        $match | Should -Not -BeNullOrEmpty

        $claimed = [int]$match.Groups[1].Value
        $actual = ($script:DefinedCommands | Sort-Object -Unique).Count

        $claimed | Should -BeLessOrEqual $actual -Because (
            "README claims $claimed+ functions but only $actual are defined")
    }

    It 'documents only commands that actually exist in Profile.ps1' {
        $section = [regex]::Match(
            $script:Readme, '(?s)## .*Functions & Aliases(.*?)\n## ')

        $section | Should -Not -BeNullOrEmpty -Because 'the Functions & Aliases section must exist'

        $documented = [regex]::Matches($section.Groups[1].Value, '(?m)^\| `([^`]+)` \|') |
            ForEach-Object { $_.Groups[1].Value }

        $documented.Count | Should -BeGreaterThan 0

        $missing = $documented | Where-Object {
            $script:DefinedCommands -notcontains $_.ToLower()
        }

        $missing | Should -BeNullOrEmpty -Because (
            "README documents commands that Profile.ps1 does not define: $($missing -join ', ')")
    }

    It 'references only Python files that exist' {
        $section = [regex]::Match(
            $script:Readme, '(?s)### .*Available Python Tools(.*?)\n### ')

        $section | Should -Not -BeNullOrEmpty

        $documented = [regex]::Matches($section.Groups[1].Value, '\*\*`([^`]+\.py)`\*\*') |
            ForEach-Object { $_.Groups[1].Value }

        $documented | Should -Not -BeNullOrEmpty

        foreach ($file in $documented) {
            $file | Should -Not -Match '\s' -Because "'$file' contains spaces and cannot be imported"
            Join-Path $script:RepoRoot "python/$file" | Should -Exist
        }
    }
}

Describe 'Repository hygiene' {

    It 'declares the MIT license it advertises' {
        Join-Path $script:RepoRoot 'LICENSE' | Should -Exist
        (Get-Content -Raw (Join-Path $script:RepoRoot 'LICENSE')) | Should -Match 'MIT License'
    }

    It 'normalizes line endings via .gitattributes' {
        Join-Path $script:RepoRoot '.gitattributes' | Should -Exist
        (Get-Content -Raw (Join-Path $script:RepoRoot '.gitattributes')) | Should -Match 'eol=lf'
    }

    It 'keeps Python filenames free of spaces' {
        $spaced = Get-ChildItem (Join-Path $script:RepoRoot 'python') -Filter '*.py' |
            Where-Object { $_.Name -match '\s' }

        $spaced | Should -BeNullOrEmpty -Because 'spaces in module names break imports'
    }
}