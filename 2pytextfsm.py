#!/usr/bin/env python
# by kkyick2
# import pkg
import os
import pandas as pd
import ntc_templates
import textfsm
from datetime import datetime


"""
    ### Usage
    ```bash
    (venv) C:\\Users\\jackyyick\\projects_local\\python\\py_pytextfsm> python pytextfsm.py
    ```
    The script will:
    1. Parse every command listed in the `commands` list
    2. Create one Excel sheet per command
    3. Save the file as `outputtextfsm/textfsm_output_YYYYMMDD_HHMM.xlsx`

    project folders
    ```
    your_project_folder/
    ├── pytextfsm.py                  ← this script
    ├── outputcmd/                     ← INPUT FOLDER
    │   └── cisco_ios/                 ← one sub-folder per platform, input conf file here
    │       ├── SW01_show_version_20251121.txt
    │       ├── SW01_show_inventory_20251121.txt
    │       ├── R1_show_interfaces_20251121.txt
    │       └── ...
    └── outputtextfsm/                 ← OUTPUT FOLDER
            └── textfsm_output_20251121_1430.xlsx
    ```

    ### Installation (Windows)
    ```bash
    # Install dependencies
    pip install --upgrade pip
    pip install pandas xlsxwriter textfsm ntc-templates
    ```
    ### Ref
    https://github.com/networktocode/ntc-templates/tree/master/ntc_templates/templates
"""

# Find the folder where ntc_templates are installed.
TEMPLATES_DIR = os.path.dirname(os.path.dirname(ntc_templates.__file__)) + '/ntc_templates/templates'
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONF_DIR = 'outputcmd'
OUT_XLS_DIR = 'outputtextfsm'
CONF_FILENAME_OFFSET = int(8)  # number of char to ignore from the end of each conf filename, eg switch01_all.txt -> device_name: switch01

def _load_template(device_type, command, templates_dir):
    # _load_template function will load correct template
    with open(f"{templates_dir}/{device_type}_{command}.textfsm") as f:
        return textfsm.TextFSM(f)


def _parse_each_file():
    # _parse_each_file will prepare a dataframe containing parsed content of each file.
    df = pd.DataFrame()

    for device_type in sorted(os.listdir(CONF_DIR)):
        for file in sorted(os.listdir(os.path.join(CONF_DIR, device_type))):
            print(os.path.join(device_type, file))

            template.Reset()  # otherwise entires from next loop item adds to the previous loop item,
            OUT_CMD_TXT = os.path.join(CONF_DIR, device_type, file)
            with open(OUT_CMD_TXT) as f:
                text = f.read()

            df_parsed = pd.DataFrame(template.ParseTextToDicts(text))
            df_parsed.insert(0, 'DEVICE_NAME', file[:-CONF_FILENAME_OFFSET]) # the script ignore last 8 char of each filename, eg switch01_all.txt -> device_name: switch01
            df = pd.concat([df, df_parsed])
    return df


def _write_to_excel(df_list):
    # this function will write the dataframes for each command into an excel file.
    DATETIME = datetime.now().strftime("%Y%m%d_%H%M")
    writer = pd.ExcelWriter(OUT_XLS_DIR +'/textfsm_output_' + DATETIME + '.xlsx', engine='xlsxwriter')
    for df, sheetname in df_list:
        df.to_excel(writer, sheet_name=sheetname, index=False)
        workbook = writer.book
        worksheet = writer.sheets[sheetname]
        cell_format = workbook.add_format()
        cell_format.set_text_wrap()
        cell_format.set_align('center')
        cell_format.set_align('vcenter')
    writer._save()


if __name__ == "__main__":
    device_type = 'juniper_junos'
    commands = [
        #'show_interfaces',
        'show_bgp_summary',
        'show_version',
    ]

    '''
    device_type = 'cisco_ios'
    commands = [
        'show_version',
        'show_inventory',
        # 'show_environment_power_all',
        #'show_vlan',
        'show_interfaces',
        #'show_interfaces_switchport',
        # 'show_ip_interface',
        'show_ip_interface_brief',
       # 'show_ip_bgp_summary',
        #'show_ip_bgp',
        #'show_ip_bgp_neighbors',
        #'show_ip_route',
         # 'show_standby_brief',
         # 'show_mac-address-table',
         # 'show_ip_arp',
        #'show_cdp_neighbors_detail',
        #'show_clock',
    ]
    '''
    # Create a seperate df for each command thereby seperate sheet for each command for all devices.
    df_list = []
    print(TEMPLATES_DIR)
    for command in commands:
        print(f"Parsing the cmdoutput of {device_type} {command}\n!")
        template = _load_template(device_type, command, TEMPLATES_DIR)
        df_list.append([_parse_each_file(), command])
    _write_to_excel(df_list)