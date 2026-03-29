import cv2


def draw(frame, roi, state):
    x, y, w, h = roi

    color = (0, 255, 0) if state == "EMPTY" else (0, 0, 255)

    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    cv2.putText(
        frame,
        state,
        (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        color,
        2,
    )

    return frame