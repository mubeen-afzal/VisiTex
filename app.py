import os
import re

import gradio as gr
from models.tracking import track  # Ensure this import is correct
from models.segementation import segment

def clean_spaces(s: str) -> str:
    return re.sub(r'\s+', ' ', s).strip()

def process_video(video_file, mode, object_classes):
    # Validate video file
    if not video_file or not os.path.exists(video_file):
        return "Invalid or missing video file.", None

    # Validate object classes
    if not object_classes:
        return "Object classes are required for tracking!", None
    
    # Clean object classes
    object_classes = [clean_spaces(class_) for class_ in object_classes.split(",")]
    print("Object Classes:", object_classes)

    # return None, r"C:\Users\mubee\Downloads\Custom OBJ Tracker\output\tracking_videos\ball_tracked_fixed.mp4"

    # Call the track function
    try:
        result = track(video_file, object_classes) if mode == "Track" else segment(video_file, object_classes)
    except Exception as e:
        return f"Processing failed due to an error: {str(e)}", None

    # Handle the result from the track function
    if result and result.get("type") == "success":
        # Check if the video file exists at the returned path
        output_video_path = result["path"]
        if os.path.exists(output_video_path):
            print("Processed video saved at:", output_video_path)
            return None, output_video_path  # Return None for message and the video path
        else:
            return "Error: Processed video file not found at the expected path.", None
    elif result and result.get("type") == "error":
        return f"Error: {result.get('error', 'Unknown error occurred')}", None
    else:
        return "Processing failed. No result returned from the tracking function.", None


demo = gr.Interface(
    fn=process_video,
    inputs=[
        gr.Video(label="Upload Video"),
        gr.Radio(["Track", "Segment"], label="Choose Mode", value="Track"),
        gr.Textbox(label="Enter Object Classes (comma-separated)", placeholder="e.g., ball, car, person"),
    ],
    outputs=[
        gr.Textbox(label="Message"),
        gr.Video(label="Processed Video Result", autoplay=True)
    ],
    title="Object Tracking & Segmentation App",
    description="Upload a video, select tracking or segmentation, and enter object classes to process the video.",
    allow_flagging="never"
)

demo.launch()
