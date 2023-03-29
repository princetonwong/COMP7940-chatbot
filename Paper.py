from dataclasses import dataclass


@dataclass
class Paper:
    name: str
    fileType: str
    fileSize: int
    fileID: str

    @property
    def human_readable_size(self):
        size = self.fileSize
        """Converts a number of bytes to a human-readable format."""
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        if size == 0:
            return '0 B'
        i = 0
        while size >= 1024 and i < len(units) - 1:
            size /= 1024
            i += 1
        return f"{size:.2f} {units[i]}"

    @property
    def gdrivelink(self):
        return f"https://drive.google.com/uc?export=download&id={self.fileID}"