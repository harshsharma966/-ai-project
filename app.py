import os
import gradio as gr
from datetime import datetime

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs

system_prompt = """You have to act as a professional doctor, I know you are not but this is for learning purpose. 
With what I see, I think you have .... Don’t add any numbers or special characters in your response. 
Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please."""

def process_inputs(audio_filepath, image_filepath):
    groq_api_key = os.environ.get("GROQ_API_KEY")
    
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY environment variable not set.")

    speech_to_text_output = transcribe_with_groq(
        "whisper-large-v3", 
        audio_filepath,
        groq_api_key
    )

    # Handle NoneType from speech transcription
    if not speech_to_text_output:
        speech_to_text_output = ""

    if image_filepath:
        doctor_response = analyze_image_with_query(
            query=system_prompt + speech_to_text_output,
            encoded_image=encode_image(image_filepath),
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "No image provided for me to analyze."

    # Generate output audio
    output_audio_path = f"output_audio_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
    text_to_speech_with_elevenlabs(input_text=doctor_response, output_filepath=output_audio_path)

    return speech_to_text_output, doctor_response, output_audio_path

# Gradio interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        
        gr.Textbox(label="Doctor's Response"),
        
        gr.Audio(label="Doctor's Voice")
    ],
    title="AI Doctor with Vision and Voice",
    allow_flagging="never",
)

iface.launch(debug=True)
