import os
import cv2
import torch
from PIL import Image
from typing import List, Dict
from transformers import OwlViTProcessor, OwlViTForObjectDetection

# Load model
processor = OwlViTProcessor.from_pretrained("google/owlvit-base-patch32")
model = OwlViTForObjectDetection.from_pretrained("google/owlvit-base-patch32")

def track(video_path: str, texts: List[str]) -> Dict:
    if not os.path.exists(video_path):
        return {"type": "error", "error": "Video file not found!"}

    video_cap = cv2.VideoCapture(video_path)
    if not video_cap.isOpened():
        return {"type": "error", "error": "Failed to open video!"}

    width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 640)
    height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 480)
    fps = video_cap.get(cv2.CAP_PROP_FPS) or 30.0  # Set default FPS if 0.0

    output_dir = "output/tracking_videos"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{os.path.basename(video_path).split('.')[0]}_tracked.mp4")

    # Use H264 or XVID codec if 'mp4v' fails
    fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Try 'H264' if XVID doesn't work
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    if not out.isOpened():
        video_cap.release()
        return {"type": "error", "error": "Failed to initialize video writer!"}

    frame_count = 0
    while True:
        ret, frame = video_cap.read()
        if not ret:
            break
        
        # Convert frame to PIL Image
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Process frame with OwlViT
        inputs = processor(text=texts, images=pil_image, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)

        # Post-process detections
        target_sizes = torch.Tensor([pil_image.size[::-1]])
        results = processor.post_process_object_detection(outputs=outputs, threshold=0.1, target_sizes=target_sizes)

        # Draw bounding boxes
        for result in results:
            for box, score, label in zip(result["boxes"], result["scores"], result["labels"]):
                box = [int(coord) for coord in box.tolist()]
                score = round(score.item(), 3)
                label_text = texts[label.item()]

                # Draw on frame
                cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
                cv2.putText(frame, f"{label_text} {score}", (box[0], box[1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Write frame
        out.write(frame)
        frame_count += 1
        print(f"Frame: {frame_count}")

    # Cleanup
    video_cap.release()
    out.release()

    if frame_count == 0:
        return {"type": "error", "message": "No frames processed!"}
    elif not os.path.exists(output_path):
        return {"type": "error", "message": "Output file not created!"}

    return {"type": "success", "path": output_path}

if __name__ == "__main__":
    print(track(r"C:/Users/mubee/Downloads/ball.mp4", ["football"]))
