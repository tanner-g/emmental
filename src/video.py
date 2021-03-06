"""Contains functionality for handling video uploads."""

import os
import uuid
from .db import delete_video_db, get_video_list_db, get_user_id_from_video, save_video_db
from .user import get_user_id

class Video():
    """Video object containing ID, extension, and uploader."""

    def __init__(self):
        self.video_id = ''
        self.extension = ''
        self.user_id = ''

    def create(self, filename, username):
        """Create a new video."""
        self.video_id = str(uuid.uuid4())
        self.extension = get_extension(filename)
        self.user_id = str(get_user_id(username))

    def load(self, video_id, extension, user_id):
        """Load an existing video."""
        self.video_id = str(video_id)
        self.extension = extension
        self.user_id = str(user_id)

    def get_path(self, directory):
        """Adds filename to the given directory."""
        return os.path.join(directory, f'{self.video_id}.{self.extension}')

    def save(self):
        """Saves the video reference to the database."""
        video_id = uuid.UUID(self.video_id).bytes
        user_id = uuid.UUID(self.user_id).bytes
        return save_video_db(video_id, self.extension, user_id)

    def delete(self):
        """Deletes the video reference from the database."""
        video_id = uuid.UUID(self.video_id).bytes
        return delete_video_db(video_id)


def is_valid_filename(filename):
    """Determines if a filename is valid (with extension)."""
    valid_extensions = ['mp4', 'webm', 'ogg']
    extension = get_extension(filename)
    return bool(extension and extension in valid_extensions)


def get_extension(filename):
    """Strips the filename before an extension."""
    return (filename[filename.rfind('.') + 1:].lower()
            if '.' in filename else '')


def get_video_list():
    """Returns a list of all videos."""
    videos = []
    videos_db = get_video_list_db()
    for video_db in videos_db:
        video = Video()
        video_id = uuid.UUID(bytes=bytes(video_db[0]))
        extension = video_db[1]
        user_id = uuid.UUID(bytes=bytes(video_db[2]))
        video.load(video_id, extension, user_id)
        videos.append(video)
    return videos

def get_user_id_from_video_id(video_id):
    """ Get user_id (creator) from a video_id (video) """
    if video_id:
        return uuid.UUID(bytes=get_user_id_from_video(uuid.UUID(video_id).bytes))
    # If no video_id supplied, return empty string.
    return ""

def delete_select_video(selected_videopath):
    """ Delete a video based on the video_id"""
    # Requirement: Should only be run after checking that requester is owner of video.
    if selected_videopath:
        spliter = selected_videopath.split(".")
        select_video_id = spliter[0]
        # Deletes video entry in DB
        delete_video_db(uuid.UUID(select_video_id).bytes)
        # Deletes video from disk
        try:
            os.remove('/srv/videos/'+selected_videopath)
        except OSError:
            pass
