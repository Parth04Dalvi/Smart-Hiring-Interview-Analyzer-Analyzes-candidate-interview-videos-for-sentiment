# This script defines the Streamlit dashboard for the Smart Hiring Interview Analyzer.
# It provides a user interface to upload videos and display the analysis results.

import streamlit as st
import requests
import json
import base64
import time

# Function to display a loading animation while the API call is in progress
def show_loading_animation():
    st.markdown("""
        <style>
        .loader {
            border: 8px solid #f3f3f3;
            border-radius: 50%;
            border-top: 8px solid #3498db;
            width: 60px;
            height: 60px;
            -webkit-animation: spin 2s linear infinite;
            animation: spin 2s linear infinite;
        }
        @-webkit-keyframes spin {
            0% { -webkit-transform: rotate(0deg); }
            100% { -webkit-transform: rotate(360deg); }
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
        <div class="loader"></div>
        """, unsafe_allow_html=True)
    st.write("Analyzing your video. This may take a few moments...")

# Streamlit UI
st.set_page_config(page_title="Hiring Interview Analyzer", layout="wide")

st.title("Smart Hiring Interview Analyzer")
st.markdown("Upload a video of a candidate interview to receive a detailed analysis on their performance.")

uploaded_file = st.file_uploader("Choose a video file...", type=['mp4', 'mov', 'avi'])

if uploaded_file is not None:
    st.video(uploaded_file, format="video/mp4")

    if st.button("Analyze Video"):
        if uploaded_file is None:
            st.error("Please upload a video file first.")
        else:
            # Display loading animation
            show_loading_animation()
            st.session_state.processing = True

            # Prepare the file for sending
            files = {'file': uploaded_file.getvalue()}
            api_url = "http://localhost:8000/analyze_interview" # Change to your FastAPI URL

            try:
                # Send the file to the FastAPI backend
                response = requests.post(api_url, files=files)
                
                # Clear the loading animation
                st.empty()

                if response.status_code == 200:
                    analysis_report = response.json()
                    st.success("Analysis complete!")
                    st.header("Analysis Report")
                    
                    # Store the report in session state to persist the display
                    st.session_state.analysis_report = analysis_report
                    st.session_state.uploaded_file = uploaded_file

                    # Display the report with improved structure
                    col1, col2 = st.columns(2)

                    with col1:
                        st.subheader("Key Insights")
                        st.markdown(f"**Confidence Score:** {analysis_report['confidence_score']:.2f}%")
                        st.progress(analysis_report['confidence_score'] / 100)
                        
                        st.markdown(f"**Overall Sentiment:** {analysis_report['sentiment_analysis']['sentiment_label']}")
                        st.markdown(f"**Primary Emotion:** {analysis_report['sentiment_analysis']['emotion_label']}")

                    with col2:
                        st.subheader("Interview Transcript")
                        st.text_area("Transcript", analysis_report['speech_to_text']['full_transcript'], height=300)
                    
                    st.markdown("---")

                    # Use expanders to organize detailed metrics
                    with st.expander("Detailed Metrics: Sentiment & Emotion"):
                        sentiment = analysis_report['sentiment_analysis']['sentiment_label']
                        sentiment_score = analysis_report['sentiment_analysis']['sentiment_score']
                        emotion = analysis_report['sentiment_analysis']['emotion_label']
                        emotion_score = analysis_report['sentiment_analysis']['emotion_score']
                        
                        st.metric(label="Overall Sentiment", value=f"{sentiment} ({sentiment_score:.2f})")
                        st.metric(label="Primary Emotion", value=f"{emotion} ({emotion_score:.2f})")
                        st.markdown("The sentiment score reflects the positive/negative tone of the words used, while the emotion metric provides a more nuanced emotional state.")

                    with st.expander("Detailed Metrics: Video & Speech"):
                        st.markdown(f"**Face Detection:** {analysis_report['video_analysis']['face_detection_percentage']:.2f}% of the time")
                        st.markdown(f"**Eye Contact:** {analysis_report['video_analysis']['eye_contact_percentage']:.2f}% of the time")
                        st.markdown("These percentages are calculated by analyzing the number of video frames where a face and eyes were detected, respectively, out of the total video frames.")

                else:
                    st.error(f"Error during analysis: {response.status_code} - {response.text}")
            
            except requests.exceptions.ConnectionError as e:
                st.empty()
                st.error("Could not connect to the FastAPI backend. Please ensure the API is running and accessible.")
                st.write(f"Error: {e}")
            except Exception as e:
                st.empty()
                st.error(f"An unexpected error occurred: {e}")

if st.session_state.get('analysis_report'):
    with st.expander("Show Raw JSON Response"):
        st.json(st.session_state.analysis_report)
    
    if st.button("Clear App"):
        # Clear the session state to reset the app
        st.session_state.clear()
        st.experimental_rerun()
