import os
import pytest
from health_app.health import Health
from health_app.data import save_all_records, load_records, get_statistics

TEST_FILE = "test_records.json"


@pytest.fixture(autouse=True)
def cleanup():
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    yield
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


# ✔ Save/load roundtrip
def test_save_load_roundtrip():
    original = [Health("User A", 70, 1.7), Health("User B", 90, 1.8)]
    save_all_records(original, TEST_FILE)
    loaded = load_records(TEST_FILE)
    assert len(loaded) == 2
    assert loaded[0].name == "User A"


# ✔ Load empty/nonexistent file
def test_load_nonexistent():
    assert load_records("ghost.json") == []


# ✔ Statistics calculation (all fields) & Category distribution
def test_statistics_accuracy():
    records = [
        Health("U1", 50, 1.8),  # Underweight
        Health("U2", 70, 1.8),  # Normal
        Health("U3", 75, 1.8),  # Normal
    ]
    save_all_records(records, TEST_FILE)
    stats = get_statistics(TEST_FILE)

    assert stats["total_records"] == 3
    assert stats["avg_bmi"] == round((15.43 + 21.60 + 23.15) / 3, 2)
    assert stats["most_common_category"] == "Normal"
    assert stats["category_distribution"]["Normal"] == 2
    assert stats["category_distribution"]["Underweight"] == 1
