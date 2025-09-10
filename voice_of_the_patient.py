import os
import base64
import logging
from dotenv import load_dotenv
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from groq import Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Records audio from the microphone and saves it as an MP3 file.

    Args:
        file_path (str): Path to save the recorded audio file.
        timeout (int): Max time to wait for a phrase to start (seconds).
        phrase_time_limit (int): Max time for a phrase to be recorded (seconds).
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            
            # Record audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            # Convert recorded audio to MP3
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

def transcribe_with_groq(stt_model, audio_filepath, api_key):
    """
    Transcribes an audio file using Groq's Whisper model.

    Args:
        stt_model (str): Whisper model name.
        audio_filepath (str): Path to the audio file.
        api_key (str): API key for Groq.

    Returns:
        str: Transcribed text.
    """
    client = Groq(api_key=api_key)

    try:
        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )
        return transcription.text
    except Exception as e:
        logging.error(f"Error in transcription: {e}")
        return None

if __name__ == "__main__":
    audio_filepath = "patient_voice_test_for_patient.mp3"
    record_audio(file_path=audio_filepath)

    if GROQ_API_KEY:
        transcription = transcribe_with_groq("whisper-large-v3", audio_filepath, GROQ_API_KEY)
        if transcription:
            logging.info(f"Transcription: {transcription}")
    else:
        logging.error("GROQ_API_KEY is missing! Make sure it's set in the environment.")
