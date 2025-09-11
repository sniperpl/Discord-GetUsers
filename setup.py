from cx_Freeze import setup, Executable

setup(
    name="getUsers",
    version="1.7",
    description="",
    options={"build_exe": {
        "include_files": ["favicon.ico"]
    }},
    executables=[Executable("index.py", base="Win32GUI", icon="favicon.ico", target_name="GetUsers")]
)