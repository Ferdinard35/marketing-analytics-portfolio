<#
Loads the Week 1 CSVs into your local PostgreSQL server.

Creates the database "analytics_apprenticeship" if it is missing, then rebuilds
the schema "week01" inside it. Safe to re-run.

Run it from a terminal in any folder:

    powershell -ExecutionPolicy Bypass -File load_postgres.ps1

psql asks for the password of the PostgreSQL user (default: postgres).
Optional parameters:  -User postgres  -PgHost localhost  -Port 5432
#>
param(
    [string]$User = "postgres",
    [string]$PgHost = "localhost",
    [int]$Port = 5432
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path

# psql is often not on PATH on Windows, so look in the default install folder too.
$psql = $null
$cmd = Get-Command psql -ErrorAction SilentlyContinue
if ($cmd) {
    $psql = $cmd.Source
} else {
    $found = @(Get-ChildItem "C:\Program Files\PostgreSQL\*\bin\psql.exe" -ErrorAction SilentlyContinue | Sort-Object FullName)
    if ($found.Count -gt 0) { $psql = $found[0].FullName }
}
if (-not $psql) {
    Write-Host "psql.exe was not found. Install PostgreSQL, or add its bin folder to PATH, then run this again."
    exit 1
}

Write-Host "Using $psql"
Write-Host "Connecting to ${PgHost}:${Port} as $User"

Push-Location $here
try {
    & $psql -U $User -h $PgHost -p $Port -d postgres -v ON_ERROR_STOP=1 -f load_postgres.sql
    $code = $LASTEXITCODE
} finally {
    Pop-Location
}

if ($code -ne 0) {
    Write-Host ""
    Write-Host "Load FAILED (psql exit code $code). The week01 schema was left as it was before this run."
    exit $code
}

Write-Host ""
Write-Host "Loaded. Database: analytics_apprenticeship   Schema: week01"
Write-Host "Tables: campaigns, campaign_spend, users, transactions"
