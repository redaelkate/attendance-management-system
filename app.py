from flask import Flask,render_template,request, jsonify, session
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from datetime import date
import sqlite3
import subprocess
import time
import json
import requests
import base64
from flask_cors import CORS
import pickle
import datetime
import pandas as pd

name="amlan"
app = Flask(__name__)
CORS(app) 
app.secret_key = 'abc123'  # Set a secret key for session management

def start_ngrok():
    try:
        # Kill any existing ngrok processes
        subprocess.run(['taskkill', '/F', '/IM', 'ngrok.exe'], capture_output=True)
        time.sleep(1)  # Wait for process to be killed
        
        # Start ngrok
        ngrok_process = subprocess.Popen(
            ['ngrok', 'http', '5000', '--authtoken', '2x6klVino9g9V0i7yaUO8GmDeWi_71fR1W5XwapgYAJAnqgsj'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for ngrok to start
        time.sleep(2)
        
        # Get the public URL
        try:
            response = requests.get('http://localhost:4040/api/tunnels')
            tunnels = response.json()['tunnels']
            return tunnels[0]['public_url']
        except:
            return None
    except Exception as e:
        print(f"Error starting ngrok: {str(e)}")
        return None



@app.route('/name', methods=['GET', 'POST'])
def name():
    if request.method=="POST":
        try:
            print("Received registration request")  # Debug log
            
            # Get form data
            name1 = request.form.get('name1')
            name2 = request.form.get('name2')
            image_data = request.form.get('image_data')
            
            print(f"Form data received - name1: {name1}, name2: {name2}, image_data length: {len(image_data) if image_data else 0}")  # Debug log
            
            if not all([name1, name2, image_data]):
                print("Missing required data")  # Debug log
                return jsonify({
                    "success": False, 
                    "error": "Missing required data. Please fill all fields and capture an image."
                }), 400
                
            # Remove the data URL prefix
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Convert base64 to image
            try:
                image_bytes = base64.b64decode(image_data)
                nparr = np.frombuffer(image_bytes, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if img is None:
                    print("Failed to decode image")  # Debug log
                    return jsonify({
                        "success": False, 
                        "error": "Invalid image data. Please try capturing the image again."
                    }), 400
                    
                # Verify face detection
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(img_rgb)
                
                if not face_locations:
                    print("No face detected in image")  # Debug log
                    return jsonify({
                        "success": False, 
                        "error": "No face detected in the image. Please make sure your face is clearly visible."
                    }), 400
                    
                if len(face_locations) > 1:
                    print("Multiple faces detected")  # Debug log
                    return jsonify({
                        "success": False, 
                        "error": "Multiple faces detected. Please upload an image with only one face."
                    }), 400
                    
            except Exception as e:
                print(f"Error processing image: {str(e)}")  # Debug log
                return jsonify({
                    "success": False, 
                    "error": f"Error processing image: {str(e)}. Please try again."
                }), 400
            
            # Create Training images directory if it doesn't exist
            path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Training images')
            if not os.path.exists(path):
                os.makedirs(path)
            
            # Save the image
            img_name = f"{name1}.png"
            img_path = os.path.join(path, img_name)
            
            try:
                with open(img_path, 'wb') as f:
                    f.write(image_bytes)
                print(f"Image saved successfully: {img_path}")  # Debug log
            except Exception as e:
                print(f"Error saving image: {str(e)}")  # Debug log
                return jsonify({
                    "success": False, 
                    "error": f"Error saving image: {str(e)}"
                }), 500
            
            # Update face encodings
            try:
                if not save_face_encodings():
                    print("Failed to update face encodings")  # Debug log
                    return jsonify({
                        "success": False, 
                        "error": "Failed to update face encodings. Please try again."
                    }), 500
                print("Face encodings updated successfully")  # Debug log
            except Exception as e:
                print(f"Error updating face encodings: {str(e)}")  # Debug log
                return jsonify({
                    "success": False, 
                    "error": f"Error updating face encodings: {str(e)}"
                }), 500
            
            print(f"Registration successful for {name1}")  # Debug log
            return jsonify({
                "success": True, 
                "message": "Registration successful! You can now use face recognition."
            }), 200
            
        except Exception as e:
            print(f"Unexpected error in registration: {str(e)}")  # Debug log
            return jsonify({
                "success": False, 
                "error": f"An unexpected error occurred: {str(e)}"
            }), 500
    else:
        return  jsonify({
            "success": False, 
            "error": "Invalid request method. Please use POST to register."
        }), 405
    




@app.route("/",methods=["GET","POST"])
def recognize():
    if request.method=="POST":
        try:
            path = 'Training images'
            images = []
            classNames = []
            myList = os.listdir(path)
            print(myList)
            
            # Load and encode all training images
            for cl in myList:
                curImg = cv2.imread(f'{path}/{cl}')
                if curImg is None:
                    print(f"Warning: Could not read image {cl}")
                    continue
                images.append(curImg)
                classNames.append(os.path.splitext(cl)[0])
            print(classNames)
            
            def findEncodings(images):
                encodeList = []
                for img in images:
                    try:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        encode = face_recognition.face_encodings(img)
                        if len(encode) > 0:
                            encodeList.append(encode[0])
                        else:
                            print("Warning: No face found in image")
                    except Exception as e:
                        print(f"Error encoding image: {str(e)}")
                return encodeList

            encodeListKnown = findEncodings(images)
            print('Encoding Complete')
            
            # Initialize webcam
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                return "Error: Could not open webcam", 500
            
            while True:
                success, img = cap.read()
                if not success:
                    print("Failed to grab frame")
                    break
                
                # Resize image for faster processing
                try:
                    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
                    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
                except Exception as e:
                    print(f"Error resizing image: {str(e)}")
                    continue

                facesCurFrame = face_recognition.face_locations(imgS)
                encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

                for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                    matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                    matchIndex = np.argmin(faceDis)

                    if faceDis[matchIndex] < 0.50:
                        name = classNames[matchIndex].upper()
                        markAttendance(name)
                        markData(name)
                    else:
                        name = 'Unknown'
                    
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                cv2.imshow('Punch your Attendance', img)
                c = cv2.waitKey(1)
                if c == 27:  # ESC key
                    break

            cap.release()
            cv2.destroyAllWindows()
            return "Face recognition completed", 200
            
        except Exception as e:
            print(f"Error in face recognition: {str(e)}")
            return f"Error in face recognition: {str(e)}", 500
    else:
        return jsonify({
            "success": False, 
            "error": "Invalid request method. Please use POST to recognize."
        }), 405

@app.route('/login',methods = ['POST'])
def login():
    #print( request.headers )
    json_data = json.loads(request.data.decode())
    username = json_data['username']
    password = json_data['password']
    #print(username,password)
    if os.path.exists('cred.csv') == False:
        data = {'username': ['admin'], 'password': ['admin']}
        df = pd.DataFrame(data)
        df.to_csv('cred.csv', index=False)
    else:
        df = pd.read_csv('cred.csv')
    #print(df.head())
    df= pd.read_csv('cred.csv')
    print(df.head())
    if len(df.loc[df['username'] == username]['password'].values) > 0:
        if df.loc[df['username'] == username]['password'].values[0] == password:
            session['username'] = username
            return 'success'
        else:
            return 'failed'
    else:
        return 'failed'
        


@app.route('/checklogin')
def checklogin():
    #print('here')
    if 'username' in session:
        return session['username']
    return 'False'


@app.route('/how',methods=["GET","POST"])
def how():
    return jsonify({
        "success": True,
        "message": "This is the how endpoint."
    }), 200
@app.route('/data',methods=["GET","POST"])
def data():
    '''user=request.form['username']
    pass1=request.form['pass']
    if user=="tech" and pass1=="tech@321" :
    '''
    if request.method=="POST":
        today=date.today()
        print(today)
        conn = sqlite3.connect('information.db')
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        print ("Opened database successfully");
        cursor = cur.execute("SELECT DISTINCT NAME,Time, Date from Attendance where Date=?",(today,))
        rows=cur.fetchall()
        print(rows)
        for line in cursor:

            data1=list(line)
        print ("Operation done successfully");
        conn.close()

        return jsonify({
            "success": True,
            "data": data1,
            "message": "Data retrieved successfully"
        }), 200
    else:
        return jsonify({
            "success": False,
            "error": "Invalid request method. Please use POST to retrieve data."
        }), 405


            
@app.route('/whole', methods=["GET", "POST"])
def whole():
    try:
        # Check if the attendance.csv file exists
        if not os.path.exists('attendance.csv'):
            print("Attendance file not found")
            return jsonify({"success": False, "data": [], "message": "Attendance file not found"}), 404

        # Load attendance data from CSV into a DataFrame
        df = pd.read_csv('attendance.csv', header=None, names=['NAME', 'Time', 'Date', 'Mode'])
        print("Attendance data loaded successfully")

        # Filter today's attendance
        todays_attendance = df[df['Date'] == date.today().strftime('%Y-%m-%d')].copy()  # Use .copy() to avoid SettingWithCopyWarning

        if todays_attendance.empty:
            print("No attendance data for today")
            return jsonify({"success": True, "data": [], "message": "No attendance data for today"}), 200

        # Ensure 'Time' column contains only valid time values and convert to string
        todays_attendance['Time'] = pd.to_datetime(todays_attendance['Time'], format='%H:%M:%S', errors='coerce').dt.strftime('%H:%M:%S')

        # Drop rows with invalid 'Time' values
        todays_attendance = todays_attendance.dropna(subset=['Time'])

        # Convert DataFrame to a list of dictionaries for JSON response
        rows = todays_attendance.to_dict(orient='records')

        return jsonify({"success": True, "data": rows, "message": "Attendance data retrieved successfully"}), 200
    except Exception as e:
        print(f"Error loading attendance data: {str(e)}")
        return jsonify({"success": False, "data": [], "message": f"Error loading attendance data: {str(e)}"}), 500

@app.route('/dashboard',methods=["GET","POST"])
def dashboard():
    return jsonify({
        "success": True,
        "message": "This is the dashboard endpoint."
    }), 200

# Sending Email about the attendance report to the faculties/ parents / etc.
# Not working currently
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

def sendMail():
    mssg=MIMEMultipart()


    server=smtplib.SMTP("smtp.gmail.com",'587')
    server.starttls()
    print("Connected with the server")
    user=input("Enter username:")
    pwd=input("Enter password:")
    server.login(user,pwd)
    print("Login Successful!")
    send=user
    rcv=input("Enter Receiver's Email id:")
    mssg["Subject"] = "Employee Report csv"
    mssg["From"] = user
    mssg["To"] = rcv

    body='''
        <html>
        <body>
         <h1>Employee Quarterly Report</h1>
         <h2>Contains the details of all the employees</h2>
         <p>Do not share confidential information with anyone.</p>
        </body>
        </html>
         '''

    body_part=MIMEText(body,'html')
    mssg.attach(body_part)

    with open("emp.csv",'rb') as f:
        mssg.attach(MIMEApplication(f.read(),Name="emp.csv"))

    server.sendmail(mssg["From"],mssg["To"],mssg.as_string())
   # server.quit()

def markAttendance(name, mode='entry', today=None):
    try:
        today = date.today().strftime('%Y-%m-%d')
        with open('attendance.csv', 'r+', errors='ignore') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                if len(entry) >= 4:  # Check if line has enough fields
                    nameList.append((entry[0], entry[1], entry[2].strip(), entry[3].strip()))  # name, time, date, mode
            
            # Check if person already marked attendance for this mode today
            for entry_name, entry_time, entry_date, entry_mode in nameList:
                if entry_name == name and entry_date == today and entry_mode == mode:
                    print(f"Already marked {mode} for {name} today")
                    return False
            
            # Mark new attendance
            now = datetime.datetime.now()
            dtString = now.strftime('%H:%M:%S')  # Ensure only time is stored
            f.writelines(f'\n{name},{dtString},{today},{mode}')
            print(f"Marked {mode} attendance for {name} at {dtString} on {today}")
            return True
    except Exception as e:
        print(f"Error marking attendance in CSV: {str(e)}")
    return False

def markData(name, mode='entry'):
    """Mark attendance in the CSV file only."""
    try:
        print(f"Marking {mode} attendance for {name}")
        now = datetime.datetime.now()
        dtString = now.strftime('%H:%M:%S')  # Ensure only time is stored
        today = date.today().strftime('%Y-%m-%d')
        
        # Open the CSV file and check for existing entries
        with open('attendance.csv', 'r+', errors='ignore') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                if len(entry) >= 4:  # Check if line has enough fields
                    nameList.append((entry[0], entry[1], entry[2].strip(), entry[3].strip()))  # name, time, date, mode
            
            # Check if person already marked attendance for this mode today
            for entry_name, entry_time, entry_date, entry_mode in nameList:
                if entry_name == name and entry_date == today and entry_mode == mode:
                    print(f"Already marked {mode} for {name} today")
                    return False
            
            # Mark new attendance
            f.writelines(f'\n{name},{dtString},{today},{mode}')
            print(f"Marked {mode} attendance for {name} at {dtString} on {today}")
            return True
    except Exception as e:
        print(f"Error marking attendance in CSV: {str(e)}")
        return False

def init_db():
    """Remove database initialization as we are using CSV files."""
    pass

def markData(name, mode='entry'):
    """Mark attendance in the CSV file only."""
    try:
        print(f"Marking {mode} attendance for {name}")
        now = datetime.datetime.now()
        dtString = now.strftime('%H:%M:%S')  # Ensure only time is stored
        today = date.today().strftime('%Y-%m-%d')
        
        # Open the CSV file and check for existing entries
        with open('attendance.csv', 'r+', errors='ignore') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                if len(entry) >= 4:  # Check if line has enough fields
                    nameList.append((entry[0], entry[1], entry[2].strip(), entry[3].strip()))  # name, time, date, mode
            
            # Check if person already marked attendance for this mode today
            for entry_name, entry_time, entry_date, entry_mode in nameList:
                if entry_name == name and entry_date == today and entry_mode == mode:
                    print(f"Already marked {mode} for {name} today")
                    return False
            
            # Mark new attendance
            f.writelines(f'\n{name},{dtString},{today},{mode}')
            print(f"Marked {mode} attendance for {name} at {dtString} on {today}")
            return True
    except Exception as e:
        print(f"Error marking attendance in CSV: {str(e)}")
        return False

def save_face_encodings():
    """Pre-encode all training images and save to a file"""
    try:
        path = 'Training images'
        if not os.path.exists(path):
            print("Training images directory not found")
            return False
            
        images = []
        classNames = []
        myList = os.listdir(path)
        
        if not myList:
            print("No training images found")
            return False
            
        for cl in myList:
            try:
                curImg = cv2.imread(f'{path}/{cl}')
                if curImg is None:
                    print(f"Warning: Could not read image {cl}")
                    continue
                    
                # Convert to RGB
                curImg = cv2.cvtColor(curImg, cv2.COLOR_BGR2RGB)
                
                # Get face locations
                face_locations = face_recognition.face_locations(curImg)
                if not face_locations:
                    print(f"Warning: No face found in image {cl}")
                    continue
                    
                # Get face encodings
                face_encodings = face_recognition.face_encodings(curImg, face_locations)
                if not face_encodings:
                    print(f"Warning: Could not encode face in image {cl}")
                    continue
                    
                # Use the first face found
                images.append(face_encodings[0])
                classNames.append(os.path.splitext(cl)[0])
                print(f"Successfully processed image {cl}")
                
            except Exception as e:
                print(f"Error processing image {cl}: {str(e)}")
                continue
            
        if not images:
            print("No valid faces found in training images")
            return False
            
        # Save encodings and names
        try:
            with open('face_encodings.pkl', 'wb') as f:
                pickle.dump((images, classNames), f)
            print(f"Successfully saved {len(images)} face encodings")
            return True
        except Exception as e:
            print(f"Error saving encodings to file: {str(e)}")
            return False
        
    except Exception as e:
        print(f"Error in save_face_encodings: {str(e)}")
        return False

def load_face_encodings():
    """Load pre-computed face encodings from file"""
    try:
        if not os.path.exists('face_encodings.pkl'):
            print("Face encodings file not found")
            return None, None
            
        with open('face_encodings.pkl', 'rb') as f:
            encodeList, classNames = pickle.load(f)
            
        return encodeList, classNames
        
    except Exception as e:
        print(f"Error loading face encodings: {str(e)}")
        return None, None

@app.route('/recognize_face', methods=['POST'])
def recognize_face():
    try:
        # Get image data from request
        data = request.get_json()
        if not data or 'image' not in data:
            print("No image data received")
            return jsonify({"success": False, "error": "No image data received"}), 400

        # Remove the data URL prefix and decode base64
        try:
            image_data = data['image'].split(',')[1]
            image_bytes = base64.b64decode(image_data)
            
            # Convert to numpy array
            nparr = np.frombuffer(image_bytes, np.uint8)
            if len(nparr) == 0:
                print("Empty image data received")
                return jsonify({"success": True, "name": "Unknown", "message": "No face detected"}), 200
                
            # Decode image
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                print("Failed to decode image")
                return jsonify({"success": True, "name": "Unknown", "message": "Failed to process image"}), 200
                
            # Check if image is empty
            if img.size == 0:
                print("Empty image after decoding")
                return jsonify({"success": True, "name": "Unknown", "message": "Empty image"}), 200
                
            print(f"Image shape: {img.shape}")
                
        except Exception as e:
            print(f"Error processing image data: {str(e)}")
            return jsonify({"success": False, "error": f"Invalid image data: {str(e)}"}), 400

        # Load pre-computed face encodings
        encodeListKnown, classNames = load_face_encodings()
        if encodeListKnown is None or classNames is None:
            print("Failed to load face encodings")
            return jsonify({"success": False, "error": "Failed to load face encodings"}), 500
            
        print(f"Loaded {len(encodeListKnown)} face encodings")
        
        # Process the current image
        try:
            # Convert to RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Get face locations
            face_locations = face_recognition.face_locations(img_rgb)
            if not face_locations:
                print("No faces found in current frame")
                return jsonify({"success": True, "name": "Unknown", "message": "No face detected"}), 200
                
            print(f"Found {len(face_locations)} faces in current frame")
                
            # Get face encodings
            face_encodings = face_recognition.face_encodings(img_rgb, face_locations)
            if not face_encodings:
                print("Could not encode faces in current frame")
                return jsonify({"success": True, "name": "Unknown", "message": "Could not process face"}), 200

            # Process each face found
            for face_encoding in face_encodings:
                # Compare with known faces
                matches = face_recognition.compare_faces(encodeListKnown, face_encoding, tolerance=0.45)
                face_distances = face_recognition.face_distance(encodeListKnown, face_encoding)
                
                if len(face_distances) > 0:
                    # Get the best match
                    best_match_index = np.argmin(face_distances)
                    best_match_distance = face_distances[best_match_index]
                    
                    print(f"Best match distance: {best_match_distance}")
                    
                    if best_match_distance < 0.45:  # Lower threshold for better accuracy
                        name = classNames[best_match_index].upper()
                        print(f"Recognized face: {name} with distance: {best_match_distance}")
                        return jsonify({
                            "success": True, 
                            "name": name,
                            "message": f"Face recognized as {name}"
                        }), 200
                    else:
                        print(f"Face distance too high: {best_match_distance}")

            print("No matching face found")
            return jsonify({
                "success": True, 
                "name": "Unknown",
                "message": "Face not recognized"
            }), 200

        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return jsonify({"success": False, "error": f"Error processing image: {str(e)}"}), 500

    except Exception as e:
        print(f"Error in face recognition: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    try:
        data = request.get_json()
        if not data or 'name' not in data or 'mode' not in data:
            return jsonify({"success": False, "error": "Missing required data"}), 400

        name = data['name']
        mode = data['mode']
        day=datetime.datetime.now().date()
        today = day.strftime('%Y-%m-%d')

        if mode not in ['entry', 'exit']:
            return jsonify({"success": False, "error": "Invalid mode"}), 400

        # Mark attendance
        csv_success = markAttendance(name, mode, today)
        db_success = markData(name, mode)
        
        if csv_success and db_success:
            return jsonify({
                "success": True,
                "message": f"{mode.capitalize()} marked for {name}"
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": f"Failed to mark {mode} for {name} - may have already been marked"
            }), 200

    except Exception as e:
        print(f"Error marking attendance: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/new_table', methods=["GET", "POST"])
def new_table():
    try:
        # Check if the new table CSV file exists
        if not os.path.exists('new_attendance.csv'):
            print("New attendance file not found, creating a new one.")
            # Create an empty DataFrame with the new structure
            new_df = pd.DataFrame(columns=['Date', 'EmployeeName', 'Status', 'EntryHour', 'LeaveHour'])
            new_df.to_csv('new_attendance.csv', index=False)

        # Load the new attendance data
        new_df = pd.read_csv('new_attendance.csv')
        print("New attendance data loaded successfully")

        # If POST request, add a new record
        if request.method == "POST":
            data = request.get_json()
            if not data or not all(key in data for key in ['Date', 'EmployeeName', 'Status', 'EntryHour', 'LeaveHour']):
                return jsonify({"success": False, "error": "Missing required data"}), 400

            # Append the new record to the DataFrame
            new_record = {
                'Date': data['Date'],
                'EmployeeName': data['EmployeeName'],
                'Status': data['Status'],
                'EntryHour': data['EntryHour'],
                'LeaveHour': data['LeaveHour']
            }
            new_df = new_df.append(new_record, ignore_index=True)
            new_df.to_csv('new_attendance.csv', index=False)
            print("New record added successfully")
            return jsonify({"success": True, "message": "Record added successfully"}), 200

        # Return the new table data
        rows = new_df.to_dict(orient='records')
        return jsonify({"success": True, "data": rows, "message": "New attendance data retrieved successfully"}), 200

    except Exception as e:
        print(f"Error handling new table: {str(e)}")
        return jsonify({"success": False, "error": f"Error handling new table: {str(e)}"}), 500

if __name__ == '__main__':
    try:
        # Initialize database on startup
        init_db()
        
        # Pre-encode faces on startup
        save_face_encodings()
        
        public_url = start_ngrok()
        if public_url:
            print(f' * Public URL: {public_url}')
        else:
            print("Starting Flask without ngrok...")
        app.run(debug=True, use_reloader=False)  # Disabled reloader to prevent duplicate processes
    except Exception as e:
        print(f"Error starting server: {str(e)}")



