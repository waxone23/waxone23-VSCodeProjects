import mido
from pythonosc import udp_client

# MIDI Setup (Adjust port name to match your APC40)
APC_PORT_NAME = "APC40 mkII 1"
# OSC Setup (Resolume's IP and Port)
OSC_IP = "127.0.0.1"
OSC_PORT = 7000

client = udp_client.SimpleUDPClient(OSC_IP, OSC_PORT)


def midi_to_osc():
    print(f"Bridge Active: Sending high-res data to Resolume on {OSC_PORT}")

    try:
        with mido.open_input(APC_PORT_NAME) as inport:
            for msg in inport:
                # Check if it's a Control Change (Knob/Fader)
                if msg.type == "control_change":
                    # Normalize MIDI 0-127 to OSC 0.0-1.0
                    val = msg.value / 127.0

                    # Example Mapping: Knob 1 (CC 48) to Master Opacity
                    if msg.control == 48:
                        client.send_message("/composition/master", val)
                        print(f"Master Opacity: {val:.2f}")

                    # Example Mapping: Knob 2 (CC 49) to Composition Speed
                    elif msg.control == 49:
                        client.send_message("/composition/speed", val)
                        print(f"Global Speed: {val:.2f}")

                    # Example Mapping: Fader 1 (CC 7) to Layer 1 Opacity
                    elif msg.control == 7:
                        client.send_message("/composition/layers/1/video/opacity", val)

    except IOError:
        print("Error: APC40 not found. Check your MIDI device names.")


if __name__ == "__main__":
    midi_to_osc()
