import cv2
import os


# The path to the cocks
images_folder = "data/mainnet"
video_name = "ad.avi"

# Load the images
images = [img for img in os.listdir(images_folder) if img.endswith(".png")]
frame = cv2.imread(os.path.join(images_folder, images[0]))
height, width, layers = frame.shape

# The video object
video = cv2.VideoWriter(video_name, 0, 1, (width, height))

# Load the images into the video
for image in images:
    video.write(cv2.imread(os.path.join(images_folder, image)))

# Release the video
cv2.destroyAllWindows()
video.release()