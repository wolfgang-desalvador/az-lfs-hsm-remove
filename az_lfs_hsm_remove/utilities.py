import json
import subprocess
import logging

def loadConfiguration(file):
    with open(file, 'r') as fid:
        configuration = json.load(fid)
    return configuration

def checkFileStatus(filePath):
    fileStatus = subprocess.check_output(["lfs hsm_state", filePath])
    logger = logging.getLogger()
    if 'released' in fileStatus:
        logger.error('The file is not restored to Lustre and cannot be removed from backend. Please release the file before.')
        return False
    elif 'archieved' not in fileStatus:
        logger.error('The file does not appear to be in the backend.')
        return False
    else:
        return True