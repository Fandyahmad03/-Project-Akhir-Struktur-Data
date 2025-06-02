import hashlib
import time
import uuid

class User:
    def __init__(self, username, email):
        self.user_id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.reported_contents = []

    def report_content(self, content_id):
        self.reported_contents.append((content_id, time.time()))

    def get_reports(self):
        return self.reported_contents
    
class User:
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email


class Content:
    def __init__(self, uploader: User, filename: str, metadata: dict):
        self.content_id = str(uuid.uuid4())
        self.uploader = uploader
        self.filename = filename
        self.metadata = metadata
        self.timestamp = time.time()
        self.checksum = self.generate_checksum(filename)
        self.is_fake = False
        self.flag_score = 0
        self.history = []

    def generate_checksum(self, filename):
        return hashlib.sha256(filename.encode()).hexdigest()

    def flag(self, score=1):
        self.flag_score += score
        self.history.append((time.time(), f"Flagged with score {score}"))
        if self.flag_score >= 5:
            self.is_fake = True

    def get_summary(self):
        return {
            "content_id": self.content_id,
            "uploader": self.uploader.username,
            "filename": self.filename,
            "checksum": self.checksum,
            "is_fake": self.is_fake,
            "flag_score": self.flag_score,
            "history": self.history,
        }

if __name__ == "__main__":
    user = User("testuser", "test@example.com")
    print("User:", user.username, user.email)
    content = Content(uploader=user, filename="contoh.jpg", metadata={"type": "image"})
    print("Content summary:", content.get_summary())

# ...existing code...

if __name__ == "__main__":
    # Objek user pertama
    user1 = User("testuser", "test@example.com")
    print("User 1:", user1.username, user1.email)

    # Objek user kedua
    user2 = User("anotheruser", "another@example.com")
    print("User 2:", user2.username, user2.email)

    # Objek content pertama
    content1 = Content(uploader=user1, filename="contoh.jpg", metadata={"type": "image"})
    print("Content 1 summary:", content1.get_summary())

    # Objek content kedua
    content2 = Content(uploader=user2, filename="video.mp4", metadata={"type": "video", "duration": 120})
    print("Content 2 summary:", content2.get_summary())

    # Contoh user1 melaporkan content2
    user1.report_content(content2.content_id)
    print("User 1 reports:", user1.get_reports())