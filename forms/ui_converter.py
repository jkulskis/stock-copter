import subprocess
import sys
import time

if __name__== '__main__':
    """Run pyuic5 by inputing the first argument as the ui filename without the .ui

    Outputs a python file in the form of sys.argv[1]+'UI.py' and replaces the old PyQt5 import
    with the newer PySide2 import
    """
    ui_filename = sys.argv[1]+'.ui'
    py_filename = sys.argv[1]+'UI.py'
    p = subprocess.Popen(['pyuic5', ui_filename, '-o', py_filename])
    p.wait() # Wait for the ui --> python conversion to finish before attempting to replace anything
    with open(py_filename, 'r+') as f:
        modified_text = f.read().replace('from PyQt5 import', 'from PySide2 import')
        f.seek(0) # set the read pointer to the beggining of the file
        f.truncate(0) # truncate the contents of the file so that we can replace the old content
        f.write(modified_text)