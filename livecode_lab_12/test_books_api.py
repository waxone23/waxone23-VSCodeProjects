def test_create_book(client):
    r = client.post("/books", json={"title": "Test", "author": "Author", "year": 2024})
    assert r.status_code == 201


def test_list_books(client):
    client.post("/books", json={"title": "Bok 1", "author": "A", "year": 2020})
    r = client.get("/books")
    assert len(r.json()) == 1


def test_get_existing_book(client):
    client.post("/books", json={"title": "Finn meg", "author": "A", "year": 2020})
    r = client.get("/books/1")
    assert r.status_code == 200
    assert r.json()["title"] == "Finn meg"


def test_get_missing_book(client):
    r = client.get("/books/999")
    assert r.status_code == 404


def test_delete_book(client):
    client.post("/books", json={"title": "Slett meg", "author": "A", "year": 2020})
    r = client.delete("/books/1")
    assert r.status_code == 200
    assert client.get("/books/1").status_code == 404
