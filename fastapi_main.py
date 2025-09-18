# This script defines the FastAPI backend for the Smart Hiring Interview Analyzer.
# It handles video uploads and calls the core analysis logic.

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import os
import tempfile
import asyncio
from pydantic import BaseModel
from typing import Optional, Any

# Assuming the core analysis logic is in a file named `main_analyzer.py`
from main_analyzer import analyze_video

# Pydantic model for the response data
class AnalysisResult(BaseModel):
    video_analysis: dict
    speech_to_text: dict
    sentiment_analysis: dict
    confidence_score: Optional[Any] # Can be a number or a dict with an error

app = FastAPI(title="Smart Hiring Interview Analyzer API")

@app.post("/analyze_interview", response_model=AnalysisResult)
async def analyze_interview_video(file: UploadFile = File(...)):
    """
    Analyzes an uploaded video file for hiring metrics.
    
    Args:
        file (UploadFile): The video file to be analyzed.
        
    Returns:
        JSONResponse: The analysis results.
    """
    # Create a temporary file to save the uploaded video
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        try:
            # Read the file in chunks and write to disk
            contents = await file.read()
            temp_file.write(contents)
            temp_file_path = temp_file.name
        finally:
            # Close the file, but don't delete it yet
            temp_file.close()

    if not temp_file_path:
        raise HTTPException(status_code=500, detail="Could not save the uploaded file.")

    try:
        # Run the analysis in a separate thread to avoid blocking the server
        loop = asyncio.get_event_loop()
        analysis_results = await loop.run_in_executor(None, analyze_video, temp_file_path)

        return JSONResponse(content=analysis_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during analysis: {str(e)}")
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

# You can run this file with `uvicorn fastapi_main:app --reload`
if __name__ == "__main__":
    uvicorn.run("fastapi_main:app", host="0.0.0.0", port=8000, reload=True)
