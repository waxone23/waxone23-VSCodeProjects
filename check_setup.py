import sys
import os
import platform

def verify_environment():
    print("--- Python Environment Check ---")
    
    # Check Python Version
    print(f"Python Version: {sys.version}")
    
    # Check if Virtual Environment is active
    # sys.prefix changes when a venv is active
    is_venv = sys.prefix != sys.base_prefix
    print(f"Virtual Environment Active: {is_venv}")
    
    # Check Working Directory (The folder you are in)
    print(f"Current Folder Path: {os.getcwd()}")
    
    # Check OS Info
    print(f"Operating System: {platform.system()} {platform.release()}")
    print("--------------------------------")

if __name__ == "__main__":
    verify_environment()
    
    print("Success! Python is running.")
    