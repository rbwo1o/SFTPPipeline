# ***********************************************************************************************************************
# *                                                                                                                     *
# *   SFTPPipeline.py                                                                                                   *
# *   Author: Robert B. Wilson                                                                                          *
# *   The purpose of this file is to serve as the entry point of the SFTPPipeline application                           *
# *                                                                                                                     *
# ***********************************************************************************************************************

import PyQt5
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import sys
from classes.Database import Database
from views.MainWindow import MainWindow
from datetime import datetime
import pysftp


# check for command line arguments
if len(sys.argv) > 1:
    n = len(sys.argv)
    db = Database()
    for i in range(1, n):
        preset = db.getPresetByID(sys.argv[i])
        if preset:
            relation = db.getRelations(preset[0][1])
            files = relation[0]
            serverInfo = relation[1]
            cnopts1 = pysftp.CnOpts()
            cnopts1.hostkeys=None
            # for each sftp server
            for data in serverInfo:
                server = data[0]
                remoteDirectory = data[1]
                credentials = db.getConnectionCredentials(server)
                for local_filePath in files:
                    try:
                        with pysftp.Connection(host=server, username=credentials[0][0], password=credentials[0][1], port=22, cnopts=cnopts1) as sftp:
                            print("Connected!")
                            with sftp.cd(remoteDirectory):
                                sftp.put(local_filePath)
                                # Inform database
                                now = datetime.now()
                                message = f"Sent {local_filePath} to {server} -> {remoteDirectory}"
                                db.addChangelog(now, message, None)
                    except Exception as e:
                        now = datetime.now()
                        message = f"Could not send {local_filePath} to {server} -> {remoteDirectory}"
                        db.addChangelog(now, message, str(e))
    del db
else:
    # display MainWindow
    app = QApplication(sys.argv)
    UI = MainWindow()
    app.exec_()