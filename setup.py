from cx_Freeze import setup, Executable
import sys

# Define build options
build_exe_options = {
    'packages': ['PyQt5', 'pandas', 'asammdf','flask'],  # List all your dependencies here
    'excludes': [],
    'include_files': [],  # Add any additional files needed by the application
    'include_msvcr': True
}

# Set base to None for console applications
base = None

setup(
    name="MDF Manager",
    version="0.1",
    description="This application manages MDF files and displays them",
    options={"build_exe": build_exe_options},
    executables=[Executable("activity.py", base=base)]
)
