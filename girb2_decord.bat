@echo off
setlocal ENABLEDELAYEDEXPANSION

set "folder=%~1"
if not defined folder set /p "folder=Enter the folder path: "

echo %folder%

if not exist "%folder%" (
  echo Folder does not exist!
  pause
  exit /b 1
)



for %%a in ("%folder%\Z__C_RJTD_2021*_FH16-33_grib2.*") do (
  set "filename=%%~na"
  set "extension=%%~xa"

  echo Processing: %%a
  wgrib2 %%a -netcdf "D:\github\transformer\transformer_MEPS\input_netcfd\%%~na.nc
)

for %%a in ("%folder%\Z__C_RJTD_2022*_FH16-33_grib2.*") do (
  set "filename=%%~na"
  set "extension=%%~xa"

  echo Processing: %%a
  wgrib2 %%a -netcdf "D:\github\transformer\transformer_MEPS\input_netcfd\%%~na.nc
)



echo All files processed.
pause
exit /b 0
