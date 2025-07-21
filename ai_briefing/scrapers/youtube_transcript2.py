import os
import re
import urllib.parse as urlparse
import requests
from bs4 import BeautifulSoup
from typing import Optional
# CORRECTED IMPORT STATEMENT:
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

def get_video_id(youtube_url: str) -> Optional[str]:
    """
    Extracts the video ID from various YouTube URL formats.
    """
    parsed_url = urlparse.urlparse(youtube_url)
    
    # Standard URL: https://www.youtube.com/watch?v=VIDEO_ID
    if 'v' in urlparse.parse_qs(parsed_url.query):
        return urlparse.parse_qs(parsed_url.query)["v"][0]
        
    # Short URL: https://youtu.be/VIDEO_ID
    elif parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
        
    # Embed URL: https://www.youtube.com/embed/VIDEO_ID
    elif parsed_url.path.startswith('/embed/'):
        return parsed_url.path.split('/')[2]
        
    return None

def get_video_title(video_id: str) -> str:
    """
    Fetches the title of the YouTube video using its video ID.
    Returns a default title on failure.
    """
    try:
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        response = requests.get(video_url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title').text
        return title.replace('- YouTube', '').strip()
    except requests.RequestException as e:
        print(f"Could not fetch video title due to a network error: {e}")
        return f"Video (ID {video_id})" # Return a fallback title

def fetch_transcript(video_id: str) -> Optional[str]:
    """
    Fetches the English transcript for a given video ID, preferring manual
    over auto-generated.
    """
    print("Fetching available transcripts...")
    try:
        # Get a list of all available transcripts.
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # Find the best English transcript from the list.
        # The library handles checking for 'en', 'en-US', etc.
        transcript = transcript_list.find_transcript(['en'])
        
        print(f"Found transcript: {transcript.language_code} "
              f"({'Auto-generated' if transcript.is_generated else 'Manual'})")
              
        # Fetch the full transcript data and join the text segments.
        transcript_data = transcript.fetch()
        transcript_text = ' '.join([entry['text'] for entry in transcript_data])
        return transcript_text
        
    except TranscriptsDisabled:
        print("Error: Transcripts are disabled for this video.")
        return None
    except NoTranscriptFound:
        print("Error: No English transcript could be found for this video.")
        return None
    except Exception as e:
        print(f"An unexpected API error occurred: {e}")
        return None

def save_transcript_to_file(transcript: str, dir_path: str, title: str) -> None:
    """
    Saves the transcript to a specified file path with a sanitized title.
    """
    # Sanitize the title to create a valid filename
    safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)
    filename = os.path.join(dir_path, f"{safe_title}.md")
    
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(f"# {title}\n\n{transcript}")
        print(f"Transcript saved successfully to: {filename}")
    except IOError as e:
        print(f"Error saving file: {e}")

def get_youtube_transcript_from_url(url: str, output_dir: str):
    """
    Main controller function to process a URL and save its transcript.
    """
    print(f"--- Processing URL: {url} ---")
    video_id = get_video_id(url)
    
    if not video_id:
        print("Error: Invalid or unsupported YouTube URL.")
        return
    
    print(f"Extracted Video ID: {video_id}")
    
    # Get video title
    title = get_video_title(video_id)
    print(f"Video Title: {title}")

    # Fetch transcript
    transcript = fetch_transcript(video_id)
    
    # Save to file if transcript was successfully fetched
    if transcript:
        save_transcript_to_file(transcript, output_dir, title)
    else:
        print("Could not save file because no transcript was fetched.")

def main():
    URL = 'https://www.youtube.com/watch?v=okHkUIW46ks'
    
    # Save to a "transcripts" sub-folder in the same directory as the script
    output_path_dir = 'transcripts'
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_path_dir):
        print(f"Creating output directory: {output_path_dir}")
        os.makedirs(output_path_dir)
    
    get_youtube_transcript_from_url(URL, output_path_dir)

if __name__ == "__main__":
    main()
