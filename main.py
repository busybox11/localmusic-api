import platform

if platform.system() == "Linux":
    import linux_server
else:
    exit("Unsupported OS. Currently supported platforms: Linux")