import os
import json
import csv
import glob
from pathlib import Path
from tempfile import NamedTemporaryFile
import google.genai as genai
from google.genai import types

# Set your Gemini API key (same as in main.py)
os.environ["GOOGLE_API_KEY"] = "AIzaSyDSUWTCJ1t7PWUONwTaqrs6gUBB45vZ_ZQ"

def get_file_size(file_bytes):
    """Get the size of file bytes in bytes"""
    return len(file_bytes)

def analyze_video_file(video_path):
    """
    Analyze a single video file using the same logic as the FastAPI backend
    
    Args:
        video_path (str): Path to the video file
        
    Returns:
        dict: Analysis result with status and response/error
    """
    try:
        # Read video file
        with open(video_path, 'rb') as f:
            video_bytes = f.read()
        
        file_size = get_file_size(video_bytes)
        client = genai.Client()
        
        prompt = (
            "Watch the video and extract the exact recipe being made. "
            "Return the recipe name, a list of ingredients with quantities, the step-by-step method, serving size, and any other relevant details. "
            "Format the response as structured JSON with keys: 'recipe_name', 'ingredients', 'method', 'serving_size', and 'additional_notes'."
        )
        
        model = "models/gemini-2.5-flash-preview-05-20"
        
        if file_size < 20 * 1024 * 1024:  # <20MB, send inline
            response = client.models.generate_content(
                model=model,
                contents=types.Content(
                    parts=[
                        types.Part(
                            inline_data=types.Blob(
                                data=video_bytes,
                                mime_type="video/mp4"
                            )
                        ),
                        types.Part(text=prompt)
                    ]
                )
            )
        else:
            # Save to temp file for upload
            with NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                tmp.write(video_bytes)
                tmp_path = tmp.name
            
            myfile = client.files.upload(file=tmp_path)
            response = client.models.generate_content(
                model=model,
                contents=[myfile, prompt]
            )
            os.remove(tmp_path)
        
        return {
            "status": "success",
            "gemini_response": response.text
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def parse_json_response(response_text):
    """
    Parse the JSON response from Gemini and extract structured data
    
    Args:
        response_text (str): Raw response text from Gemini
        
    Returns:
        dict: Parsed recipe data
    """
    try:
        # Try to extract JSON from the response
        # Sometimes Gemini wraps JSON in markdown code blocks
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            json_str = response_text[start:end].strip()
        elif "```" in response_text:
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            json_str = response_text[start:end].strip()
        else:
            json_str = response_text.strip()
        
        return json.loads(json_str)
    except Exception as e:
        # If parsing fails, return the raw response
        return {
            "recipe_name": "Parse Error",
            "ingredients": [],
            "method": [],
            "serving_size": "Unknown",
            "additional_notes": f"Failed to parse JSON: {str(e)}. Raw response: {response_text[:200]}..."
        }

def process_video_folder(folder_path):
    """
    Process all video files in the specified folder
    
    Args:
        folder_path (str): Path to folder containing videos
    """
    # Video file extensions to process
    video_extensions = ['*.mp4', '*.mov', '*.avi', '*.mkv', '*.wmv', '*.flv', '*.webm']
    
    # Find all video files
    video_files = []
    for ext in video_extensions:
        video_files.extend(glob.glob(os.path.join(folder_path, ext)))
        video_files.extend(glob.glob(os.path.join(folder_path, ext.upper())))
    
    if not video_files:
        print(f"No video files found in {folder_path}")
        return
    
    print(f"Found {len(video_files)} video files to process")
    
    # Prepare CSV data
    csv_data = []
    
    # Process each video
    for i, video_path in enumerate(video_files, 1):
        video_name = os.path.basename(video_path)
        print(f"\nProcessing {i}/{len(video_files)}: {video_name}")
        
        # Analyze video
        result = analyze_video_file(video_path)
        
        if result["status"] == "success":
            # Parse the JSON response
            recipe_data = parse_json_response(result["gemini_response"])
            
            # Add file info to recipe data
            recipe_data["video_file"] = video_name
            recipe_data["video_path"] = video_path
            
            # Save individual JSON file
            json_filename = os.path.splitext(video_name)[0] + "_recipe.json"
            json_path = os.path.join(folder_path, json_filename)
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(recipe_data, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Saved JSON: {json_filename}")
            
            # Prepare CSV row
            csv_row = {
                "video_file": video_name,
                "recipe_name": recipe_data.get("recipe_name", ""),
                "ingredients": str(recipe_data.get("ingredients", [])),
                "method": str(recipe_data.get("method", [])),
                "serving_size": recipe_data.get("serving_size", ""),
                "additional_notes": recipe_data.get("additional_notes", ""),
                "status": "success"
            }
            
        else:
            print(f"✗ Error: {result['error']}")
            
            # Add error row to CSV
            csv_row = {
                "video_file": video_name,
                "recipe_name": "",
                "ingredients": "",
                "method": "",
                "serving_size": "",
                "additional_notes": f"Error: {result['error']}",
                "status": "error"
            }
        
        csv_data.append(csv_row)
    
    # Save CSV file
    csv_path = os.path.join(folder_path, "recipe_analysis_results.csv")
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ["video_file", "recipe_name", "ingredients", "method", "serving_size", "additional_notes", "status"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"\n✓ Processing complete!")
    print(f"✓ CSV results saved to: {csv_path}")
    print(f"✓ Individual JSON files saved in: {folder_path}")

if __name__ == "__main__":
    # Main folder path containing videos
    main_video_folder = "/Users/benjaminhawkins/Documents/Downloaded videos for gemini test 2"
    instapot_folder = os.path.join(main_video_folder, "Instapot specific")
    
    # Process main folder
    if os.path.exists(main_video_folder):
        print(f"Starting batch processing of videos in: {main_video_folder}")
        process_video_folder(main_video_folder)
    else:
        print(f"Error: Main folder not found: {main_video_folder}")
        exit(1)
    
    # Process Instapot specific subfolder
    if os.path.exists(instapot_folder):
        print(f"\n" + "="*60)
        print(f"Starting batch processing of videos in: {instapot_folder}")
        print("="*60)
        process_video_folder(instapot_folder)
    else:
        print(f"Warning: Instapot folder not found: {instapot_folder}")
    
    print(f"\n" + "="*60)
    print("ALL PROCESSING COMPLETE!")
    print("="*60) 