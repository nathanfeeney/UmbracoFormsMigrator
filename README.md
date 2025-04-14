# Config File PreValues Transformer

This Python script is designed to **recursively find and reformat `preValues`** within JSON blocks embedded in `.config` XML files. It is primarily intended for migrating or updating old Umbraco Forms configurations.

---

## What It Does

- Parses `.config` files in a given folder.
- Locates `Pages` elements containing JSON (wrapped in CDATA).
- Finds `preValues` lists and converts them from:

  ```json
  "preValues": ["Option 1", "Option 2"]
  ```

  to:

  ```json
  "preValues": [
    { "value": "Option 1", "sortOrder": 0 },
    { "value": "Option 2", "sortOrder": 1 }
  ]
  ```

- Re-wraps the modified JSON in CDATA and saves the updated XML back to the same file.

---

## Folder Path Setup

Update the `FOLDER_PATH` variable in the script to point to the directory containing your `.config` files:

```python
FOLDER_PATH = r"C:\Path\To\Your\Config\Files"
```

---

## Requirements

- Python 3.x
- lxml library

Install dependencies:

```bash
pip install lxml
```

---

## Usage

1. Place the script in your working directory.
2. Update the `FOLDER_PATH` variable as described above.
3. Run the script using:

```bash
python script_name.py
```

---

## Debugging and Logging

- Includes `print()` debug statements to trace the JSON transformation process.
- If a file contains invalid XML or malformed JSON, it will be skipped with a message.

---

## Output

- Transformed `.config` files with updated `preValues`.
- Original structure (aside from the modified JSON) is preserved.
- A final count of processed files is printed to the console.

---

## Notes

- **Back up your config files before running the script**.
- Changes are saved directly to the original files.

---

## License

MIT – Free to use and modify.
