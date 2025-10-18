@echo off
echo Adding files to git...
git add .
echo.
echo Committing changes...
git commit -m "Add HR Platform recommendation system

- Created database models for users, companies, vacancies, resumes
- Implemented recommendation engine with skill matching algorithm
- Added FastAPI backend with REST endpoints
- Created web interface for recommendations
- Added test data seeding scripts
- Fixed SQLite compatibility issues"
echo.
echo Pushing to sc3.v1 branch...
git push origin sc3.v1
echo.
echo Done!
pause
