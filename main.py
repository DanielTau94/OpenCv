import cv2
from flask import Flask, render_template, request, jsonify, Response
import threading

app = Flask(__name__, static_folder='static')


class VideoStreamer:
    def __init__(self):
        self.cap1 = None
        self.cap2 = None
        self.color = True
        self.width = 1080
        self.height = 720
        self.lock = threading.Lock()  

    def _open_videos(self, video_path1, video_path2=None):
        self.cap1 = cv2.VideoCapture(video_path1)

        if not self.cap1.isOpened():
            print("Error: Video 1 not found.")
            return False

        if video_path2:
            self.cap2 = cv2.VideoCapture(video_path2)

            if not self.cap2.isOpened():
                print("Error: Video 2 not found.")
                self.cap1.release()  
                return False

        return True

    def _release_videos(self):
        if self.cap1:
            self.cap1.release()
        if self.cap2:
            self.cap2.release()

    def _read_frame(self, cap):
        with self.lock:
            ret, frame = cap.read()
        return ret, frame

    def stream_video(self, video_path):
        if not self._open_videos(video_path):
            return

        while True:
            ret, frame = self._read_frame(self.cap1)
            if not ret:
                break

            if not self.color:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            frame = cv2.resize(frame, (self.width, self.height))

            ret, buffer = cv2.imencode('.jpg', frame)
            frame_data = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

    def stream_two_videos_side_by_side(self, video_path1, video_path2):
        if not self._open_videos(video_path1, video_path2):
            return

        while True:
            ret1, frame1 = self._read_frame(self.cap1)
            ret2, frame2 = self._read_frame(self.cap2)

            if not ret1 or not ret2:
                break

            h1, w1 = frame1.shape[:2]
            h2, w2 = frame2.shape[:2]
            aspect_ratio = h1 / h2

            new_width = int(w2 * aspect_ratio)
            frame2_resized = cv2.resize(frame2, (new_width, h1))

            combined_frame = cv2.hconcat([frame1, frame2_resized])

            if not self.color:
                combined_frame = cv2.cvtColor(
                    combined_frame, cv2.COLOR_BGR2GRAY)

            combined_frame = cv2.resize(
                combined_frame, (self.width, self.height))

            ret, buffer = cv2.imencode('.jpg', combined_frame)
            frame_data = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')

    def set_color(self, color):
        self.color = (color == "color")

    def set_size(self, width, height):
        self.width = int(width)
        self.height = int(height)


vs = VideoStreamer()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/set_color", methods=["POST"])
def set_color():
    data = request.get_json()
    color = data.get("color")
    vs.set_color(color)
    return jsonify({"message": f"Color set to '{color}'."})


@app.route("/set_size", methods=["POST"])
def set_size():
    data = request.get_json()
    width = data.get("width")
    height = data.get("height")
    vs.set_size(width, height)
    return jsonify({"message": f"Size set to {width}x{height}."})


@app.route("/start_one_video_stream")
def start_one_video_stream():
    return Response(vs.stream_video("<YourPath>"), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/start_two_video_streams")
def start_two_video_streams():
    return Response(vs.stream_two_videos_side_by_side("<YourPath>", "<YourPath"), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run()
