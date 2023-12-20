import os
from flask import Flask, render_template, request
import PIL
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure generative AI
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_story', methods=['POST'])
def generate_story():
    if 'image' not in request.files:
        return "No image file provided in the request."

    image = PIL.Image.open(request.files['image'].stream)
    vision_model = genai.GenerativeModel('gemini-pro-vision')

    try:
        response = vision_model.generate_content(["Write a 100 words story from the Picture", image])
        story = response.text  # Adjust this line based on the actual structure of the response
        return render_template('story.html', story=story)
    except Exception as e:
        return render_template('error.html', error_message=str(e))

if __name__ == '__main__':
    app.run(debug=True)

