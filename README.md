# Magic Voice Switch

## Overview

Magic Voice Switch is a project inspired by a popular [Instagram video](https://www.instagram.com/reel/C4j-rE4S3Qe/?igsh=NDZsc3VuNWw4djZk) where magic words like "開damn~~" and "關damn~~" are used to control lights. Although the video was proven to involve manual control, this project aims to bring the idea to life by using voice commands to control lights.

The project supports two modes:
1. **Machine Learning Mode**: Uses a model trained with Teachable Machine to recognize specific magic words.
2. **Speech-to-Text (STT) Mode**: Recognizes similar sounding words to classify them into categories.

### Categories
- 0: Background Noise
- 1: 開damn
- 2: 開燈
- 3: 關damn
- 4: 關燈

## Future Plans
- Integrate with Raspberry Pi to control physical LED lights.
- Develop a more visually appealing web interface for cloud deployment.

## Dependencies

#### Audio Processing
- `librosa`
- `numpy`
- `PyAudio`

#### Speech Recognition
- `SpeechRecognition`
- `openai`

#### Machine Learning and AI
- `tensorflow`

#### Environment Management
- `python-dotenv`

## Setup Instructions

### Build `venv` for **MacOS**

Mac should `brew install portaudio` at first to install `PyAudio`.

```shell
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ deactivate
$ rm -rf venv     # remove the venv
```

### Build `venv` for **Windows**
```shell
$ pip install virtualenv
$ virtualenv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
$ deactivate
$ rmdir /s venv     # remove the venv
```

## Running the Project
Run the following command to start the voice recognition loop:

`python main.py`

You will be prompted to choose the mode:

1. If you choose **Model**, the system will use the trained model for recognition.
2. If you choose **STT**, you will be prompted to choose between Google or OpenAI for speech-to-text processing.
