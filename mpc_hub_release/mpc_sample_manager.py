from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
import os
import shutil
import zipfile

app = FastAPI()

BASE_DIR = "/app/MPC_Samples"
FOLDERS = ["Drums", "Synths", "Vocals", "Unsorted"]

for folder in FOLDERS:
    os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, search: str = ""):
    sample_list = []
    for folder in FOLDERS:
        f_path = os.path.join(BASE_DIR, folder)
        if os.path.exists(f_path):
            for file in os.listdir(f_path):
                if not file.startswith(".") and (search.lower() in file.lower()):
                    sample_list.append({"name": file, "category": folder})

    html_content = f"""
    <html>
        <head>
            <title>MPC Sample Hub Pro</title>
            <style>
                body {{ font-family: sans-serif; background: #121212; color: #eee; padding: 20px; }}
                .card {{ background: #1e1e1e; padding: 20px; border-radius: 8px; border: 1px solid #333; margin-bottom: 20px; }}
                button {{ background: #ff5722; color: white; padding: 10px; border: none; cursor: pointer; border-radius: 4px; font-weight: bold; }}
                audio {{ height: 35px; filter: invert(100%); }}
                table {{ width: 100%; border-collapse: collapse; }}
                td {{ padding: 12px; border-bottom: 1px solid #333; }}
            </style>
        </head>
        <body>
            <h1>🎹 MPC Sample Hub Pro v1.0.4</h1>
            <div class="card">
                <h3>📤 Upload Sample</h3>
                <form action="/upload/" method="post" enctype="multipart/form-data">
                    <input type="file" name="file" required>
                    <select name="folder">
                        {" ".join([f'<option value="{f}">{f}</option>' for f in FOLDERS])}
                    </select>
                    <button type="submit">Upload</button>
                </form>
            </div>
            <div class="card">
                <h3>📂 Library <a href="/download-all/" style="float:right;"><button style="background:#2196f3;">📦 Download ZIP</button></a></h3>
                <table>
                    {"".join([f'<tr><td>{s["name"]}</td><td>{s["category"]}</td><td><audio controls src="/play/{s["category"]}/{s["name"]}"></audio></td></tr>' for s in sample_list])}
                </table>
            </div>
        </body>
    </html>
    """
    return html_content


@app.post("/upload/")
async def upload_sample(file: UploadFile = File(...), folder: str = Form(...)):
    file_path = os.path.join(BASE_DIR, folder, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        buffer.flush()
        os.fsync(buffer.fileno())
    return RedirectResponse(url="/", status_code=303)


@app.get("/play/{{folder}}/{{filename}}")
async def play_sample(folder: str, filename: str):
    # DYNAMICALLY FIXING PATH FOR PLAYBACK
    file_path = os.path.join(BASE_DIR, folder, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    ext = filename.split(".")[-1].lower()
    mimes = {{"wav": "audio/wav", "mp3": "audio/mpeg", "aif": "audio/x-aiff"}}
    return FileResponse(file_path, media_type=mimes.get(ext, "audio/wav"))


@app.get("/download-all/")
async def download_all():
    zip_path = "/tmp/MPC_PACK.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in FOLDERS:
            f_dir = os.path.join(BASE_DIR, f)
            for root, _, files in os.walk(f_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.join(f, file))
    return FileResponse(zip_path, filename="MPC_PACK.zip")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
