import tarfile, zipfile, io
from typing import List, Tuple

def safe_list_zip(data: bytes, max_entries: int = 1000) -> List[str]:
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        names = z.namelist()
        if len(names) > max_entries:
            raise ValueError("Archive too large")
        for n in names:
            if ".." in n or n.startswith("/"):
                raise ValueError("Path traversal detected")
        return names
