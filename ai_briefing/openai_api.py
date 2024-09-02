from openai import OpenAI

from dotenv import load_dotenv
import os
# Load environment variables from the .env file
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')



client = OpenAI(
    # This is the default and can be omitted
    api_key=OPENAI_API_KEY,
)

TEXT = "The economic landscape is marked by a striking contrast between strong fundamental indicators and public sentiment. Despite near-record low unemployment, robust job creation, and significant economic growth fueled by consumer spending, a palpable disconnect exists as many Americans remain skeptical of the economy's strength. This skepticism is mirrored in the financial sector, where there's a notable shift towards safe haven assets like gold, driven by investors seeking stability amid uncertainties."

response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=TEXT,
)

streamed_response = response.with_streaming_response()

# Now, use the streamed_response to write to a file
# Assuming `response` contains the binary audio data from the TTS request
with open("output.mp3", "wb") as file:
    file.write(response.content)