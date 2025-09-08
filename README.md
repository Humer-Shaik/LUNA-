# LUNA – Advanced AI-Powered Visualization for Education

- LUNA is a prototype system that transforms live classroom lectures into rich, real-time visualizations using AI. The core vision is to empower educators (from grade school through PhD levels) to simply speak about a topic and watch LUNA generate detailed diagrams, animations, or illustrations on the fly.  

- For example, a biology teacher explaining the human heart could simply describe each chamber and blood flow, and LUNA would instantly produce annotated images or animations of the heart’s anatomy – eliminating manual searching and making complex concepts visible and memorable.  

- LUNA aligns with UNESCO’s call to use AI to *“address some of the biggest challenges in education”* and *“innovate teaching and learning practices”* ([unesco.org](https://unesco.org)).  

- By leveraging the latest speech-recognition and generative models, LUNA aims to amplify creativity and learning in every classroom. Studies consistently show that our brains *“are wired to process visual information more efficiently than text alone,”* and that visual aids *“significantly enhance both student engagement and long-term retention”* ([graduateprogram.org](https://graduateprogram.org)).  

- LUNA’s real-time visuals tap into this power: as one toolmaker notes, converting speech into images can enhance *“understanding, memory retention, and emotional connection to the content”* ([speechillustrator.com](https://speechillustrator.com)).

---

## Key Features

- **Speech-to-Visualization Pipeline:** Teachers speak naturally into a microphone (just as in any lecture), and LUNA’s backend immediately transcribes the speech and interprets the content. Using this input, the system generates context-appropriate images or diagrams. No manual prompting, extra apps, or keyboard input is needed during the lesson – it all happens automatically.

- **Advanced AI Models:** LUNA integrates state-of-the-art AI engines. A speech-recognition model (e.g. Whisper or Google Speech API) converts audio to text. That text is then fed into a text-to-image generative model (such as Stable Diffusion, DALL·E, or a fine-tuned domain-specific model) to create high-quality visuals. This combines natural language understanding with image synthesis.

- **Curriculum Flexibility:** LUNA supports a wide range of subjects and levels. Whether illustrating geometric theorems in middle school math, visualizing chemical reactions in high school, or drawing organ systems in university biology, the system adapts. For instance, in anatomy class it could draw labeled organs; in physics it could animate force vectors. Educators can choose or customize visual styles (diagrams, photorealistic images, cartoons, etc.) to match their curriculum.

- **Real-Time Interaction:** The system updates visuals continuously as the lecture progresses. Teachers can pause, repeat, or rephrase on the fly, and LUNA refines the image content accordingly. This creates an interactive lecture experience: students see concepts appear as they are discussed, maintaining focus and curiosity.

- **Efficiency and Personalization:** Like many AI tools for teachers, LUNA reduces preparation time. Instead of searching for graphics or drawing diagrams by hand, educators provide simple spoken prompts. Research shows that generative AI lets teachers create lesson content *“simply by providing a short prompt”* ([edutopia.org](https://edutopia.org)).  

- **Broad Accessibility:** LUNA is designed to work from elementary classrooms up through advanced seminars. The system’s interface and complexity can be tuned: younger students might see simpler, cartoonish diagrams, while graduate students might get detailed, realistic images. This universal design ensures *“every educator [can] learn about AI and leverage this technology”* to benefit students ([edutopia.org](https://edutopia.org)).

---



### Front-End (`index.html`)
The web interface runs in the teacher’s browser. It includes a microphone input button and an image display area. When the teacher speaks, client-side JavaScript captures the audio (via the Web Audio API) and streams it to the backend. The interface also allows the teacher to select visualization styles (diagram vs. photograph, etc.) or pause/resume the feed. In practice, `index.html` might use WebSockets or periodic AJAX to send short audio chunks to the server and receive generated images. This file contains HTML markup and may reference `scripts.js` to handle audio recording and display.

### Backend (`app.py`)
This Python application handles requests from the front-end. Using a web framework like Flask or FastAPI, `app.py` exposes an endpoint (e.g. `/generate`) that accepts audio data or text. The backend passes incoming audio to a speech-recognition library/API (such as OpenAI’s Whisper, Google Speech-to-Text, or another ASR engine) to get a transcript. That transcript is then fed to the model integration (next component). Finally, the generated image (or image URL) is sent back to the browser for display. The backend also manages session state (keeping track of the current scene) and can queue requests to avoid overload.

### Model Integration (`model.py`)
This module ties together the AI models. It implements a function like `generate_visual(text, style)` that takes the recognized lecture text (and any user settings) and produces an image. Internally, it might prepend or append fixed instructional prompts to ensure consistency (for example, always including the phrase “educational illustration of”). For generation, it calls a pre-trained text-to-image engine (such as Stable Diffusion via the HuggingFace Diffusers library, or the OpenAI DALL·E API). The module may also use post-processing (like adding labels or highlights) specific to educational content. All model loading and inference is done here; if large models are used, the project may recommend running on a GPU server.

### Optional Static Files
If needed, static assets like custom CSS or JS libraries would live under a `static/` folder. For a minimal prototype, most logic lives in `index.html`, `app.py`, and `model.py`.

---

## Installation & Setup

### Prerequisites
- Python 3.8+  
- GPU recommended (CPU supported, slower performance)  
- Git installed  

### Clone the Repository
```bash
git clone https://github.com/your-org/LUNA.git
cd LUNA
Create a Virtual Environment
python3 -m venv env
source env/bin/activate    # On Windows: env\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Note: 
```bash
You may need additional system packages (e.g. ffmpeg for audio processing).
If using OpenAI or other cloud APIs, set your API keys as environment variables:

export OPENAI_API_KEY=...
```

### Download/Prepare Models

If using open-source models, download them as instructed (e.g. Stable Diffusion). For Whisper or other ASR, install weights or configure API. Ensure heavy models are loaded once at server start to reduce latency.

### Run the Server
```bash
flask run --host=0.0.0.0 --port=8000
(Or python app.py if configured with if __name__ == '__main__':.)
```

### Open the Front-End

Go to:
```bash
http://localhost:8000/index.html
```
### Permissions

Grant microphone permission when prompted. Speak lecture content, and LUNA will begin generating visuals.

### Usage Example

Starting a Session: The teacher clicks “Start” and begins speaking (e.g. “This is the human heart. It has four chambers: the left atrium, right atrium, left ventricle, and right ventricle…”).
Visualization Output: Within seconds, a schematic of a heart appears with labeled chambers. As more details are described (“The aorta carries oxygenated blood out of the heart…”), the image is refined (blood flow arrows, labeled aorta).
Interactive Control: Teachers can pause, clear, or switch visualization style (schematic vs. cartoon). Beyond Biology: In geometry (triangles, circles), in history (maps), etc. — speaking directly generates context-aware images.

### Project Structure (Files)
```bash
index.html: The HTML/CSS/JS front-end. Includes a microphone toggle button, output canvas/image, and script for audio capture (via Web Audio API).
```
### app.py: Flask server, example:
```bash
from flask import Flask, request, jsonify
import model
app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    audio_data = request.files['audio']
    text = transcribe_audio(audio_data)    # use speech-to-text
    image_bytes = model.generate_visual(text, style="education")
    return jsonify({'image': encode_to_base64(image_bytes)})
```

### model.py:
```bsh
from diffusers import StableDiffusionPipeline
pipe = StableDiffusionPipeline.from_pretrained(...)

def generate_visual(prompt, style):
    full_prompt = f"{style} illustration of {prompt}"
    image = pipe(full_prompt).images[0]
    return image
```

#### requirements.txt:
```bash
Flask
diffusers
torch
whisper
numpy
pillow
```

Example Quick Start
```bash
git clone https://github.com/your-org/LUNA.git
cd LUNA
python3 -m venv env && source env/bin/activate
pip install -r requirements.txt
flask run --host=0.0.0.0 --port=8000
# Open http://localhost:8000 in your browser and speak into the mic.

```

# INTERFACE
<img width="1465" height="800" alt="Screenshot 2025-09-08 at 10 37 02 AM" src="https://github.com/user-attachments/assets/28aac4fc-5fbf-4c00-89b7-b495613237ca" />



### Sources

This project concept is inspired by recent advances in educational AI and visualization tools:
unesco.org
graduateprogram.org
speechillustrator.com
edutopia.org

### LICENSE 
This project is licensed under a Proprietary License.  
You may not copy, modify, or distribute this software without explicit written permission from the author.
