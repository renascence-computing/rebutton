# re:button Config

## Yes / No
- 109[control_change]=osascript -e 'tell application "System Events" to keystroke "y"'
- 107[control_change]=osascript -e 'tell application "System Events" to keystroke "n"'
- 105[control_change]=osascript -e 'tell application "System Events" to keystroke "t"'

## Control Keys
- 86[control_change]=open -a "Sublime Text" /Users/vsenger/code/renascence/rebutton/rebutton-config.md
- 85[control_change]=mosquitto_pub -h localhost -t playground/relay -m $value

## Audio keys
- 84[note_on]=python3 /Users/vsenger/code/renascence/rebutton/text_to_speech.py "Renaissance"
- 85[note_on]=python3 /Users/vsenger/code/renascence/rebutton/text_to_speech.py "Renascence"
- 86[note_on]=open -a Spotify && osascript -e 'tell application "Spotify" to play'
- 87[note_on]=open -a Spotify && osascript -e 'tell application "Spotify" to pause'
- 14[control_change]=osascript -e "set volume output volume $value"

## Apps keys
- 96[note_on]=/Applications/Kiro.app/Contents/MacOS/Electron /Users/vsenger/code/renascence/reos-core
- 97[note_on]=/Applications/Kiro.app/Contents/MacOS/Electron /Users/vsenger/code/renascence/reos-money
- 98[note_on]=/Applications/Kiro.app/Contents/MacOS/Electron /Users/vsenger/code/renascence
- 99[note_on]=/Applications/Kiro.app/Contents/MacOS/Electron /Users/vsenger/2025/0-Downloads/projects
- 92[note_on]=open -a "Microsoft PowerPoint"
- 93[note_on]=open -a Firefox

# Orange Keys
- 112[note_on]=balance=$(curl -s http://localhost:8080/entryResource/balance/BofA | jq -r '.balance'); python3 /Users/vsenger/code/renascence/rebutton/text_to_speech.py "Your balance in Bank of America is $balance"
- 113[note_on]=balance=$(curl -s http://localhost:8080/entryResource/balance/BofA-6707V | jq -r '.balance'); python3 /Users/vsenger/code/renascence/rebutton/text_to_speech.py "Your credit card balance is $balance"

- 48[note_on]=open -a "Photo Booth" && sleep 3 && osascript -e 'tell application "Photo Booth" to shoot a picture' && osascript -e 'tell application "Photo Booth" to quit'