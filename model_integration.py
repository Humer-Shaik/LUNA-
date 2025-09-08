import torch
import os
import tempfile
import torchaudio
from transformers import pipeline
from diffusers import StableDiffusionXLPipeline
from PIL import Image

# Load Whisper-large-v3 for transcription
asr_pipeline = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-large-v3",
    device=0 if torch.cuda.is_available() else -1,
)

# Load Stable Diffusion XL for image generation
sd_pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
)
if torch.cuda.is_available():
    sd_pipe = sd_pipe.to("cuda")


def generate_images_from_audio(audio_path, num_images=2):
    """
    Takes an audio file, transcribes it with Whisper, and generates images using Stable Diffusion XL.
    Returns (list_of_image_paths, transcription_text).
    """
    try:
        # Step 1: Transcribe audio
        transcription_result = asr_pipeline(audio_path)
        transcription = transcription_result["text"].strip()

        # Step 2: Use transcription as prompt for SDXL
        prompt = f"An artistic and detailed visual representation of: {transcription}"

        images = []
        for i in range(num_images):
            img = sd_pipe(prompt, num_inference_steps=40, guidance_scale=7.5).images[0]

            # Save image
            output_dir = "generated_images"
            os.makedirs(output_dir, exist_ok=True)
            img_path = os.path.join(output_dir, f"image_{i}.png")
            img.save(img_path)
            images.append(img_path)

        return images, transcription

    except Exception as e:
        print("Error in pipeline:", str(e))
        return [], None
