@echo off
call "C:\Users\OCC\projects_local\python\py-netscript\venv\Scripts\activate.bat"
start python 1pyshowcmd.py device_empf_iosnxos_p_hw.csv -o C:\Users\OCC\output\empf_pr
start python 1pyshowcmd.py device_empf_iosnxos_p_conf.csv -o C:\Users\OCC\output\empf_pr
start python 1pyshowcmd.py device_empf_iosnxos_p_all.csv -o C:\Users\OCC\output\empf_pr
start python 1pyshowcmd.py device_empf_fortinet_p_hw.csv -o C:\Users\OCC\output\empf_pr
start python 1pyshowcmd.py device_empf_fortinet_p_conf.csv -o C:\Users\OCC\output\empf_pr
start python 1pyshowcmd.py device_empf_fortinet_p_all.csv -o C:\Users\OCC\output\empf_pr