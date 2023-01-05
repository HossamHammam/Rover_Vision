import numpy as np
import math


def deg2rad(phi):
    # Convert angle in degrees to radians
    return np.pi * phi / 180

def rad2deg(phi):
    # Convert angle in radians to degrees
    return 180 * phi / np.pi

def normalize_angle_deg(phi):
    # Normalize angle to range (-180, 180)
    phi_rad = deg2rad(phi)
    return rad2deg(np.arctan2(np.sin(phi_rad), np.cos(phi_rad)))

def distance(p1, p2):
    # Calculate Euclidean distance between two points
    return np.linalg.norm(np.array(p1) - np.array(p2))


def heading_to_pos_deg(p1, p2):
    # Calculate heading from p1 to p2 in degrees
    diff = np.array(p2) - np.array(p1)
    return rad2deg(math.atan2(diff[1], diff[0]))


def is_overhanging_rock_ahead(Rover):
    h,w = Rover.img.shape[0:2]
    black_rock_mask = cv2.inRange(Rover.img, (0,0,0), (8,8,8))
    x_margin = 3*w//8
    x1,x2 = x_margin, w - x_margin

    black_rock_idx_y, black_rock_idx_x = black_rock_mask[:,x1:x2].nonzero()
    if black_rock_idx_y.size == 0:
        return False

    return np.min(black_rock_idx_y) < 4 and np.max(black_rock_idx_y) > h * 0.575



def is_obstacle_ahead(Rover, range=20, bearing=0):
    idx_in_front = np.where((np.abs(Rover.obs_angles - bearing) < deg2rad(15)) & (Rover.obs_dists < range))[0]

    if len(idx_in_front) < 5:
        print("Mindist: N/A")
        return False
    else:
        min_dist = np.min(Rover.obs_dists[idx_in_front])
        print("Mindist: %.2f" % min_dist)
        return True


def distance_to_obstacle(Rover, bearing=0):
    idx_in_front = np.where((np.abs(Rover.obs_angles - bearing) < deg2rad(15)))[0]

    if len(idx_in_front) < 5:
        return 1000
    else:
        return np.min(Rover.obs_dists[idx_in_front])



def is_rock_ahead(Rover):
    idx_in_front = np.where(np.abs(Rover.rock_angles) < deg2rad(2.5))[0]
    return len(idx_in_front)


def is_rock_near(Rover):
    return Rover.rock_angles.size > 0


def bearing_to_rock(Rover):
    return np.mean(Rover.rock_angles)


def bearing_to_rock_deg(Rover):
    return rad2deg(bearing_to_rock(Rover))



def distance_to_rock(Rover):
    if len(Rover.rock_dists):
        return np.min(Rover.rock_dists)
    else:
        return 1e9



def obstacle_bearing(Rover, direction, min_dist=0, max_dist=30):
    if direction > 0:
        idx_obs_near = np.where((Rover.obs_dists < max_dist) & (Rover.obs_dists > min_dist) & (Rover.obs_angles > 0))[0]
    else:
        idx_obs_near = np.where((Rover.obs_dists < max_dist) & (Rover.obs_dists > min_dist) & (Rover.obs_angles < 0))[0]

    if not idx_obs_near.size:
        return 90 * np.sign(direction)
    else:
        return rad2deg(np.min(Rover.obs_angles[idx_obs_near]))

