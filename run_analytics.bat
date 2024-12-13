@echo off
REM Batch file to profile a Python script using cProfile

REM Change the script name and output file name below
set SCRIPT_NAME=Hive_Game.py
set PROFILE_OUTPUT=profile_data.prof

echo Running Python profiler on %SCRIPT_NAME%...
python -m cProfile -o %PROFILE_OUTPUT% %SCRIPT_NAME%

echo Profiling complete. Results saved to %PROFILE_OUTPUT%.
pause
