from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import ffmpeg
import os
import time
import argparse

def download_bbb_recording(recording_url, output_number):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Initialize the driver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Get the recording page
        driver.get(recording_url)
        
        # Wait for the page to load and extract the meeting ID
        meeting_id = recording_url.split('/')[-1]
        base_url = '/'.join(recording_url.split('/')[:-4])
        
        # Construct the deskshare and audio URLs
        deskshare_url = f"{base_url}/presentation/{meeting_id}/deskshare/deskshare.webm"
        audio_url = f"{base_url}/presentation/{meeting_id}/video/webcams.webm"
        
        # Use numbered filenames
        deskshare_file = f"deskshare_{output_number}.webm"
        audio_file = f"webcams_{output_number}.webm"
        mp4_file = f"video_{output_number:02d}.mp4"  # Using 02d for padding with zeros
        
        # Download the deskshare webm file
        print("Downloading deskshare.webm...")
        response = requests.get(deskshare_url, stream=True)
        
        if response.status_code == 200:
            with open(deskshare_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Download the audio webm file
            print("Downloading webcams.webm...")
            response = requests.get(audio_url, stream=True)
            if response.status_code == 200:
                with open(audio_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                # Combine video and audio using ffmpeg
                print("Converting and combining to MP4...")
                stream = ffmpeg.input(deskshare_file)
                audio_stream = ffmpeg.input(audio_file)
                stream = ffmpeg.output(stream, audio_stream, mp4_file,
                                    vcodec='libx264',  # Change from 'copy' to 'libx264' to allow resolution change
                                    acodec='aac',
                                    video_bitrate='2000k',  # Decent bitrate for 720p
                                    s='1280x720')  # Set resolution to 720p
                ffmpeg.run(stream, overwrite_output=True)
                
                # Clean up the webm files
                os.remove(deskshare_file)
                os.remove(audio_file)
                
                print(f"Recording has been downloaded and converted to {mp4_file}")
            else:
                print(f"Failed to download the audio. Status code: {response.status_code}")
        else:
            print(f"Failed to download the recording. Status code: {response.status_code}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        driver.quit()

# Modified main section
if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Download BBB recordings from URLs in a file')
    parser.add_argument('-f', '--file', default='url.txt',
                        help='Path to the file containing URLs (default: url.txt)')
    args = parser.parse_args()

    # Read URLs from file
    try:
        with open(args.file, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
        
        # Process each URL with a numbered output
        for index, url in enumerate(urls, 1):
            print(f"\nProcessing video {index} of {len(urls)}")
            print(f"URL: {url}")
            download_bbb_recording(url, index)
            
    except FileNotFoundError:
        print(f"Error: {args.file} file not found. Please create a file with one URL per line.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
