import os


def test_data_directory_exists():
    # This ensures your project structure is correct
    assert os.path.exists("data/")


def test_ranked_file_generation():
    # This ensures your pipeline actually creates the output file
    if os.path.exists("data/students_ranked.csv"):
        assert os.path.getsize("data/students_ranked.csv") > 0
