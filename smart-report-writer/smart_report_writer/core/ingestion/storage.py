from typing import Optional
from smart_report_writer.core.utils.logging import get_logger
from urllib.parse import quote_plus

class StorageClient:
    def __init__(self, s3, bucket: str):
        self.s3 = s3
        self.bucket = bucket
        self.log = get_logger("storage")

    def put_bytes(self, data: bytes, key: str) -> str:
        self.s3.put_object(Bucket=self.bucket, Key=key, Body=data)
        return key

    def get_presigned_url(self, key: str, expires: int = 3600) -> str:
        return self.s3.generate_presigned_url("get_object", Params={"Bucket": self.bucket, "Key": key}, ExpiresIn=expires)
