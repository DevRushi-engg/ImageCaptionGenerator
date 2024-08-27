import requests
from flask import Flask, render_template, request, jsonify

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/generate', methods=['POST'])
    def generate():
        data = request.get_json()
        prompt = data.get('prompt')

        # Hugging Face API setup
        api_url = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
        headers = {"Authorization": f"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"}

        # Make the API call for image generation
        response = requests.post(api_url, headers=headers, json={"inputs": prompt})
        image_data = response.content

        # Save the image locally
        image_path = "static/generated_image.png"
        with open(image_path, "wb") as f:
            f.write(image_data)

        # Return the image URL
        image_url = f"/{image_path}"
        caption = f"Generated caption for: {prompt}"

        return jsonify({'image_url': image_url, 'caption': caption})

    return app
