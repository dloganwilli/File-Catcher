FileCatcher
FileCatcher is a desktop GUI tool built in Python using Tkinter. It scans all connected drives and your Downloads folder for specific file types (.png and .pka by default), then lets you either display, copy, or move those files to a new location. It includes live scanning feedback, logging, a revert option, and a built-in mini game to kill time while scanning.

Features
Scans all available drives and the user's Downloads folder

Filters for .png and .pka files (customizable in code)

Three scan modes: display only, copy, or move

GUI built with Tkinter (black/green console aesthetic)

Spinner animation and live path updates during scan

Logging of all found and moved/copied files

Revert function to undo the last move action

Realtime console output during scan

Embedded “click-the-dot” mini game while you wait

How to Use
Start the application

bash
Copy
Edit
python FileCatcher.py
Choose a scan mode at the bottom:

Display Only

Copy Files

Move Files

Click "Start Scan" and let it run.

It will scan every connected drive and your Downloads folder.

Matching files are listed in the output box.

If you chose Copy or Move, you’ll be prompted to pick a target folder.

To pause or stop, use the Pause/Stop buttons.

To undo a move, click “Revert Last Action.” It restores files to their original paths using a saved log.

Requirements
Python 3.6+

Built-in libraries only (no external dependencies)

File Types
The script currently looks for:

python
Copy
Edit
selected_exts = [".png", ".pka"]
You can change this in the scan_for_files() function.

Logging
log.txt: All actions like files found, copied, moved, or errors

revert_log.json: Stores move history for undo functionality

UI Preview (no screenshot yet)
Console-style GUI (green text on black)

Scrolling output window

Status spinner and live folder updates

Dot-click mini game at the bottom

To-Do / Future Improvements
Add file type filter UI

Custom file extensions from settings

Export results as CSV or TXT

Add confirmation for large file moves

Author
Logan Williamson (dloganwilli)
