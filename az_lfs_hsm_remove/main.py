import sys
import os
import logging

from .lfs_blob_client import LFSBlobClient

def main():
    fileToRemove = sys.argv[-1]

    if os.path.exists(fileToRemove):
        LFSBlobClient().lfs_hsm_remove(fileToRemove)
    else:
        logger = logging.getLogger()
        logger.error('The file provided does not exist on the system')
    
