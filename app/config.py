from dataclasses import dataclass


@dataclass
class Config:
    model_path: str = "yolov8n.pt"
    iou_threshold: float = 0.1
    conf_threshold: float = 0.4

    output_video: str = "outputs/output.mp4"
    output_csv: str = "outputs/events.csv"

    debounce_seconds: float = 1.0