# CHOP Execute DAT - robust MIDI routing to brain

# Reference the brain DAT
midi_brain_op = op('/project1/python_logic/midi_listener_DAT')
midi_brain = None
if midi_brain_op and hasattr(midi_brain_op, 'module'):
    midi_brain = midi_brain_op.module

def safe_call(func_name, channel, sampleIndex, val, prev):
    """Call a function on midi_brain if it exists."""
    if midi_brain and hasattr(midi_brain, func_name):
        func = getattr(midi_brain, func_name)
        func(channel, sampleIndex, val, prev)
        print(f"[CHOP] Called {func_name} -> {channel.name} val={val}")

# CHOP Execute callbacks
def onOffToOn(channel, sampleIndex, val, prev):
    safe_call('onOffToOn', channel, sampleIndex, val, prev)

def whileOn(channel, sampleIndex, val, prev):
    safe_call('whileOn', channel, sampleIndex, val, prev)

def onOnToOff(channel, sampleIndex, val, prev):
    safe_call('onOnToOff', channel, sampleIndex, val, prev)

def whileOff(channel, sampleIndex, val, prev):
    safe_call('whileOff', channel, sampleIndex, val, prev)

def onValueChange(channel, sampleIndex, val, prev):
    safe_call('onValueChange', channel, sampleIndex, val, prev)

