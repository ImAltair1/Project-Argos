from uuid import uuid4

# Starting off small first
class GameCopy:
    def __init__(self, platform, format, ownership_type, 
                copy_id=None):

        self.id = copy_id if copy_id is not None else str(uuid4())
        self.platform = platform
        self.format = format
        self.ownership_type = ownership_type

    def __str__(self):
        return f"{self.platform} ({self.format})"

    def __repr__(self):
        return (
            f"GameCopy("
            f"id='{self.id}'"
            f"platform='{self.platform}', "
            f"format='{self.format}', "
            f"ownership_type='{self.ownership_type}'"
            f")"
            )




