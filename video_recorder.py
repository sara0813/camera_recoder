import cv2 as cv
import time

video = cv.VideoCapture(0)
output_filename = 'recorded_video.avi'
fps = video.get(cv.CAP_PROP_FPS) or 30.0
width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter(output_filename, fourcc, fps, (width, height))

is_recording = False
wait_msec = int(1000 / fps)
start_time = None
is_grayscale = False

while True:
    valid, frame = video.read()
    if not valid:
        break

    if is_grayscale:
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)

    if is_recording:
        cv.circle(frame, (50, 50), 15, (0, 0, 255), -1)
        elapsed_time = int(time.time() - start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        time_str = f"{minutes:02}:{seconds:02}"
        cv.putText(frame, f"Recording: {time_str}", (10, height - 10), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)

    cv.imshow('Webcam Recorder', frame)

    key = cv.waitKey(wait_msec) & 0xFF
    if key == 27:
        break
    elif key == 32:
        is_recording = not is_recording
        if is_recording:
            start_time = time.time()
        else:
            start_time = None
    elif key == 114:
        is_grayscale = not is_grayscale

    if is_recording:
        out.write(frame)

cv.destroyAllWindows()
