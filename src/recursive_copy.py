import os
import shutil

def recursive_copy(source_dir: str, dest_dir: str):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    print("Purged dest dir")
    
    os.makedirs(dest_dir)
    print("Created dest dir")
    
    for filename in os.listdir(source_dir):
        source = os.path.join(source_dir, filename)
        dest = os.path.join(dest_dir, filename)
        
        if os.path.isfile(source):
            shutil.copy2(source, dest)
            print(f"Copied from {source} to {dest}")
        elif os.path.isdir(source):
            recursive_copy(source, dest)
    
    print(f"Finished copied from {source_dir} to {dest_dir}")
    