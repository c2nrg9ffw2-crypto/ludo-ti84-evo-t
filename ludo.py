# Ludo ("Mensch aergere dich nicht") for the TI-84 Evo
# 2-4 players, some can be the calculator. Roll the die and race your
# 4 pieces around the board into your home lane. Land on someone and they
# go back to their yard! You need a 6 to bring a piece out; a 6 rolls again.
# Keys: enter = roll / move, left/right = choose a piece, clear = quit
import random
from ti_draw import clear, set_color, draw_text
from ti_draw import fill_rect as ti_fill_rect
try:
    from ti_draw import get_screen_dim
    SW, SH = get_screen_dim()
except:
    SW, SH = 319, 209

# Keep every box inside the screen and never stop the game over one box.
# The Evo draws boxes 1 pixel too small, so we ask for 1 pixel more.
def fill_rect(x, y, w, h):
    if x < 0:
        w, x = w + x, 0
    if y < 0:
        h, y = h + y, 0
    w, h = min(w, SW - x), min(h, SH - y)
    if w > 0 and h > 0:
        try:
            ti_fill_rect(x, y, w + 1, h + 1)
        except:
            pass
# Draw in a hidden buffer and show the finished picture at once: no flicker
try:
    from ti_draw import use_buffer, paint_buffer
    use_buffer()
except:
    paint_buffer = None
try:
    from ti_system import get_key as read_key
except:
    from ti_system import getKey as read_key
# On the Evo get_key wants one number. Find out once at the start.
try:
    read_key()
    key = read_key
except TypeError:
    def key():
        return read_key(0)
try:
    from ti_system import store_list, recall_list
except:
    store_list = recall_list = None
try:
    from time import sleep
except:
    from ti_system import sleep
try:
    import gc
except:
    gc = None

LEFT = (2, 24)
RIGHT = (1, 26)
UP = (3, 25)
DOWN = (4, 34)
OK = (5, 105)                 # enter
SECOND = (21, 22)             # 2nd, mode
QUIT = (9, 45)                # clear
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (150, 150, 150)
YELLOW = (255, 220, 0)

def paint():
    if paint_buffer:
        paint_buffer()

def write(x, y, s):                    # text that can never stop the game
    try:
        draw_text(x, y, s)
    except:
        pass

def wait_for(keys):
    paint()
    while True:
        k = key()
        if k in keys:
            return k
        sleep(0.05)

# Numbers saved in a calculator list, so they stay after quitting
def load(name, n):
    try:
        l = [int(v) for v in recall_list(name)]
    except:
        l = []
    return (l + [0] * n)[:n]

def save(name, l):
    try:
        store_list(name, l)
    except:
        pass

# Text panel on the right side: rows 30 px high, the whole row is wiped first
def text(row, s, col=WHITE):
    set_color(*BLACK)
    fill_rect(TX, row * 30, SW - TX, 29)
    set_color(*col)
    write(TX, row * 30 + 22, s)

def box_frame(x, y, w, h, t, col):     # a frame t pixels thick
    set_color(*col)
    fill_rect(x, y, w, t)
    fill_rect(x, y + h - t, w, t)
    fill_rect(x, y, t, h)
    fill_rect(x + w - t, y, t, h)

def title_screen(name, col, line):
    clear()
    set_color(*BLACK)
    fill_rect(0, 0, SW, SH)
    set_color(*col)
    write(SW // 2 - 80, 25, name)
    set_color(*WHITE)
    write(SW // 2 - 80, 55, line)

# A menu on the start screen. Returns the chosen number, or -1 for clear.
def menu(options, choice, hint):
    x = SW // 2 - 80
    set_color(*BLACK)
    fill_rect(0, 64, SW, SH - 64)
    set_color(*WHITE)
    write(x, 202, hint)
    while True:
        for i in range(len(options)):
            set_color(*BLACK)
            fill_rect(x - 20, 64 + i * 28, 230, 27)
            set_color(*(YELLOW if i == choice else GREY))
            write(x, 90 + i * 28, ("> " if i == choice else "  ") + options[i])
        k = wait_for(UP + DOWN + OK + QUIT)
        if k in QUIT:
            return -1
        if k in OK:
            return choice
        if k in UP:
            choice = (choice - 1) % len(options)
        if k in DOWN:
            choice = (choice + 1) % len(options)

CELL = 13                     # board square size
X0 = 4
Y0 = (SH - 15 * CELL) // 2
TX = X0 + 15 * CELL + 8       # text panel (black, so text is fine)
PCOL = [(230, 30, 30), (0, 180, 0), (240, 200, 0), (30, 110, 255)]
PLIGHT = [(255, 160, 160), (150, 230, 150), (255, 240, 150), (160, 200, 255)]
PNAME = ["Red", "Green", "Yellow", "Blue"]
PATH = (235, 235, 235)        # white-ish squares of the track
CURSOR = (0, 230, 255)

# The 52 track squares (row, column), clockwise, starting at red's start
TRACK = ([(6, c) for c in range(1, 6)] + [(r, 6) for r in range(5, -1, -1)] + [(0, 7)] +
         [(r, 8) for r in range(0, 6)] + [(6, c) for c in range(9, 15)] + [(7, 14)] +
         [(8, c) for c in range(14, 8, -1)] + [(r, 8) for r in range(9, 15)] + [(14, 7)] +
         [(14, 6)] + [(r, 6) for r in range(13, 8, -1)] + [(8, c) for c in range(5, -1, -1)] +
         [(7, 0), (6, 0)])
START = [0, 13, 26, 39]       # where each colour comes out of its yard
# Home lane (5 squares) and the last square (6th) for each colour
LANE = [[(7, c) for c in range(1, 7)], [(r, 7) for r in range(1, 7)],
        [(7, c) for c in range(13, 7, -1)], [(r, 7) for r in range(13, 7, -1)]]
YARD = [(0, 0), (0, 9), (9, 9), (9, 0)]     # top-left of each 6 x 6 yard
SPOT = [(1, 1), (1, 4), (4, 1), (4, 4)]     # piece places inside a yard
GOAL = 56                     # 0-50 track, 51-55 home lane, 56 = home

pos = [[-1] * 4 for s in range(4)]          # per colour: -1 = in the yard

def where(s, k):               # board square of colour s, piece k
    p = pos[s][k]
    if p < 0:
        return (YARD[s][0] + SPOT[k][0], YARD[s][1] + SPOT[k][1])
    if p <= 50:
        return TRACK[(START[s] + p) % 52]
    return LANE[s][p - 51]

# ---------- drawing ----------
BASE = {}                      # colour of every board square without pieces
for i in range(52):
    BASE[TRACK[i]] = PATH
for s in range(4):
    BASE[TRACK[START[s]]] = PLIGHT[s]
    for sq in LANE[s][:5]:
        BASE[sq] = PLIGHT[s]
    BASE[LANE[s][5]] = PCOL[s]
    for k in range(4):
        BASE[(YARD[s][0] + SPOT[k][0], YARD[s][1] + SPOT[k][1])] = WHITE
BASE[(7, 7)] = (60, 60, 60)

def square(sq):
    r, c = sq
    set_color(*BASE.get(sq, BLACK))
    fill_rect(X0 + c * CELL, Y0 + r * CELL, CELL - 1, CELL - 1)

def piece(sq, s, many=False):  # a round-ish piece with a black edge
    x, y = X0 + sq[1] * CELL, Y0 + sq[0] * CELL
    set_color(*BLACK)
    fill_rect(x + 2, y + 1, 8, 10)
    fill_rect(x + 1, y + 2, 10, 8)
    set_color(*PCOL[s])
    fill_rect(x + 4, y + 3, 4, 6)
    fill_rect(x + 3, y + 4, 6, 4)
    if many:                   # 2 or more pieces here: white dot
        set_color(*WHITE)
        fill_rect(x + 5, y + 5, 2, 2)

def redraw(sq, seats):         # a square with whatever pieces stand on it
    square(sq)
    for s in seats:
        here = [k for k in range(4) if where(s, k) == sq]
        if here:
            piece(sq, s, len(here) > 1)

def draw_board(seats):
    clear()
    set_color(*BLACK)
    fill_rect(0, 0, SW, SH)
    for s in range(4):         # yards: a coloured block with white spots
        set_color(*(PCOL[s] if s in seats else (60, 60, 60)))
        fill_rect(X0 + YARD[s][1] * CELL, Y0 + YARD[s][0] * CELL, 6 * CELL - 1, 6 * CELL - 1)
    for sq in BASE:
        square(sq)
    for s in seats:
        for k in range(4):
            redraw(where(s, k), seats)

def cursor(sq):                # frame inside the square (redraw the square to remove it)
    box_frame(X0 + sq[1] * CELL, Y0 + sq[0] * CELL, CELL - 1, CELL - 1, 2, CURSOR)

def die(v):
    x, y = TX + 10, 66
    set_color(*WHITE)
    fill_rect(x, y, 30, 30)
    set_color(*BLACK)
    for q in {1: [4], 2: [0, 8], 3: [0, 4, 8], 4: [0, 2, 6, 8], 5: [0, 2, 4, 6, 8], 6: [0, 2, 3, 5, 6, 8]}[v]:
        fill_rect(x + 4 + (q % 3) * 8, y + 4 + (q // 3) * 8, 6, 6)

def roll():
    for t in range(5):         # a little shake
        v = random.randrange(1, 7)
        die(v)
        paint()
        sleep(0.06)
    return v

# ---------- rules ----------
def moves(s, d):               # pieces of colour s that can move d squares
    out = []
    for k in range(4):
        p = pos[s][k]
        if p < 0:
            if d == 6:
                out.append(k)
        elif p + d <= GOAL:
            out.append(k)
    return out

def move(s, k, d, seats):      # move a piece square by square; returns captured colour or -1
    p = pos[s][k]
    steps = [0] if p < 0 else list(range(p + 1, p + d + 1))
    for q in steps:
        old = where(s, k)
        pos[s][k] = q
        redraw(old, seats)
        redraw(where(s, k), seats)
        paint()
        sleep(0.08)
    hit = -1
    if pos[s][k] <= 50:        # landed on someone? they go back to their yard
        sq = where(s, k)
        for o in seats:
            if o == s:
                continue
            for j in range(4):
                if 0 <= pos[o][j] <= 50 and where(o, j) == sq:
                    pos[o][j] = -1
                    hit = o
                    redraw(where(o, j), seats)
        if hit >= 0:
            redraw(sq, seats)
    return hit

# ---------- computer player ----------
def ai_pick(s, d, seats, opts):
    best, pick = -999, opts[0]
    for k in opts:
        p = pos[s][k]
        new = 0 if p < 0 else p + d
        v = new - max(p, 0)                     # progress
        if p < 0:
            v += 40                             # bring a piece out
        if new > 50:
            v += 30                             # safe in the home lane
        if new == GOAL:
            v += 30
        if new <= 50:
            t = (START[s] + new) % 52
            for o in seats:
                if o == s:
                    continue
                for j in range(4):
                    q = pos[o][j]
                    if 0 <= q <= 50:
                        ot = (START[o] + q) % 52
                        if ot == t:
                            v += 60             # capture!
                        elif 1 <= (t - ot) % 52 <= 6:
                            v -= 15             # someone could catch it next
        v += random.random()
        if v > best:
            best, pick = v, k
    return pick

# ---------- game ----------
def choose_players(stats):
    title_screen("LUDO", PCOL[0], "Wins " + " ".join(str(w) for w in stats))
    while True:
        n = menu(["2 players", "3 players", "4 players"], 0, "UP/DOWN + ENTER")
        if n < 0:
            return None
        n += 2
        c = menu(["All people"] + [str(k) + " computer" + ("s" if k > 1 else "") for k in range(1, n)],
                 0, "CLEAR: back")
        if c >= 0:
            return n, c

def game(n, comps):            # returns the winning colour, or -1 for quit
    seats = {2: [0, 2], 3: [0, 1, 2], 4: [0, 1, 2, 3]}[n]
    computer = seats[n - comps:]
    for s in range(4):
        pos[s] = [-1] * 4
    draw_board(seats)
    text(0, "LUDO")
    text(6, "CLEAR:quit")
    t = 0
    while True:
        s = seats[t]
        comp = s in computer
        text(1, PNAME[s] + (" C" if comp else ""), PCOL[s])
        # with no piece out yet you get 3 tries to roll a 6
        tries = 3 if all(p < 0 or p == GOAL for p in pos[s]) else 1
        again = False
        while tries:
            tries -= 1
            if comp:
                text(4, "")
                paint()
                sleep(0.4)
            else:
                text(4, "ENTER:roll", YELLOW)
                if wait_for(OK + QUIT) in QUIT:
                    return -1
            d = roll()
            opts = moves(s, d)
            if not opts:
                text(4, "No move")
                paint()
                sleep(0.7)
                if d == 6:
                    again = True
                    break
                continue
            if comp or len(opts) == 1:
                k = ai_pick(s, d, seats, opts) if comp else opts[0]
                sleep(0.3)
            else:                                   # choose a piece
                text(4, "L/R + ENTER", YELLOW)
                i = 0
                while True:
                    sq = where(s, opts[i])
                    cursor(sq)
                    key_ = wait_for(LEFT + RIGHT + OK + QUIT)
                    redraw(sq, seats)
                    if key_ in QUIT:
                        return -1
                    if key_ in OK:
                        break
                    i = (i + (1 if key_ in RIGHT else -1)) % len(opts)
                k = opts[i]
            hit = move(s, k, d, seats)
            text(4, ("Got " + PNAME[hit] + "!") if hit >= 0 else "")
            if all(p == GOAL for p in pos[s]):
                return s
            again = d == 6
            break
        if not again:
            t = (t + 1) % n

# --- start ---
stats = load("LUDO", 4)        # wins per colour
while True:
    setup = choose_players(stats)
    if setup is None:
        break
    w = game(*setup)
    if w < 0:
        continue
    stats[w] += 1
    save("LUDO", stats)
    text(4, PNAME[w], PCOL[w])
    text(5, "wins!", PCOL[w])
    text(6, "ENTER:menu")
    if wait_for(OK + QUIT) in QUIT:
        break
paint()
