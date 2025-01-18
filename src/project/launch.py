import os
import subprocess

def main():
    # Obtenez le chemin vers le dashboard.py
    dashboard_path = os.path.join(os.path.dirname(__file__), "dashboard.py")
    # Lancer Streamlit pour exécuter le dashboard
    subprocess.run(["streamlit", "run", dashboard_path])
