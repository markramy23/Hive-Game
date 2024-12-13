@echo off
REM Batch file to visualize profiling data using SnakeViz

REM Change the profiling data file name below if needed
set PROFILE_OUTPUT=profile_data.prof

if exist %PROFILE_OUTPUT% (
    echo Launching SnakeViz to visualize %PROFILE_OUTPUT%...
    snakeviz %PROFILE_OUTPUT%
) else (
    echo Profiling data file %PROFILE_OUTPUT% not found. Ensure the file exists.
)

pause
