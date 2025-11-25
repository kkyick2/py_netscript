**README.md**  
**Cisco Show-Command Parser with NTC-Templates & TextFSM**  
`2pytextfsm.py` – Bulk parse Cisco `show` command outputs into a single Excel workbook (one sheet per command).

### Features

- Uses the excellent **ntc-templates** collection (hundreds of ready-made TextFSM templates)
- Parses **all devices of the same platform** in one run
- Adds a **DEVICE_NAME** column automatically
- Outputs a timestamped Excel file (`.xlsx`) with **one sheet per command**
- Fully automatic – just drop your raw text files in the right folder

### Folder Structure (required)

```
your_project_folder/
├── 2pytextfsm.py                  ← this script
├── outputcmd/                     ← INPUT FOLDER (do not rename)
│   └── cisco_ios/                 ← one sub-folder per platform
│       ├── SW01_show_version_20251121.txt
│       ├── SW01_show_inventory_20251121.txt
│       ├── R1_show_interfaces_20251121.txt
│       └── ...
└── outputtextfsm/                 ← OUTPUT FOLDER (created automatically)
        └── textfsm_output_20251121_1430.xlsx
```

**Important:**  
File names **must** contain the device hostname at the beginning.  
Example (anything after the first underscore is ignored):

```
SW-Core-01_show_version.txt
R2_show_ip_interface_brief.txt
```

### Installation (Windows – recommended in a virtual environment)

```bash
# 1. Clone or copy the script
cd C:\Users\jackyyick\projects_local\python\py_netscript

# 2. Create a fresh venv (highly recommended)
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install pandas xlsxwriter textfsm ntc-templates
```

### Usage

```bash
(venv) C:\Users\jackyyick\projects_local\python\py_netscript> python 2pytextfsm.py
```

The script will:

1. Auto-detect the ntc-templates location
2. Parse every command listed in the `commands` list
3. Create one Excel sheet per command
4. Save the file as `outputtextfsm/textfsm_output_YYYYMMDD_HHMM.xlsx`

### Supported Commands (uncomment to enable)

```python
commands = [
    'show_version',
    'show_inventory',
    'show_interfaces',
    'show_ip_interface_brief',
    # 'show_vlan',
    # 'show_interfaces_switchport',
    # 'show_ip_bgp_summary',
    # ... and many more – just remove the #
]
```

All templates are provided by **ntc-templates** → https://github.com/networktocode/ntc-templates

### Known Limitations / To-Do

- Currently supports **only cisco_ios** (easy to extend – just add folder + change `device_type`)
- Device name extraction uses `file[:-8]` (works if your files end with 8 characters like `_123.txt`).  
  For maximum robustness, replace this line in `_parse_each_file()` with:

```python
df_parsed.insert(0, 'DEVICE_NAME', file.split('_', 1)[0])
```

- Excel column auto-width is currently commented out (uncomment and adjust if needed)

### Credits

- Original author: **kkyick2**
- TextFSM templates: **Network to Code – ntc-templates**
- Bug-fixes & README: ChatGPT (you!)

Enjoy clean, structured network data in seconds instead of hours!
