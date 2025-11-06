# 👁️ Visora - Vision Assistance System

<div align="center">

**AI-powered computer vision for the visually impaired**

Real-time object detection with audio navigation guidance

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green.svg)](https://opencv.org/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-red.svg)](https://github.com/ultralytics/ultralytics)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.18+-orange.svg)](https://streamlit.io/)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture)
- [Requirements](#-requirements)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**Visora** is an intelligent vision assistance system designed to help visually impaired individuals navigate their environment safely and independently. The system uses state-of-the-art computer vision technology (YOLOv8) to detect objects in real-time and provides immediate audio feedback with directional guidance.

### Key Capabilities

- **Real-time Object Detection**: Detects 80+ different object classes using YOLOv8
- **Audio Navigation**: Provides spoken directional guidance (e.g., "Person detected at front-right, close")
- **Dual Interface**: Available as both a web application (Streamlit) and command-line interface
- **Smart Directional System**: Divides the camera view into 8 directional sectors for precise navigation
- **Cross-platform Support**: Works on Windows, Linux, and macOS

---

## ✨ Features

### 🎥 Real-time Vision Processing

- Live camera feed processing with OpenCV
- High-performance object detection using YOLOv8
- Configurable confidence and IOU thresholds
- Support for multiple camera backends (DirectShow, Media Foundation, V4L2)

### 🔊 Audio Guidance

- Text-to-speech announcements for detected objects
- Directional information (center, front-right, right, back-right, back, back-left, left, front-left)
- Distance indicators (very close, close, moderate distance, far away)
- Asynchronous audio processing to avoid blocking

### 🧭 Navigation Assistance

- Intelligent object prioritization (persons prioritized over other objects)
- 8-sector directional system for precise location reporting
- Distance calculation based on object position relative to frame center
- Context-aware navigation instructions

### 🌐 Web Interface

- Modern, accessible Streamlit-based web interface
- Real-time video feed with object annotations
- Single image detection mode
- Interactive configuration panel
- Responsive design with custom styling

### 💻 Command-Line Interface

- Lightweight CLI mode for resource-constrained environments
- Keyboard controls (press 'q' to quit)
- Console logging for debugging
- Minimal overhead for maximum performance

---

## 🚀 Installation

### Prerequisites

- **Python 3.8+** (Python 3.9+ recommended)
- **Webcam/Camera** connected to your computer
- **Windows 10/11**, **Linux**, or **macOS**

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/visora.git
cd visora
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download YOLOv8 Model

The YOLOv8 model (`yolov8n.pt`) should already be included in the repository. If not, it will be automatically downloaded on first run.

---

## ⚡ Quick Start

### Web Interface (Recommended)

**Windows:**

```bash
run_web.bat
```

**Linux/macOS:**

```bash
python -m streamlit run app/web_interface.py
```

The web interface will automatically open in your default browser at `http://localhost:8501`

### Command-Line Interface

**Windows:**

```bash
run_cli.bat
```

**Linux/macOS:**

```bash
python -m app.main --mode cli
```

Press `q` to quit the CLI application.

---

## 📖 Usage

### Web Interface Mode

1. **Launch the application** using `run_web.bat` or the Streamlit command
2. **Configure settings** in the sidebar:
   - Adjust confidence threshold (0.0 - 1.0)
   - View navigation guide
   - Access troubleshooting tips
3. **Single Image Detection**:
   - Click "Browse files" to upload an image
   - Or use the camera input to capture a photo
   - View detected objects with annotations
4. **Real-time Detection**:
   - The system automatically starts real-time detection
   - View live video feed with object annotations
   - Listen to audio announcements
   - Click "Stop Detection" to pause

### CLI Mode

1. **Launch the application** using `run_cli.bat` or the Python command
2. **View the camera feed** with object annotations
3. **Listen to audio announcements** for detected objects
4. **Press 'q'** to quit the application

### Navigation Guide

The system divides the camera view into 8 directional sectors:

- **Center**: Directly ahead
- **Front-right/Left**: Slightly to the side
- **Right/Left**: To the side
- **Back-right/Left**: Behind and to the side
- **Back**: Directly behind

Distance indicators:

- **Very close**: Object is very near the center
- **Close**: Object is relatively close
- **Moderate distance**: Object is at medium distance
- **Far away**: Object is far from the center

---

## ⚙️ Configuration

### Environment Variables

You can configure the system using environment variables:

```bash
# Model configuration
MODEL_NAME=yolov8n.pt              # YOLOv8 model file
CONFIDENCE_THRESHOLD=0.5           # Detection confidence threshold (0.0-1.0)
IOU_THRESHOLD=0.45                 # Intersection over Union threshold

# Camera configuration
CAMERA_SOURCE=0                    # Camera device index
CAMERA_BACKEND=dshow               # Camera backend (dshow, msmf, v4l2, auto)
FRAME_WIDTH=640                    # Frame width in pixels
FRAME_HEIGHT=480                   # Frame height in pixels

# Navigation configuration
DIRECTION_SECTORS=8                # Number of directional sectors
OBJECT_DISTANCE_THRESHOLD=50       # Distance threshold in pixels

# Streamlit configuration
STREAMLIT_PORT=8501                # Web interface port
```

### Configuration File

Edit `app/config.py` to change default settings:

```python
# Model configuration
CONFIDENCE_THRESHOLD = 0.5
IOU_THRESHOLD = 0.45

# Camera configuration
CAMERA_SOURCE = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Navigation configuration
DIRECTION_SECTORS = 8
OBJECT_DISTANCE_THRESHOLD = 50
```

---

## 📁 Project Structure

```
visora/
├── app/
│   ├── __init__.py           # Package initialization
│   ├── main.py               # Main entry point
│   ├── config.py             # Configuration management
│   ├── vision.py             # Object detection (YOLOv8)
│   ├── audio.py              # Text-to-speech engine
│   ├── navigation.py         # Navigation assistance
│   └── web_interface.py      # Streamlit web interface
├── yolov8n.pt                # YOLOv8 nano model (lightweight)
├── requirements.txt           # Python dependencies
├── run_cli.bat               # CLI launcher (Windows)
├── run_web.bat               # Web launcher (Windows)
├── test_camera.py            # Camera testing script
├── test_components.py        # Component testing script
└── README.md                 # This file
```

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│  ┌──────────────┐              ┌──────────────┐         │
│  │  Web (Streamlit) │          │  CLI (OpenCV) │        │
│  └──────────────┘              └──────────────┘         │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                    Main Controller                       │
│                    (app/main.py)                         │
└─────────────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Vision      │ │  Navigation  │ │   Audio      │
│  (YOLOv8)    │ │  Assistant   │ │   Manager    │
└──────────────┘ └──────────────┘ └──────────────┘
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  Camera      │ │  Direction   │ │  TTS Engine  │
│  (OpenCV)    │ │  Calculator  │ │  (pyttsx3)   │
└──────────────┘ └──────────────┘ └──────────────┘
```

### Data Flow

1. **Camera Capture**: OpenCV captures frames from the camera
2. **Object Detection**: YOLOv8 processes frames and detects objects
3. **Direction Calculation**: Navigation assistant calculates object position and direction
4. **Audio Announcement**: Audio manager converts text to speech and announces
5. **Visual Feedback**: Annotated frames displayed in UI (web/CLI)

---

## 📦 Requirements

### Python Packages

- `ultralytics>=8.0.0` - YOLOv8 object detection
- `torch>=1.13.0` - PyTorch deep learning framework
- `torchvision>=0.14.0` - Computer vision utilities
- `opencv-python>=4.5.0` - Camera and image processing
- `numpy>=1.21.0` - Numerical operations
- `streamlit>=1.18.0` - Web interface framework
- `pyttsx3>=2.90` - Text-to-speech engine
- `pillow>=9.0.0` - Image processing

### System Requirements

- **CPU**: Multi-core processor recommended
- **RAM**: Minimum 4GB, 8GB+ recommended
- **GPU**: Optional (CUDA-compatible GPU for faster inference)
- **Camera**: USB webcam or built-in camera
- **Audio**: Speakers or headphones for audio feedback

---

## 🔧 Troubleshooting

### Camera Issues

**Problem**: Camera not detected or cannot be accessed

**Solutions**:

1. Ensure no other application is using the camera
2. Check camera permissions in system settings
3. Try a different camera if available
4. Restart your computer
5. Check camera drivers in Device Manager (Windows)
6. Try different camera backends:
   ```python
   # In config.py, change:
   CAMERA_BACKEND = "msmf"  # or "dshow", "v4l2", "auto"
   ```

### Audio Issues

**Problem**: No audio announcements

**Solutions**:

1. Check system volume settings
2. Verify audio output device is connected
3. Test TTS engine:
   ```python
   import pyttsx3
   engine = pyttsx3.init()
   engine.say("Test")
   engine.runAndWait()
   ```
4. On Linux, install required TTS packages:
   ```bash
   sudo apt-get install espeak
   ```

### Performance Issues

**Problem**: Slow detection or high CPU usage

**Solutions**:

1. Reduce frame resolution in `config.py`:
   ```python
   FRAME_WIDTH = 320
   FRAME_HEIGHT = 240
   ```
2. Increase confidence threshold to reduce detections:
   ```python
   CONFIDENCE_THRESHOLD = 0.7
   ```
3. Use GPU acceleration (if available):
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

### Model Loading Issues

**Problem**: YOLOv8 model not found

**Solutions**:

1. Ensure `yolov8n.pt` is in the project root directory
2. The model will be automatically downloaded on first run
3. Check internet connection for automatic download
4. Manually download from [Ultralytics](https://github.com/ultralytics/ultralytics)

### Import Errors

**Problem**: Module not found errors

**Solutions**:

1. Ensure virtual environment is activated
2. Reinstall requirements:
   ```bash
   pip install -r requirements.txt --upgrade
   ```
3. Check Python version (3.8+ required):
   ```bash
   python --version

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/visora.git
cd visora

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install development dependencies
pip install -r requirements.txt

# Run tests
python test_components.py
python test_camera.py
```

### Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Keep functions focused and modular
