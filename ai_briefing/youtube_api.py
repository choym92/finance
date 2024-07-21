from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse as urlparse


def get_video_id(youtube_url):
    # Parse the URL
    parsed_url = urlparse.urlparse(youtube_url)

    # Extract query parameters from the URL
    video_id = urlparse.parse_qs(parsed_url.query).get("v")

    # The video_id is a list, so return the first item
    if video_id:
        return video_id[0]
    else:
        # Handle URLs without a 'v' parameter, like youtu.be shortlinks
        if parsed_url.hostname == 'youtu.be':
            return parsed_url.path[1:]
        else:
            return None

URL = 'https://www.youtube.com/watch?v=Wo5dMEP_BbI&t=355s'

video_id = get_video_id(URL)

YouTubeTranscriptApi.get_transcript(video_id)

# Fetch the transcript
transcript = YouTubeTranscriptApi.get_transcript(video_id)

# Concatenating all the text entries into a single string
transcript_string = ' '.join([entry['text'] for entry in transcript])

transcript_string