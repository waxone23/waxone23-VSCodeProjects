# 🎹 MPC Sample Hub Pro (v1.0.0)
**The Wireless Bridge for Hardware Producers**

MPC Sample Hub Pro is a lightweight FastAPI application designed to eliminate the "SD Card Shuffle." Record samples on any device, upload them wirelessly to your Mac, audition them in the browser, and export an organized library ready for your Akai MPC.

---

## 🚀 One-Click Setup (macOS)
1. **Open Docker Desktop:** Ensure Docker is running on your Mac.
2. **Launch:** Double-click the `Launch_MPC_Hub.command` file in this folder.
3. **Access:** Your browser will automatically open to `http://localhost:8000`.

---

## ✨ Features
* **Wireless Uploads:** Record on your phone/tablet and beam files directly to your Studio Mac.
* **Instant Audition:** Integrated HTML5 player to preview `.wav`, `.mp3`, and `.aif` files.
* **Smart Hierarchy:** Auto-sorts samples into `Drums`, `Synths`, or `Vocals` folders.
* **Batch Export:** One-click "Download All" as a structured `.zip` file for your MPC SD card.
* **Dockerized:** Runs in an isolated container—no Python environment setup required.

---

## 📂 Project Structure (Waxone23 Standard)
The Hub automatically maintains this structure in your Mac's `Music` folder:
```text
/Users/[YourName]/Music/MPC_Samples/
├── Drums/          # Kicks, Snares, Hats
├── Synths/         # Moog M32, DFAM, Subharmonicon takes
├── Vocals/         # One-shots and phrases
└── Unsorted/       # Fresh captures# waxone23-VSCodeProjects
