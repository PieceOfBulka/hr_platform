@echo off
echo Fetching SQL files from data_base_script branch...
git fetch origin
git checkout data_base_script
git checkout sc3.v1
git checkout data_base_script -- *.sql
echo.
echo SQL files copied to current branch
pause
