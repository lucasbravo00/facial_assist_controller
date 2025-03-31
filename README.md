# Face Recognition Attendance System

This is a simple facial recognition program that simulates an attendance control system using a webcam. It compares captured faces with pre-stored images located in the `Employees` folder. Users can fill this folder with images of their preferred faces for recognition.

By default, the `Employees` folder contains test faces of famous characters for demonstration purposes.

## Features
- Uses a webcam to capture real-time images.
- Detects and encodes faces using the `face_recognition` library.
- Compares detected faces with stored employee images.
- Logs recognized employees with timestamps in `log.csv`.
- Draws a rectangle around detected faces and displays names.

## Installation

Ensure you have Python installed, then install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Place images of the people to be recognized inside the `Employees` folder.
2. Run the program:
   
   ```bash
   python face_recognition_attendance.py
   ```
3. The webcam will capture an image and attempt to recognize a face.
4. If a match is found, the name will be displayed, and the entry will be logged in `log.csv`.
5. If no match is found, the program will notify that the person is not registered.

## Notes
- The `Employees` folder must contain images with clear and well-lit faces for better accuracy.
- The threshold for recognition is set at `0.6` (lower values make recognition stricter, higher values make it more lenient).
- The program currently works only with one face at a time.

## Dependencies
- `opencv-python`
- `face-recognition`
- `numpy`

## License
This is a simple educational project and is provided as-is without any warranties.
