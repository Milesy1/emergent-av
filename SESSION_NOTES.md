# Session Notes — TD Kick Visualiser
_Last updated: 10 Apr 2026_

---

## What we built

A MIDI-driven visual flash in TouchDesigner:
- When a kick drum note fires → `geo_kick` becomes visible (spinning neon green line)
- When the note ends → `geo_kick` hides

---

## Operator map

```
/project1/
├── python_logic/
│   └── midi_listener_DAT     ← brain: detects note on/off, calls _set_gate()
├── midi_ctrl/
│   └── chopexec1             ← CHOP Execute DAT, forwards MIDI events to midi_listener_DAT
├── sop_pool/
│   └── geo_kick (geometryCOMP)
│       ├── line1 (lineSOP)       ← A=(0,-2,0) B=(0,2,0), length 4, Y axis
│       ├── transform1 (transformSOP) ← rz = absTime.seconds * 60 (continuous spin)
│       └── out1 (nullSOP)        ← display flag = True
├── modular_render/
│   ├── cam1 (cameraCOMP)     ← tx=2, ty=3, tz=15, lookat=origin_null
│   ├── origin_null (nullCOMP) ← at (0,0,0), used as cam lookat target
│   ├── light1 (lightCOMP)    ← point light at (4,6,4)
│   ├── render1 (renderTOP)   ← geometry=geo_kick, camera=cam1, lights=light1
│   └── out1 (outTOP)         ← selecttop=render1
└── gate_kick (constantCHOP)  ← single channel 'gate', driven by _set_gate()
```

---

## Current state of geo_kick

- **material**: NOT yet set — needs `phong_line` (see Next session below)
- **par.display / par.render**: controlled by `_set_gate()` in `midi_listener_DAT`
  - gate=1 → display=True, render=True (kick note on)
  - gate=0 → display=False, render=False (kick note off)
- Internal chain: `line1 → transform1 → out1`

---

## Next session — first thing to do

Create the material and finish the setup:

1. **Delete** `/project1/modular_render/line_mat` (leftover from previous attempt)

2. **Create** a `phongMAT` named `phong_line` inside `/project1/modular_render`:
   - Diffuse: `(0, 1, 0)` neon green
   - Emit: `(0, 0.6, 0)` neon green
   - **Wireframe**: `'topology'` ← this is the correct string value, NOT `'on'`
   - **Wire Width**: `2.0` pixels
   - This renders the lineSOP edge as a flat screen-space line — no 3D tube

3. **Fix line1** inside `geo_kick`:
   - `line1.par.pay = -2`, `line1.par.pby = 2` → length 4 along Y
   - (lineSOP has no single "length" param — uses point A and point B)

4. **Assign material**:
   ```python
   op('/project1/sop_pool/geo_kick').par.material = '/project1/modular_render/phong_line'
   ```

5. **Force geo_kick visible** briefly to screenshot the result:
   ```python
   gk = op('/project1/sop_pool/geo_kick')
   gk.par.display = True
   gk.par.render  = True
   ```
   Then reset to False after confirming it looks right.

---

## Key lessons learned this session

| Problem | Cause | Fix |
|---|---|---|
| geo_kick always black | `_set_gate(0)` sets `par.render=False` when no MIDI | Force True for testing, then reset |
| lineMAT = fat capsule | lineMAT extrudes lines into 3D tubes (that's its design) | Use phongMAT + wireframe=topology instead |
| wireframe='on' invalid | PhongMAT options are `'off'`, `'tesselated'`, `'topology'` | Use `'topology'` for SOP edge lines |
| geo_kick corrupt state | Too many create/destroy cycles left stale internal state | Delete COMP entirely, create fresh |
| cook loop | `par.pathop` left set to `'out1'` (invalid sibling path) | Clear to `''` |

---

## MIDI note detection logic (midi_listener_DAT)

- Listens for `last_velocity` channel going 0→positive → `_set_gate(1)`
- Listens for `last_note` channel going positive→0 → `_set_gate(0)`
- Internal `_channel_prev_val` dict tracks previous values (CHOP Execute `prev` arg is unreliable)
- `_set_gate()` directly sets `geo_kick.par.display` and `geo_kick.par.render`

---

## TD instance

- Port: check with `td_list_instances` at session start (instance ID changes between restarts)
- Project file: `emergent.toe` at `C:/Users/Miles/Desktop/Projects/TDCursor`
