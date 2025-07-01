# S25CameraSystem
 A multi-tool project for detecting and analyzing High Dynamic Range (HDR)

# HDR Capture Detector

A multi-tool project for detecting and analyzing High Dynamic Range (HDR) image captures on Android devices. This repository includes:

-  **Android App**: Logs device camera capabilities and memory usage to a Markdown file.
-  **Python Script**: Monitors `logcat` for HDR events and saves pre-trigger logs.
-  **MATLAB Script**: Analyzes image dynamic range and contrast to infer HDR likelihood.

---

## Components

### 1. `MainActivity.kt`
- Queries `CameraCharacteristics` and system memory stats.
- Prompts user to save logs as a `.md` file.
- Supports Android 13+ HDR profile inspection.

### 2. `AndroidManifest.xml`
- Declares camera and storage permissions.
- Registers `MainActivity` with proper intent filters.

### 3. `logcat_hdr_monitor.py`
- Monitors `adb logcat` in real time.
- Triggers on HDR-related keywords (e.g., `Exposure`).
- Notifies macOS via `osascript` and saves buffered logs.

### 4. `analyze_hdr_image.m`
- Loads images from local folder.
- Computes dynamic range, local contrast, and bit depth.
- Heuristically scores images on HDR likelihood (0–4 scale).
- Visualizes histogram and local contrast map.

---

##  Quick Start

### Android App
1. Build and deploy the app using Android Studio.
2. Grant camera permission.
3. Select save location when prompted.
4. Review generated `camera_hdr_memory_log.md`.

### Python Script
```bash
python logcat_hdr_monitor.py
