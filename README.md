```markdown
# EyeGazeAlert: Real-Time Assistive Eye-Tracking & Notification System for Motor-Impaired Patients

An embedded, low-cost computer vision notification system designed to assist patients with Amyotrophic Lateral Sclerosis (ALS) and severe motor disabilities in communicating urgent help requests to caregivers using eye gaze and blink dynamics.

This repository contains the complete open-source Python software stack, hardware configuration guidelines, and experimental evaluation scripts for a dual-camera Raspberry Pi 4 setup that operates reliably in real-time under low-light and variable patient positioning conditions.

---

## Repository Structure

```text
EyeGazeAlert/
├── core/                                      # Core computer vision and hardware control modules
│   ├── Camera_1.py                            # Main detection loop for primary camera input (left eye processing)
│   ├── Camera_2.py                            # Main detection loop for secondary camera input (right eye processing)
│   ├── gaze.py                                # Gaze direction computation and iris whitening ratio calculation
│   ├── blink.py                               # Eyelid aspect ratio and blinking detection routines
│   ├── dimensions.py                          # Dynamic resolution and frame sizing helper utilities
│   ├── variables.py                           # System calibration, GPIO pin configuration, and threshold limits
│   └── led.py                                 # GPIO controller for RGB visual status indicators
├── config/                                    # System configuration and calibration variables
│   └── shape_predictor_81_face_landmarks.dat
├── assets/                                    # Audio assets and helper scripts
│   └── sound.py                               # Asynchronous audio alert player using WAV files
├── scripts/                                   # Master execution scripts
│   └── run_me_eye_gaze.sh                     # Master execution script orchestrating the end-to-end system
├── .gitignore                                 # Ignores local model weights (*.dat), audio files, and cache
└── README.md

```

---

## Motivation & Clinical Objective

Patients suffering from late-stage **Amyotrophic Lateral Sclerosis (ALS)** experience progressive muscle atrophy, leading to loss of vocalization and physical movement. Because extraocular muscles remain functional throughout the progression of the disease, eye movement offers a crucial communication gateway.

`EyeGazeAlert` serves as a digital "cry for help" system for non-verbal patients. It features:

* **Dual Alert Triggers:**
1. **Intentional Blink Sequence:** Two deliberate blinks trigger an audible spoken request ("Help please").
2. **Sustained Gaze Focus:** Continuous focus on a camera module for a set duration triggers a high-intensity emergency alarm.


* **Low-Cost Accessibility:** Built using off-the-shelf webcams, Raspberry Pi GPIO, and open-source libraries (`dlib`, `OpenCV`), avoiding proprietary $1,000+ eye-tracking hardware.
* **Low-Light Operation:** Modified webcams with Infrared/LED visual status lights allow nighttime monitoring during patient therapy or sleep.

---

## Hardware Architecture & Setup

The system integrates low-cost hardware components managed via a central micro-controller:

* **Processing Unit:** Raspberry Pi 4 Model B (8GB RAM, Broadcom BCM2711 @ 1.5GHz).
* **Optical Sensors:** Dual Turbo-X W21 1080p webcams positioned at calibrated angles toward the patient's eyes.
* **Feedback System:**
* **Status LEDs:** 5V RGB LEDs connected via GPIO (Green = Ideal Position, Blue = Blink Warning, Red = Alarm Warning).
* **Audio Output:** External 6W speakers playing synthetic speech or loud alarms.



```text
               ┌────────────────────────┐
               │    Power Supply (5V)   │
               └───────────┬────────────┘
                           ▼
┌──────────────┐   ┌─────────────────┐   ┌─────────────┐
│  Camera 1    ├──►│  Raspberry Pi 4 │──►│   RGB LEDs  │
│  Camera 2    ├──►│ (Microcontroller)├──►│   Speakers  │
└──────────────┘   └─────────────────┘   └─────────────┘

```

---

## Software Methodology & Signal Processing

The system extracts 81 facial landmarks using a customized `dlib` shape predictor model (`shape_predictor_81_face_landmarks.dat`) to isolate eye regions:

### 1. Whitening Ratio (Gaze Focus)

Measures the ratio of sclera (white pixels) to pupil region within the segmented eye bounding box (`core/gaze.py`).

* **Ideal Threshold:** A Whitening Ratio score within `[0.55, 0.60]` indicates the patient's gaze is centered directly at the sensor.

### 2. Blinking Ratio (Blink Detection)

Calculates the ratio between the horizontal eye distance and the vertical Euclidean distance between upper/lower eyelid landmarks (`core/blink.py`):


$$\text{Blinking Ratio} = \frac{\text{Euclidean Length (Horizontal)}}{\text{Euclidean Length (Vertical)}}$$

* **Thresholding:** Values exceeding `[2.3, 2.5]` register an intentional eyelid closure (blink).

---

## Experimental Evaluation & Calibration

System stability was evaluated across **45 real-world laboratory configurations** combining 3 patient bed positions (**Seated**, **Supine/Back**, and **Lateral/Side**), 5 vertical distances (1.0m to 3.0m), and 3 camera inclination angles ($45^\circ$, $60^\circ$, and $75^\circ$).

### Optimal Parameter Windows

| Patient Position | Camera Angle | Whitening Ratio Threshold (Gaze) | Blinking Ratio Threshold (Blink) |
| --- | --- | --- | --- |
| **Seated** | **75°** | `[0.40, 0.70]` | `[2.00, 2.70]` |
| **Supine (Back)** | **75°** | `[0.50, 0.60]` | `[2.20, 2.70]` |
| **Lateral (Side)** | **75°** | `[0.55, 0.60]` | `[2.30, 2.50]` |
| **Global Intersection** | **75°** | **`[0.55, 0.60]`** | **`[2.30, 2.50]`** |

> **Key Finding:** A camera inclination angle of **75°** provides total separation between active/resting states across all distances up to 3.0 meters, preventing false positives during sleep or involuntary eye flutter.

---

## Quick Start & Installation

### 1. Requirements

* **OS:** Linux (Ubuntu 20.04 LTS / Raspberry Pi OS)
* **Python Version:** 3.7+

### 2. Dependencies

Install required Python packages and system libraries:

```bash
sudo apt-get update
sudo apt-get install python3-opencv libdlib-dev libwiringpi-dev libasound2-dev
pip install wiringpi simpleaudio dlib numpy opencv-python

```

### 3. Model Weights

Download the 81-landmark model file and place it in your path:

```bash
# Ensure shape_predictor_81_face_landmarks.dat is located at your working directory or path

```

### 4. Execution

Run the system using the master execution script:

```bash
bash scripts/run_me_eye_gaze.sh

```

---

## 📜 Authors & Academic Citation

Developed at the **Technical University of Crete (TUC)** in collaboration with:

* **SenseLab Space Informatics Laboratory** (School of Mineral Resources Engineering)
* **Micro-cutting & Manufacturing Simulation Laboratory** (School of Production Engineering and Management)

**Author:** Nikolaos Kanakis

**Supervisors:** Prof. Aristomenis Antoniadis, Assoc. Prof. Panagiotis Partsinevelos

*Chania, Greece (2021)*

```

```