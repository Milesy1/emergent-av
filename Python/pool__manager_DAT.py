# -----------------------------
# pool_manager_DAT - system helpers
# -----------------------------
# Reference your external table
POOL_MANAGER_OP = op('/project1/python_logic/pool_manager_table')

def kill_switch(paths=None):
    """Turn off display/render for SOPs in pool."""
    if not paths:
        paths = [row[0].val for row in POOL_MANAGER_OP.rows() if len(row) >= 1 and row[0].val]
    for path in paths:
        geo = op(path)
        if geo:
            geo.render = False
            geo.display = False
    print("Kill switch activated")

def show_all(paths=None):
    """Turn on display/render for SOPs in pool."""
    if not paths:
        paths = [row[0].val for row in POOL_MANAGER_OP.rows() if len(row) >= 1 and row[0].val]
    for path in paths:
        geo = op(path)
        if geo:
            geo.render = True
            geo.display = True
    print("Show all activated")

def randomize_all(paths=None):
    """Randomize positions of SOPs (example)."""
    import random
    if not paths:
        paths = [row[0].val for row in POOL_MANAGER_OP.rows() if len(row) >= 1 and row[0].val]
    for path in paths:
        geo = op(path)
        if geo:
            if 'tx' in geo.pars(): geo.par.tx = random.uniform(-1,1)
            if 'ty' in geo.pars(): geo.par.ty = random.uniform(-1,1)
            if 'tz' in geo.pars(): geo.par.tz = random.uniform(-1,1)
    print("Randomize all executed")

def ensure_sops_exist(paths):
    """Create default grid inside SOPs if empty."""
    for path in paths:
        geo = op(path)
        if geo and not geo.children:
            geo.create(sopType='grid', name='grid1')
            print(f"Created grid in {path}")
