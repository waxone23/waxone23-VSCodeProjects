#!/bin/bash
PROJECT_PATH="$HOME/waxone23-VSCodeProjects"
cd "$PROJECT_PATH"

# Activate the virtual environment
source venv/bin/activate

# Launch PyMovie
python venv/lib/python3.11/site-packages/pymovie/main.py
