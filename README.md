This is a program that turns a web cam into a security camera and will create separate motion files as they occur in real time.
Must have Python and Conda installed. Install requirements in your environment by running:
pip -r requirements.txt

Intrusion Detection System
This system uses OpenCV to detect motion from your webcam and sends email alerts when motion is detected.

Setup
Environment Variables (Windows):

To securely store sensitive information (email credentials and script path), create the following environment variables on your Windows system:

EMAIL_MOTION: Your email address (for sending alerts).

EMAIL_PASSWORD: Your email password.

TO_EMAIL_MOTION: The email address where alerts should be sent.

OPENCV_PATH:  The base path of your OpenCV installation. For example:

C:\Users\<your_username>\Documents\...\<opencv_for_beginners>
(Replace <your_username> with your actual username, and complete the path to your opencv_for_beginners directory.)

PowerShell Script:

Open the start_intrusion.ps1 PowerShell script.

Modify the $scriptPath variable to include the rest of the path to your Intrusion_Detection.py script, like this:

PowerShell
$scriptPath = "$env:OPENCV_PATH\opencv_for_beginners\Webcam-motion-detection\Intrusion_Detection.py"
Use code with caution.

Save the script.

Running the System
Activate Environment: Make sure your Python environment is activated (where OpenCV is installed).
Execute: Run the start_intrusion.ps1 PowerShell script.
Code Overview
The Intrusion_Detection.py script does the following:

Captures video: Accesses your webcam to capture frames.
Detects motion: Uses background subtraction and image processing techniques to identify movement in the video stream.
Sends email alerts: When motion is detected, it triggers an email notification using your configured environment variables.
Important Note: This README assumes you have OpenCV installed and a basic understanding of setting up environment variables on Windows. If you need assistance with these steps, please refer to relevant tutorials or documentation.

Directory Structure

your_project_directory
├── opencv_for_beginners
│   ├── Webcam-motion-detection          
│   │   ├── Intrusion_Detection.py     <-- Main Python script
│   │   └── start_intrusion.ps1        <-- PowerShell script to start the system
├── ...other files and folders...