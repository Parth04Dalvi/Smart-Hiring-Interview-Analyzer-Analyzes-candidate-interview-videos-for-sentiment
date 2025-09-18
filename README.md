# Smart-Hiring-Interview-Analyzer-Analyzes-candidate-interview-videos-for-sentiment
Smart Hiring Interview Analyzer
This project is a proof-of-concept for a smart hiring tool that analyzes candidate interview videos. It breaks down an interview video to provide objective metrics on a candidate's performance, including sentiment, speech clarity, and confidence.

Features
Video Processing: Utilizes OpenCV to handle video streams and analyze visual cues.

Speech-to-Text: Employs OpenAI's Whisper model to accurately transcribe spoken words from the interview audio.

Sentiment & Emotion Analysis: Uses a pre-trained PyTorch model to detect the emotional tone of the candidate's speech.

API Backend: Built with FastAPI to serve the analysis logic and handle video uploads.

Dashboard: A Streamlit dashboard provides a user-friendly interface to upload videos and view the analysis results.

Technology Stack
Python

OpenCV: Video frame processing.

Whisper: Speech-to-text transcription.

PyTorch: Deep learning for sentiment and emotion analysis.

FastAPI: High-performance API.

Streamlit: Interactive web dashboard.

Getting Started
1. Prerequisites
Ensure you have Python 3.8 or newer installed. This project also requires the command-line tool ffmpeg for audio processing.

Install FFmpeg:

On Ubuntu or Debian:

sudo apt update && sudo apt install ffmpeg

On MacOS (using Homebrew):

brew install ffmpeg

On Windows (using Chocolatey):

choco install ffmpeg

2. Setup
Clone this repository to your local machine:

git clone [https://github.com/your-username/smart-hiring-analyzer.git](https://github.com/your-username/smart-hiring-analyzer.git)
cd smart-hiring-analyzer

Create and activate a virtual environment:

# On Unix or MacOS
python -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate

Install the required Python packages:

pip install -r requirements.txt

3. Usage
The core logic is contained in main_analyzer.py. This script demonstrates the individual components of the analysis pipeline.

To run the complete application, you will need to set up the FastAPI backend and the Streamlit frontend.

FastAPI Backend (Conceptual)
You would create a main.py for FastAPI to define an endpoint that accepts a video file. This endpoint would then call the functions from main_analyzer.py to perform the analysis and return a JSON response.

Streamlit Dashboard (Conceptual)
You would create an app.py for Streamlit. This app would provide a file uploader widget, a button to trigger the analysis (by calling your FastAPI endpoint), and a section to display the results returned from the API.

Project Structure
smart-hiring-analyzer/
├── main_analyzer.py       # Core analysis logic (OpenCV, Whisper, PyTorch)
├── requirements.txt       # Project dependencies
└── README.md              # This file
