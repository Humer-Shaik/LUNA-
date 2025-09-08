from flask import Flask, render_template, request, redirect, flash
import os
import base64
from datetime import datetime
from model_integration import generate_images_from_audio

app = Flask(__name__)
app.secret_key = "luna_secret"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    images = []
    transcription = None

    if request.method == "POST":
        audio_data = request.form.get("audio")
        if not audio_data:
            flash("No audio data received")
            return redirect(request.url)

        try:
            # Extract base64 string (remove header: "data:audio/wav;base64,")
            if "," in audio_data:
                audio_data = audio_data.split(",")[1]

            audio_bytes = base64.b64decode(audio_data)

            # Save to file with timestamp
            filename = f"recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            with open(filepath, "wb") as f:
                f.write(audio_bytes)

            # Pass file path to ML pipeline
            images, transcription = generate_images_from_audio(filepath)

        except Exception as e:
            flash(f"Error processing audio: {str(e)}")
            return redirect(request.url)

    return render_template("index.html", images=images, transcription=transcription)


if __name__ == "__main__":
    app.run(debug=True)
