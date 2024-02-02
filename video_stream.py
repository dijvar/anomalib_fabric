import sys
import cv2
from threading import Thread


class VideoStream:
    """Helper class for implementing multi-threading for video processing."""

    def __init__(self, video_path: str) -> None:
        self.video_path = video_path
        self.video_capture = cv2.VideoCapture(self.video_path)
        if not self.video_capture.isOpened():
            print("[Exiting]: Error opening video file.")
            sys.exit(0)

        # Read the first frame
        self.grabbed, self.frame = self.video_capture.read()
        if not self.grabbed:
            print("[Exiting] No more frames to read")
            sys.exit(0)

        self.stopped = True
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True

    def start(self) -> None:
        """Start the thread to read frames from the video stream."""
        self.stopped = False
        self.thread.start()

    def update(self) -> None:
        """Continuously update the frame from the video stream."""
        #TODO count u Buradan kaldır
        temp_frame_count = 0
        while True:
            if self.stopped:
                break
            self.grabbed, self.frame = self.video_capture.read()
            # print(f"[{self.grabbed}] - streamed frames number: {temp_frame_count}")
            # predict_filename = f"outputs/temp/streamed_frame_{temp_frame_count}.jpg"
            # try:
            #     cv2.imwrite(predict_filename, self.frame)
            #     pass
            # except:
            #     pass
            temp_frame_count += 1
            if not self.grabbed:
                print("[Exiting] No more frames to read")
                self.stopped = True
                break

    def read(self):
        """Return the current frame."""
        return self.frame

    def stop(self) -> None:
        """Indicate that the thread should be stopped."""
        self.stopped = True


class VideoStreamCamRaspberry:
    """Video Stream for Rasberry Pi with ArduCam camera."""
    def __init__(self, stream_id: int = 0) -> None:
        self.stream_id = stream_id

        # opening video capture stream
        self.video_capture = cv2.VideoCapture(self.stream_id)
        if self.video_capture.isOpened() is False:
            print("[Exiting]: Error accessing cam stream.")
            sys.exit(0)
        fps_input_stream = int(self.video_capture.get(5))  # hardware fps
        print(f"FPS of input stream: {fps_input_stream}")

        # reading a single frame from vcap stream for initializing
        self.grabbed, self.frame = self.video_capture.read()
        if self.grabbed is False:
            print("[Exiting] No more frames to read")
            sys.exit(0)
        # self.stopped is initialized to False
        self.stopped = True
        # thread instantiation
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True  # daemon threads run in background

    def start(self) -> None:
        """Method to start thread."""
        self.stopped = False
        self.thread.start()

    def update(self) -> None:
        """Method passed to thread to read next available frame."""
        while True:
            if self.stopped is True:
                break
            self.grabbed, self.frame = self.video_capture.read()
            if self.grabbed is False:
                print("[Exiting] No more frames to read")
                self.stopped = True
                break
        self.video_capture.release()

    def read(self):
        """Method to return latest read frame."""
        return self.frame

    def stop(self) -> None:
        """Method to stop reading frames."""
        self.stopped = True