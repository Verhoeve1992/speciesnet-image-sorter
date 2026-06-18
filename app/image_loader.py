import os
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtGui import QIcon, QPixmap
from .thumbnail_creator import create_thumbnail
from .video_utils import VIDEO_EXTENSIONS as VIDEO_EXTS
from PyQt6.QtCore import Qt, QSize

def load_image(file_path, image_label):
    """Load and display the image in the label."""
    image = QPixmap(file_path)
    scaled_image = image.scaled(
        image_label.size(),
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation
    )
    image_label.setPixmap(scaled_image)

def load_folder_images(folder_path, file_list):
    """Load all image and video files from the specified folder."""
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    file_list.clear()
    
    # Combine image and video extensions
    all_extensions = image_extensions + VIDEO_EXTS
    
    media_files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if os.path.splitext(f)[1].lower() in all_extensions
    ]
    media_files.sort()
    
    for media_path in media_files:
        item = QListWidgetItem()
        # Try to create thumbnail, use file icon for videos if thumbnail fails
        try:
            icon = QIcon(create_thumbnail(media_path))
        except Exception:
            # For videos, we'll use a generic icon since thumbnail_creator may not support video
            icon = QIcon()
        
        item.setIcon(icon)
        basename = os.path.basename(media_path)
        # Add [VIDEO] marker for video files
        if os.path.splitext(media_path)[1].lower() in VIDEO_EXTS:
            item.setText(f"[VIDEO] {basename}")
        else:
            item.setText(basename)
        item.setData(Qt.ItemDataRole.UserRole, media_path)
        file_list.addItem(item)
    
    return media_files