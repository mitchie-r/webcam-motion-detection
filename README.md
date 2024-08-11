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
   cd path/to/your_project_directory


pip install -r requirements.txt

git clone https://github.com/mitchredd77/webcam-motion-detection

Environment Variables (Windows)
To securely store sensitive information (email credentials), create the following environment variables:

EMAIL_MOTION: Your email address.
EMAIL_PASSWORD: Your email password.
TO_EMAIL_MOTION: The email address where alerts should be sent.

1. Running the System
2. Open a terminal or command prompt.

Navigate to the project directory:

Bash

cd path/to/your_project_directory

3. Execute the Python script:

python app.py

Important Note
This README assumes a basic understanding of setting up environment variables. If you need assistance, please refer to relevant tutorials or documentation.
