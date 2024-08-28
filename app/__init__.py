from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os

def create_app():
    app = Flask(__name__, static_folder='../static', static_url_path='/static')

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/generate', methods=['POST'])
    def generate():
        data = request.get_json()
        prompt = data.get('prompt')

        api_url = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
        headers = {"Authorization": f"Bearer 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"}

        response = requests.post(api_url, headers=headers, json={"inputs": prompt})
        image_data = response.content

        image_filename = "generated_image.png"
        image_path = os.path.join(app.static_folder, image_filename)
        with open(image_path, "wb") as f:
            f.write(image_data)

        return jsonify({
            'image_url': f'/static/{image_filename}',
            'caption': f"Generated caption for: {prompt}"
        })

    @app.route('/static/<path:filename>')
    def custom_static(filename):
        return send_from_directory(app.static_folder, filename)

    return app