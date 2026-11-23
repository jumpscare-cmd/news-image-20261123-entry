#!/usr/bin/env python3
"""Newspaper front page poster - Monday, 23 November 2026.
Standard library only. Deterministic: no randomness, no timestamps, no network.
Generates entry.png (1024x1024) in the same directory as this file.
"""
import os
import struct
import zlib

W = 1024
H = 1024
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (90, 90, 90)
LIGHT = (230, 230, 230)
DARKGREY = (60, 60, 60)

# 5x7 bitmap font: each glyph is 7 rows of 5 chars, '#' = on, '.' = off
FONT = {
    'A': ["01110","10001","10001","11111","10001","10001","10001"],
    'B': ["11110","10001","10001","11110","10001","10001","11110"],
    'C': ["01110","10001","10000","10000","10000","10001","01110"],
    'D': ["11110","10001","10001","10001","10001","10001","11110"],
    'E': ["11111","10000","10000","11110","10000","10000","11111"],
    'F': ["11111","10000","10000","11110","10000","10000","10000"],
    'G': ["01110","10001","10000","10111","10001","10001","01111"],
    'H': ["10001","10001","10001","11111","10001","10001","10001"],
    'I': ["01110","00100","00100","00100","00100","00100","01110"],
    'J': ["00111","00010","00010","00010","00010","10010","01100"],
    'K': ["10001","10010","10100","11000","10100","10010","10001"],
    'L': ["10000","10000","10000","10000","10000","10000","11111"],
    'M': ["10001","11011","10101","10101","10001","10001","10001"],
    'N': ["10001","11001","10101","10011","10001","10001","10001"],
    'O': ["01110","10001","10001","10001","10001","10001","01110"],
    'P': ["11110","10001","10001","11110","10000","10000","10000"],
    'Q': ["01110","10001","10001","10001","10101","10010","01101"],
    'R': ["11110","10001","10001","11110","10100","10010","10001"],
    'S': ["01111","10000","10000","01110","00001","00001","11110"],
    'T': ["11111","00100","00100","00100","00100","00100","00100"],
    'U': ["10001","10001","10001","10001","10001","10001","01110"],
    'V': ["10001","10001","10001","10001","10001","01010","00100"],
    'W': ["10001","10001","10001","10101","10101","11011","10001"],
    'X': ["10001","10001","01010","00100","01010","10001","10001"],
    'Y': ["10001","10001","01010","00100","00100","00100","00100"],
    'Z': ["11111","00001","00010","00100","01000","10000","11111"],
    'a': ["00000","00000","01110","00001","01111","10001","01111"],
    'b': ["10000","10000","11110","10001","10001","10001","11110"],
    'c': ["00000","00000","01110","10000","10000","10001","01110"],
    'd': ["00001","00001","01111","10001","10001","10001","01111"],
    'e': ["00000","00000","01110","10001","11111","10000","01110"],
    'f': ["00110","01001","01000","11110","01000","01000","01000"],
    'g': ["00000","01111","10001","10001","01111","00001","01110"],
    'h': ["10000","10000","11110","10001","10001","10001","10001"],
    'i': ["00100","00000","01100","00100","00100","00100","01110"],
    'j': ["00010","00000","00110","00010","00010","10010","01100"],
    'k': ["10000","10000","10010","10100","11000","10100","10010"],
    'l': ["01100","00100","00100","00100","00100","00100","01110"],
    'm': ["00000","00000","11010","10101","10101","10101","10101"],
    'n': ["00000","00000","11110","10001","10001","10001","10001"],
    'o': ["00000","00000","01110","10001","10001","10001","01110"],
    'p': ["00000","00000","11110","10001","11110","10000","10000"],
    'q': ["00000","00000","01111","10001","01111","00001","00001"],
    'r': ["00000","00000","10110","11001","10000","10000","10000"],
    's': ["00000","00000","01111","10000","01110","00001","11110"],
    't': ["01000","01000","11100","01000","01000","01001","00110"],
    'u': ["00000","00000","10001","10001","10001","10011","01101"],
    'v': ["00000","00000","10001","10001","10001","01010","00100"],
    'w': ["00000","00000","10001","10101","10101","10101","01010"],
    'x': ["00000","00000","10001","01010","00100","01010","10001"],
    'y': ["00000","00000","10001","10001","01111","00001","01110"],
    'z': ["00000","00000","11111","00010","00100","01000","11111"],
    '0': ["01110","10001","10011","10101","11001","10001","01110"],
    '1': ["00100","01100","00100","00100","00100","00100","01110"],
    '2': ["01110","10001","00001","00110","01000","10000","11111"],
    '3': ["11111","00010","00100","00010","00001","10001","01110"],
    '4': ["00010","00110","01010","10010","11111","00010","00010"],
    '5': ["11111","10000","11110","00001","00001","10001","01110"],
    '6': ["00110","01000","10000","11110","10001","10001","01110"],
    '7': ["11111","00001","00010","00100","01000","01000","01000"],
    '8': ["01110","10001","10001","01110","10001","10001","01110"],
    '9': ["01110","10001","10001","01111","00001","00010","01100"],
    ' ': ["00000","00000","00000","00000","00000","00000","00000"],
    '.': ["00000","00000","00000","00000","00000","01100","01100"],
    ',': ["00000","00000","00000","00000","01100","00100","01000"],
    ':': ["00000","01100","01100","00000","01100","01100","00000"],
    ';': ["00000","01100","01100","00000","01100","00100","01000"],
    "'": ["00100","00100","01000","00000","00000","00000","00000"],
    '"': ["01010","01010","00000","00000","00000","00000","00000"],
    '-': ["00000","00000","00000","01110","00000","00000","00000"],
    '!': ["00100","00100","00100","00100","00100","00000","00100"],
    '?': ["01110","10001","00001","00110","00100","00000","00100"],
    '(': ["00010","00100","01000","01000","01000","00100","00010"],
    ')': ["01000","00100","00010","00010","00010","00100","01000"],
    '/': ["00001","00010","00010","00100","01000","01000","10000"],
    '%': ["10001","10010","00010","00100","01000","01001","10001"],
    '$': ["00100","01111","10100","01110","00101","11110","00100"],
    '&': ["01100","10010","10100","01000","10101","10010","01101"],
    '*': ["00000","10101","01110","11111","01110","10101","00000"],
    '+': ["00000","00100","00100","11111","00100","00100","00000"],
    '=': ["00000","00000","11111","00000","11111","00000","00000"],
    '_': ["00000","00000","00000","00000","00000","00000","11111"],
    '<': ["00010","00100","01000","10000","01000","00100","00010"],
    '>': ["01000","00100","00010","00001","00010","00100","01000"],
    '[': ["01110","01000","01000","01000","01000","01000","01110"],
    ']': ["01110","00010","00010","00010","00010","00010","01110"],
    '#': ["01010","01010","11111","01010","11111","01010","01010"],
    '@': ["01110","10001","10111","10101","10110","10000","01110"],
    '~': ["00000","00000","01011","10110","00000","00000","00000"],
    '^': ["00100","01010","10001","00000","00000","00000","00000"],
    '|': ["00100","00100","00100","00100","00100","00100","00100"],
    '\\': ["10000","01000","01000","00100","00010","00010","00001"],
}

class Canvas:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.px = bytearray([255]) * (w * h * 3)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i+1], self.px[i+2] = color

    def fill_rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            if yy < 0 or yy >= self.h:
                continue
            for xx in range(x, x + w):
                if 0 <= xx < self.w:
                    self.set(xx, yy, color)

    def hline(self, x, y, w, color, thick=1):
        self.fill_rect(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.fill_rect(x, y, thick, h, color)

    def line(self, x0, y0, x1, y1, color):
        dx = abs(x1 - x0); dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1; sy = 1 if y0 < y1 else -1
        err = dx + dy; x, y = x0, y0
        while True:
            self.set(x, y, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy; x += sx
            if e2 <= dx:
                err += dx; y += sy

    def circle(self, cx, cy, r, color):
        # outline circle (midpoint)
        x, y, d = 0, r, 1 - r
        while x <= y:
            for px, py in [(cx+x, cy+y), (cx-x, cy+y), (cx+x, cy-y), (cx-x, cy-y),
                           (cx+y, cy+x), (cx-y, cy+x), (cx+y, cy-x), (cx-y, cy-x)]:
                self.set(px, py, color)
            x += 1
            if d < 0:
                d += 2 * x + 1
            else:
                y -= 1; d += 2 * (x - y) + 1

    def fill_circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            dx = int((r * r - (yy - cy) * (yy - cy)) ** 0.5) if abs(yy - cy) <= r else 0
            for xx in range(cx - dx, cx + dx + 1):
                self.set(xx, yy, color)

    def ellipse_outline(self, cx, cy, rx, ry, color):
        for deg in range(0, 360):
            import math
            a = math.radians(deg)
            x = int(cx + rx * math.cos(a)); y = int(cy + ry * math.sin(a))
            self.set(x, y, color)

def text_width(text, scale):
    return len(text) * (5 * scale + scale) - scale if text else 0

def draw_text(c, x, y, text, scale, color=BLACK):
    cx = x
    for ch in text:
        glyph = FONT.get(ch, FONT.get('?', FONT[' ']))
        # fallback: unknown chars become '?'
        if ch not in FONT:
            glyph = FONT['?']
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == '1':
                    c.fill_rect(cx + col * scale, y + row * scale, scale, scale, color)
        cx += 5 * scale + scale
    return cx

def draw_text_centered(c, cx_center, y, text, scale, color=BLACK):
    w = text_width(text, scale)
    draw_text(c, cx_center - w // 2, y, text, scale, color)

def wrap_text(text, max_width, scale):
    words = text.split(' ')
    lines = []
    cur = ''
    for word in words:
        trial = word if not cur else cur + ' ' + word
        if text_width(trial, scale) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            # long word: hard split by chars
            while text_width(word, scale) > max_width:
                # take as many chars as fit
                n = max_width // (6 * scale)
                lines.append(word[:n]); word = word[n:]
            cur = word
    if cur:
        lines.append(cur)
    return lines

def draw_wrapped(c, x, y, text, max_width, scale, color=BLACK, line_gap=4):
    lines = wrap_text(text, max_width, scale)
    yy = y
    for line in lines:
        draw_text(c, x, yy, line, scale, color)
        yy += 7 * scale + line_gap
    return yy

def draw_headline_wrapped(c, x, y, text, max_width, scale, color=BLACK, line_gap=3):
    return draw_wrapped(c, x, y, text, max_width, scale, color, line_gap)

def draw_globe(c, cx, cy, r):
    # Globe: outer circle, latitude/longitude lines, land blobs as small rects
    c.fill_circle(cx, cy, r, WHITE)
    c.circle(cx, cy, r, BLACK)
    c.circle(cx, cy, r - 2, BLACK)
    # equator and latitude lines (ellipses)
    c.ellipse_outline(cx, cy, r - 2, 12, BLACK)
    c.ellipse_outline(cx, cy, r - 2, int(r * 0.55), BLACK)
    c.ellipse_outline(cx, cy, r - 2, int(r * 0.85), BLACK)
    # longitude ellipses (vertical)
    c.ellipse_outline(cx, cy, 12, r - 2, BLACK)
    c.ellipse_outline(cx, cy, int(r * 0.55), r - 2, BLACK)
    c.ellipse_outline(cx, cy, int(r * 0.85), r - 2, BLACK)
    # vertical centre line and horizontal centre line
    c.vline(cx, cy - r + 2, 2 * r - 4, BLACK)
    c.hline(cx - r + 2, cy, 2 * r - 4, BLACK)
    # land blobs (filled small shapes)
    c.fill_rect(cx - 55, cy - 45, 34, 22, BLACK)
    c.fill_rect(cx - 45, cy - 28, 22, 16, BLACK)
    c.fill_rect(cx + 12, cy - 38, 28, 18, BLACK)
    c.fill_rect(cx + 28, cy + 8, 30, 20, BLACK)
    c.fill_rect(cx - 28, cy + 28, 26, 14, BLACK)
    c.fill_rect(cx + 5, cy + 38, 18, 10, BLACK)

def draw_bar_chart(c, x, y, w, h, values, labels, color=BLACK):
    # axes
    c.hline(x, y + h, w, BLACK, 2)
    c.vline(x, y, h, BLACK, 2)
    n = len(values)
    bw = (w - 20) // n
    maxv = max(values)
    for i, v in enumerate(values):
        bh = int((v / maxv) * (h - 24))
        bx = x + 12 + i * bw
        by = y + h - bh
        c.fill_rect(bx, by, bw - 10, bh, BLACK)
        # value label above bar (scale 1)
        draw_text(c, bx, by - 12, str(v), 1, BLACK)
        # category label below axis (scale 1)
        draw_text(c, bx, y + h + 6, labels[i], 1, BLACK)

def chunk(b, n):
    return [b[i:i+n] for i in range(0, len(b), n)]

def write_png(c, path):
    raw = bytearray()
    for yy in range(c.h):
        raw.append(0)  # filter None
        start = yy * c.w * 3
        raw.extend(c.px[start:start + c.w * 3])
    def png_chunk(ctype, data):
        ch = struct.pack('>I', len(data)) + ctype + data
        ch += struct.pack('>I', zlib.crc32(ctype + data) & 0xffffffff)
        return ch
    ihdr = struct.pack('>IIBBBBB', c.w, c.h, 8, 2, 0, 0, 0)
    png = b'\x89PNG\r\n\x1a\n'
    png += png_chunk(b'IHDR', ihdr)
    png += png_chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    png += png_chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)

def main():
    c = Canvas(W, H)
    # outer border
    c.fill_rect(0, 0, W, 4, BLACK)
    c.fill_rect(0, H - 4, W, 4, BLACK)
    c.fill_rect(0, 0, 4, H, BLACK)
    c.fill_rect(W - 4, 0, 4, H, BLACK)
    M = 32  # margin
    CW = W - 2 * M  # 960

    # --- Top line: Vol / No. ---
    draw_text(c, M, 18, "VOL. 128  -  No. 327", 1, GREY)
    draw_text(c, W - M - text_width("PRICE: $2.50", 1), 18, "PRICE: $2.50", 1, GREY)

    # --- Masthead ---
    draw_text_centered(c, W // 2, 36, "THE DAILY HERALD", 7, BLACK)
    # decorative rule under masthead: thick + thin
    c.hline(M, 118, CW, BLACK, 4)
    c.hline(M, 125, CW, BLACK, 1)
    # date line
    draw_text_centered(c, W // 2, 134, "Monday, 23 November 2026", 2, BLACK)
    # left/right of date line
    draw_text(c, M, 134, "WORLD  -  WAR  -  MARKETS", 1, GREY)
    draw_text(c, W - M - text_width("EST. 1898", 1), 134, "EST. 1898", 1, GREY)
    c.hline(M, 158, CW, BLACK, 1)

    # --- Lead kicker ---
    draw_text_centered(c, W // 2, 168, "CLIMATE  -  COP31  -  TURKEY", 2, BLACK)

    # --- Lead headline (2 lines, centred, scale 5) ---
    draw_text_centered(c, W // 2, 192, "COP31 ENDS", 5, BLACK)
    draw_text_centered(c, W // 2, 232, "WITHOUT A DEAL", 5, BLACK)
    # subhead
    draw_text_centered(c, W // 2, 276, "Longest climate talks in history close", 2, BLACK)
    draw_text_centered(c, W // 2, 294, "after nearly 48 hours of overtime", 2, BLACK)
    c.hline(M, 318, CW, BLACK, 1)

    # --- Lead story: text left (600px), globe right (300px) ---
    lead_x = M
    lead_w = 600
    lead_y = 330
    y = draw_wrapped(c, lead_x, lead_y,
        "UN climate talks in Turkey ended without a deal, closing the longest UN climate conference in history after nearly 48 hours of overtime.",
        lead_w, 2, BLACK, 4)
    y += 6
    y = draw_wrapped(c, lead_x, y,
        "Negotiators left with no final agreement after deadlock over finance, fossil fuels and loss and damage.",
        lead_w, 2, BLACK, 4)

    # Globe illustration on right
    gx = M + 640
    gy = 330
    c.fill_rect(gx - 10, gy - 8, 320, 150, WHITE)
    # frame
    c.hline(gx - 10, gy - 8, 320, BLACK, 2)
    c.hline(gx - 10, gy + 142, 320, BLACK, 2)
    c.vline(gx - 10, gy - 8, 150, BLACK, 2)
    c.vline(gx + 310, gy - 8, 150, BLACK, 2)
    draw_globe(c, gx + 150, gy + 62, 58)
    draw_text_centered(c, gx + 150, gy + 128, "THE WORLD WAITS", 1, BLACK)

    c.hline(M, 480, CW, BLACK, 2)
    c.hline(M, 485, CW, BLACK, 1)

    # --- Column stories: 3 columns ---
    col_w = 304
    gap = 24
    col_x = [M, M + col_w + gap, M + 2 * (col_w + gap)]
    # vertical rules between columns
    for vx in [M + col_w + 12, M + 2 * col_w + gap + 12]:
        c.vline(vx, 496, 488, BLACK, 1)

    # Helper to draw a story block, returns next y
    def story(x, y, kicker, headline, body, max_y):
        draw_text(c, x, y, kicker, 1, GREY)
        y += 14
        y = draw_headline_wrapped(c, x, y, headline, col_w, 2, BLACK, 3)
        y += 4
        c.hline(x, y, col_w, BLACK, 1)
        y += 8
        y = draw_wrapped(c, x, y, body, col_w, 2, BLACK, 3)
        return y

    # Row 1: stories 2,3,4  y=496
    y1 = story(col_x[0], 496, "UKRAINE  -  SEA DRONE",
        "Ukraine sinks Russian warship",
        "Seven naval drones sank a Russian warship off a Libya base, destroying a Ka-27 helicopter and hitting cargo ship MV Angara.", 0)
    y2 = story(col_x[1], 496, "IRAN  -  WAR",
        "Trump: Iran wants a deal",
        "Trump said Iran wants a deal but not one acceptable to him. Iran struck US positions in Bahrain; a civilian site was hit, two injured.", 0)
    y3 = story(col_x[2], 496, "UKRAINE  -  STRIKES",
        "15 killed in Kyiv region",
        "Russian strikes killed at least 15 in the Kyiv region. A child was killed in Kryvyi Rih, officials said.", 0)

    # rule between rows
    c.hline(M, 668, CW, BLACK, 1)

    # Row 2: stories 5,6,7  y=680
    y4 = story(col_x[0], 680, "USA  -  POLITICS",
        "Democrats win big House majority",
        "US Democrats clinched their biggest House majority in decades, reshaping the balance of power in Washington.", 0)
    y5 = story(col_x[1], 680, "INDONESIA  -  FIRE",
        "24 dead in factory fire",
        "A factory fire in Banten left 24 body bags recovered. About 30 people are still unaccounted for as teams search the site.", 0)
    y6 = story(col_x[2], 680, "USA  -  AVIATION",
        "Delta delays 1,000 flights",
        "Delta delayed over 1,000 flights at its Atlanta hub after a technical issue disrupted operations through the day.", 0)

    c.hline(M, 856, CW, BLACK, 1)

    # Row 3: stories 8 and 9, plus bar chart
    # Story 8 in col 1
    y7 = story(col_x[0], 868, "SOUTH KOREA",
        "Cabinet reshuffle in Seoul",
        "The education minister resigned over college entrance exam confusion.", 0)
    # Story 9 in col 2 with chart in col 3
    y8 = story(col_x[1], 868, "MARKETS",
        "Oil tumbles, Asia sells off",
        "Oil tumbled; Asian markets sold off on AI valuation fears.", 0)
    # Bar chart in col 3
    draw_text(c, col_x[2], 868, "MARKETS  -  CHART", 1, GREY)
    draw_text(c, col_x[2], 882, "AI fears hit Asia", 2, BLACK)
    draw_bar_chart(c, col_x[2], 912, col_w, 36, [8, 6, 4], ["OIL", "ASIA", "AI"], BLACK)

    # Footer rule and text (above bottom border)
    # Note: row 3 text ends before footer; place footer at 1000? Actually canvas 1024, bottom border at 1020.
    # Use y=1004 for footer line inside? Adjust: footer at bottom area 1006 is too low, so place footer text at 1002 is clipped.
    # Instead footer is drawn at y=1000 area is tight; draw footer line at 1008 is not visible.
    # To keep footer legible, we draw it just above the bottom border at y=1000 with scale 1 (height 7).
    c.hline(M, 998, CW, BLACK, 1)
    draw_text(c, M, 1006, "THE DAILY HERALD  -  Monday, 23 November 2026  -  Page 1", 1, GREY)
    draw_text(c, W - M - text_width("All stories verified 23 Nov 2026", 1), 1006, "All stories verified 23 Nov 2026", 1, GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    write_png(c, out)
    print("wrote " + out)

if __name__ == "__main__":
    main()
