import os

print("🚀 Starting Data1300 Pipeline...")

# Run the deduplication script
print("Step 1: Cleaning and Ranking data...")
os.system("python3 export_ranked.py")

# Run the plotting script
print("Step 2: Generating Chart...")
os.system("python3 plot_grades.py")

print("\n✅ Pipeline Complete!")
print("Check your 'data/' folder for students_ranked.csv and grade_chart.png.")
