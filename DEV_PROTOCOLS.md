import face_recognition
import pickle
import os

def encrypt_identity(image_path, output_filename="identity.dat"):
    # 1. Load the image
    image = face_recognition.load_image_file(image_path)
    
    # 2. Generate the math (Vector)
    # This creates a list of 128 numbers that represent the face
    encoding = face_recognition.face_encodings(image)[0]
    
    # 3. Save to a binary file (Not an image)
    with open(output_filename, 'wb') as f:
        pickle.dump(encoding, f)
        
    # 4. Scorched Earth: Delete the photo
    os.remove(image_path)
    print(f"Identity encrypted to {output_filename}. Source image destroyed.")

# Usage:
# encrypt_identity("joel_setup.jpg")
from scipy.spatial import distance

def calculate_ear(eye_points):
    # Vertical distances
    A = distance.euclidean(eye_points[1], eye_points[5])
    B = distance.euclidean(eye_points[2], eye_points[4])
    # Horizontal distance
    C = distance.euclidean(eye_points[0], eye_points[3])
    
    # The Ratio
    ear = (A + B) / (2.0 * C)
    return ear

# IN YOUR MAIN LOOP:
# 1. If EAR < 0.25 (User is blinking):
#    blink_counter += 1
# 2. If blink_counter >= 3 (A deliberate blink):
#    liveness_confirmed = True
def check_duress(landmarks):
    # Example: Check if hand is covering mouth
    # If the system can find eyes but fails to find mouth landmarks
    if eyes_detected and not mouth_detected:
        return True # DURESS TRIGGERED
    return False

# IN MAIN LOOP:
if match_found:
    if check_duress(landmarks):
        print("!!! DURESS DETECTED !!!")
        execute_silent_alarm() # Send Discord webhook, lock PC, etc.
    else:
        grant_access()
