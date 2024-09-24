from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
from io import BytesIO
from PIL import Image
import cv2
import numpy as np

app = FastAPI()

# Dummy GAN function that processes the image and returns a video
def gan_model_process(image: Image.Image):
    # Here, you would use your trained GAN to process the image
    # Currently, we'll simulate by converting the image to a video

    # Convert the PIL Image to a format compatible with OpenCV (for video generation)
    image_np = np.array(image)

    # Create a VideoWriter object
    height, width, layers = image_np.shape
    video_path = "output_video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Video codec for mp4
    video = cv2.VideoWriter(video_path, fourcc, 1.0, (width, height))

    # Simulate a video with the same image repeated for 10 frames
    for _ in range(10):
        video.write(image_np)

    video.release()  # Finalize the video file
    return video_path

@app.get("/")
def helloWorld():
    return{'Hello':'World'}

# API endpoint to receive the image and process it
@app.post("/process-image/")
async def process_image(file: UploadFile = File(...)):
    # Read the uploaded image file
    image = Image.open(BytesIO(await file.read()))

    # Pass the image to your GAN processing function
    video_path = gan_model_process(image)

    # Return the video file as response
    return FileResponse(video_path, media_type="video/mp4", filename="output_video.mp4")

# To run the server:
# uvicorn filename:app --reload
