from cx_Freeze import setup, Executable

setup(
    name="getUsers",
    version="1.5",
    description="",
    executables=[Executable("index.py", base="Win32GUI", icon="GetUsers.ico")]
)