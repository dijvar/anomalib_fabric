from pathlib import Path

from anomaly_detection import AnomalyDetector

def main():
    # Paths for the model and metadata
    weights_path = Path.cwd() / "results/padim/mvtec/carpet/run/weights"
    openvino_model_path = weights_path / "openvino" / "model.bin"
    metadata_path = weights_path / "openvino" / "metadata.json"
    video_path = "datasets/test_videos/test1.mp4"  # Update this path to your video file
    detector = AnomalyDetector(video_path=video_path, model_path=openvino_model_path, metadata_path=metadata_path)
    detector.process_video()

if __name__ == "__main__":
    main()
