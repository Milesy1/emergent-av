def debug(msg):
    log_dat = op('/project1/python_logic/debug_log')
    if log_dat:
        try:
            log_dat.appendRow([msg])
        except Exception as e:
            print(f"[DEBUG LOG ERROR] Failed to write to debug log: {e}")
    print(msg)

midi_brain_op = op('/project1/python_logic/midi_listener_DAT')
midi_brain = midi_brain_op.module if midi_brain_op else None

if midi_brain:
    debug("[CHOP EXEC] midi_brain loaded")
else:
    debug("[CHOP EXEC ERROR] Could not load midi_listener_DAT")


def safe_call(func_name, channel, sampleIndex, val, prev):
    """Forward CHOP Execute callback to midi_listener_DAT (midi_brain) when defined."""
    if midi_brain and hasattr(midi_brain, func_name):
        getattr(midi_brain, func_name)(channel, sampleIndex, val, prev)


def onValueChange(channel, sampleIndex, val, prev):
    print(f"[CHOP RAW] onValueChange {channel.name} val={val}")
    debug(f"[CHOP] onValueChange -> {channel.name} val={val}")
    safe_call("onValueChange", channel, sampleIndex, val, prev)
    
    # Handle CC (Control Change) messages
    # Support both "cc_" and "control_" naming patterns
    channel_lower = channel.name.lower()
    is_cc = ('cc_' in channel_lower or 'control_' in channel_lower) and val is not None
    
    if is_cc:
        # Extract CC number from channel name (e.g., "cc_1" -> 1, "control_74" -> 74, "cc_74" -> 74)
        param_mod = op('/project1/python_logic/parameter_mod_DAT')
        if param_mod and hasattr(param_mod.module, 'apply_cc_modulation'):
            try:
                # Extract CC number from channel name (handle both "cc_" and "control_" patterns)
                if 'cc_' in channel_lower:
                    cc_str = channel_lower.split('cc_')[-1].split('/')[0]
                elif 'control_' in channel_lower:
                    cc_str = channel_lower.split('control_')[-1].split('/')[0]
                else:
                    return
                cc_number = int(cc_str)
                
                # Validate CC number is within MIDI range (0-127)
                if not (0 <= cc_number <= 127):
                    debug(f"[BRAIN ERROR] Invalid CC number {cc_number} from {channel.name} (must be 0-127)")
                    return
                
                # Get CC value (0-127)
                cc_value = int(val) if val is not None else 0
                # Clamp CC value to valid range
                cc_value = max(0, min(127, cc_value))
                
                # Apply CC modulation
                param_mod.module.apply_cc_modulation(cc_number, cc_value)
                debug(f"[BRAIN] Applied CC modulation: CC {cc_number} = {cc_value}")
                
            except ValueError as e:
                debug(f"[BRAIN ERROR] Failed to parse CC number from {channel.name}: {e}")
            except AttributeError as e:
                debug(f"[BRAIN ERROR] Parameter modulation module missing apply_cc_modulation method: {e}")
            except Exception as e:
                debug(f"[BRAIN ERROR] Unexpected error processing CC from {channel.name}: {e}")

def onOffToOn(channel, sampleIndex, val, prev):
    print(f"[CHOP RAW] onOffToOn {channel.name} val={val}")
    debug(f"[CHOP] onOffToOn -> {channel.name} val={val}")
    safe_call("onOffToOn", channel, sampleIndex, val, prev)
    if 'note_' in channel.name and val > 0:
        # OPTIMIZED: Process only the note that changed, not all active notes
        param_mod = op('/project1/python_logic/parameter_mod_DAT')
        if param_mod and hasattr(param_mod.module, 'apply_note_modulation'):
            try:
                note_num = int(channel.name.split('note_')[-1].split('/')[0])
                # Validate note number is within MIDI range (0-127)
                if not (0 <= note_num <= 127):
                    debug(f"[BRAIN ERROR] Invalid note number {note_num} for note ON from {channel.name} (must be 0-127)")
                    return
                # Get velocity value
                velocity = int(val) if val > 0 else 64  # Default to 64 if no velocity
                param_mod.module.apply_note_modulation(note_num, velocity)
                debug(f"[BRAIN] Applied modulation for note {note_num} with velocity {velocity}")
            except ValueError as e:
                debug(f"[BRAIN ERROR] Failed to parse note number from {channel.name}: {e}")
            except AttributeError as e:
                debug(f"[BRAIN ERROR] Parameter modulation module missing method: {e}")
            except Exception as e:
                debug(f"[BRAIN ERROR] Unexpected error processing note ON from {channel.name}: {e}")

def onOnToOff(channel, sampleIndex, val, prev):
    debug(f"[CHOP] onOnToOff -> {channel.name} val={val}")
    if midi_brain and hasattr(midi_brain, 'onOnToOff'):
        midi_brain.onOnToOff(channel, sampleIndex, val, prev)
    if 'note_' in channel.name and val == 0:
        param_mod = op('/project1/python_logic/parameter_mod_DAT')
        if param_mod and hasattr(param_mod.module, 'apply_note_off'):
            try:
                note_num = int(channel.name.split('note_')[-1].split('/')[0])
                # Validate note number is within MIDI range (0-127)
                if not (0 <= note_num <= 127):
                    debug(f"[BRAIN ERROR] Invalid note number {note_num} for note OFF from {channel.name} (must be 0-127)")
                    return
                param_mod.module.apply_note_off(note_num)
                debug(f"[BRAIN] Applied note OFF for note {note_num}")
            except ValueError as e:
                debug(f"[BRAIN ERROR] Failed to parse note number from {channel.name}: {e}")
            except AttributeError as e:
                debug(f"[BRAIN ERROR] Parameter modulation module missing method: {e}")
            except Exception as e:
                debug(f"[BRAIN ERROR] Unexpected error processing note OFF from {channel.name}: {e}")

def whileOn(channel, sampleIndex, val, prev):
    pass

def whileOff(channel, sampleIndex, val, prev):
    pass