#!/bin/bash
# Paths
SOURCE="$HOME/waxone23-VSCodeProjects/data/output_analysis"
DEST="$HOME/Library/Mobile Documents/com~apple~CloudDocs/PyMovie_Backups"

# Create destination folder in iCloud if it doesn't exist
mkdir -p "$DEST"

echo "☁️  Syncing your lightcurves to iCloud..."
# cp -R copies the folder; -u (if available) or rsync is better for syncing
rsync -av --progress "$SOURCE/" "$DEST/"

echo "✅ Backup complete! Your files are now being uploaded to the cloud."
