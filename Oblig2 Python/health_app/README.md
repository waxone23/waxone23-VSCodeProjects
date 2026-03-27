# Health Tracker CLI - Oblig 2
**Author:** Brede Korsmo  
**Course:** ITPE1400 / DAPE1400 - Applied IT  
**Institution:** OsloMet  

## Project Overview
This application is a professional-grade command-line tool designed to track health metrics. It allows users to manage health records, calculate Body Mass Index (BMI), determine ideal body weight, and receive personalized health advice based on World Health Organization (WHO) categories.

The project demonstrates key software engineering principles:
- **Object-Oriented Programming (OOP):** Encapsulated logic within the `Health` class.
- **Data Persistence:** Immediate serialization of data to JSON format.
- **Defensive Programming:** Robust input validation and exception handling.
- **Automated Testing:** 100% test coverage using `pytest`.



---

## Technical Stack
- **Language:** Python 3.12+ (Tested on 3.14 Alpha)
- **Dependency Management:** `uv`
- **Build System:** `hatchling`
- **Testing Framework:** `pytest`
- **Data Format:** JSON

---

## Installation & Setup

### 1. Prerequisites
Ensure you have the `uv` package manager installed. If not, install it via:
```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
2. Environment Setup
Navigate to the project root and create the virtual environment:

Bash
uv venv
source .venv/bin/activate
3. Install Package
Install the project in editable mode with development dependencies:

Bash
uv pip install -e ".[dev]"
Usage
To launch the interactive menu, run the following command from the project root:

Bash
python -m health_app.main
Menu Options:
Add Health Record: Enter name, weight, and height. Data is validated and saved immediately.

View All Records: Displays all saved entries with BMI, Category, and Ideal Weight difference.

View Statistics: Shows total records, average BMI, and category distribution.

Save & Quit: Safely exits the application.

Development & Testing
This project follows a strict testing protocol to ensure data integrity.

Running Unit Tests
To execute the full test suite (12 tests covering logic, validation, and persistence):

Bash
pytest tests/ -v
Project Structure
Plaintext
health_app/
├── src/
│   └── health_app/
│       ├── health.py    # Core Domain Logic
│       ├── data.py      # Persistence & Statistics
│       └── main.py      # CLI Interface
├── tests/               # Unit Test Suite
├── pyproject.toml       # Project Metadata
└── uv.lock              # Dependency Lockfile
Final Submission Checklist
[x] All 12 tests passing.

[x] JSON persistence verified with indent=2.

[x] uv.lock file generated and included.

[x] Input validation prevents application crashes.


---

### One Final Step for your PDF:
If you want this README to look amazing in your PDF, I recommend using the **Markdown PDF** extension I mentioned earlier. It will render all those headings, bold text, and code blocks into a beautifully formatted document.

**Would you like me to help you draft a short "Executive Summary" for your cover page to go along with this?**