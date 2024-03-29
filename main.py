import cv2
import json
import trt_pose.coco
import torch
import time
import numpy as np
import pyrealsense2 as rs
from torch2trt import TRTModule
from trt_pose.draw_objects import DrawObjects
from trt_pose.parse_objects import ParseObjects
from rover.controls import *
from pose_detection.pose_detection import *

OPTIMIZED_MODEL = 'pose_detection/resnet18_baseline_att_224x224_A_epoch_249_trt.pth'
HUMAN = 'pose_detection/human_pose.json'
WIDTH = 640
HEIGHT = 480
BRAKE_DISTANCE = 1269

def preprocess(image):
    mean = torch.Tensor([0.485, 0.456, 0.406]).to(device).view(1, 3, 1, 1)
    std = torch.Tensor([0.229, 0.224, 0.225]).to(device).view(1, 3, 1, 1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (224, 224))
    image = torch.from_numpy(image).permute(2, 0, 1).unsqueeze(0).float().to(device)
    image = image.div(255.0)
    image = (image - mean) / std
    return image

# Load model and topology
with open(HUMAN, 'r') as f:
    human_pose = json.load(f)
topology = trt_pose.coco.coco_category_to_topology(human_pose)

# Instantiate TensorRT
model_trt = TRTModule()
model_trt.load_state_dict(torch.load(OPTIMIZED_MODEL))

# Doing stuff (tbd)
parse_objects = ParseObjects(topology)
draw_objects = DrawObjects(topology)
device = torch.device('cuda')

rover = Controls()

# Initialize RealSense camera
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, WIDTH, HEIGHT, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
pipeline.start(config)

body = Body()
speed = 0
pose_change = False

prev_pose = "No Pose"
center = [WIDTH/2, HEIGHT/2]
current_angle = 90
started = False

prev_frame_time = time.time()

try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        # Convert depth frame to numpy array
        depth_image = np.asanyarray(depth_frame.get_data())

        if not color_frame or not depth_frame:
            continue

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())

        # Process the image for pose estimation
        data = preprocess(color_image)
        cmap, paf = model_trt(data)
        cmap, paf = cmap.detach().cpu(), paf.detach().cpu()
        counts, objects, peaks = parse_objects(cmap, paf)
        
        # Classify the pose and display it
        pose_classification, chest_in_frame = classify_pose(peaks, counts, objects, topology, body)
        cv2.putText(color_image, pose_classification, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        if pose_classification == "T-Pose":
            started = True
            speed = 1
            rover.forward(speed)
        elif pose_classification == "S-Pose":
            started = False
            rover.brake()
        
        if started == True:
            # Access depth data (in millimeters)
            depth_value_at_pixel = depth_image[int(body.chest[1]), int(body.chest[0])]
            print(f"Depth value at {body.chest[0]}, {body.chest[1]} pixel: {depth_value_at_pixel}")

            if depth_value_at_pixel < BRAKE_DISTANCE:
                rover.brake()
                speed = 1
            else:
                if chest_in_frame:
                    rover.forward(speed)

                x_diff = body.chest[0] - center[0]
                x_diff = (0.28125 * x_diff) + 90
                current_angle = x_diff
                print(current_angle)
                rover.turn(current_angle)
            
                prev_chest = body.chest

        
        # Draw poses and display them
        draw_keypoints_and_values(color_image, counts, objects, peaks, topology)

        # Calculate FPS and display it
        current_frame_time = time.time()
        fps = (1 / (current_frame_time - prev_frame_time))
        prev_frame_time = current_frame_time
        fps_text = f'FPS: {fps:.0f}'
        cv2.putText(color_image, fps_text, (color_image.shape[1] - 150, color_image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Display the image
        cv2.imshow('Pose Estimation', color_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    
    rover.brake()
    pipeline.stop()
    cv2.destroyAllWindows()





