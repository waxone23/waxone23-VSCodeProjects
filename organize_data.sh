#!/bin/bash
PROJECT_PATH="$HOME/waxone23-VSCodeProjects/data/raw_videos"

echo "🔭 Looking for astronomical video files (.adv, .avi, .ser, .fits) in Downloads..."
mv ~/Downloads/*.{adv,avi,ser,fits} "$PROJECT_PATH" 2>/dev/null

echo "📂 Current files in your raw_videos folder:"
ls -lh "$PROJECT_PATH"
