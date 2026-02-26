#!/usr/bin/env python3
import mido
import re
import subprocess
import os

def parse_config(filename):
    config = {}
    with open(filename) as f:
        for line in f:
            match = re.match(r'^-\s*(\d+)\[(\w+)\]=(.+)$', line.strip())
            if match:
                note, event_type, command = match.groups()
                config[(int(note), event_type)] = command.strip()
    return config

config = parse_config("rebutton-config.md")
midi_port = mido.open_input(mido.get_input_names()[0])
print(f"Listening on {midi_port.name}...")

for msg in midi_port:
    key = (getattr(msg, 'note', None) or getattr(msg, 'control', None), msg.type)
    print(msg)
    if key in config and config[key]:
        command = config[key]
        # Replace variables
        command = command.replace('$value', str(getattr(msg, 'value', '')))
        command = command.replace('$velocity', str(getattr(msg, 'velocity', '')))
        print(f"Executing: {command}")
        subprocess.Popen(command, shell=True)
