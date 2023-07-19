import os

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

from .utilities import loadConfiguration, checkFileStatus


class LFSBlobClient(BlobServiceClient):
    def __init__(self, configurationFile='/etc/az_lfs_hsm_remove.json', **kwargs) -> None:
        configuration = loadConfiguration(configurationFile)
        self.accountURL = configuration.get('accountURL')
        self.containerName = configuration.get('containerName')
        super().__init__(self.accountURL, credential=DefaultAzureCredential(), **kwargs)

    def lfs_hsm_remove(self, filePath):
        absolutePath = os.path.abspath(filePath)
        if checkFileStatus(absolutePath):
            client = self.get_blob_client(container=self.containerName, blob=absolutePath)
            client.delete_blob()