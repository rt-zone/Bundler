# make_fs.py
import littlefs
import os, sys

BLOCK_SIZE  = 4096
BLOCK_COUNT = 212

EXCLUDE_DIRS  = {'.git', '.github', '__pycache__', '.venv', '.vscode'}
EXCLUDE_FILES = {'.gitignore', 'README.md', 'readme.md', 'LICENSE','.micropico'}
EXCLUDE_EXTS  = {'.pyc'}

fs = littlefs.LittleFS(block_size=BLOCK_SIZE, block_count=BLOCK_COUNT)

libs_dir = sys.argv[1]   # pass your libs/ folder

for root, dirs, files in os.walk(libs_dir):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]  # prune excluded dirs
    for name in files:
        if name in EXCLUDE_FILES or os.path.splitext(name)[1] in EXCLUDE_EXTS:
            continue
        local_path  = os.path.join(root, name)
        remote_path = "/" + os.path.relpath(local_path, libs_dir).replace("\\", "/")
        
        # create parent dirs on fs
        remote_dir = os.path.dirname(remote_path)
        parts = [p for p in remote_dir.split("/") if p]
        for i in range(len(parts)):
            d = "/" + "/".join(parts[:i+1])
            try:
                fs.mkdir(d)
            except FileExistsError:
                pass
        
        with open(local_path, "rb") as f:
            with fs.open(remote_path, "wb") as lf:
                lf.write(f.read())
        print(f"  + {remote_path}")

with open("filesystem.bin", "wb") as f:
    f.write(bytes(fs.context.buffer))

print(f"filesystem.bin written ({len(fs.context.buffer)} bytes)")