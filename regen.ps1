# Regenerate Qt UI + resource Python files from their sources
# Run after editing assets/index.ui or assets/resources.qrc

pyside6-uic --from-imports assets/index.ui -o saj/generated/index_ui.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "pyside6-uic failed" -ForegroundColor Red
    exit 1
}

pyside6-rcc assets/resources.qrc -o saj/generated/resources_rc.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "pyside6-rcc failed" -ForegroundColor Red
    exit 1
}

Write-Host "Regenerated UI + resources" -ForegroundColor Green