import tkinter as tk
from tkinter import messagebox
import DaVinciResolveScript as dvr_script


# --- Place your previously built functions here ---
def run_organizer():
    # Insert the "Smart Bins" code here
    print("Running Organizer...")
    messagebox.showinfo("Success", "Clips organized into Smart Bins!")


def run_cst_notes():
    # Insert the "Auto CST" code here
    print("Applying Color Notes...")
    messagebox.showinfo("Success", "Color Space Transform notes applied!")


def run_marker_injector():
    # Insert the "Master Marker" code here
    print("Injecting Markers...")
    messagebox.showinfo("Success", "AI Markers added to timeline!")


# --- GUI Construction ---
def create_panel():
    root = tk.Tk()
    root.title("Resolve Workflow Pro")
    root.geometry("250x300")
    root.attributes("-topmost", True)  # Keeps the window floating over Resolve

    label = tk.Label(
        root, text="Workflow Automation", font=("Helvetica", 12, "bold"), pady=10
    )
    label.pack()

    # Button 1: Organization
    btn_org = tk.Button(
        root, text="📁 Organize Media", command=run_organizer, width=20, pady=5
    )
    btn_org.pack(pady=5)

    # Button 2: Color Notes
    btn_color = tk.Button(
        root, text="🎨 Apply Color Notes", command=run_cst_notes, width=20, pady=5
    )
    btn_color.pack(pady=5)

    # Button 3: Markers
    btn_marker = tk.Button(
        root, text="📍 Inject AI Markers", command=run_marker_injector, width=20, pady=5
    )
    btn_marker.pack(pady=5)

    # Exit Button
    btn_exit = tk.Button(
        root, text="Close", command=root.destroy, width=20, pady=5, fg="red"
    )
    btn_exit.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    create_panel()
