import os
import cv2
import torch
import numpy as np
from PIL import Image
from typing import List, Dict
from transformers import CLIPSegProcessor, CLIPSegForImageSegmentation

# Load model
processor = CLIPSegProcessor.from_pretrained("CIDAS/clipseg-rd64-refined")
model = CLIPSegForImageSegmentation.from_pretrained("CIDAS/clipseg-rd64-refined")

def segment(video_path: str, texts: List[str]) -> Dict:
    if not os.path.exists(video_path):
        return {"type": "error", "error": "Video file not found!"}

    video_cap = cv2.VideoCapture(video_path)
    if not video_cap.isOpened():
        return {"type": "error", "error": "Failed to open video!"}

    width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
    height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480)
    fps = video_cap.get(cv2.CAP_PROP_FPS) or 30.0

    output_dir = "output\\segmentation_videos"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{os.path.basename(video_path).split('.')[0]}_segmented.mp4")

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    if not out.isOpened():
        video_cap.release()
        return {"type": "error", "error": "Failed to initialize video writer!"}

    frame_count = 0
    while True:
        ret, frame = video_cap.read()
        if not ret:
            break
        
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        original_size = pil_image.size

        # Process frame with CLIPSeg
        inputs = processor(text=texts, images=[pil_image] * len(texts), padding="max_length", return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)

        preds = outputs.logits
        segmentation_map = np.zeros_like(frame)

        # Apply segmentation masks
        for mask in preds:
            mask_np = torch.sigmoid(mask).squeeze().cpu().numpy()
            resized_mask = cv2.resize(mask_np, original_size)
            binary_mask = resized_mask > 0.30
            segmentation_map[binary_mask] = frame[binary_mask]

        out.write(segmentation_map)
        frame_count += 1
        print(f"Frame: {frame_count}")

    video_cap.release()
    out.release()

    if frame_count == 0:
        return {"type": "error", "message": "No frames processed!"}
    elif not os.path.exists(output_path):
        return {"type": "error", "message": "Output file not created!"}

    return {"type": "success", "path": output_path}

if __name__ == "__main__":
    print(segment_video(r"C:/Users/mubee/Downloads/ball.mp4", ["person"]))
