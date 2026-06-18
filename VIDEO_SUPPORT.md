# SpeciesNet Video Support Feature

## Overview
Added comprehensive video support to the SpeciesNet image sorter application. Users can now process video files directly - the application automatically extracts frames from videos and runs SpeciesNet analysis on those frames.

## What's New

### 1. New Module: `app/video_utils.py`
A dedicated utility module for handling video processing:

- **`get_video_files(folder_path)`**: Finds all video files in a folder
- **`extract_frames(video_path, output_folder, frame_interval, max_frames)`**: Extracts frames from a single video
  - Extracts every Nth frame (default: 30, which is ~1 frame/second at 30fps)
  - Saves frames as JPG files in a `{video_name}_frames` folder
  - Returns detailed metadata about extraction
- **`extract_frames_batch(video_files, ...)`**: Process multiple videos

**Supported Video Formats**:
- `.mp4`, `.avi`, `.mov`, `.mkv`, `.flv`, `.wmv`, `.webm`

### 2. Enhanced: `app/image_loader.py`
Updated to load both images and videos:

- Now detects video files in addition to image files
- Video files are marked with `[VIDEO]` prefix in the file list
- Gracefully handles video files that may not have thumbnail previews

### 3. Enhanced: `app/speciesnet_buttonwidget.py`
Updated SpeciesNet widget with video processing capabilities:

- **`extract_video_frames(folder)`**: Automatically detects and extracts frames from videos in the target folder
- Combines extracted video frames with regular images for SpeciesNet processing
- Provides detailed logging of video processing steps
- Supports mixed workflows (images + videos in the same folder)

### 4. Updated: `pyproject.toml`
Added `opencv-python>=4.8.0` as a dependency for video frame extraction.

## How to Use

### Basic Workflow
1. Place your video files (`.mp4`, `.avi`, etc.) in a folder alongside or without images
2. Open the folder in the application
3. Click the **"SpeciesNet"** button
4. The application will:
   - Detect any video files
   - Extract frames automatically (one frame per second by default)
   - Run SpeciesNet on all frames
   - Save results in `predictions.json`

### Example Directory Structure
```
my_wildlife_videos/
├── animal_clip1.mp4          # Video file
├── animal_clip2.avi          # Video file
├── photo1.jpg                # Regular image
├── animal_clip1_frames/       # Auto-generated
│   ├── animal_clip1_frame_000000.jpg
│   ├── animal_clip1_frame_000001.jpg
│   └── ...
├── animal_clip2_frames/       # Auto-generated
│   ├── animal_clip2_frame_000000.jpg
│   └── ...
└── predictions.json          # SpeciesNet results (after running)
```

## Technical Details

### Frame Extraction Configuration
The default settings extract 1 frame per second (assuming 30fps video):
- **frame_interval**: 30 (every 30th frame)
- **max_frames**: None (all frames extracted)

To customize, modify in `speciesnet_buttonwidget.py`:
```python
result = extract_frames(video_file, frame_interval=30)
```

### Frame Naming Convention
Extracted frames follow this pattern:
```
{video_name}_frame_{frame_number:06d}.jpg
```
Example: `wildlife_clip_frame_000042.jpg`

### Results Organization
- All frames are processed by SpeciesNet
- Results are stored in a single `predictions.json` file per folder
- Frame source (which video, which frame number) is encoded in the filename
- Easy to trace predictions back to source video and frame

## Dependencies
- **opencv-python**: For video decoding and frame extraction
- All other dependencies unchanged (speciesnet, PyQt6, numpy, etc.)

## Logging
Video processing includes detailed logging:
- Video detection and file count
- Frame extraction progress and statistics
- Frame count and extraction details
- Errors and warnings

Check the application logs window or console for detailed information about video processing.

## Performance Considerations
- **Frame extraction**: Depends on video codec and resolution
  - Typically fast (seconds to minutes for typical wildlife videos)
- **SpeciesNet processing**: Same as image processing
  - Add time based on number of extracted frames
- **Storage**: Default 1 fps extraction = ~1-2 images per second of video

### Optimization Tips
1. Adjust `frame_interval` to extract fewer frames if needed:
   - `frame_interval=60` → 1 frame per 2 seconds
   - `frame_interval=15` → 2 frames per second

2. Use `max_frames` to limit processing for testing:
   - `max_frames=100` → extract only first 100 frames

## Error Handling
- Invalid video files are skipped with warnings logged
- Missing codecs are handled gracefully (opencv fallback)
- Mixed video/image folders work seamlessly
- UI remains responsive during extraction (runs in worker thread)

## Future Enhancements
Possible future improvements:
- GUI controls for frame extraction settings
- Progress bar for video processing
- Adaptive frame selection (extract keyframes only)
- Batch video processing with progress tracking
- GPU acceleration for frame extraction
