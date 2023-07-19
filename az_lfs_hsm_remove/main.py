import sys
import os
import logging

from .lfs_blob_client import LFSBlobClient

def main():
    fileToRemove = sys.argv[-1]
    logger = logging.getLogger()

    if os.path.isdir(fileToRemove):
        logger.error('HSM operates on folders, not on files. The input path refers to a folder.')
    elif os.path.exists(fileToRemove):
        LFSBlobClient().lfs_hsm_remove(fileToRemove)
    else:
        logger.error('The file provided does not exist on the system')
    
