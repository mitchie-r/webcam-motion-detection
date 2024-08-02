import cv2
import numpy as np
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import platform

# Email configuration (replace with your actual credentials)
from_email = os.environ.get("EMAIL_MOTION")
password = os.environ.get("EMAIL_PASSWORD")  # Retrieve password from environment variable
to_email = os.environ.get("TO_EMAIL_MOTION")
subject = "Motion Detected!"
message = "Dear Dude,\n\nThere's some motion!"

def list_available_cameras():
    """
    Lists available cameras along with their properties.
    """

    index = 0
    camera_list = []

    while True:
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            break

        camera_properties = {}

        # Get common properties
        camera_properties["index"] = index
        camera_properties["width"] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        camera_properties["height"] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        camera_properties["fps"] = cap.get(cv2.CAP_PROP_FPS)

        # Get backend-specific properties (handle potential AttributeError)
        try:
            if platform.system() == "Windows":
                camera_properties["api"] = cap.get(cv2.CAP_PROP_BACKEND)  # For Windows
            else:
                camera_properties["api"] = cap.get(cv2.CAP_PROP_GSTREAMER_BACKEND)  # For Linux (GStreamer)
        except AttributeError:
            camera_properties["api"] = "Unknown"

        camera_list.append(camera_properties)
        index += 1
        cap.release()

    return camera_list

def camera_choice(camera_list):
    while True:  # Loop until valid input is received
        choice = input(f"""Choose a camera to use (1, 2, 3, etc):
                         {', '.join([f'Camera {camera["index"]+1}: {camera["width"]}x{camera["height"]} @ {camera["fps"]}fps' for camera in camera_list])}
                         ###############################""")
        # Check if choice is a valid number between 1 and the total number of cameras
        if choice.isdigit() and 1 <= int(choice) <= len(camera_list):
            return int(choice) - 1
        else:
            print("Invalid choice. Please try again.")

def drawBannerText(frame, text, banner_height_percent=0.08, font_scale=0.8, text_color=(0, 255, 0), font_thickness=2):
    banner_height = int(banner_height_percent * frame.shape[0])
    cv2.rectangle(frame, (0, 0), (frame.shape[1], banner_height), (0, 255, 0), thickness=-1)
    left_offset = 20
    location = (left_offset, int(10 + (banner_height_percent * frame.shape[0]) / 2))
    cv2.putText(frame, text, location, cv2.FONT_HERSHEY_SCRIPT_COMPLEX, font_scale, text_color, font_thickness, cv2.LINE_AA)

def kernel_choice():
    while True:  # Loop until valid input is received
        choice = input("""################################
                        Which kernel size did you want to choose? 
                        Available kernel sizes:
                            1. (3, 3)
                            2. (5, 5)
                            3. (7, 7)
                            4. (9, 9)
                        ###############################""")
        # Check if choice is a valid number between 1 and 4
        if choice.isdigit() and 1 <= int(choice) <= 4: 
            choice = int(choice)
            kernel_sizes = [(3, 3), (5, 5), (7, 7), (9, 9)]
            return kernel_sizes[choice - 1]
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

def choose_min_area():
    while True:  # Loop until valid input is received
        choice = input("""################################
                        What is the minimum area of your motion? 
                        Please choose between 50 and 1200
                        the lower the number, the more motion sensitvity
                        ###############################""")
        # Check if choice is a valid number between 1 and 4
        if choice.isdigit() and 50 <= int(choice) <= 1200: 
            choice = int(choice)
            return choice
        else:
            print("Invalid choice. Please enter a number between 50 and 1200.")

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

def motion_detection(ksize, min_contour_area, source):
    # Video source and settings
    source = source
    timeout = 45

    # Colors
    red = (0, 0, 255)
    yellow = (0, 255, 255)
    green = (0, 255, 0)
    orange = (0, 165, 255)

    video_cap = cv2.VideoCapture(source)
    if not video_cap.isOpened():
        print('Unable to open video source:', source)

    frame_w = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_h = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video_cap.get(cv2.CAP_PROP_FPS))
    size = (frame_w, frame_h)

    # Video output file (using MP4-compatible codec)
    video_out_alert_file = 'video_out_alert_1.mp4'

    # Define the folder for motion detection videos
    motion_detection_folder = 'Motion_Detection'

    # Name for the current motion that's happening
    current_motion_video_file = 'current_motion.mp4'

    # Create the folder if it doesn't exist
    if not os.path.exists(motion_detection_folder):
        os.makedirs(motion_detection_folder)

    # Check if video exists from a previous motion and delete it if not
    video_out_alert_file = os.path.join(motion_detection_folder, current_motion_video_file)
    if os.path.exists(video_out_alert_file):
        os.remove(video_out_alert_file)
        print("Last video deleted!")


    # Check if the video was already created in a previous motion
    for vids in range(1, 100):
        test_file_name = f'current_motion_{vids}.mp4'
        if not os.path.exists(os.path.join(motion_detection_folder, test_file_name)):
            current_motion_video_file = test_file_name
            break

        # Construct the full path for the current motion video
        current_motion_video_file = os.path.join(motion_detection_folder, current_motion_video_file)


    video_out_alert = cv2.VideoWriter(video_out_alert_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
    current_motion_vid = cv2.VideoWriter(current_motion_video_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
    # Background subtraction and parameters
    bg_sub = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400.0)
    max_contours = 3
    frame_count = 0
    frame_start = 30

    # Timer for motion detection
    timer_started = False
    start_time = time.time()
    elapsed_time = time.time()

    # Process video frames.
    while True:
        ret, frame = video_cap.read()
        frame_count += 1
        if frame is None:
            break
        else:
            frame_erode_c = frame.copy()
            current_motion = frame.copy()

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
                    cv2.drawContours(frame_fg_mask_erode_c, filtered_contours, -1, orange, 2)
                    if not timer_started:
                        start_time = time.time()
                        timer_started = True
                        print("Timer Started!")
                    # Sort the filtered contours by area (descending)
                    contours_sorted = sorted(filtered_contours, key=cv2.contourArea, reverse=True)

                    # Find the coordinates of the overall bounding box
                    x1, y1, w, h = cv2.boundingRect(np.vstack(contours_sorted[:max_contours]))
                    x2, y2 = x1 + w, y1 + h

                    # Draw bounding rectangle and banner
                    
                    cv2.rectangle(frame_erode_c, (x1, y1), (x2, y2), yellow, 2)
                    drawBannerText(frame_erode_c, 'Motion Detected', text_color=red)
                    cv2.rectangle(current_motion, (x1, y1), (x2, y2), yellow, 2)
                    drawBannerText(current_motion, 'Motion Detected', text_color=red)
                drawBannerText(frame_fg_mask_erode_c, 'Foreground Mask (Eroded + Contours)')

            frame_view = np.hstack([frame_fg_mask_erode_c, frame_erode_c])
            frame_view = cv2.resize(frame_view, None, fx=0.7, fy=0.7)
            video_out_alert.write(frame_erode_c)
            if timer_started:
                current_motion_vid.write(current_motion)
                elapsed_time = time.time() - start_time
                if elapsed_time > timeout:
                    break
            cv2.imshow('Composite Frame', frame_view)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
    video_cap.release()
    video_out_alert.release()
    current_motion_vid.release()
    if timer_started:
        send_email_ionos(from_email, password, to_email, subject, message)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    #cams = list_available_cameras()
    #cam_choice = camera_choice(cams)
    #ksize = kernel_choice()
    #min_area = choose_min_area()
    motion_detection((7, 7), 700, 0)
    
