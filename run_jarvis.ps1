Set-Location -Path (Split-Path -Path $MyInvocation.MyCommand.Definition -Parent)
python -m jarvis.main @args
