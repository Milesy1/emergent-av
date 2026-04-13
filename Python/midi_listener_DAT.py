# -----------------------------
# midi_listener_DAT
# Stores MIDI note/CC state and exposes top-level functions
# -----------------------------

note_events = {}
cc_values = {}

# Last seen value per channel.name â€” CHOP Execute `prev` is often wrong for MIDI aggregates.
_channel_prev_val = {}

# Kick geometry in sop_pool (line â†’ transform chain)
GEO_KICK_PATH = "/project1/sop_pool/geo_kick"


def _float_or_zero(x):
    try:
        if x is None:
            return 0.0
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def _is_cc_channel(channel_name):
    lower = channel_name.lower()
    return "cc_" in lower or "control_" in lower


def _gate_from_midi_edges(channel, val, prev):
    """
    TDA_MIDI: gate on last_velocity rising above 0; gate off when last_note hits 0.
    Other non-CC channels: any 0â†’positive = on, positiveâ†’0 = off.

    Edges use _channel_prev_val (updated each call). TouchDesigner's onValueChange
    `prev` argument is not reliable for channels like last_velocity.
    """
    name = channel.name
    lower = name.lower()
    if _is_cc_channel(name):
        return

    raw_stored = _channel_prev_val.get(name)
    tracked_prev = 0.0 if raw_stored is None else _float_or_zero(raw_stored)
    cv = _float_or_zero(val)
    td_prev = prev  # only for debug text

    if "last_velocity" in lower:
        if cv > 0 and tracked_prev <= 0:
            pass  # GATE DISABLED FOR RENDER TEST
            # _set_gate(
            #     1,
            #     reason=f"last_velocity edge {tracked_prev!r}->{cv!r} (td_prev={td_prev!r})",
            # )
    elif "last_note" in lower:
        if cv <= 0 and tracked_prev > 0:
            pass  # GATE DISABLED FOR RENDER TEST
            # _set_gate(
            #     0,
            #     reason=f"last_note off {tracked_prev!r}->{cv!r} (td_prev={td_prev!r})",
            # )
    else:
        if cv > 0 and tracked_prev <= 0:
            pass  # GATE DISABLED FOR RENDER TEST
            # _set_gate(
            #     1,
            #     reason=f"generic on {name} {tracked_prev!r}->{cv!r} (td_prev={td_prev!r})",
            # )
        elif cv <= 0 and tracked_prev > 0:
            pass  # GATE DISABLED FOR RENDER TEST
            # _set_gate(
            #     0,
            #     reason=f"generic off {name} {tracked_prev!r}->{cv!r} (td_prev={td_prev!r})",
            # )

    _channel_prev_val[name] = cv


def _channel_note_number(channel_name):
    """Parse MIDI note index from channel names like 'note_36'."""
    lower = channel_name.lower()
    if "note_" not in lower:
        return None
    try:
        return int(lower.split("note_")[-1].split("/")[0])
    except ValueError:
        return None


def _set_gate(value, reason=""):
    """
    Drive gate: storage, parent custom par (Gate/gate), /project1/gate_kick, and geo_kick visibility.
    Do not return early when `me` is unset (e.g. ad-hoc calls); CHOP callbacks always have `me`.
    """
    fv = float(1 if value else 0)
    on = fv > 0.5
    try:
        if me:
            me.store("gate", fv)
    except Exception:
        pass
    try:
        parent = me.parent() if me else None
        if parent:
            pg = parent.par("Gate") or parent.par("gate")
            if pg:
                pg.val = fv
    except Exception:
        pass
    gc = op("/project1/gate_kick")
    if gc and hasattr(gc.par, "const0value"):
        try:
            gc.par.const0value = fv
        except Exception:
            pass
    geo = op(GEO_KICK_PATH)
    if geo:
        try:
            geo.par.display = on
            geo.par.render = on
            disp = geo.par.display.val
            rend = geo.par.render.val
            tag = f" ({reason})" if reason else ""
            print(
                f"[MIDI GATE]{tag} op({GEO_KICK_PATH!r}).display={disp!r} "
                f".render={rend!r} (wanted on={on})"
            )
        except Exception as ex:
            print(f"[MIDI GATE ERROR] geo {GEO_KICK_PATH}: {ex}")
    else:
        print(f"[MIDI GATE WARN] no operator at {GEO_KICK_PATH!r}")


def onValueChange(channel, sampleIndex, val, prev):
    """
    Called when any MIDI channel value changes.
    """
    try:
        if "cc" in channel.name.lower():
            cc_values[channel.name] = val
        elif val > 0:
            note_events[channel.name] = val
        elif val <= 0 and channel.name in note_events:
            # Remove note from state when it goes OFF
            del note_events[channel.name]
        _gate_from_midi_edges(channel, val, prev)
        print(f"[MIDI LISTENER] Value change: {channel.name} = {val}")
    except Exception as e:
        print(f"[MIDI LISTENER ERROR] onValueChange: {e}")

def onOffToOn(channel, sampleIndex, val, prev):
    """
    Called when note goes from off -> on.
    """
    try:
        if val > 0:
            note_events[channel.name] = val
        lower = channel.name.lower()
        if _channel_note_number(channel.name) is not None or "last_velocity" in lower:
            pass  # GATE DISABLED FOR RENDER TEST
            # _set_gate(1, reason=f"onOffToOn {channel.name}")
        print(f"[MIDI LISTENER] Note ON: {channel.name} = {val}")
    except Exception as e:
        print(f"[MIDI LISTENER ERROR] onOffToOn: {e}")

def onOnToOff(channel, sampleIndex, val, prev):
    """
    Called when note goes from on -> off.
    """
    try:
        # Remove note from state when it goes OFF
        if channel.name in note_events:
            del note_events[channel.name]
        lower = channel.name.lower()
        if _channel_note_number(channel.name) is not None or "last_note" in lower:
            pass  # GATE DISABLED FOR RENDER TEST
            # _set_gate(0, reason=f"onOnToOff {channel.name}")
        print(f"[MIDI LISTENER] Note OFF: {channel.name} (removed from state)")
    except Exception as e:
        print(f"[MIDI LISTENER ERROR] onOnToOff: {e}")