# re:Button

<div align="center">

**The Interface Revolution**

*Physical Computing Meets AI*

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.7+-green.svg)](https://www.python.org/)

</div>

---

## Overview

**re:Button** transforms physical MIDI controllers into intelligent command centers for your digital life—similar to StreamDeck, but open-source, DIY, and much more powerful.

Imagine creating your own keyboard but instead of regular keys, it triggers smart shortcuts that help you operate your life. Press a button to check your bank balance, turn a knob to control system volume, launch project workspaces, control media playback, or trigger custom workflows with a single touch.

Part of the [Renascence Computing](https://kiro.dev) ecosystem—rethinking how we interact with computers to serve our lives, not the other way around.

## Features

- 🎹 **Universal MIDI Support** - Works with any MIDI controller
- 📝 **Markdown Configuration** - Simple, human-readable config files
- 🚀 **Instant Execution** - Shell commands, scripts, API calls, anything
- 🔊 **Audio Feedback** - Text-to-speech integration via AWS Polly
- 🏠 **IoT Integration** - MQTT support for smart home control
- 🤖 **AI-Powered** - Use Kiro CLI to generate and optimize mappings
- ⚡ **Lightweight** - Core implementation in ~30 lines of Python

## Quick Start

### Prerequisites

- Python 3.7+
- Any MIDI controller (Presonus ATOM recommended - US$ 136)
- macOS, Linux, or Windows

### Installation

```bash
# Clone the repository
git clone https://github.com/renascence-computing/rebutton.git
cd rebutton

# Install dependencies
pip install -r requirements.txt

# On macOS, you might also need:
brew install portmidi
```

### Basic Usage

1. **Connect your MIDI controller** via USB

2. **Discover button numbers:**
   ```bash
   python3 rebutton-mqtt.py
   ```
   Press buttons to see their MIDI note/control numbers

3. **Configure your buttons** in `rebutton-config.md`:
   ```markdown
   # Quick Responses
   - 109[control_change]=osascript -e 'tell application "System Events" to keystroke "y"'
   
   # Launch Apps
   - 96[note_on]=/Applications/Kiro.app/Contents/MacOS/Electron ~/code/project
   
   # Media Control
   - 86[note_on]=open -a Spotify && osascript -e 'tell application "Spotify" to play'
   - 14[control_change]=osascript -e "set volume output volume $value"
   ```

4. **Run re:Button:**
   ```bash
   python3 rebutton.py
   ```

5. **Start pressing buttons!** 🎉

## Configuration Guide

### Configuration Format

The `rebutton-config.md` file uses a simple format:

```
- <note_number>[<event_type>]=<command>
```

**Event Types:**
- `note_on` - Button press
- `note_off` - Button release
- `control_change` - Knob/slider movement

**Variables:**
- `$value` - MIDI value (0-127)
- `$velocity` - Note velocity (0-127)

### Example Configurations

#### Project Launchers
```markdown
# Open different workspaces with Kiro
- 96[note_on]=/Applications/Kiro.app/Contents/MacOS/Electron ~/code/project1
- 97[note_on]=/Applications/Kiro.app/Contents/MacOS/Electron ~/code/project2
- 98[note_on]=/Applications/Kiro.app/Contents/MacOS/Electron ~/code/project3
```

#### Media Control
```markdown
# Spotify controls
- 86[note_on]=open -a Spotify && osascript -e 'tell application "Spotify" to play'
- 87[note_on]=open -a Spotify && osascript -e 'tell application "Spotify" to pause'

# Volume knob (0-127 mapped to 0-100)
- 14[control_change]=osascript -e "set volume output volume $value"
```

#### Quick Text Responses
```markdown
# Type common responses
- 109[control_change]=osascript -e 'tell application "System Events" to keystroke "yes"'
- 107[control_change]=osascript -e 'tell application "System Events" to keystroke "no"'
- 105[control_change]=osascript -e 'tell application "System Events" to keystroke "thanks"'
```

#### Smart API Integration
```markdown
# Check bank balance with text-to-speech
- 112[note_on]=balance=$(curl -s http://localhost:8080/api/balance | jq -r '.balance'); python3 text_to_speech.py "Your balance is $balance"

# Check credit card balance
- 113[note_on]=balance=$(curl -s http://localhost:8080/api/credit | jq -r '.balance'); python3 text_to_speech.py "Your credit card balance is $balance"
```

#### IoT/Smart Home Control
```markdown
# Send MQTT messages to control devices
- 85[control_change]=mosquitto_pub -h localhost -t home/lights/brightness -m $value
- 88[note_on]=mosquitto_pub -h localhost -t home/lights/power -m "on"
- 89[note_on]=mosquitto_pub -h localhost -t home/lights/power -m "off"
```

#### Photo Capture
```markdown
# Quick photo with Photo Booth
- 48[note_on]=open -a "Photo Booth" && sleep 3 && osascript -e 'tell application "Photo Booth" to shoot a picture' && osascript -e 'tell application "Photo Booth" to quit'
```

## Technical Details

### Core Components

#### `rebutton.py`
Main application that listens for MIDI events and executes configured commands.

```python
#!/usr/bin/env python3
import mido
import re
import subprocess

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

for msg in midi_port:
    key = (getattr(msg, 'note', None) or getattr(msg, 'control', None), msg.type)
    if key in config:
        command = config[key].replace('$value', str(getattr(msg, 'value', '')))
        subprocess.Popen(command, shell=True)
```

#### `rebutton-mqtt.py`
Debug tool that publishes MIDI events to MQTT for discovery and monitoring.

**Features:**
- Lists available MIDI devices
- Publishes all MIDI events to `reos/key/atom` topic
- JSON payload with note, velocity, control, and value
- Filters out aftertouch events

#### `text_to_speech.py`
AWS Polly integration for audio feedback.

**Features:**
- Converts text to speech using AWS Polly
- Caches generated MP3 files (MD5 hash-based)
- Plays audio using `afplay` (macOS)

**Requirements:**
- AWS credentials configured (`~/.aws/credentials`)
- boto3 library

### Architecture

```
┌─────────────────┐
│  MIDI Controller│
│  (USB Device)   │
└────────┬────────┘
         │ MIDI Events
         ▼
┌─────────────────┐
│  rebutton.py    │
│  - Parse config │
│  - Listen MIDI  │
│  - Execute cmds │
└────────┬────────┘
         │
         ├──────────────┐
         │              │
         ▼              ▼
┌─────────────┐  ┌──────────────┐
│ Shell Cmds  │  │ MQTT Broker  │
│ - Apps      │  │ - IoT        │
│ - Scripts   │  │ - Debugging  │
│ - APIs      │  │              │
└─────────────┘  └──────────────┘
```

## Hardware Recommendations

### Presonus ATOM (Recommended)
- **Price:** ~US$ 136
- **Features:** 16 velocity-sensitive pads, 8 knobs, 20 buttons
- **Pros:** Excellent build quality, perfect size, great value
- **Cons:** None significant

### Alternatives
- **Akai MPD218:** Budget option (~$99)
- **Novation Launchpad:** Grid-focused (~$149)
- **Any MIDI keyboard:** Use keys as buttons
- **DIY Arduino MIDI:** Build your own!

## Use Cases

### Most Popular Configurations

1. **Project Launchers** - Dedicated buttons for each workspace
2. **Volume Control Knob** - Much better than keyboard shortcuts
3. **Quick Responses** - "Yes/No/Thanks" saves typing in meetings
4. **Photo Capture** - Quick photos with Photo Booth for video calls
5. **Smart Home Control** - Send MQTT messages to control lights and devices
6. **Financial Shortcuts** - Check balances via API with audio feedback
7. **Media Control** - Spotify play/pause/next without leaving keyboard

## Using Kiro CLI for Configuration

Leverage Kiro's AI capabilities to create and manage your button mappings:

```bash
kiro-cli chat
```

**Example prompts:**

```
> "Help me create a rebutton config that opens my project folders 
   on buttons 96-99 and controls Spotify on buttons 86-87"

> "Generate a command to check my bank balance via API and 
   speak it using text-to-speech"

> "I have 16 pads. Suggest an ergonomic layout for: 
   4 project launchers, 4 media controls, 4 quick responses"

> "Create a button that takes a screenshot and uploads it to S3"

> "How do I map a knob to control my smart lights brightness?"
```

## Troubleshooting

### MIDI Device Not Found
```bash
# List available MIDI devices
python3 -c "import mido; print(mido.get_input_names())"

# If empty, check USB connection and drivers
```

### Commands Not Executing
- Check shell syntax in your config
- Test commands manually in terminal first
- Look for error messages in console output
- Ensure proper escaping of quotes and special characters

### Text-to-Speech Not Working
```bash
# Verify AWS credentials
aws sts get-caller-identity

# Test Polly directly
aws polly synthesize-speech --text "Hello" --output-format mp3 --voice-id Joanna test.mp3
```

### MQTT Connection Issues
```bash
# Test MQTT broker
mosquitto_pub -h localhost -t test -m "hello"

# Check if broker is running
ps aux | grep mosquitto
```

## Advanced Topics

### Multiple MIDI Devices
Edit `rebutton.py` to select a specific device:
```python
# List devices
print(mido.get_input_names())

# Select by index
midi_port = mido.open_input(mido.get_input_names()[1])
```

### Running as a Service

**macOS (launchd):**
Create `~/Library/LaunchAgents/com.rebutton.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.rebutton</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/path/to/rebutton.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Load with: `launchctl load ~/Library/LaunchAgents/com.rebutton.plist`

**Linux (systemd):**
Create `/etc/systemd/system/rebutton.service`:
```ini
[Unit]
Description=re:Button MIDI Controller
After=network.target

[Service]
Type=simple
User=<your-username>
WorkingDirectory=/path/to/rebutton
ExecStart=/usr/bin/python3 /path/to/rebutton.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable with: `sudo systemctl enable --now rebutton`

### Custom Event Handlers
Extend `rebutton.py` to add custom logic:
```python
# Add before command execution
if key == (96, 'note_on'):
    # Custom logic here
    print("Special handling for button 96")
```

## Integration with Renascence Ecosystem

re:Button is part of the larger Renascence Computing vision:

- **[re:OS](https://kiro.dev)** - Operating system reimagined
- **[re:Money](https://bit.ly/intro-to-remoney)** - Personal finance API
- **[Kiro CLI](https://kiro.dev)** - AI-powered development assistant

Use re:Button to create physical interfaces for these systems!

## Contributing

Contributions welcome! Areas of interest:

- Additional example configurations
- Platform-specific guides (Windows, Linux)
- Hardware reviews and recommendations
- Integration with other Renascence projects
- Documentation improvements

## License

Apache License 2.0 - See [LICENSE](LICENSE) file for details.

## Resources

- **Documentation:** [docs/index.html](docs/index.html)
- **GitHub:** https://github.com/renascence-computing/rebutton
- **Kiro CLI:** https://kiro.dev
- **re:Money:** https://bit.ly/intro-to-remoney
- **Blog:** https://dev.to (step-by-step guide)

## Why This Matters

### Tangible Interface
Physical buttons create a tangible interface to your digital life. Instead of context-switching between apps and memorizing shortcuts, you have dedicated controls for what matters most.

### AI-Powered Evolution
Combined with AI (via Kiro), you can rapidly prototype and evolve your interface. The barrier between "I wish I could..." and "Done!" shrinks to minutes.

### Infinitely Customizable
Your button layout will be completely different from anyone else's because your life and workflows are unique. What will you put on your buttons?

---

<div align="center">

**Renascence Computing © 2026 - The Digital Reborn**

[kiro.dev](https://kiro.dev) | [re:Money](https://bit.ly/intro-to-remoney) | [Modernization](https://bit.ly/modern-ai)

</div>
