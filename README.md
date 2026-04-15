---
title: AnemiaSense
emoji: 🩸
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
---

# Anemia Detection from Palm and ECG Data 🩸🖐🏻

This project aims to detect anemia utilizing image-based datasets (like palm images) applying Convolutional Neural Networks (CNN). The repository is currently extending its scope to also ingest ECG data to perform comprehensive anemia classification.

## Features
- **Binary Classification**: Diagnoses whether a sample is `Anemic` or `Non-anemic`.
- **Custom CNN Architecture**: Built natively using TensorFlow and Keras. Includes robust normalization, downsampling, and regularization techniques (Dropout) to prevent overfitting during training. 
- **Image Augmentation**: Real-time data augmentation (rotations, zooms, flips, shifts) via Keras `ImageDataGenerator` to improve model generalization over small datasets.
- **Callbacks Strategy**: Incorporates `EarlyStopping` preventing wasteful epoch runs and `ReduceLROnPlateau` enabling delicate loss tracking convergence.

## Project Structure
```text
.
├── .gitignore              # Ignores local datasets and models from being pushed
├── README.md               # You are here
├── requirements.txt        # Identifies the Python dependencies
├── src/                    
│   └── train_cnn.py        # Centralized script to run the advanced model training
├── data/                   # (Not tracked) Expected dataset folder containing `Anemic` & `Non-anemic` images
├── ecg/                    # (Not tracked) ECG data folder encompassing ptbdb_normal.csv
└── archive/                # Deprecated Jupyter notebooks
```

## Setup Instructions

### 1. Requirements
Ensure you have Python configured correctly. Preferably, set up a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
# Or on Windows:
# .\venv\Scripts\activate
```

Next, install the required packages:
```bash
pip install -r requirements.txt
```

### 2. Dataset Preparation
Ensure your data is organized such that `anemia_code/data/` contains exactly two folders:
- `Anemic/`
- `Non-anemic/`

Populate these folders with the corresponding Palm image classes. Note that these are excluded from Git to avoid clogging the repository size.

For the **ECG implementation (WIP)**, the directory `ecg/` naturally encompasses comma-separated files such as `ptbdb_normal.csv`.

### 3. Training the Model
From the root directory, simply run:
```bash
python src/train_cnn.py
```
Outputs from this script include a `best_anemia_cnn_model.keras` which saves your best weights during runtime, a `final_anemia_cnn_model.keras`, and finally a generated `training_history.png` depicting accuracy bounds over intervals.

## Future Plans (WIP)
- Extending models to accommodate and process inputs stemming from `ptbdb_normal.csv` via the `ecg/` folder infrastructure.
- Potentially applying Transfer Learning topologies (such as MobileNetV2) if palm data variability continues to rise.
