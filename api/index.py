from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import json
import os

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["GET"],  # Only allow GET requests
    allow_headers=["*"],
)

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load student marks data from the same directory as this file
try:
    with open(os.path.join(current_dir, 'q-vercel-python.json')) as f:
        students_data = json.load(f)
except FileNotFoundError:
    students_data = []
    print("Warning: q-vercel-python.json not found. No student data loaded.")

@app.get("/api")
async def get_marks(name: Optional[List[str]] = Query(None)):
    """
    Get marks for one or more students by name.
    Example: /api?name=John&name=Alice
    """
    if not name:
        return {"error": "Please provide at least one name"}
    
    marks: List[Optional[int]] = []
    for student_name in name:
        # Look for the student in the data (case-insensitive)
        mark = next((student["marks"] for student in students_data 
                     if student["name"].lower() == student_name.lower()), None)
        marks.append(mark)
    
    return {"marks": marks}

@app.get("/")
async def root():
    return {"message": "Student Marks API. Use /api?name=X&name=Y to get marks."}

# Run app locally with uvicorn if called directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("index:app", host="0.0.0.0", port=8000, reload=True)
