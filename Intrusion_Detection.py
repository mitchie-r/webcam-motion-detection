import cv2
import numpy as np
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Email configuration (replace with your actual credentials)
from_email = os.environ.get("EMAIL_MOTION")
password = os.environ.get("EMAIL_PASSWORD")  # Retrieve password from environment variable
to_email = os.environ.get("TO_EMAIL_MOTION")
subject = "Motion Detected!"
message = "Dear Dude,\n\nThere's some motion!"

# Video source and settings
source = 0
timeout = 45

video_cap = cv2.VideoCapture(source)
if not video_cap.isOpened():
    print('Unable to open video source:', source)

frame_w = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_h = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video_cap.get(cv2.CAP_PROP_FPS))
size = (frame_w, frame_h)

# Video output file (using MP4-compatible codec)
video_out_alert_file = 'video_out_alert_1.mp4'
video_out_alert = cv2.VideoWriter(video_out_alert_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

def drawBannerText(frame, text, banner_height_percent=0.08, font_scale=0.8, text_color=(0, 255, 0), font_thickness=2):
    banner_height = int(banner_height_percent * frame.shape[0])
    cv2.rectangle(frame, (0, 0), (frame.shape[1], banner_height), (0, 255, 0), thickness=-1)
    left_offset = 20
    location = (left_offset, int(10 + (banner_height_percent * frame.shape[0]) / 2))
    cv2.putText(frame, text, location, cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, font_thickness, cv2.LINE_AA)

def send_email_ionos(from_email, password, to_email, subject, body):
    """Sends an email using an IONOS business email account."""
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.ionos.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Background subtraction and parameters
bg_sub = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400.0)
ksize = (10, 10)
min_contour_area = 1200
max_contours = 3
frame_count = 0
frame_start = 30

# Colors
red = (0, 0, 255)
yellow = (0, 255, 255)
green = (0, 255, 0)

# Timer for motion detection
timer_started = False
start_time = None

# Process video frames.
while True:
    ret, frame = video_cap.read()
    frame_count += 1
    if frame is None:
        break
    else:
        frame_erode_c = frame.copy()

    # Create a foreground mask for the current frame.
    fg_mask = bg_sub.apply(frame)

    if frame_count > frame_start:
        # Erosion and motion area detection.
        fg_mask_erode_c = cv2.erode(fg_mask, np.ones(ksize, np.uint8))
        motion_area_erode = cv2.findNonZero(fg_mask_erode_c)

        if motion_area_erode is not None:
            xe, ye, we, he = cv2.boundingRect(motion_area_erode)
            cv2.rectangle(frame_erode_c, (xe, ye), (xe + we, ye + he), red, thickness=2)
            drawBannerText(frame_erode_c, 'Motion Detected', text_color=red)

        # Convert foreground masks to color.
        frame_fg_mask_erode_c = cv2.cvtColor(fg_mask_erode_c, cv2.COLOR_GRAY2BGR)

        # Find contours.
        contours_erode, hierarchy = cv2.findContours(fg_mask_erode_c, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours_erode) > 0:
            # Filters contours_erode for areas larger than the min_contour_area
            filtered_contours = [cnt for cnt in contours_erode if cv2.contourArea(cnt) > min_contour_area]

            if filtered_contours:
                cv2.drawContours(frame_fg_mask_erode_c, filtered_contours, -1, green, 2)
                if not timer_started:
                    start_time = time.time()
                    timer_started = True
                    print("Timer Started!")
                elapsed_time = time.time() - start_time
                print(elapsed_time)
                if elapsed_time > timeout:
                   break

                # Sort the filtered contours by area (descending)
                contours_sorted = sorted(filtered_contours, key=cv2.contourArea, reverse=True)

                # Find the coordinates of the overall bounding box
                x1, y1, w, h = cv2.boundingRect(np.vstack(contours_sorted[:max_contours]))
                x2, y2 = x1 + w, y1 + h

                # Draw bounding rectangle and banner
                cv2.rectangle(frame_erode_c, (x1, y1), (x2, y2), yellow, 2)
                drawBannerText(frame_erode_c, 'Motion Detected', text_color=red)

            drawBannerText(frame_fg_mask_erode_c, 'Foreground Mask (Eroded + Contours)')

        frame_view = np.hstack([frame_fg_mask_erode_c, frame_erode_c])
        frame_view = cv2.resize(frame_view, None, fx=0.7, fy=0.7)
        video_out_alert.write(frame_erode_c)
        cv2.imshow('Composite Frame', frame_view)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video_cap.release()
video_out_alert.release()
cv2.destroyAllWindows()

send_email_ionos(from_email, password, to_email, subject, message)