from cx_Freeze import setup, Executable
import sys

# Add this if you're using PyQt5
build_exe_options = {
    'packages': ['PyQt5', 'pandas', 'asammdf'],
    'excludes': [],
    'include_files': [],
    'include_msvcr': True
}

# The base parameter is used for GUI applications
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # For Windows GUI applications

setup(
    name="MDF Manager",
    version="0.1",
    description="This application manages MDF files and displays them",
    options={"build_exe": build_exe_options},
    executables=[Executable("Front\main.py", base=base)]  # Use raw string for paths
)
