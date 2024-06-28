# 3D-Print-Monitor-Near-Real-Time-3D-Print-Analysis-and-Notification-System
An open-source solution for real-time monitoring and analysis of 3D prints using a webcam, with automatic email notifications for detected issues and print completion.

# Project Title: 3D Print Monitoring and Analysis System

## Summary
This project provides a comprehensive solution for monitoring and analyzing 3D prints in near real-time using a webcam. The system captures images of the ongoing 3D print, analyzes the image to detect potential issues such as fires, spaghetti stringing, and bed adhesion problems, and sends email notifications in case of detected issues or upon completion of the print.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/3d-print-monitor.git
   cd 3d-print-monitor
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Ensure your webcam is connected and configured correctly.
2. Update the following variables in the code with your actual credentials and paths:
   - `gmail_user`: Your Gmail email address.
   - `gmail_password`: Your Gmail password or app-specific password.
   - `recipient_email`: The email address where notifications should be sent.
   - `api_key`: Your OpenAI API key.

3. Run the main script:
   ```
   python app.py
   ```

The script will continuously capture images from the webcam, analyze them for potential 3D printing issues, and send email notifications accordingly.

## Adding Features
Contributions to this project are welcome! Here are a few ideas for additional features you could add:
1. **Enhanced Image Analysis**: Improve the image analysis algorithm to detect more types of issues or provide more detailed feedback.
2. **Implement Real-time Video Analysis**: Implement Real-time Video Analysis
3. **Web Interface**: Create a web interface to view the live feed of the 3D print and receive real-time updates.
4. **Historical Data**: Implement a feature to log and review the history of prints and detected issues.
5. **Multiple Camera Support**: Allow monitoring of multiple 3D printers simultaneously.

Feel free to fork the repository and submit pull requests with your improvements.

## License
This project is open-source under the MIT License. You are free to use, modify, and distribute this software. However, please provide appropriate recognition.
