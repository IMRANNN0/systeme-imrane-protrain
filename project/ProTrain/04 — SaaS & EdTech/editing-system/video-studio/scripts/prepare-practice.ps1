$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech

$runtimeRoot = Split-Path -Parent $PSScriptRoot
$mediaRoot = Join-Path $runtimeRoot 'public/practice'
New-Item -ItemType Directory -Path $mediaRoot -Force | Out-Null

$sentences = @(
    'My average is only one part of my profile.',
    'Before choosing, I compare the published requirements.',
    'Then I check what each option really asks for.'
)

for ($index = 0; $index -lt $sentences.Count; $index++) {
    $speech = [System.Speech.Synthesis.SpeechSynthesizer]::new()
    try {
        $speech.SelectVoice('Microsoft Zira Desktop')
        $speech.Rate = -1
        $speech.SetOutputToWaveFile((Join-Path $mediaRoot ('take-' + ($index + 1) + '.wav')))
        $speech.Speak($sentences[$index])
    }
    finally {
        $speech.Dispose()
    }
}

python (Join-Path $PSScriptRoot 'prepare-practice.py')
if ($LASTEXITCODE -ne 0) {
    throw 'Practice asset preparation failed'
}
