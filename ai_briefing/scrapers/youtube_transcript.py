from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse as urlparse
import requests
from bs4 import BeautifulSoup
from typing import Optional

def get_video_id(youtube_url: str) -> Optional[str]:
    """
    Extracts the video ID from a YouTube URL.

    Parameters:
    youtube_url (str): The URL of the YouTube video.

    Returns:
    Optional[str]: The video ID if found, otherwise None.
    """
    parsed_url = urlparse.urlparse(youtube_url)
    video_id = urlparse.parse_qs(parsed_url.query).get("v")
    
    if video_id:
        return video_id[0]
    elif parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    else:
        return None

def get_video_title(video_id: str) -> str:
    """
    Fetches the title of the YouTube video using its video ID.

    Parameters:
    video_id (str): The ID of the YouTube video.

    Returns:
    str: The title of the video.
    """
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    response = requests.get(video_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('title').text
    return title.replace('- YouTube', '').strip()

from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound

def fetch_transcript(video_id: str) -> Optional[str]:
    """
    Attempts to fetch the transcript in English (manual or auto-generated).
    """
    try:
        # Try manually uploaded English transcript first
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        return ' '.join([entry['text'] for entry in transcript])
    except Exception as e:
        print(f"First attempt (manual 'en') failed: {e}")
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            try:
                # Try to get a manually created English transcript
                transcript = transcript_list.find_transcript(['en'])
            except NoTranscriptFound:
                # Fallback: Try to get auto-generated English transcript
                transcript = transcript_list.find_generated_transcript(['en'])
            return ' '.join([entry['text'] for entry in transcript.fetch()])
        except Exception as e2:
            print(f"Second attempt (auto 'en') failed: {e2}")
            return None

    
def list_available_transcripts(video_id: str):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        for transcript in transcript_list:
            print(f"Available transcript: {transcript.language} ({transcript.language_code}), generated: {transcript.is_generated}")
    except Exception as e:
        print(f"Error listing transcripts: {e}")

def save_transcript_to_file(transcript: str, file_path: str, title: str) -> None:
    """
    Saves the transcript to a specified file path with the video title.

    Parameters:
    transcript (str): The transcript text to be saved.
    file_path (str): The directory path where the file will be saved.
    title (str): The title of the video to be used as the filename.

    Returns:
    None
    """
    safe_title = title.replace('/', '-').replace('\\', '-')  # Ensure valid filename
    with open(f"{file_path}/{safe_title}.md", 'w', encoding='utf-8') as file:
        file.write(f"# {title}\n\n{transcript}")  # Markdown formatted content

def get_youtube_transcript(URL, output_dir, title=None):
    # get video_id
    video_id = get_video_id(URL)
    if not video_id:
        print("Invalid Youtube URL:", URL)
        return
    
    # get video title if title is not defined
    if title is None:
        print("Title not defined. Getting video title from Youtube...")
        title = get_video_title(video_id)
        print(title)

    # **NEW: List available transcripts**
    list_available_transcripts(video_id)

    transcript = fetch_transcript(video_id)
    save_transcript_to_file(transcript, output_dir, title)
    print(f'Transcript saved to {output_dir}/{title}.md')


def main():
    URL = 'https://www.youtube.com/watch?v=bBvPQZmPXwQ'
    output_path_dir = '/Users/youngmincho/Documents/Youtube Transcripts/'
    output_path_dir = '/Users/youngmincho/Library/Mobile Documents/iCloud~md~obsidian/Documents/Note/03. Archives/Youtube Transcripts'
    
    get_youtube_transcript(URL, output_path_dir)

if __name__ == "__main__":
    main()