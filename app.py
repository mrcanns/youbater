import yt_dlp
import pygame
import json
import os
from fuzzywuzzy import process

def start_music(name):
    pygame.mixer.init()
    pygame.mixer.music.load(name)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def download_video_as_mp3(video_url):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        print("MP3 downloaded successfully!")
    except Exception as e:
        print(f"Error: {e}")

def play_playlist():
    with open("playlist.json", "r") as file:
        playlist = json.load(file)

    print("Playing playlist...")
    for mp3_file in playlist:
        print(f"Playing Music: {mp3_file}")
        start_music(mp3_file)

def search_and_play_music(part):
    with open("playlist.json", "r") as file:
        playlist = json.load(file)
    best_match = process.extractOne(part, playlist)

    if best_match and best_match[1] > 80:
        print(f"Found music: {best_match[0]}")
        start_music(best_match[0])
    else:
        print("No match found.")

def main():
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "-p":
            play_playlist()
        elif sys.argv[1] == "-play" and len(sys.argv) > 2:
            search_and_play_music(sys.argv[2])
        else:
            print("Invalid parameter!")
    else:
        video_url = input("Enter YouTube video URL: ")
        download_video_as_mp3(video_url)
        
if __name__ == "__main__":
    main()

