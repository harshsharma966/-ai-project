import os
from gtts import gTTS

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)


input_text= " ram ram pandat ji "
text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")

#Step1b: Setup Text to Speech–TTS–model with ElevenLabs
import elevenlabs
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY=os.environ.get("ELEVENLABS_API_KEY")

def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio=client.generate(
        text= input_text,
        voice= "Aria",
        output_format= "mp3_22050_32",
        model= "eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)

#text_to_speech_with_elevenlabs_old(input_text, output_filepath="elevenlabs_testing.mp3") 

#Step2: Use Model for Text output to Voice


import os
import subprocess
import platform
from pydub import AudioSegment
from gtts import gTTS

def text_to_speech_with_gtts(input_text, output_filepath="output.mp3", language="en"):
    """Generate speech using gTTS and play it across different OS."""
    try:
        # Generate MP3 file
        gTTS(text=input_text, lang=language, slow=False).save(output_filepath)

        # Determine OS and play the file
        os_name = platform.system()
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath], check=True)
        elif os_name == "Windows":  # Windows requires WAV format
            wav_filepath = output_filepath.replace(".mp3", ".wav")
            AudioSegment.from_mp3(output_filepath).export(wav_filepath, format="wav")
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();'], check=True)
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath], check=True)  # Alternative: 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    
    except subprocess.CalledProcessError as e:
        print(f"Failed to play audio: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_text = "john bnega don muje rokega kon"
text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")

import os
import subprocess
import platform
from pydub import AudioSegment
import elevenlabs
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

def text_to_speech_with_elevenlabs(input_text, output_filepath="output.mp3"):
    """Generate speech using ElevenLabs API and play it across different OS."""
    try:
        # Load environment variables
        load_dotenv()
        api_key = os.getenv("ELEVENLABS_API_KEY")
        client = ElevenLabs(api_key=api_key)

        # Generate speech
        audio = client.generate(
            text=input_text,
            voice="Aria",
            output_format="mp3_22050_32",
            model="eleven_turbo_v2"
        )
        elevenlabs.save(audio, output_filepath)

        # Play audio based on OS
        os_name = platform.system()
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath], check=True)
        elif os_name == "Windows":  # Windows requires WAV format
            wav_filepath = output_filepath.replace(".mp3", ".wav")
            AudioSegment.from_mp3(output_filepath).export(wav_filepath, format="wav")
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();'], check=True)
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath], check=True)  # Alternative: 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    
    except subprocess.CalledProcessError as e:
        print(f"Failed to play audio: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# # Example usage
# text_to_speech_with_elevenlabs(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")

