# pacemaker-security
_______
Required Modules
______

os, json, cryptography, bcrypt, base64, tkinter, socket, sys, errno, threading, datetime, re, secrets, typing, random, neurokit2, matplotlib, tkmacosx, numpy

All modules can be installed using the pip3 install “module-name”
______
How to run the program
_____

The pacemaker client resides in the client directory and the server in the server directory.

To run the program, first run the gui.py file with the python3 gui.py command. Next enter the login username: admin and password: heartbeat.

You will then be brought to a loading screen while the program waits for the pacemaker to connect.

Now in the client directory run the pacemaker_client.py file with python3. The GUI will detect the connection and navigate to the menu to allow for the monitoring and editing of pacemaker settings.

Editable settings include. Each setting can only be changed one at time. Do not change multiple settings at once. This will cause unexpected behavior which may crash the program.

Pacemaker Modes: DDD,AAI,VVI. Encryption: ON/OFF.

