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

        # Placeholder for image and caption generation
        # For now, return a dummy image URL and caption
        image_url = "https://via.placeholder.com/300"
        caption = f"Generated caption for: {prompt}"

        return jsonify({'image_url': image_url, 'caption': caption})

    return app
