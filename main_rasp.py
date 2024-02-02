from pathlib import Path

from anomaly_detection import AnomalyDetectorRaspberry

def main():
    # Paths for the model and metadata
    weights_path = Path.cwd() / "results/padim/mvtec/carpet/run/weights"
    openvino_model_path = weights_path / "openvino" / "model.bin"
    metadata_path = weights_path / "openvino" / "metadata.json"
    stream_id = 0  # Update this path to your video file
    detector = AnomalyDetectorRaspberry(stream_id=stream_id, model_path=openvino_model_path, metadata_path=metadata_path)
    detector.process_video()

if __name__ == "__main__":
    main()
