from cx_Freeze import setup, Executable

setup(
    name="getUsers",
    version="1.3c",
    description="",
    executables=[Executable("getUsers.py", base="Win32GUI", icon="GetUsers.ico")]
)