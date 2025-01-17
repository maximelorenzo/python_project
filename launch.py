import os
import subprocess

def main():
    dashboard_path = os.path.join(os.path.dirname(__file__), "src/project/dashboard.py")
    subprocess.run(["streamlit", "run", dashboard_path])
