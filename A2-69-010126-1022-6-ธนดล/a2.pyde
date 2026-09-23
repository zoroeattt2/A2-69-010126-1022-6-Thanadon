import random

GRID_SIZE = 8
CELL_SIZE = 48
BOARD_X = 58
BOARD_Y = 60

PALETTE = [
    (245, 93, 62),   # Orange-Red
    (66, 133, 244),  # Blue
    (52, 168, 83),   # Green
    (251, 188, 5),   # Yellow
    (171, 71, 188),  # Purple
]

SHAPE_TEMPLATES = [
    ([(0, 0)], 0),
    ([(0, 0), (1, 0), (0, 1), (1, 1)], 1),
    ([(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)], 2),
    ([(0, 0), (1, 0)], 3),
    ([(0, 0), (1, 0), (2, 0)], 4),
    ([(0, 0), (1, 0), (2, 0), (3, 0)], 0),
    ([(0, 0), (0, 1)], 1),
    ([(0, 0), (0, 1), (0, 2)], 2),
    ([(0, 0), (0, 1), (0, 2), (0, 3)], 3),
    ([(0, 0), (0, 1), (1, 1)], 4),
    ([(0, 0), (1, 0), (0, 1)], 0),
    ([(0, 0), (1, 0), (1, 1)], 1),
    ([(0, 1), (1, 1), (1, 0)], 2),
]

def draw_square(x,y,size, fill_color, stroke_color, corner_weight):
    fill(fill_color[0], fill_color[1], fill_color[2])
    stroke(stroke_color[0], stroke_color[1], stroke_color[2])
    strokeWeight(1)
    rect(x, y, size, size, corner_weight)

class Board:x
    fill(fill_color[0], fill_color[1], fill_color[2])
    stroke(stroke_color[0], stroke_color[1], stroke_color[2])
    strokeWeight(1)
    rect(x, y, size, size, corner_weight)

class Particle:
    def __init__(self, x, y, color_rgb):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        self.size = random.uniform(6, 12)
        self.color_rgb = color_rgb
        self.life = 255

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.size -= 0.3
        self.life -= 12

    def draw(self):
        noStroke()
        fill(self.color_rgb[0], self.color_rgb[1], self.color_rgb[2], max(0, self.life))
        ellipse(self.x, self.y, max(0, self.size), max(0, self.size))

    def is_dead(self):
        return self.life <= 0 or self.size <= 0

class Board:
    def __init__(self, size, cell_size, origin_x, origin_y):
        self.size = size
        self.cell_size = cell_size
        self.ox = origin_x
        self.oy = origin_y
        
        self.grid = []
        r = 0
        while r < self.size:
            row = []
            c = 0
            while c < self.size:
                row.append(None)
                c += 1
            self.grid.append(row)
            r += 1

    def draw(self):
        r = 0
        while r < self.size:
            c = 0
            while c < self.size:
                x = self.ox + c * self.cell_size
                y = self.oy + r * self.cell_size
                val = self.grid[r][c]
                if val is None:
                    draw_square(x, y, self.cell_size, (220, 225, 230), (200, 205, 210), 4)
                else:
                    draw_square(x, y, self.cell_size, PALETTE[val], (255, 255, 255), 4)
                c += 1
            r += 1

    def can_place(self, piece, target_r, target_c):
        i = 0
        while i < len(piece.blocks):
            dc, dr = piece.blocks[i]
            r = target_r + dr
            c = target_c + dc
            if r < 0 or r >= self.size or c < 0 or c >= self.size:
                return False
            if self.grid[r][c] is not None:
                return False
            i += 1
        return True

    def place(self, piece, target_r, target_c):
        i = 0
        while i < len(piece.blocks):
            dc, dr = piece.blocks[i]
            r = target_r + dr
            c = target_c + dc
            self.grid[r][c] = piece.color_idx
            i += 1

    def clear_lines(self):
        global particles
        rows_to_clear = []
        cols_to_clear = []

        r = 0
        while r < self.size:
            full = True
            c = 0
            while c < self.size:
                if self.grid[r][c] is None:
                    full = False
                    break
                c += 1
            if full:
                rows_to_clear.append(r)
            r += 1

        c = 0
        while c < self.size:
            full = True
            r = 0
            while r < self.size:
                if self.grid[r][c] is None:
                    full = False
                    break
                r += 1
            if full:
                cols_to_clear.append(c)
            c += 1

        cells_to_clear = []
        i = 0
        while i < len(rows_to_clear):
            r_idx = rows_to_clear[i]
            c = 0
            while c < self.size:
                if (r_idx, c) not in cells_to_clear:
                    cells_to_clear.append((r_idx, c))
                c += 1
            i += 1

        i = 0
        while i < len(cols_to_clear):
            c_idx = cols_to_clear[i]
            r = 0
            while r < self.size:
                if (r, c_idx) not in cells_to_clear:
                    cells_to_clear.append((r, c_idx))
                r += 1
            i += 1

        i = 0
        while i < len(cells_to_clear):
            cr, cc = cells_to_clear[i]
            val = self.grid[cr][cc]
            if val is not None:
                col_rgb = PALETTE[val]
                cell_x = self.ox + cc * self.cell_size
                cell_y = self.oy + cr * self.cell_size
                
                p_count = 0
                while p_count < 8:
                    px = cell_x + self.cell_size / 2.0
                    py = cell_y + self.cell_size / 2.0
                    particles.append(Particle(px, py, col_rgb))
                    p_count += 1
                    
                self.grid[cr][cc] = None
            i += 1

        return len(rows_to_clear) + len(cols_to_clear)

class Piece:
    def __init__(self, blocks, color_idx, anchor_x, anchor_y):
        self.blocks = blocks
        self.color_idx = color_idx
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.x = anchor_x
        self.y = anchor_y
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.mini_cell = 24
    
    def draw(self):
    def contains_point(self, px, py):
    def reset_pos(self):

board = None
hand = [0, 0, 0]
score = 0
game_over = False
selected_piece = None
selected_index = -1

def spawn_hand():
    global hand

def is_hand_empty():
def check_game_over():
    global game_over

def setup():
    global board, score, game_over

def draw():
    if selected_piece != None:
    if game_over:

def mousePressed():
    global selected_piece, selected_index, game_over

def mouseDragged():

def mouseReleased():
    global selected_piece, selected_index, score, game_over
    if selected_piece == None:
    if board.can_place(selected_piece, target_r, target_c):
    
    
    
