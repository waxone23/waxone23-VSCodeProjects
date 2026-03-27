#!/bin/bash
PROJECT_PATH="$HOME/waxone23-VSCodeProjects"
cd "$PROJECT_PATH"

echo "🧹 Cleaning up Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

echo "📝 Removing temporary PyMovie logs/temp files..."
rm -f play-Temp.py
# Add any other temporary file patterns here if they appear

echo "✅ Cleanup complete! Your project folder is tidy."
