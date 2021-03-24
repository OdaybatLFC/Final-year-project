from cx_Freeze import setup, Executable

setup(name = "GAME" ,
      version = "1.1.0" ,
      options = {"build_exe": {"packages":["pygame"],
                               "include_files":["img/","screen.png"]}} ,
      executables = [Executable("Game.py", base = "Win32GUI", icon = "gameicon2.ico")]
)
