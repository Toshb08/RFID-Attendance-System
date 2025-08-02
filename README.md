RFID ATTENDANCE SYSTEM: A microcontroller-based system that automates attendance using RFID tags. It enhances accuracy, ensures real-time monitoring, and supports smart institutional management.

Tech Stack & Tools

1. Hardware: Arduino Uno, RC522 RFID Module, RFID Tags, Buzzer, LEDs
2. Programming Language: C/C++ (Arduino IDE), Python
3. Libraries: MFRC522, Wire, Time, matplotlib (Python)
4. Data Storage: CSV and local storage
5. Real-time notification: Email via SMTP
6. Cloud: AWS S3, Watchdog(Python library) to identify realtime file changes

Key Features:

RFID-based user identification for attendance

Real-time attendance logging

Unknown tag detection and alert system

Time-based access control (e.g., fixed login window)

Email notifications on successful/failed scans

Daily attendance summary with charts (matplotlib)

Offline-first system with sync capability

Automatic sync on cloud platform to ensure backup



Setup Instructions:
1. Hardware Configuration
   
Assemble the RFID-based circuit using Arduino, RC522 RFID reader, and other required components.(Refer to images attached)

2. Upload Arduino Sketch

Flash the provided RFID sketch onto your Arduino board using the Arduino IDE.

3. Enable Cloud Integration
 
Create an AWS S3 bucket.

Generate and download the Secret Access Keys for programmatic access.

4. Activate Watchdog Service

Open a command prompt and run the watchdog script.

Enter the AWS access credentials when prompted.

Then execute cloud.py to enable real-time cloud logging.

5. Run Attendance Logging Script

Execute attendance.py.

Configure the script with appropriate email IDs.

Ensure SMTP access is enabled for your Gmail account via an app-specific password or access key.

Begin scanning RFID tags.

6. Attendance Report Generation

Attendance records are automatically saved in an Excel file.

Date and time are fetched from the system clock.


![RFID 2](https://github.com/user-attachments/assets/56beb20b-03da-44b0-9275-a64bc8e4bc18)
![RFID 1](https://github.com/user-attachments/assets/61960064-eaa9-4cf2-96a3-fe72ac9d8030)

