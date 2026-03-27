import mido
import time

# --- CONFIGURATION ---
APC_NAME = "APC40 mkII"  # Partial names work better with 'find_port'
RESOLUME_NAME = "IAC Driver Bus 1"  # Or 'Resolume MIDI Out'


def find_port(name_list, target):
    """Finds the actual system name that contains our target string."""
    for name in name_list:
        if target.lower() in name.lower():
            return name
    return None


def get_ports():
    """Wait until all MIDI ports are available."""
    while True:
        in_name = find_port(mido.get_input_names(), APC_NAME)
        out_name = find_port(mido.get_output_names(), APC_NAME)
        res_name = find_port(mido.get_output_names(), RESOLUME_NAME)

        if in_name and out_name and res_name:
            return in_name, out_name, res_name

        print(
            f"Waiting for devices... (APC: {'OK' if in_name else 'MISSING'}, Resolume: {'OK' if res_name else 'MISSING'})"
        )
        time.sleep(2)


def bridge():
    apc_in, apc_out, res_out = get_ports()
    shift_held = False

    try:
        with mido.open_input(apc_in) as inport, mido.open_output(
            res_out
        ) as outport, mido.open_output(apc_out) as apc_led:
            # Initialize APC40 Mode 2
            init_msg = mido.Message(
                "sysex",
                data=[0x47, 0x7F, 0x29, 0x60, 0x00, 0x04, 0x42, 0x09, 0x01, 0x01],
            )
            apc_led.send(init_msg)
            print("--- Bridge Active & APC40 Initialized ---")

            for msg in inport:
                # Logic for Shift Button (Note 98)
                if msg.type == "note_on" and msg.note == 98:
                    shift_held = True
                    continue
                if msg.type == "note_off" and msg.note == 98:
                    shift_held = False
                    continue

                # If Shift is held, move the message to Channel 2
                if shift_held and hasattr(msg, "channel"):
                    msg = msg.copy(channel=1)  # MIDI Channel 2 (0-indexed)

                # Send to Resolume
                outport.send(msg)

                # Send Feedback to APC (Green LED)
                if msg.type in ["note_on", "note_off"]:
                    apc_led.send(msg.copy(velocity=1, channel=0))

    except Exception as e:
        print(f"Connection lost: {e}. Retrying...")
        bridge()  # Restart the loop


if __name__ == "__main__":
    bridge()
