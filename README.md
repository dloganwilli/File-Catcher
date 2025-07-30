# FileCatcher

FileCatcher is a desktop GUI utility built in Python using Tkinter. It scans all connected drives and the user's Downloads folder for specific file types (`.png` and `.pka` by default). It offers three modes: display-only, copy, or move. The app features live scanning feedback, action logging, a revert function for moved files, and a built-in mini game while scanning.

## Features

- Scans all connected drives and the Downloads folder
- Filters for `.png` and `.pka` file types (editable in the code)
- Modes: display-only, copy files, or move files
- Tkinter GUI styled with black/green terminal aesthetic
- Realtime scan feedback with spinner and path display
- Scrollable output box for listing results
- Logging of actions to `log.txt`
- Revert button restores moved files using `revert_log.json`
- Built-in click-the-dot mini game to pass time during scans

## Built With

- Python 3
- Tkinter for GUI
- `os`, `shutil`, `threading`, `json`, and other standard libraries

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/dloganwilli/File-Catcher.git
   cd File-Catcher
   ```

2. Run the app:
   ```bash
   python FileCatcher.py
   ```

3. Choose one scan mode:
   - Display Only
   - Copy Files
   - Move Files

4. Click "Start Scan" and wait for results. You’ll be prompted for a destination folder if copying or moving files.

5. You can pause/stop the scan or revert the last move action using the buttons at the bottom.

## File Types

By default, the app looks for:
```python
selected_exts = [".png", ".pka"]
```
You can modify this in the `scan_for_files()` function if needed.

## Logging

- `log.txt`: Logs found files and all copy/move actions
- `revert_log.json`: Stores move actions for the revert feature

## To-Do / Future Improvements

- Add UI option to select file types
- Export scan results as CSV or TXT
- Add drag-and-drop file support
- Add total file size and progress bar

## Author

Logan Williamson  
[GitHub](https://github.com/dloganwilli)
