import cv2
import argparse
import os

from config import Config
from detector import PersonDetector
from state_machine import TableStateMachine
from analytics import compute_metrics
from visualizer import draw
from utils import person_in_roi


def main(video_path):
    os.makedirs("outputs", exist_ok=True)

    config = Config()

    cap = cv2.VideoCapture(video_path)

    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("Cannot read video")

    roi = cv2.selectROI("Select Table", frame, False)
    cv2.destroyAllWindows()

    x, y, w, h = roi
    roi_box = (x, y, x + w, y + h)

    detector = PersonDetector(config.model_path, config.conf_threshold)
    sm = TableStateMachine(config.debounce_seconds)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(
        config.output_video,
        fourcc,
        25,
        (frame.shape[1], frame.shape[0]),
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0

        boxes = detector.detect(frame)

        person_present = person_in_roi(
            boxes, roi_box, config.iou_threshold
        )

        sm.update(timestamp, person_present)

        frame = draw(frame, roi, sm.state)

        out.write(frame)

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

    avg_delay = compute_metrics(sm.events, config.output_csv)

    if avg_delay:
        print(f"Average delay: {avg_delay:.2f} sec")
    else:
        print("Not enough data")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)

    args = parser.parse_args()

    main(args.video)