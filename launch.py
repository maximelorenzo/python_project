import os
import subprocess

if __name__ == "__main__":
    file_path = os.path.join("src", "project", "dashboard.py")  
    subprocess.run(["streamlit", "run", file_path])
