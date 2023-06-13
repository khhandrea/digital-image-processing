import cv2
import numpy as np

def delete_background(self, frames):
    avg = np.zeros_like(frames[0], dtype='uint64')
    i=0
    for frame in frames:
        i+=1
        avg += frame
    avg = np.array(avg / i, dtype='uint8') 
    for j, frame in enumerate(frames):
        frames[j] =  frame - avg
    return frames

def thresholding(self, frames, thres_min, thres_max):
    for i, frame in enumerate(frames):
        _, frames[i] = cv2.threshold(frame, thres_min, 255, cv2.THRESH_TOZERO)
        _, frames[i] = cv2.threshold(frame, thres_max, 0, cv2.THRESH_TOZERO_INV)
    return frames

def connect_components(self, frames, original_frames, area_min):
    for k, frame in enumerate(frames):
        cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(frame[:,:,2])
        for i in range(1, cnt):
            (x, y, w, h, area) = stats[i]
            if area < area_min:
                continue
            cv2.rectangle(original_frames[k], (x, y), (x+w, y+h), (0,0,255), 2)
    return original_frames

def hand_detection(self, frames):
    hsv_frames = self.frames_rgb_to_hsv(frames)
    back_deleted_frames = self.delete_background(hsv_frames[:,:,:,2].copy())
    hsv_frames[:,:,:,2] = self.thresholding(back_deleted_frames, 100, 240)
    
    hsv_frames = self.frames_hsv_to_rgb(hsv_frames)
    connected_frames = self.connect_components(hsv_frames, frames, 3000)

    return connected_frames

def vehicle_detection(self, frames):
    hsv_frames = self.frames_rgb_to_hsv(frames)
    back_deleted_frames = self.delete_background(hsv_frames[:,:,:,2].copy())
    hsv_frames[:,:,:,2] = self.thresholding(back_deleted_frames, 30, 230)
    
    hsv_frames = self.frames_hsv_to_rgb(hsv_frames)
    connected_frames = self.connect_components(hsv_frames, frames, 120)

    return connected_frames