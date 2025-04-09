# from deepface import DeepFace
# import cv2

# # Load your face database (store images of 50 persons in a folder)
# face_db_path = "images"  # Folder with images of 50 people (like "name1.jpg", "name2.jpg")

# # Initialize webcam
# cap = cv2.VideoCapture(0)

# print("Starting Face Recognition...")

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     try:
#         result = DeepFace.find(
#             img_path=frame,
#             db_path=face_db_path,
#             model_name='ArcFace',
#             detector_backend='opencv',
#             enforce_detection=False
#         )

#         if len(result[0]) > 0:
#             identity = result[0].iloc[0]['identity']
#             print(f"Matched with: {identity}")
#             cv2.putText(frame, f"Matched: {identity.split('/')[-1]}", (50, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
#         else:
#             cv2.putText(frame, "Unknown Face", (50, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

#     except Exception as e:
#         print("Face not found")

#     cv2.imshow("Face Recognition", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


from flask import Flask, render_template, request, jsonify
from deepface import DeepFace
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename
# import os
import csv
from datetime import datetime
from your_email_script import send_attendance_email
app = Flask(__name__)

# Configuration
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

face_db_path = "images"  # Folder with images of 50 people
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ATTENDANCE_FOLDER = 'attendance'
# TEACHER_EMAIL = "yogeshsoni233005@gmail.com"
TEACHER_EMAIL ="poojaraj8310@gmail.com"



# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    if 'frame' not in request.files:
        return jsonify({'error': 'No frame part'}), 400

    file = request.files['frame']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Read the image
    frame = cv2.imread(file_path)


    try:
        # Perform face recognition
        result = DeepFace.find(
            img_path=frame,
            db_path=face_db_path,
            model_name='ArcFace',
            detector_backend='opencv',
            enforce_detection=False
        )

        if len(result[0]) > 0:
            identity = result[0].iloc[0]['identity']
            response = {'status': 'success', 'message': f"Matched: {identity.split('/')[-1]}"}
            # Log the match to a CSV file
            name = {identity.split('/')[-1]}  # the name from face recognition
            today = datetime.now().strftime("%Y-%m-%d")
            time_now = datetime.now().strftime("%H:%M:%S")
            filename = f"attendance_{today}.csv"
            filepath = os.path.join("attendance", filename)

            # create folder if not exists
            os.makedirs("attendance", exist_ok=True)

            # check if file exists
            file_exists = os.path.isfile(filepath)

            # create file with header if new
            if not file_exists:
                with open(filepath, mode='w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Name", "Time"])

            # check if name already marked
            with open(filepath, mode='r') as f:
                existing_names = [row[0] for row in csv.reader(f)][1:]  # skip header

            if name not in existing_names:
                with open(filepath, mode='a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([name, time_now])

        else:
            response = {'status': 'success', 'message': "Unknown Face"}

    except Exception as e:
        response = {'status': 'error', 'message': str(e)}

    # Clean up
    if os.path.exists(file_path):
        os.remove(file_path)

    return jsonify(response)
@app.route('/send_email', methods=['POST'])
def send_email():
    today = datetime.now().strftime("%Y-%m-%d")
    attendance_file = os.path.join(ATTENDANCE_FOLDER, f"attendance_{today}.csv")

    if os.path.exists(attendance_file):
        send_attendance_email(TEACHER_EMAIL, attendance_file)
        return jsonify({'message': 'Attendance Email Sent!'})
    else:
        return jsonify({'message': 'Attendance file not found!'})
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)