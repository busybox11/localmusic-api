import platform

if platform.system() == "Linux":
    import subprocess

    subprocess.call("python3 linux_server.py", shell=True)
else:
    exit("Unsupported OS. Currently supported platforms: Linux")
