# imports
import time
from pathlib import Path
import cv2
from matplotlib import pyplot as plt

from video_stream import VideoStream
from video_stream import VideoStreamCamRaspberry
from anomalib.deploy import OpenVINOInferencer

class AnomalyDetector:
    """Class for anomaly detection from a video file."""

    def __init__(self, video_path: str, model_path: Path, metadata_path: Path):
        self.video_stream = VideoStream(video_path)
        self.inferencer = OpenVINOInferencer(
            path=model_path,
            metadata=metadata_path,
            device="CPU"
        )

    def process_video(self):
        """Process the video and perform anomaly detection."""
        self.video_stream.start()
        start_time = time.time()
        frame_count = 0

        while not self.video_stream.stopped:
            frame = self.video_stream.read()
            if frame is None:
                break

            # Process frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            predictions = self.inferencer.predict(image=frame_rgb)
            # print(f"proccesed frame count: {frame_count}, Prediction Score: {predictions.pred_score}")
            filename = f"outputs/frame_{frame_count}.jpg"
            predict_filename = f"outputs/predict_frame_{frame_count}.jpg"

            cv2.imwrite(filename, frame)
            cv2.imwrite(predict_filename, predictions.pred_mask)

            frame_count += 1

        end_time = time.time()
        fps = frame_count / (end_time - start_time)
        print(f"Processed {frame_count} frames at {fps:.2f} FPS")

        self.video_stream.stop()

# Create an instance of the AnomalyDetector
#detector = AnomalyDetector(video_path="path_to_video.mp4", model_path=openvino_model_path, metadata_path=metadata_path)
#detector.process_video()


class AnomalyDetectorRaspberry:
    """Class for anomaly detection from a video file."""

    def __init__(self, stream_id: int, model_path: Path, metadata_path: Path):
        self.video_stream = VideoStreamCamRaspberry(stream_id)
        self.inferencer = OpenVINOInferencer(
            path=model_path,
            metadata=metadata_path,
            device="CPU"
        )

    def process_video(self):
        """Process the video and perform anomaly detection."""
        self.video_stream.start()
        start_time = time.time()
        frame_count = 0

        while not self.video_stream.stopped:
            frame = self.video_stream.read()
            if frame is None:
                break

            # Process frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            predictions = self.inferencer.predict(image=frame)
            # print(f"proccesed frame count: {frame_count}, Prediction Score: {predictions.pred_score}")
            filename = f"outputs/frame_{frame_count}.jpg"
            predict_filename = f"outputs/predict_frame_{frame_count}.jpg"

            cv2.imwrite(filename, frame)
            cv2.imwrite(predict_filename, predictions.pred_mask)

            frame_count += 1

        end_time = time.time()
        fps = frame_count / (end_time - start_time)
        print(f"Processed {frame_count} frames at {fps:.2f} FPS")

        self.video_stream.stop()
