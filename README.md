# TurretGuard - Autonomous Drowning Detection & Response System

An intelligent water safety system that combines computer vision, machine learning, and robotics to automatically detect drowning incidents and provide immediate response through an automated water rescue turret. 

## Overview

TurretGuard is an innovative safety solution developed for HackThe6ix that addresses the critical issue of drowning prevention. The system uses real-time computer vision to monitor water areas, detect drowning incidents, and automatically deploy rescue equipment through a servo-controlled turret system.

### Key Features

- **Real-time Drowning Detection**: AI-powered computer vision using YOLO and Edge Impulse models
- **Automated Response System**: Servo-controlled turret that can deploy rescue equipment
- **Multi-platform Integration**: OpenMV camera system with Arduino motor control
- **Live Dashboard**: Real-time monitoring interface with camera feed and system status
- **Low-latency Processing**: Optimized for immediate response times in emergency situations

## System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   OpenMV H7     │───▶│  Arduino Uno     │───▶│  Servo Turret   │
│  (AI Vision)    │    │ (Motor Control)  │    │   System        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Dashboard GUI  │    │ Serial Protocol  │    │ Rescue Device   │
│   (Monitoring)  │    │  Communication   │    │   Deployment    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## AI Models & Detection

### YOLO Model (`best.pt`)
- Custom-trained YOLOv8 model for drowning detection
- Trained on 1615+ image samples at 96x96 resolution
- Classes detected:
  - Person drowning
  - Person in water
  - Person NOT in water
  - Various watercraft (boats, kayaks, surfboards)

### Edge Impulse FOMO Model
- Fast Object Motion Detection using MobileNetV2 0.35
- Optimized for real-time processing on OpenMV H7
- 4 feature class segmentations
- 60-epoch architecture with GPU training
- RAM-optimized EON compiler integration

## Project Structure

```
torret_hackthe6ix/
├── AI & Computer Vision
│   ├── best.pt                      # Trained YOLO model weights
│   ├── clean_and_train_yolo.py      # YOLO training pipeline
│   ├── merge_yolo_datasets.py       # Dataset preprocessing
│   ├── inference_low_fps.py         # Video inference testing
│   └── kid_drowning.mp4            # Test video sample
│
├── OpenMV Camera System
│   ├── drowning_detection_system.py # Main Edge Impulse detection
│   ├── master_drowning_detection_system.py # Complete detection pipeline
│   ├── dashboard_detection.py       # Dashboard integration
│   ├── init_contour.py             # Contour initialization
│   ├── labels.txt                  # Model class labels
│   └── constants.txt               # System constants
│
├── Arduino Control System
│   ├── arduino_sketches/
│   │   ├── motorTesting/           # Motor control testing
│   │   ├── servoTesting/           # Servo control testing
│   │   └── read_serial/            # Serial communication
│   └── arduino_serial.py           # Python-Arduino bridge
│
├── Control Interface
│   ├── dashbaord.py                # Main GUI dashboard
│   ├── camera_listener.py          # Camera data monitoring
│   └── requirements.txt            # Python dependencies
│
└── Documentation
    └── README.md                   # This file
```

## Getting Started

### Prerequisites

**Hardware:**
- OpenMV H7 Camera Plus
- Arduino Uno/Nano
- Servo motors (for turret control)
- DC motors (for device deployment)
- USB cables for serial communication

**Software:**
- Python 3.8+
- OpenMV IDE
- Arduino IDE

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pekachoo/torret_hackthe6ix.git
   cd torret_hackthe6ix
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Upload Arduino sketches:**
   - Open Arduino IDE
   - Upload the appropriate sketch from `arduino_sketches/` to your Arduino

4. **Configure OpenMV camera:**
   - Open OpenMV IDE
   - Upload the Edge Impulse model and scripts from `OpenMV/` directory
   - Ensure `trained.tflite` and `labels.txt` are on the OpenMV storage

### Usage

1. **Start the main control system:**
   ```bash
   python arduino_serial.py
   ```

2. **Launch the monitoring dashboard:**
   ```bash
   python dashbaord.py
   ```

3. **Test video inference (optional):**
   ```bash
   python inference_low_fps.py
   ```

## Configuration

### Serial Port Configuration
Update the following in your Python scripts based on your system:

```python
# Arduino connection
ARDUINO_PORT = '/dev/ttyUSB0'  # Update for your system
ARDUINO_BAUD = 9600

# OpenMV camera connection  
CAM_PORT = '/dev/ttyACM0'      # Update for your system
CAM_BAUD = 115200
```

### Detection Sensitivity
Adjust detection parameters in the OpenMV scripts:

```python
min_confidence = 0.5  # Minimum confidence for detection
```

## System Performance

- **Detection Latency**: < 200ms
- **Camera Resolution**: 320x240 (QVGA)
- **Processing Window**: 240x240 optimized
- **Model Accuracy**: 85%+ on test dataset
- **Real-time FPS**: 1-5 FPS (configurable)

## Hardware Setup

### Turret Assembly
1. Mount servos for azimuth and elevation control
2. Attach rescue device deployment mechanism
3. Connect Arduino to servo control pins
4. Wire DC motors for device launching

### Camera Positioning
1. Mount OpenMV camera with clear water view
2. Ensure stable power supply
3. Position for optimal detection coverage

## Troubleshooting

**Common Issues:**

- **Serial Connection Problems**: Check port permissions and device connections
- **Model Loading Errors**: Ensure `.tflite` and `labels.txt` are on OpenMV storage
- **Detection Accuracy**: Adjust lighting conditions and camera positioning
- **Motor Control Issues**: Verify Arduino pin connections and power supply

## Contributing

This project was developed during HackThe6ix. Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License. OpenMV components retain their original licensing.

## Acknowledgments

- **HackThe6ix** - Hackathon platform
- **Edge Impulse** - AI model training platform
- **OpenMV** - Computer vision hardware and software
- **Ultralytics** - YOLO implementation

## Safety Notice

This system is a prototype developed for educational and demonstration purposes. While designed with safety in mind, it should not be used as the sole water safety measure. Always ensure proper human supervision and certified safety equipment are present in aquatic environments.

---

**Made with ❤️ for water safety at HackThe6ix 2025**
