from pythonosc import dispatcher, osc_server
import mido

# MIDI Output to APC40
APC_OUT = mido.open_output("APC40 mkII 1")


def handle_composition_feedback(address, *args):
    # Resolume sends 0.0 to 1.0, APC40 LEDs need 0 to 127
    value = int(args[0] * 127)

    # Map OSC address to MIDI CC
    if "/composition/master" in address:
        # CC 48 is the first knob ring on APC40 MKII
        msg = mido.Message("control_change", control=48, value=value)
        APC_OUT.send(msg)


# Setup OSC Receiver
dispatch = dispatcher.Dispatcher()
dispatch.map("/composition/master", handle_composition_feedback)

# Start Server (Listening on Port 7001 - Set Resolume Outgoing to this port)
server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 7001), dispatch)
print("Feedback Loop Active. Waiting for Resolume OSC Out...")
server.serve_forever()
