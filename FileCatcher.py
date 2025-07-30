import os
import shutil
import string
import threading
import random
import json
import time
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog

# Global flags and variables
pause_event = threading.Event()
stop_event = threading.Event()
scanning = False
found_files = []
revert_log = []
spinner_frames = ["|", "/", "-", "\\"]
dot_score = 0
dot_item = None

LOG_FILE = "log.txt"
REVERT_LOG_FILE = "revert_log.json"

# Initialize GUI
root_window = tk.Tk()
root_window.title("Freakbob File Catcher")
root_window.geometry("850x650")
root_window.configure(bg="black")

# Frames
top_frame = tk.Frame(root_window, bg="black")
top_frame.pack(pady=10)
middle_frame = tk.Frame(root_window, bg="black")
middle_frame.pack()
bottom_frame = tk.Frame(root_window, bg="black")
bottom_frame.pack(pady=10)

# Spinner and live path
spinner_label = tk.Label(top_frame, text="", fg="lime", bg="black", font=("Consolas", 16))
spinner_label.pack()

current_path_label = tk.Label(top_frame, text="", fg="gray", bg="black", font=("Consolas", 10))
current_path_label.pack()

# Output box
output_box = scrolledtext.ScrolledText(middle_frame, width=100, height=25, bg="black", fg="lime", font=("Consolas", 10))
output_box.pack()

# Scan mode checkboxes
display_only_var = tk.BooleanVar()
copy_var = tk.BooleanVar()
move_var = tk.BooleanVar()

tk.Checkbutton(bottom_frame, text="Display Only", variable=display_only_var, fg="white", bg="black", selectcolor="black").grid(row=0, column=0)
tk.Checkbutton(bottom_frame, text="Copy Files", variable=copy_var, fg="white", bg="black", selectcolor="black").grid(row=0, column=1)
tk.Checkbutton(bottom_frame, text="Move Files", variable=move_var, fg="white", bg="black", selectcolor="black").grid(row=0, column=2)

# Logging
def write_log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.ctime()}: {message}\n")

def save_revert_log():
    with open(REVERT_LOG_FILE, "w") as f:
        json.dump(revert_log, f, indent=2)

def load_revert_log():
    if os.path.exists(REVERT_LOG_FILE):
        with open(REVERT_LOG_FILE, "r") as f:
            return json.load(f)
    return []
def revert_files():
    global revert_log
    revert_log = load_revert_log()
    errors = 0
    for entry in revert_log:
        try:
            if os.path.exists(entry["new"]):
                shutil.move(entry["new"], entry["original"])
                write_log(f"Reverted: {entry['new']} -> {entry['original']}")
        except Exception as e:
            errors += 1
            write_log(f"Error reverting {entry['new']}: {e}")
    messagebox.showinfo("Revert Complete", f"Revert finished with {errors} error(s).")
    revert_log = []
    save_revert_log()

def get_available_drives():
    return [f"{letter}:/" for letter in string.ascii_uppercase if os.path.exists(f"{letter}:/")]

def get_downloads_folder():
    return str(Path.home() / "Downloads")

def scan_for_files():
    global scanning, found_files, revert_log
    scanning = True
    found_files = []
    revert_log = []
    selected_exts = [".png", ".pka"]
    drives = get_available_drives()
    downloads = get_downloads_folder()
    all_paths = drives + [downloads]

    output_box.insert(tk.END, "Scanning the following locations:\n")
    for path in all_paths:
        output_box.insert(tk.END, f" - {path}\n")
    output_box.insert(tk.END, "\n")
    write_log("Scan started.")
    count = 0

    for drive in all_paths:
        for root, _, files in os.walk(drive):
            if stop_event.is_set():
                scanning = False
                return
            pause_event.wait()
            current_path_label.config(text=f"Scanning: {root}")
            root_window.update_idletasks()

            for file in files:
                if any(file.lower().endswith(ext) for ext in selected_exts):
                    full_path = os.path.join(root, file)
                    found_files.append(full_path)
                    if count < 100:
                        output_box.insert(tk.END, full_path + "\n")
                        count += 1
                    write_log(f"Found: {full_path}")
    scanning = False
    current_path_label.config(text="")
    write_log(f"Scan complete. {len(found_files)} file(s) found.")
    show_summary()

def rotate_spinner(index=0):
    if not scanning:
        spinner_label.config(text="")
        return
    spinner_label.config(text=f"Scanning {spinner_frames[index % len(spinner_frames)]}")
    root_window.after(150, lambda: rotate_spinner(index + 1))

def show_summary():
    if not found_files:
        messagebox.showinfo("No Files", "No matching files found.")
        return
    result = messagebox.askyesno("Summary", f"{len(found_files)} files found.\nProceed with selected action?")
    if result:
        handle_files()

def handle_files():
    global revert_log
    target_folder = filedialog.askdirectory(title="Choose Target Folder")
    if not target_folder:
        return

    for file in found_files:
        filename = os.path.basename(file)
        destination = os.path.join(target_folder, filename)
        try:
            if move_var.get():
                shutil.move(file, destination)
                revert_log.append({"original": file, "new": destination})
                write_log(f"Moved: {file} -> {destination}")
            elif copy_var.get():
                shutil.copy2(file, destination)
                write_log(f"Copied: {file} -> {destination}")
        except Exception as e:
            write_log(f"Error processing {file}: {e}")
    if move_var.get():
        save_revert_log()
    messagebox.showinfo("Action Complete", f"{'Copied' if copy_var.get() else 'Moved'} {len(found_files)} files.")
def start_scan():
    if display_only_var.get() + copy_var.get() + move_var.get() != 1:
        messagebox.showwarning("Invalid Option", "Select only one mode: Display, Copy, or Move.")
        return
    output_box.delete(1.0, tk.END)
    stop_event.clear()
    threading.Thread(target=scan_for_files).start()
    rotate_spinner()

def pause_scan():
    if pause_event.is_set():
        pause_event.clear()
    else:
        pause_event.set()

def stop_scan():
    stop_event.set()

# --- Mini Dot Game ---
def spawn_dot_game():
    global dot_item
    if dot_item:
        canvas.delete(dot_item)
    x, y = random.randint(10, 390), random.randint(10, 190)
    dot_item = canvas.create_oval(x, y, x + 20, y + 20, fill="red")
    canvas.tag_bind(dot_item, "<Button-1>", hit_dot)

def hit_dot(event):
    global dot_score
    dot_score += 1
    score_label.config(text=f"Score: {dot_score}")
    spawn_dot_game()

# --- Bottom Buttons ---
tk.Button(bottom_frame, text="Start Scan", command=start_scan, bg="gray", fg="white").grid(row=0, column=3)
tk.Button(bottom_frame, text="Pause", command=pause_scan, bg="gray", fg="white").grid(row=0, column=4)
tk.Button(bottom_frame, text="Stop", command=stop_scan, bg="gray", fg="white").grid(row=0, column=5)
tk.Button(bottom_frame, text="Revert Last Action", command=revert_files, bg="darkred", fg="white").grid(row=0, column=6)

# --- Mini Game Frame ---
game_frame = tk.Frame(root_window, bg="black")
game_frame.pack(pady=10)

canvas = tk.Canvas(game_frame, width=400, height=200, bg="black")
canvas.pack()

score_label = tk.Label(game_frame, text="Score: 0", fg="lime", bg="black", font=("Consolas", 12))
score_label.pack()

spawn_dot_game()

# --- Final Setup ---
pause_event.set()
root_window.mainloop()
