@echo off
setlocal enabledelayedexpansion

set "python_command=python -m gprMax"
set "additional_arguments=--geometry-only"

for %%f in (*.in) do (
    echo Running gprMax on %%f
    %python_command% "%%f" %additional_arguments%
)

endlocal