import json
import subprocess
import logging
import os

def loadConfiguration(file):
    with open(file, 'r') as fid:
        configuration = json.load(fid)
    return configuration

def checkFileStatus(filePath):
    fileStatus = str(subprocess.check_output(["lfs", "hsm_state", filePath]))
    logger = logging.getLogger()
    if 'released' in fileStatus:
        logger.error('The file is not restored to Lustre and cannot be removed from backend. Please release the file before.')
        return False
    elif 'archived' not in fileStatus:
        logger.error('The file does not appear to be in the backend.')
        return False
    else:
        return True
    
def get_relative_path(path):
    mountPath = os.path.abspath(path)
    while not os.path.ismount(mountPath):
        mountPath = os.path.dirname(mountPath)

    relativePath = os.path.abspath(path).replace(mountPath, "")    

    if relativePath[0] == '/':
        relativePath = relativePath[1:]
    
    return relativePath