import os
import subprocess

def main():
    dashboard_path = os.path.join(os.path.dirname(__file__), "dashboard.py")
    subprocess.run(["streamlit", "run", dashboard_path])
