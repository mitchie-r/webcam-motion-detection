# Intrusion Detection System

This system uses OpenCV to turn your webcam into a security camera, detecting motion and sending email alerts.

## Setup

### Prerequisites

1. **Anaconda (or Miniconda):** Download and install from [https://www.anaconda.com/download/](https://www.anaconda.com/download/) (Choose the appropriate installer for your system - Windows, macOS, or Linux).
2. **Python:** If you installed Anaconda, Python is already included. Otherwise, download and install from [https://www.python.org/downloads/](https://www.python.org/downloads/).

### Installation

1. **Open a terminal or command prompt.** 
2. **Navigate to the project directory:**
   ```bash
   cd path/to/your_project_directory/opencv_for_beginners/Webcam-motion-detection

   pip install -r requirements.txt

   Absolutely! Here's the revised README file, focusing on the key changes you mentioned:

Markdown
# Intrusion Detection System

This system uses OpenCV to turn your webcam into a security camera, detecting motion and sending email alerts.

## Setup

### Prerequisites

1. **Anaconda (or Miniconda):** Download and install from [https://www.anaconda.com/download/](https://www.anaconda.com/download/) (Choose the appropriate installer for your system - Windows, macOS, or Linux).
2. **Python:** If you installed Anaconda, Python is already included. Otherwise, download and install from [https://www.python.org/downloads/](https://www.python.org/downloads/).

### Installation

1. **Open a terminal or command prompt.** 
2. **Navigate to the project directory:**
   ```bash
   cd path/to/your_project_directory/opencv_for_beginners/Webcam-motion-detection
Use code with caution.

Install required packages:
Bash
pip install -r requirements.txt
Use code with caution.

Environment Variables (Windows)
To securely store sensitive information (email credentials), create the following environment variables:

EMAIL_MOTION: Your email address.
EMAIL_PASSWORD: Your email password.
TO_EMAIL_MOTION: The email address where alerts should be sent.

Running the System
Open a terminal or command prompt.
Navigate to the project directory:

cd path/to/your_project_directory/opencv_for_beginners/Webcam-motion-detection

Execute the Python script:

python Intrusion_Detection.py

The Intrusion_Detection.py script:

Captures video: Accesses your webcam to capture frames.
Detects motion: Uses background subtraction and image processing to identify movement.
Sends email alerts: When motion is detected, it triggers an email notification.
Important Note
This README assumes a basic understanding of setting up environment variables. If you need assistance, please refer to relevant tutorials or documentation.

Directory Structure

your_project_directory
├── opencv_for_beginners
│   ├── Webcam-motion-detection        
│   │   ├── Intrusion_Detection.py     <-- Main Python script
│   │   └── requirements.txt           <-- List of required Python packages
├── ...other files and folders...