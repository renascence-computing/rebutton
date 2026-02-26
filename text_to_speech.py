#!/usr/bin/env python3
import sys
import hashlib
import os
import boto3
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: python text_to_speech.py <text>")
        sys.exit(1)
    
    text = sys.argv[1]
    text_hash = hashlib.md5(text.encode()).hexdigest()
    filename = f"/tmp/speech_{text_hash}.mp3"
    
    if os.path.exists(filename):
        print(f"Using cached file: {filename}")
    else:
        polly = boto3.client('polly')
        response = polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId='Joanna'
        )
        
        with open(filename, 'wb') as f:
            f.write(response['AudioStream'].read())
        
        print(f"Created: {filename}")
    
    subprocess.run(['afplay', filename])

if __name__ == "__main__":
    main()
