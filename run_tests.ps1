Set-Location -Path (Split-Path -Path $MyInvocation.MyCommand.Definition -Parent)
python -m pip install -r requirements.txt
pytest -q
