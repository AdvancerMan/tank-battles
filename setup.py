
from cx_Freeze import setup, Executable

exe = Executable(
    script="main.py",
    base="Win32GUI"
)

setup(
    name="Tank's Batalii",
    version="0.1",
    description="Tankoviye Batalii",
    executables=[exe]
)
