from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from tempfile import NamedTemporaryFile

import google.genai as genai
from google.genai import types

# Set your Gemini API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyDSUWTCJ1t7PWUONwTaqrs6gUBB45vZ_ZQ"

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-vercel-app.vercel.app",  # Replace with your actual Vercel domain
        "https://*.vercel.app"  # Allow all Vercel subdomains
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_file_size(file_bytes):
    return len(file_bytes)

@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):
    video_bytes = await file.read()
    file_size = get_file_size(video_bytes)
    client = genai.Client()
    prompt = (
        "Watch the video and extract the exact recipe being made. "
        "Return the recipe name, a list of ingredients with quantities, the step-by-step method, serving size, and any other relevant details. "
        "IMPORTANT: If you cannot determine exact quantities from the video, provide reasonable estimates based on typical recipe proportions and cooking practices. "
        "For example: "
        "- If you see 'add some oil' but can't see the exact amount, estimate '2 tablespoons oil' "
        "- If you see 'season with salt' but no specific amount, estimate '1/2 teaspoon salt' "
        "- If you see 'add a pinch of spice' but can't see the amount, estimate '1/4 teaspoon' "
        "- If serving size is not clear, estimate based on the ingredients and cooking method shown "
        "- For ingredients like 'garlic' without quantity, estimate '2-3 cloves' or '1 tablespoon minced' "
        "- For 'to taste' ingredients, provide a starting amount like '1/4 teaspoon' "
        "Do NOT use 'No quantity specified' or 'Not specified' - always provide reasonable estimates. "
        "Format the response as structured JSON with keys: 'recipe_name', 'ingredients', 'method', 'serving_size', and 'additional_notes'."
    )
    model = "models/gemini-2.5-flash-preview-05-20"
    try:
        if file_size < 20 * 1024 * 1024:  # <20MB, send inline
            response = client.models.generate_content(
                model=model,
                contents=types.Content(
                    parts=[
                        types.Part(
                            inline_data=types.Blob(
                                data=video_bytes,
                                mime_type=file.content_type or "video/mp4"
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
        return JSONResponse(content={
            "status": "success",
            "gemini_response": response.text
        })
    except Exception as e:
        return JSONResponse(content={
            "status": "error",
            "error": str(e)
        }, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 