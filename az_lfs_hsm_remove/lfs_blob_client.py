import os
import subprocess
import logging

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError

from .utilities import loadConfiguration, checkFileStatus, get_relative_path


class LFSBlobClient(BlobServiceClient):
    def __init__(self, configurationFile='/etc/az_lfs_hsm_remove.json', **kwargs) -> None:
        configuration = loadConfiguration(configurationFile)
        self.accountURL = configuration.get('accountURL')
        self.containerName = configuration.get('containerName')
        super().__init__(self.accountURL, credential=DefaultAzureCredential(exclude_workload_identity_credential=True, exclude_environment_credential=True), **kwargs)

    def lfs_hsm_remove(self, filePath, force=False):
        absolutePath = os.path.abspath(filePath)
        logger = logging.getLogger()

        ### In case path is available on the filesystem, now use hsm_remove standard command since supported
        if os.path.exists(absolutePath):
            if checkFileStatus(absolutePath):
                try:
                    subprocess.check_output(["lfs", "hsm_remove", absolutePath])
                except subprocess.CalledProcessError as error:
                    logger.error(f"Failed in removing file {absolutePath}.")
                    raise error
        elif force:
            try:
                client = self.get_blob_client(container=self.containerName, blob=get_relative_path(absolutePath))
                client.delete_blob()
            except ResourceNotFoundError as error:             
                if force:
                    logger.info("Data seems not to be anymore on the HSM backend.")
                else:
                    logger.error("Data seems not to be anymore on the HSM backend even if hsm_state expects it to be there.")
                    raise error
            try:
                subprocess.check_output(["lfs", "hsm_set", "--lost", absolutePath])
                subprocess.check_output(["lfs", "hsm_set", "--dirty", absolutePath])
            except subprocess.CalledProcessError:
                if force:
                    pass
                else:
                    logger.error("Failed in setting hsm_state correctly. Please check the file status.")
                    raise error