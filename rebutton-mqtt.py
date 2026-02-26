#!/usr/bin/env python3
import mido
import paho.mqtt.client as mqtt
import json

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "reos/key/atom"

def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker: {rc}")

client = mqtt.Client()
client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT)
client.loop_start()

print("Available MIDI inputs:")
for i, name in enumerate(mido.get_input_names()):
    print(f"{i}: {name}")

#port_idx = int(input("Select MIDI port: "))
#midi_port = mido.open_input(mido.get_input_names()[port_idx])
midi_port = mido.open_input(mido.get_input_names()[0])

print(f"Listening on {midi_port.name}...")

for msg in midi_port:
    if msg.type == "aftertouch" or msg.type == "polytouch":
        continue
    payload = json.dumps({
        "type": msg.type,
        "note": getattr(msg, 'note', None),
        "velocity": getattr(msg, 'velocity', None),
        "control": getattr(msg, 'control', None),
        "value": getattr(msg, 'value', None)
    })
    client.publish(MQTT_TOPIC, payload)
    print(f"Sent: {payload}")
