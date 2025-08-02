import serial
import time
import pandas as pd
from datetime import datetime, timedelta
from datetime import time as dt_time
import smtplib
from email.message import EmailMessage

# Email config (the sender's email)
EMAIL_ADDRESS = ''
EMAIL_PASSWORD = '' #enter your email secret key, configure using your gmail account
#generate your key for access to gmaik 

# send_email for dynamic recipient
def send_email(subject, content, to):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to
    msg.set_content(content)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

# Map of UID strings to (Name, Roll Number, Email)
rfid_students = {
    "59534518": ("Name1", "11", "abc@xyz.com"),
    "24653AA7": ("Name2", "9", "ghi@qwe.com")  
}

# Set up serial connection
ser = serial.Serial('COM4', 9600)
time.sleep(4)

# Excel setup
today = datetime.now().strftime("%Y-%m-%d")
filename = f"Attendance_{today}.xlsx"

# Load or create attendance sheet
try:
    df = pd.read_excel(filename)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Roll Number", "Name", "Time"])

print("Waiting for RFID scans...")

# Track last attendance time for each UID
last_attendance_time = {}
TIME_GAP = timedelta(minutes=1)  #Time duration between 2 scans

while True:
    line = ser.readline().decode('utf-8').strip()

    current_time = datetime.now().time()
    start_time = dt_time(8, 0)   # 8:00 AM
    end_time = dt_time(17, 0)    # 5:00 PM

    if not (start_time <= current_time <= end_time):
        print("Attendance window is closed. Try between 08:00 and 17:00.")
        time.sleep(1)
        continue

    if "UID tag:" in line:
        uid = line.split("UID tag:")[-1].replace(" ", "").upper()

        #for unknown uid handling
        if uid in rfid_students:
            name, roll, to_email = rfid_students[uid]
            current_dt = datetime.now()

            #duplication check
            if uid not in last_attendance_time or current_dt - last_attendance_time[uid] >= TIME_GAP:
                timestamp = current_dt.strftime("%H:%M:%S")
                df = pd.concat([df, pd.DataFrame([[roll, name, timestamp]], columns=df.columns)], ignore_index=True)
                df.to_excel(filename, index=False)

                last_attendance_time[uid] = current_dt

                print(f"Attendance marked for {name} ({roll}) at {timestamp}")
                send_email(
                    subject=f"Attendance Marked: {name}",
                    content=f"{name} ({roll}) marked present at {timestamp}.",
                    to=to_email
                )
            else:
                print(f"{name} ({roll}) already marked present recently.")
        else:
            print("Unknown UID:", uid)
            send_email(
                subject="Unknown UID Detected",
                content=f"An unrecognized UID was scanned: {uid}",
                to='admin@stu.com'  # put an Admin email for unauthorised notification alert
            )
