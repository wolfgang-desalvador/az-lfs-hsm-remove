import sys
import os

from .lfs_blob_client import LFSBlobClient

def main():
    fileToRemove = sys.argv[-1]

    if os.path.exists(fileToRemove):
        LFSBlobClient().lfs_hsm_remove(fileToRemove)

    
