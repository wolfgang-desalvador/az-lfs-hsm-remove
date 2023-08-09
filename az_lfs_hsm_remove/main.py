import sys
import os
import logging
import argparse

from .lfs_blob_client import LFSBlobClient

def main():
    parser = argparse.ArgumentParser(prog='Azure LFS HSM Remove', description='This utility helps managing removed files from Azure Blob Lustre HSMbackend.')

    parser.add_argument('-f', "--force", default=False, required=False, action='store_true', help="This forces removal from Blob Storage independently from the HSM status. Use carefully.")     

    args, extras = parser.parse_known_args()
    
    logger = logging.getLogger()

    if not extras:
        logger.error('No filename specified.')
        sys.exit(1)

    fileToRemove = extras[-1]
    

    if os.path.isdir(fileToRemove):
        logger.error('HSM operates on files, not on folders. The input path refers to a folder.')
    elif args.force or os.path.exists(fileToRemove):
        LFSBlobClient().lfs_hsm_remove(fileToRemove, args.force)
    else:
        logger.error('The file provided does not exist on the system')
    
