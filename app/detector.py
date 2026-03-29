from ultralytics import YOLO


class PersonDetector:
    def __init__(self, model_path: str, conf_threshold: float):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold

    def detect(self, frame):
        results = self.model(frame, verbose=False)[0]

        boxes = []

        for r in results.boxes:
            cls = int(r.cls[0])
            conf = float(r.conf[0])

            if cls == 0 and conf > self.conf_threshold:
                x1, y1, x2, y2 = map(int, r.xyxy[0])
                boxes.append((x1, y1, x2, y2))

        return boxes