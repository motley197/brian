1. Edit settings.json to reflect your own personal installation
2. In the folder where you are working (prob. includes source files), create a folder .vscode
3. Copy these files into the .vscode folder you created in (2)
4. Open a terminal, and switch to the virtual environment 
   e.g. source ~/zephyrproject/.venv/bin/activate
5. Run vscode with:
   code .

6. Run the tasks (crtl-shift-p) build, clean, flash etc..
7. You should be able to debug using the debug window (ctrl-shift-D)

Credit: https://www.hackster.io/philippmanstein/debug-the-raspberry-pi-pico-running-zephyr-rtos-on-macos-5b4436
