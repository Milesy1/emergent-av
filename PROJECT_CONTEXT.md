# Emergent — AV Performance System

### Repository
https://github.com/Milesy1/emergent-av

## Project Context for Cursor Sessions

### START OF SESSION CHECKLIST
1. Open TouchDesigner with `tdcursor.toe`
2. Open Ableton Live
3. Open Command Prompt and run: `npx touchdesigner-mcp-server@latest --stdio`
   - Wait for: `MCP server started in stdio mode`
   - Keep this window open for the whole session
4. In Cursor Settings → MCP, toggle `touchdesigner` off then on
5. Say: "Read PROJECT_CONTEXT.md and continue from current build status"

### Project file
`C:/Users/Miles/Desktop/Projects/TDCursor/tdcursor.toe`

### MCP servers (all required)
- `twozero_td` — streamableHttp, http://localhost:40404/mcp
- `touchdesigner` — must run `npx touchdesigner-mcp-server@latest --stdio` in terminal first
- `ableton` — uvx ableton-mcp
- `render` — npx @renderinc/mcp-server

### TD MCP troubleshooting
- 404 errors → npm server not running, start it in terminal
- MCP tools missing → Cursor Settings → MCP → toggle touchdesigner off/on
- TD MCP component is at `/project1/mcp_webserver_base` — do not modify

---

### Confirmed TD project structure
*Last verified by MCP scan 15/04/2026*

**`/project1`** — 9 direct children:

| Operator | Type | Notes |
|---|---|---|
| `out1` | outTOP | ← from `modular_render` |
| `sop_pool` | containerCOMP | raw SOP/CHOP library |
| `midi_ctrl` | containerCOMP | TDAbleton MIDI input |
| `python_logic` | containerCOMP | all script logic |
| `modular_render` | containerCOMP | render pipeline |
| `debug_text` | textTOP | |
| `mcp_webserver_base` | baseCOMP | MCP server — do not modify |
| `osc_ff` | oscinCHOP | Receives Fragment Flow OSC on port 9000. netaddress must be `127.0.0.1` (not `localhost` — IPv6 conflict). Requires Windows Firewall inbound UDP 9000 rule for TD process. |
| `null_ff` | nullCHOP | Stable reference point downstream of `osc_ff` |

---

**`/project1/midi_ctrl`:**
- `abletonMIDI` (baseCOMP) — TDAbleton component, Track: 1-Drum Rack, Device: TDA_MIDI
  - `merge1` (mergeCHOP)
  - `defaults/noteData` (constantCHOP)
  - `noteSplitter` / `lastNoteSplitter` (scriptCHOP)
  - `oscin_device` (oscinCHOP)
  - `replaceSplits` / `replaceDefaults` / `lastNoteReplace` (replaceCHOP)
  - `reorder1` (reorderCHOP)
  - `CallbacksExt` (selectDAT)
  - `AbletonMIDIExt` / `emptyCallbacks` / `deviceCallbacks` (textDAT)
  - `callbackCreator` (executeDAT)
  - `oscinDAT_device` (oscinDAT)
  - `chopexec_noteData` (chopexecuteDAT) — chop=`oscin_device`
  - `abletonBase` (baseCOMP)
  - `parexec1` (parexecuteDAT)
  - `oscin_outputs` (oscinCHOP)
- `null_kickTrig` (nullCHOP) — kick trigger output
- `chopexec1` (chopexecuteDAT) — chop=`/project1/midi_ctrl/null_kickTrig`
- `abletonMIDI1_callbacks` (textDAT)

---

**`/project1/python_logic`:**
- `chopexec1` (chopexecuteDAT) — chop=`/project1/midi_ctrl/abletonMIDI/merge1`
- `midi_listener_DAT` (chopexecuteDAT) — ⚠️ chop currently empty, needs wiring
- `pool__manager_DAT` (chopexecuteDAT) — ⚠️ chop currently empty, needs wiring. Note double underscore in name
- `parameter_mod_DAT` (textDAT)
- `pool_manager_table` (tableDAT)
- `utils_DAT` (textDAT)
- `state_dat` (textDAT)
- `debug_log` (textDAT)
- `list_params` (textDAT)

---

**`/project1/sop_pool`** — raw SOP/CHOP library (no geometry COMPs at this level):

SOPs:
- `line01` (lineSOP), `line_null` (nullSOP)
- `circle02` (circleSOP), `circle_draw_null1` (nullSOP)
- `sphere01` (sphereSOP), `sphere_null` (nullSOP)
- `box01` (boxSOP), `box_null` (nullSOP)
- `switch1` (switchSOP), `switchnull` (nullSOP)
- `transform1,2,3,5,7` (transformSOP)
- `rectangle1-2` (rectangleSOP)
- `carve1` (carveSOP)

CHOPs:
- `lag1-3` (lagCHOP)
- `math1-3` (mathCHOP)
- `null1-3` (nullCHOP)
- `null3_firstU`, `null2_secondu` (nullCHOP)
- `select1-3` (selectCHOP)
- `limit1` (limitCHOP)
- `trigger1` (triggerCHOP)
- `logic1` (logicCHOP)

DATs:
- `null1-3_export` (tableDAT)

Other:
- `annotate1` (annotateCOMP)

---

**`/project1/modular_render`:**
- `render1` (renderTOP) — geo=`geo1,geo2,geo3,geo4`, cam=`cam1`, lights=`light1`
  - ⚠️ lights path currently has typo `ligjht1` — must be corrected to `light1`
- `null1` (nullTOP) ← from `render1`
- `out1` (outTOP) ← from `null1`
- `cam1` (cameraCOMP) — tx=0, ty=0, tz=5
- `light1` (lightCOMP)
- `geo1` (geometryCOMP) — mat=`line2`
- `geo2` (geometryCOMP) — mat=`line1`
- `geo3` (geometryCOMP) — mat=`line5`
- `geo4` (geometryCOMP) — mat=`line4`
- `line1,2,4,5` (lineMAT) ×4
- `parameter1` (parameterDAT)

---

**`/project1/mcp_webserver_base`** — do not modify:
- `mpc_webserver` (webserverDAT)
- `import_modules` (textDAT)
- `mcp_webserver_script` (textDAT)

---

### Render pipeline
`render1` → `null1` → `out1` → `/project1/out1` → perform window
Status: working — 4 geometry COMPs with Line MATs rendering confirmed.

---

### Python files on disk
`C:/Users/Miles/Desktop/Projects/TDCursor/Python/`

| File | Size | Modified | Notes |
|---|---|---|---|
| `chopexec1.py` | 6 KB | 12/04/2026 | Main CHOP execute logic |
| `midi_listener_DAT.py` | 6 KB | 12/04/2026 | MIDI listener logic |
| `pool_manager_DAT.py` | 2 KB | 02/11/2025 | ⚠️ Not updated since Feb — may be stale |
| `dat_chopexec1_td_49452_7` | 2 KB | 10/04/2026 | TD-exported backup of chopexec1 |
| `dat_list_params_td_49452_6` | 1 KB | 10/04/2026 | Parameter list |
| `dat_parameter_mod_DAT_td_27496_1` | 34 KB | 09/11/2025 | Large parameter mapping table |
| `dat_pool_manager_DAT_td_49452_4` | 2 KB | 10/04/2026 | Pool manager backup |
| `dat_utils_DAT_td_49452_5` | 2 KB | 10/04/2026 | Utilities backup |

⚠️ `midi_actions_DAT.py` referenced in previous context doc — not found in folder. Remove from references.

---

### Python file summaries

#### `chopexec1.py`
- **Purpose:** Primary CHOP Execute dispatcher. Forwards all CHOP callbacks to `midi_listener_DAT` via `safe_call`, then handles CC and note events separately: extracts CC number/value and calls `parameter_mod_DAT.apply_cc_modulation`; on note-on calls `apply_note_modulation` with note + velocity; on note-off calls `apply_note_off`.
- **TD operator:** `/project1/midi_ctrl/chopexec1` (chopexecuteDAT), chop=`null_kickTrig`
- **Inputs:** CHOP channel data from `null_kickTrig`; `midi_listener_DAT` module (loaded at top-level); `parameter_mod_DAT` module (accessed per-callback)
- **Outputs / side effects:** Calls brain module functions; calls parameter modulation functions; appends rows to `debug_log`; prints to Textport
- **Dependencies:** `/project1/python_logic/midi_listener_DAT`, `/project1/python_logic/parameter_mod_DAT`, `/project1/python_logic/debug_log`
- **Known issues:** `midi_brain` module reference is resolved once at load — stale if `midi_listener_DAT` is reloaded without reloading this DAT. `onOnToOff` calls `midi_brain.onOnToOff` directly rather than via `safe_call` (inconsistent).

#### `midi_listener_DAT.py`
- **Purpose:** Core MIDI brain. Maintains in-memory state for active notes (`note_events`) and CC values (`cc_values`). Implements edge-detection on CHOP channels using a tracked-prev dict (because TD's `prev` arg is unreliable for aggregate MIDI channels). Exposes `_set_gate()` to toggle `geo_kick.par.display/render`, update `/project1/gate_kick` constantCHOP, and write to parent COMP custom par and `me.store`.
- **TD operator:** `/project1/python_logic/midi_listener_DAT` (chopexecuteDAT), chop currently empty
- **Inputs:** CHOP callback args (`channel`, `val`, `prev`) forwarded from `chopexec1`
- **Outputs / side effects:** Sets `geo_kick.par.display/render`; sets `/project1/gate_kick.par.const0value`; writes `me.store("gate", fv)`; sets parent COMP `Gate`/`gate` custom par; prints gate state to Textport
- **Dependencies:** `/project1/sop_pool/geo_kick` (hardcoded path — op does not exist in current file); `/project1/gate_kick` (does not exist in current file)
- **Known issues:** ⚠️ All `_set_gate()` call sites are commented out (`# GATE DISABLED FOR RENDER TEST`) — gate system is entirely non-functional. Both hardcoded paths (`geo_kick`, `gate_kick`) do not exist in `tdcursor.toe`.

#### `pool__manager_DAT.py` (also `dat_pool__manager_DAT_td_49452_4.py` — identical)
- **Purpose:** Bulk visibility and layout manager for geometry COMPs. Reads operator paths from `pool_manager_table` and provides `kill_switch()` (all off), `show_all()` (all on), `randomize_all()` (scatter tx/ty/tz randomly), `ensure_sops_exist()` (create default grid SOP in empty geos). Called explicitly via `.module`; not auto-triggered.
- **TD operator:** `/project1/python_logic/pool__manager_DAT` (chopexecuteDAT), chop currently empty
- **Inputs:** `/project1/python_logic/pool_manager_table` tableDAT (column 0 = operator paths); optional `paths` argument list
- **Outputs / side effects:** Sets `.render`/`.display` on pool operators; sets `.par.tx/ty/tz`; may create `gridSOP` inside empty geometry COMPs
- **Dependencies:** `/project1/python_logic/pool_manager_table`; `import random`
- **Known issues:** `randomize_all` checks `if 'tx' in geo.pars()` — `pars()` returns Par objects not strings, so this is always `False`; randomisation silently never runs. Uses `.render`/`.display` direct attributes rather than `.par.render`/`.par.display` (inconsistent with rest of codebase). `ensure_sops_exist` passes `sopType='grid'` — may need `'gridSOP'`.

#### `dat_parameter_mod_DAT_td_27496_1.txt`
- **Purpose:** MIDI-to-parameter mapping engine (the largest module, 783 lines). Reads three table DATs and maps note/CC events to TD operator parameters. Supports three switch modes: Mode 1 (momentary), Mode 2 (latch — new note turns previous off), Mode 3 (toggle — any press flips state). Geometry mappings use random or velocity-scaled values. CC messages are linearly interpolated 0–127 → min/max. All table reads are cached by row/column count.
- **TD operator:** `/project1/python_logic/parameter_mod_DAT` (textDAT module). Called from `chopexec1.py` via `.module.apply_note_modulation/apply_note_off/apply_cc_modulation`.
- **Inputs:** `/simple_midi_mapper/mappings_table` (geometry note→param mappings); `/simple_midi_mapper/midi_reactive_mappings` (switch/latch/toggle mappings); `/simple_midi_mapper/cc_mappings` (CC mappings); `note`, `velocity`, `cc_number`, `cc_value` as function args
- **Outputs / side effects:** Sets `par.val` on target operators; calls `sop.cook()` or `sop.cook(force=True)`; maintains `mode2_last_note`, `mode3_states`, `_mapping_cache` dicts in memory
- **Dependencies:** All three `/simple_midi_mapper/...` tableDATs (⚠️ do not exist in `tdcursor.toe`); `import random`
- **Known issues:** ⚠️ All three mapping table paths reference `/simple_midi_mapper/...` which does not exist — entire parameter modulation system returns empty on every call. `DEBUG_MODE = False` hardcoded; `FORCE_COOK_SOPS = False`. Mode 2/3 state dicts are never cleared when mappings change.

#### `dat_utils_DAT_td_49452_5.txt`
- **Purpose:** General utility library providing reusable helpers: `scale_value()` (linear/exponential/log interpolation), `apply_variation()` (random noise), `get_or_create_sop()` (resolve or create SOP inside a geo), `get_numeric_par()` (safe parameter accessor), `get_note_name()` / `get_cc_name()` (channel name string parsers).
- **TD operator:** `/project1/python_logic/utils_DAT` (textDAT module). Imported by other scripts via `.module`.
- **Inputs:** Arguments passed to each function; `op()` global inside `get_or_create_sop()`
- **Outputs / side effects:** All pure functions except `get_or_create_sop()` which may create a new SOP inside a geometryCOMP
- **Dependencies:** `import random`; TD `op()` global
- **Known issues:** `get_or_create_sop()` returns `geo.children[0]` if any children exist regardless of type or name — could return wrong child. No validation that `sopType` string is a valid TD type.

#### `dat_list_params_td_49452_6.txt`
- **Purpose:** One-shot diagnostic script. Resolves `op('/project1/sop_pool/box01')` and prints a sorted list of all parameter names on that operator. Used to discover correct par names for `box01` boxSOP.
- **TD operator:** `/project1/python_logic/list_params` (textDAT). Run manually — not a callback module.
- **Inputs:** `/project1/sop_pool/box01`
- **Outputs / side effects:** Prints sorted par name list to Textport only — no persistent effects
- **Dependencies:** `/project1/sop_pool/box01` must exist
- **Known issues:** Hardcoded to `box01`; purely a one-shot debug tool with no reuse value.

#### `dat_chopexec1_td_49452_7.py`
- **Purpose:** Simpler, earlier version of the `chopexec1` dispatcher. Forwards all five CHOP Execute callbacks to `midi_listener_DAT` via `safe_call` only — no CC parsing, no note modulation routing. A snapshot/backup of a prior iteration.
- **TD operator:** Snapshot export from a previous `chopexecuteDAT` (pid 49452). Not the live version.
- **Inputs:** CHOP callbacks; `midi_listener_DAT` module
- **Outputs / side effects:** Forwards callbacks to `midi_brain` only
- **Dependencies:** `/project1/python_logic/midi_listener_DAT`
- **Known issues:** Superseded by `chopexec1.py` — stale snapshot, not in use.

---

### Known blockers

1. **Gate system disabled** — all `_set_gate()` call sites in `midi_listener_DAT.py` are commented out (`# GATE DISABLED FOR RENDER TEST`). The MIDI → geometry visibility trigger is completely non-functional.

2. **Hardcoded paths don't exist** — `midi_listener_DAT.py` references `/project1/sop_pool/geo_kick` and `/project1/gate_kick`, neither of which exist in `tdcursor.toe`. These must be created or the paths updated before the gate system can work.

3. **Parameter modulation table paths unverified** — `parameter_mod_DAT` references `/simple_midi_mapper/...` table DAT paths — these were not found in the MCP scan but the modulation system is confirmed working at runtime when Ableton is playing. Locate and document the actual operator path in a future session.

4. **`render1` lights path typo** — `render1.par.lights` references `ligjht1` (misspelled) instead of `light1`. Lighting is not applied to the render.

5. **`pool__manager_DAT.randomize_all` silent bug** — `if 'tx' in geo.pars()` always evaluates to `False` because `pars()` returns Par objects, not strings. Position randomisation never executes despite appearing to run successfully.

6. **TD OSC `netaddress` must be `127.0.0.1`** — setting `netaddress` to `localhost` causes TD to bind on IPv6 (`::1`), breaking UDP receive from Ableton which sends on IPv4. Fix via Textport: `op('/project1/osc_ff').par.netaddress.val = '127.0.0.1'`

7. **Windows Firewall rule required for OSC receive** — inbound UDP port 9000 must be explicitly allowed for the TouchDesigner process. Rule name: `TouchDesigner OSC UDP 9000`. Add via elevated PowerShell: `New-NetFirewallRule -DisplayName "TouchDesigner OSC UDP 9000" -Direction Inbound -Protocol UDP -LocalPort 9000 -Action Allow -Profile Any`

---

### Current build status
- Render pipeline working ✓
- TDAbleton MIDI input working ✓
- MCP connected ✓
- OSC bridge (Fragment Flow → TD) working ✓ — `/live_amp1` channel confirmed live on `osc_ff`
- Gate system not yet built
- OSC bridge (FastAPI) not yet built
- Claude API integration not yet built

### Next steps
1. Fix lights typo in `render1` (`ligjht1` → `light1`)
2. Wire `midi_listener_DAT` to appropriate CHOP
3. Wire `pool__manager_DAT` to appropriate CHOP
4. Get Cursor to read and summarise all Python files — add summaries to this doc
5. Build FastAPI OSC bridge as Windows service
6. Connect Claude API for mid-performance parameter generation

---

### Architecture
- Ableton Live → TDAbleton MIDI → TouchDesigner geometry
- FastAPI OSC bridge — Python Windows service routing between all components
- Claude API generates parameter sets on demand mid-performance
- Lorenz chaos attractors drive continuous float streams between MIDI events
- Fragment Flow M4L device broadcasts VST amplitude and FFT as OSC from Ableton

### Visual target
Black background, neon green rotating line geometry, triggered by kick MIDI note. Eventually: asymmetric pulse outward from centre on note on, retracts on note off.