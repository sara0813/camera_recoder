import cv2 as cv
import time

# 웹캠 열기
video = cv.VideoCapture(0)  # 0: 기본 웹캠
output_filename = 'recorded_video.avi'  # 저장할 동영상 파일명
fps = video.get(cv.CAP_PROP_FPS) or 30.0  # FPS 값 가져오기 (없으면 기본값 30)
width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))  # 프레임 너비
height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))  # 프레임 높이
fourcc = cv.VideoWriter_fourcc(*'XVID')  # 비디오 코덱 설정
out = cv.VideoWriter(output_filename, fourcc, fps, (width, height))  # 비디오 저장 객체

is_recording = False  # 초기 모드는 Preview
wait_msec = int(1000 / fps)  # 대기 시간 설정
start_time = None  # 녹화 시작 시간
is_grayscale = False  # 흑백 모드 초기값

while True:
    valid, frame = video.read()
    if not valid:
        break

    # Space 키를 누르면 흑백 모드로 전환
    if is_grayscale:
        frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  # 흑백 변환
        frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)  # 다시 컬러로 변환

    # 녹화 중이면 빨간색 원 그리기
    if is_recording:
        cv.circle(frame, (50, 50), 15, (0, 0, 255), -1)  # 좌측 상단에 빨간 원
        elapsed_time = int(time.time() - start_time)  # 녹화 시간 계산
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        time_str = f"{minutes:02}:{seconds:02}"
        cv.putText(frame, f"Recording: {time_str}", (10, height - 10), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)

    cv.imshow('Webcam Recorder', frame)  # 화면에 프레임 표시

    key = cv.waitKey(wait_msec) & 0xFF  # 키 입력 대기
    if key == 27:  # ESC 키: 종료
        break
    elif key == 32:  # Space 키: 녹화 모드 토글
        is_recording = not is_recording  # 상태 변경
        if is_recording:
            start_time = time.time()  # 녹화 시작 시간 기록
        else:
            start_time = None  # 녹화 중지가 되면 시간 초기화
    elif key == 114:  # 'r' 키: 흑백 모드 토글
        is_grayscale = not is_grayscale  # 흑백 모드 전환

    if is_recording:
        out.write(frame)  # 녹화 중이면 프레임 저장


cv.destroyAllWindows()