import google.generativeai as genai
from PIL import Image
import base64
import io

genai.configure(api_key="AIzaSyDRyVRhe0_wdN1zqAI-RwOb9tb0mWZFfsE")
model = genai.GenerativeModel(
    'gemini-1.5-flash-latest',
    
    )

def call_gemini_service(request):
    
    request_json = request.get_json(silent=True)
    type = 'none'

    if request_json and 'type' in request_json:
        type = request_json['type']
        
        if type == "call_only_text_gemini" and 'prompt' in request_json:
            return call_only_text_gemini(request_json['prompt'])
        
        elif type == "call_only_img_gemini" and 'img_base64' in request_json:
            return call_only_img_gemini(request_json['img_base64'])
        
        elif type == "call_img_with_prompt_gemini" and 'img_base64' in request_json and 'prompt' in request_json:
            return call_img_with_prompt_gemini(request_json['img_base64'], request_json['prompt'])
        
        else:
            return "Error: check body"

    else:
        return "Error: no type"
    
def call_only_text_gemini(prompt):
    
    response = model.generate_content(prompt)
    
    return response.text

def call_only_img_gemini(img_base64):
    
    img_data = base64.b64decode(img_base64)
    img = Image.open(io.BytesIO(img_data))

    response = model.generate_content(img)

    return response.text

def call_img_with_prompt_gemini(img_base64, prompt):
    
    img_data = base64.b64decode(img_base64)
    img = Image.open(io.BytesIO(img_data))

    response = model.generate_content([prompt, img])

    return response.text