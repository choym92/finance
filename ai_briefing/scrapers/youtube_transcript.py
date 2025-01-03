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

def fetch_transcript(video_id: str) -> str:
    """
    Fetches and concatenates the transcript of a YouTube video.

    Parameters:
    video_id (str): The ID of the YouTube video.

    Returns:
    str: The concatenated transcript text.
    """
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_string = ' '.join([entry['text'] for entry in transcript])
    return transcript_string

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
    with open(f"{file_path}/{safe_title}.txt", 'w', encoding='utf-8') as file:
        file.write(transcript)

def get_youtube_trainscript(URL, output_dir, title=None):
    # get video_id
    video_id = get_video_id(URL)
    if not video_id:
        print("Invalid Youtube URL:", URL)
        return
    
    # get video title if title is not defined
    if title is None:
        print("Title not defined. Getting video title from Youtube...")
        title = get_video_title(video_id)

    transcript = fetch_transcript(video_id)
    save_transcript_to_file(transcript, output_dir, title)
    print(f'Transcript saved to {output_dir}{title}.txt')


def main():
    URL = 'https://www.youtube.com/watch?v=dI_TmTW9S4c&t=3881s'
    output_path_dir = '/Users/youngmincho/Documents/Youtube Transcripts/'
    
    get_youtube_trainscript(URL, output_path_dir)

if __name__ == "__main__":
    main()
