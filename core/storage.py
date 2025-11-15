from .settings import settings


class Storage:
    def __init__(self, connection_string: str, container_name: str):
        from azure.storage.blob.aio import BlobServiceClient

        self.blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        self.container_client = self.blob_service_client.get_container_client(
            container_name
        )

    async def list_blobs(self, name_starts_with: str):
        return self.container_client.list_blobs(name_starts_with=name_starts_with)

    async def upload_blob(self, blob_name: str, data: bytes) -> None:
        blob_client = self.container_client.get_blob_client(blob_name)
        await blob_client.upload_blob(data, overwrite=True)

    async def download_blob(self, blob_name: str) -> bytes:
        blob_client = self.container_client.get_blob_client(blob_name)
        download_stream = await blob_client.download_blob()
        return await download_stream.readall()


storage = Storage(
    connection_string=settings.storage_connection_string,
    container_name=settings.storage_container_name,
)
