from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
import time
from PIL import Image

def create_app():
    app = Flask(__name__, static_folder='../static', static_url_path='/static')

    IMAGE_FILENAME = "generated_image.png"

    def requests_retry_session(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 503, 504),
        session=None,
    ):
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/generate', methods=['POST'])
    def generate():
        data = request.get_json()
        prompt = data.get('prompt')

        # Input validation
        if not prompt or len(prompt.strip()) == 0:
            return jsonify({'error': "Prompt cannot be empty."}), 400
        if len(prompt) > 100:
            return jsonify({'error': "Prompt is too long. Please use fewer than 100 characters."}), 400

        api_url = "https://api-inference.huggingface.co/models/davisbro/half_illustration"
        headers = {"Authorization": f"Bearer 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"}

        try:
            response = requests_retry_session().post(api_url, headers=headers, json={"inputs": prompt}, timeout=60)
            response.raise_for_status()
            image_data = response.content
        except requests.exceptions.Timeout:
            app.logger.error("Request timed out.")
            return jsonify({'error': "The request took too long. Please try again later."}), 504
        except requests.exceptions.TooManyRedirects:
            app.logger.error("Too many redirects.")
            return jsonify({'error': "The service encountered too many redirects. Please try again later."}), 500
        except requests.exceptions.RequestException as e:
            app.logger.error(f"Failed to generate image: {str(e)}")
            return jsonify({'error': "Failed to generate image. The service might be temporarily unavailable. Please try again later."}), 503

        image_path = os.path.join(app.static_folder, IMAGE_FILENAME)
        try:
            with open(image_path, "wb") as f:
                f.write(image_data)
        except IOError as e:
            app.logger.error(f"Failed to save image: {str(e)}")
            return jsonify({'error': "Failed to save the generated image. Please try again."}), 500

        return jsonify({
            'image_url': f'/static/{IMAGE_FILENAME}?t={int(time.time())}',
            'caption': f"Generated caption for: {prompt}"
        })

    @app.route('/static/<path:filename>')
    def custom_static(filename):
        return send_from_directory(app.static_folder, filename)

    return app
