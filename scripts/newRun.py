import serial
import time
import csv
import pandas as pd
import numpy as np
import joblib
import warnings
import subprocess
from scipy.signal import find_peaks

# Suppress specific UserWarnings related to feature names
warnings.filterwarnings("ignore", category=UserWarning, message=".*does not have valid feature names.*")

# Set up the serial connection (replace 'COM_PORT' with your ESP32 port)
esp32_port = 'COM9'  # Change this to your ESP32 port
baud_rate = 115200
ser = serial.Serial(esp32_port, baud_rate, timeout=1)

time.sleep(1)  # Wait for the connection to establish
print("All connections established")

# Function to collect sensor data and store it in the buffer
def collect_data(count=20):
    i = 1
    while i <= count :
        with open('C:/Users/Khush/Desktop/Masters_Academics/First_Semester/Mobile_Assignments/JawSense/khushi_data/{}.csv'.format(i), 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(["Accel_X", "Accel_Y", "Accel_Z", "Gyro_X", "Gyro_Y", "Gyro_Z"])  # Write header
            # Start recording
            if not ser.is_open:
                ser.open()
            ser.write(b'START\n')
            print("Perform gesture: ", i)
            time.sleep(0.1)
            start_time = time.time()
            while time.time() - start_time < 4:
                if ser.in_waiting > 0:
                    data = ser.readline().decode('utf-8').strip()  # Read data from ESP32
                    data = data.split(": ")[-1]
                    # Split the data string into separate values
                    values = data.split(',')
                    if len(values) == 6:  # Ensure we have the right number of values
                        csv_writer.writerow(values)  # Write to file
        
        ser.close()
        features = combine_data('C:/Users/Khush/Desktop/Masters_Academics/First_Semester/Mobile_Assignments/JawSense/khushi_data/{}.csv'.format(i))
        gesture = predict_word(features)
        print("Gesture performed is", gesture)
        perform_gesture(gesture)
        i = i + 1
        time.sleep(1)
    
def extract_features(df):
    features = {}
    for col in ['Accel_X', 'Accel_Y', 'Accel_Z', 
                 'Gyro_X', 'Gyro_Y', 'Gyro_Z']:
        # Time-domain features
        features[f"{col}_mean"] = df[col].mean()
        features[f'{col}_std'] = df[col].std()
        # features[f"{col}_min"] = df[col].min()
        # features[f"{col}_max"] = df[col].max()
        features[f"{col}_median"] = df[col].median()
    accel_mag = np.sqrt(df['Accel_X']**2 + df['Accel_Y']**2 + df['Accel_Z']**2)
    
    # Syllable Count Estimation
    features['syllable_count'] = estimate_syllables(accel_mag)

    # print(features['syllable_count'])
    return features


def estimate_syllables(signal):
    threshold = signal.mean() + 1 * signal.std()  
    peaks, _ = find_peaks(signal, height=threshold, distance=60)  # Minimum distance between peaks
    return len(peaks)


def combine_data(filepath):

    try:
        with open(filepath, 'r') as file:
            # Process the file (example: reading the content)
            data = pd.read_csv(file)
    
            # Extract features
            features = extract_features(data)

            return features

    except FileNotFoundError:
        print("The file was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

# Define function with "undetected" category for low confidence

def predict_word(input_row):
    # # Load the trained model
    model = joblib.load('../khushi_final_models/word.pkl')
    # Load the classes 
    classes = np.load('../khushi_final_models/label_encoder.npy', allow_pickle=True)

    input_row_array = np.array([list(input_row.values())])
    
    # Make prediction and calculate probabilities
    probabilities = model.predict_proba(input_row_array)
    max_prob = np.max(probabilities)

    # Determine the output based on confidence
    if max_prob < 0.2:
        return "undetected"
    else:
        predicted_label = classes[np.argmax(probabilities)]
        return predicted_label


def perform_gesture(gesture):
    if gesture == "CallManavUMass":
        dial_number()
    elif gesture == 'end':
        end_call()
    elif gesture == "PickUpCall":
        accept_call()
    elif gesture == "unlock":
        unlock_device_and_type_password()
    else:
        print("undetected gesture")

def adb_command(command):
    """Function to run an ADB command."""
    result = subprocess.run(["adb", "shell"] + command.split(), capture_output=True, text=True)
    return result.stdout.strip()

def accept_call():
    """Simulate pressing the 'Call' button to accept an incoming call."""
    print("Accepting the call...")
    time.sleep(5)
    adb_command("input keyevent KEYCODE_CALL")
    time.sleep(5)

def dial_number(phone_number = "+14134721185"):
    """Dials the specified phone number using the Android dialer."""
    print(f"Dialing {phone_number}...")
    adb_command(f"am start -a android.intent.action.CALL -d tel:{phone_number}")
    time.sleep(5)

def end_call():
    """Simulate pressing the 'End Call' button to terminate an active call."""
    print("Ending the call...")
    adb_command("input keyevent KEYCODE_ENDCALL")
    time.sleep(5)

def unlock_device_and_type_password(password = "lalywrav"):
    """Unlock device and type password."""
    print("Unlocking device...")
    # Turn on the screen if it's off
    adb_command("input keyevent KEYCODE_WAKEUP")

    # Wait a moment for the device to wake up
    time.sleep(1)

    # Simulate swipe-up to open the password screen
    adb_command("input swipe 500 1500 500 500")  # Swipe from bottom to top (coordinates may vary)
    
    # Simulate typing the password (if the screen is unlocked)
    adb_command(f"input text {password}")

    # Simulate pressing the Enter key (KEYCODE_ENTER)
    adb_command("input keyevent KEYCODE_ENTER")
    time.sleep(5)

collect_data()
