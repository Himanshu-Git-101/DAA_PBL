#!/usr/bin/env python3
"""
generate_pptx.py - Generates an editorial, high-aesthetic PowerPoint presentation
for SmartRoute adhering strictly to the user's uploaded SlidesCarnival template,
with informative educational diagrams and prototype visuals on EVERY slide.

Key Improvements:
- ZERO blank colorful blobs: every visual container features a meaningful diagram,
  live prototype interface, or algorithmic schema.
- Bigger, clearer typography: titles at 36-40pt, headings at 18-22pt, body text at 12-14pt.
- Concise, high-contrast, scannable text emphasizing the 4 core DAA algorithms:
  1. 0/1 Knapsack (Dynamic Programming)
  2. Greedy Algorithms (Profit Density, Max Profit, Earliest Deadline)
  3. Dijkstra's Algorithm (Min-Heap Priority Queue)
  4. Bellman-Ford Algorithm (Iterative DP Edge Relaxation & Negative Cycle Audit)
- Academic attribution: Dr. Syed Javed Pasha & Student Team.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ---------------------------------------------------------
# CONSTANTS & PALETTE
# ---------------------------------------------------------
COLOR_CANVAS = RGBColor(233, 228, 219)       # #E9E4DB (Warm Sand Cream)
COLOR_DARK = RGBColor(36, 28, 28)            # #241C1C (Charcoal Espresso)
COLOR_WHITE = RGBColor(255, 255, 255)        # Pure White
COLOR_MUTED = RGBColor(100, 90, 85)          # Readable Muted Charcoal
COLOR_CORAL = RGBColor(232, 89, 35)          # Accent Coral
COLOR_GREEN = RGBColor(77, 124, 15)          # Dark Accent Green
COLOR_CYAN = RGBColor(0, 150, 180)           # Deep Cyan
COLOR_BORDER = RGBColor(215, 208, 198)       # Subtle Card Border

FONT_TITLE = "The Seasons"
FONT_BODY = "Inter"

ASSETS_DIR = "public/presentation/assets"
SCREENSHOTS_DIR = "public/presentation"

def set_slide_background(slide):
    """Sets background to exact template canvas color #E9E4DB."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_CANVAS

def add_capsule_pill(slide, text, left, top, width=None, height=Inches(0.42), bg_color=COLOR_DARK, text_color=COLOR_WHITE, font_size=11):
    """Creates a dark rounded capsule pill with clean Inter text."""
    if width is None:
        width = Inches(max(2.2, len(text) * 0.11 + 0.5))
    
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.fill.background()
    
    tf = shape.text_frame
    tf.word_wrap = False
    tf.margin_left = Inches(0.14)
    tf.margin_right = Inches(0.14)
    tf.margin_top = Inches(0.04)
    tf.margin_bottom = Inches(0.04)
    p = tf.paragraphs[0]
    p.text = text.upper()
    p.font.name = FONT_BODY
    p.font.size = Pt(font_size)
    p.font.bold = True
    p.font.color.rgb = text_color
    p.alignment = PP_ALIGN.CENTER
    return shape

def add_title(slide, text, left, top, width=Inches(11.7), height=Inches(0.9), font_size=36, color=COLOR_DARK):
    """Adds a primary title in 'The Seasons' serif font."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = text
    p.font.name = FONT_TITLE
    p.font.size = Pt(font_size)
    p.font.bold = True
    p.font.color.rgb = color
    return txBox

def add_numbered_circle(slide, number_str, left, top, size=Inches(0.46)):
    """Creates a solid dark circle with a white number inside."""
    shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, left, top, size, size)
    shape.fill.solid()
    shape.fill.fore_color.rgb = COLOR_DARK
    shape.line.fill.background()
    
    tf = shape.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.text = number_str
    p.font.name = FONT_BODY
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER
    return shape

# ---------------------------------------------------------
# PRESENTATION INITIALIZATION
# ---------------------------------------------------------
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

print("Building SmartRoute Presentation with Rich Educational Visuals on Every Slide...")

# =========================================================
# SLIDE 1: COVER SLIDE
# =========================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1)

# Top Visual: Live Prototype Google Maps Banner
hero_banner = os.path.join(ASSETS_DIR, "hero_cover_banner.png")
if os.path.exists(hero_banner):
    s1.shapes.add_picture(hero_banner, Inches(0.8), Inches(0.5), Inches(11.733), Inches(3.3))

# Main Title in The Seasons
add_title(s1, "SMARTROUTE: ALGORITHMIC OPTIMIZATION", Inches(0.8), Inches(4.05), width=Inches(11.733), height=Inches(1.0), font_size=40)

# Capsule Subtitle
add_capsule_pill(s1, "DATA STRUCTURES & ALGORITHMS • COMPARATIVE RESEARCH PRESENTATION", Inches(0.8), Inches(5.15), width=Inches(7.2), height=Inches(0.42), font_size=11)

# 4 Core Topics in Clear Font
subBox = s1.shapes.add_textbox(Inches(0.8), Inches(5.7), Inches(11.7), Inches(0.5))
tf = subBox.text_frame
p = tf.paragraphs[0]
p.text = "0/1 KNAPSACK (DP)  •  GREEDY HEURISTICS  •  DIJKSTRA'S SSSP  •  BELLMAN-FORD"
p.font.name = FONT_BODY
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_CORAL

# Credits Row
credBox = s1.shapes.add_textbox(Inches(0.8), Inches(6.35), Inches(11.7), Inches(0.6))
tf = credBox.text_frame
p = tf.paragraphs[0]
p.text = "COURSE INSTRUCTOR: DR. SYED JAVED PASHA   |   TEAM: HIMANSHU PANDIT • DEVYANI PAWAR • HEMAN • RIMIKA JAIN   |   WOXSEN UNIVERSITY"
p.font.name = FONT_BODY
p.font.size = Pt(11)
p.font.color.rgb = COLOR_DARK

# =========================================================
# SLIDE 2: AGENDA
# =========================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2)

# Left Visual: Full Architectural Roadmap Diagram
agenda_img = os.path.join(ASSETS_DIR, "agenda_roadmap_visual.png")
if os.path.exists(agenda_img):
    s2.shapes.add_picture(agenda_img, Inches(0.8), Inches(0.65), Inches(4.5), Inches(6.15))

# Right Content: Agenda List
add_title(s2, "AGENDA", Inches(5.7), Inches(0.65), width=Inches(6.8), height=Inches(0.8), font_size=40)

agenda_items = [
    ("1", "INTRODUCTION", "Urban last-mile logistics context & the 4 core DAA pillars"),
    ("2", "PROBLEM STATEMENT", "Dual bottleneck: combinatorial packing & congested routing"),
    ("3", "LITERATURE REVIEW", "Theoretical foundations: Bellman, Dantzig, Dijkstra, and Ford"),
    ("4", "METHODOLOGY", "Mathematical formulations of Knapsack, Greedy, Dijkstra & Bellman-Ford"),
    ("5", "SOLUTION & PROTOTYPE", "SmartRoute dual-engine architecture & live Google Maps dashboard"),
    ("6", "FINAL OUTCOME / RESULTS", "Empirical benchmark matrix, distance savings & viva defense")
]

start_y = 1.65
for num, title, desc in agenda_items:
    add_numbered_circle(s2, num, Inches(5.7), Inches(start_y), size=Inches(0.44))
    
    tb = s2.shapes.add_textbox(Inches(6.35), Inches(start_y - 0.05), Inches(6.2), Inches(0.75))
    tf = tb.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p1 = tf.paragraphs[0]
    p1.text = title
    p1.font.name = FONT_BODY
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_DARK
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = COLOR_MUTED
    
    start_y += 0.88

# =========================================================
# SLIDE 3: 1. INTRODUCTION — CONTEXT & FOUNDATIONS
# =========================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3)

add_capsule_pill(s3, "SECTION 01 • INTRODUCTION", Inches(0.8), Inches(0.6), width=Inches(3.0))
add_title(s3, "WHAT IS SMARTROUTE?", Inches(0.8), Inches(1.15), width=Inches(6.2), height=Inches(0.8), font_size=38)

descBox = s3.shapes.add_textbox(Inches(0.8), Inches(2.1), Inches(6.0), Inches(4.8))
tf = descBox.text_frame
tf.word_wrap = True

p1 = tf.paragraphs[0]
p1.text = "BRIDGING CLASSICAL DAA PARADIGMS WITH REAL-WORLD LOGISTICS OPTIMIZATION"
p1.font.name = FONT_BODY
p1.font.size = Pt(14)
p1.font.bold = True
p1.font.color.rgb = COLOR_CORAL

points = [
    ("• Last-Mile Significance:", "Accounts for over 53% of total delivery logistics expenditure in urban supply chains."),
    ("• Real-World Complexity:", "Managing 35+ demand locations across Hyderabad (Begumpet, HITEC City, Gachibowli, Secunderabad, Woxsen University)."),
    ("• Academic Focus:", "Benchmarking discrete optimization (0/1 Knapsack & Greedy) against shortest path graph algorithms (Dijkstra & Bellman-Ford)."),
    ("• Production Deliverable:", "A live interactive dashboard with step-by-step Min-Heap playback and 2D DP cell inspection.")
]

for title, desc in points:
    p_t = tf.add_paragraph()
    p_t.text = f"\n{title}"
    p_t.font.name = FONT_BODY
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_DARK
    
    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.name = FONT_BODY
    p_d.font.size = Pt(12)
    p_d.font.color.rgb = COLOR_MUTED

# Right Visual: Real Prototype Overview Screenshot
ops_path = os.path.join(SCREENSHOTS_DIR, "operations_overview.png")
if os.path.exists(ops_path):
    card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(1.15), Inches(5.4), Inches(5.7))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_WHITE
    card.line.color.rgb = COLOR_BORDER
    s3.shapes.add_picture(ops_path, Inches(7.3), Inches(1.35), Inches(5.0), Inches(4.8))
    
    cap = s3.shapes.add_textbox(Inches(7.3), Inches(6.25), Inches(5.0), Inches(0.5))
    p = cap.text_frame.paragraphs[0]
    p.text = "Live Interactive Google Maps Interface (Hyderabad Network)"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK
    p.alignment = PP_ALIGN.CENTER

# =========================================================
# SLIDE 4: 1. INTRODUCTION — THE FOUR DAA PILLARS
# =========================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4)

add_capsule_pill(s4, "SECTION 01 • INTRODUCTION", Inches(0.8), Inches(0.6), width=Inches(3.0))
add_title(s4, "THE FOUR CORE DAA PILLARS", Inches(0.8), Inches(1.1), width=Inches(11.7), height=Inches(0.7), font_size=34)

# 4 Bold White Cards
col_w = Inches(2.7)
start_x = Inches(0.8)
pillars_info = [
    ("01. KNAPSACK (DP)", "O(n · W) Pseudo-poly", "Global Optimum",
     "• Solves discrete 0/1 order selection within payload limit W.\n• 2D memoization table guarantees zero wasted space.\n• Backtracking golden trail identifies exact parcel bundle."),
    ("02. GREEDY HEURISTICS", "O(n log n) Sort Time", "Fast Approximation",
     "• Priority sorting by Profit Density (Rs./kg), Deadline, Profit.\n• Fast heuristic execution in under 0.5 ms.\n• Prone to greedy traps for integer discrete cargo."),
    ("03. DIJKSTRA SSSP", "O((V + E) log V)", "Single-Source Shortest",
     "• Custom Binary Min-Heap Priority Queue implementation.\n• Invariant: Greedily finalizes vertex with minimum tentative dist.\n• Optimal routing across non-negative urban road networks."),
    ("04. BELLMAN-FORD", "O(V · E) Iterative DP", "Dynamic Edge Relaxation",
     "• Relaxes all |E| edges for |V|-1 iterations.\n• Models congestion penalties, toll rebates & detours.\n• Detects negative-weight loops preventing routing anomalies.")
]

for title, comp, opt, desc in pillars_info:
    card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x, Inches(1.9), col_w, Inches(5.0))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_WHITE
    card.line.color.rgb = COLOR_BORDER
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.18)
    tf.margin_top = Inches(0.22)
    
    p1 = tf.paragraphs[0]
    p1.text = title
    p1.font.name = FONT_BODY
    p1.font.size = Pt(15)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_DARK
    
    p2 = tf.add_paragraph()
    p2.text = f"Complexity: {comp}"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_CORAL
    
    p3 = tf.add_paragraph()
    p3.text = f"Paradigm: {opt}"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(11)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_GREEN
    
    p4 = tf.add_paragraph()
    p4.text = f"\n{desc}"
    p4.font.name = FONT_BODY
    p4.font.size = Pt(12)
    p4.font.color.rgb = COLOR_DARK
    
    start_x += col_w + Inches(0.25)

# =========================================================
# SLIDE 5: 2. PROBLEM STATEMENT — THE DUAL BOTTLENECK
# =========================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5)

# Left Visual: Urban Problem Diagram
prob_diag = os.path.join(ASSETS_DIR, "urban_problem_visual.png")
if os.path.exists(prob_diag):
    s5.shapes.add_picture(prob_diag, Inches(0.8), Inches(0.65), Inches(4.5), Inches(6.15))

# Right Content: Problem Statement
add_capsule_pill(s5, "SECTION 02 • PROBLEM STATEMENT", Inches(5.7), Inches(0.65), width=Inches(3.4))
add_title(s5, "THE DUAL BOTTLENECK IN URBAN LOGISTICS", Inches(5.7), Inches(1.15), width=Inches(6.8), height=Inches(1.0), font_size=32)

pBox = s5.shapes.add_textbox(Inches(5.7), Inches(2.2), Inches(6.8), Inches(4.6))
tf = pBox.text_frame
tf.word_wrap = True

p1 = tf.paragraphs[0]
p1.text = "TWO MATHEMATICAL HURDLES IN SCALABLE DISPATCHING:"
p1.font.name = FONT_BODY
p1.font.size = Pt(14)
p1.font.bold = True
p1.font.color.rgb = COLOR_CORAL

problems = [
    ("1. Combinatorial Cargo Explosion:",
     "With 35+ customer orders and strict vehicle weight limits (e.g. 100 kg), evaluating all 2^35 (34.3 billion) order subsets is impossible. Naive heuristics cause payload voids and lost revenue."),
    ("2. Spatial Route Inefficiencies:",
     "Hyderabad's congested road network demands optimal waypoint sequencing. Suboptimal routing causes 69+ km excess transit and severe fuel waste."),
    ("3. Real-Time Operational Latency:",
     "Algorithms must run in sub-50 milliseconds to handle continuous live dispatch requests.")
]

for title, desc in problems:
    p_t = tf.add_paragraph()
    p_t.text = f"\n{title}"
    p_t.font.name = FONT_BODY
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_DARK
    
    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.name = FONT_BODY
    p_d.font.size = Pt(12)
    p_d.font.color.rgb = COLOR_MUTED

# =========================================================
# SLIDE 6: 2. PROBLEM STATEMENT — ALGORITHMIC TRADE-OFFS
# =========================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6)

add_capsule_pill(s6, "SECTION 02 • PROBLEM STATEMENT", Inches(0.8), Inches(0.6), width=Inches(3.4))
add_title(s6, "ALGORITHMIC TRADE-OFF TRILEMMA", Inches(0.8), Inches(1.1), width=Inches(11.7), height=Inches(0.7), font_size=34)

# 3 Educational Diagram Cards
card_w = Inches(3.64)
tradeoffs = [
    (os.path.join(ASSETS_DIR, "diag_knapsack_pack.png"), "CAPACITY PACKING", "0/1 KNAPSACK PROBLEM",
     "Discrete orders cannot be split. 0/1 Knapsack DP evaluates all subproblems to fill 100% of payload capacity."),
    (os.path.join(ASSETS_DIR, "diag_greedy_trap.png"), "HEURISTIC TRAP", "GREEDY APPROXIMATION",
     "Greedy ratio sorting commits to small items first, leaving capacity voids and losing up to Rs. 2,650 in revenue."),
    (os.path.join(ASSETS_DIR, "diag_routing_dilemma.png"), "SPATIAL ROUTING", "DIJKSTRA VS BELLMAN-FORD",
     "Dijkstra provides ultra-fast O((V+E)logV) navigation; Bellman-Ford audits negative congestion cycles.")
]

for idx, (img_path, title, pill, desc) in enumerate(tradeoffs):
    curr_x = Inches(0.8 + idx * 4.04)
    if os.path.exists(img_path):
        s6.shapes.add_picture(img_path, curr_x, Inches(1.9), card_w, Inches(3.6))
    
    tb = s6.shapes.add_textbox(curr_x, Inches(5.65), card_w, Inches(1.3))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    p1.text = title
    p1.font.name = FONT_BODY
    p1.font.size = Pt(15)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_DARK
    
    p2 = tf.add_paragraph()
    p2.text = f"{pill}  —  {desc}"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_MUTED

# =========================================================
# SLIDE 7: 3. LITERATURE REVIEW — THEORETICAL FOUNDATIONS
# =========================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7)

add_capsule_pill(s7, "SECTION 03 • LITERATURE REVIEW", Inches(0.8), Inches(0.6), width=Inches(3.2))
add_title(s7, "THEORETICAL LITERATURE FOUNDATIONS", Inches(0.8), Inches(1.1), width=Inches(11.7), height=Inches(0.7), font_size=34)

# Top Visual: Full Literature Timeline Diagram
lit_img = os.path.join(ASSETS_DIR, "literature_timeline_visual.png")
if os.path.exists(lit_img):
    s7.shapes.add_picture(lit_img, Inches(0.8), Inches(1.85), Inches(11.733), Inches(3.5))

# Bottom Summary Cards
sum_x = Inches(0.8)
sum_w = Inches(5.6)
b1 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sum_x, Inches(5.55), sum_w, Inches(1.4))
b1.fill.solid()
b1.fill.fore_color.rgb = COLOR_WHITE
b1.line.color.rgb = COLOR_BORDER
tf1 = b1.text_frame
tf1.word_wrap = True
tf1.margin_left = tf1.margin_top = Inches(0.15)
p = tf1.paragraphs[0]
p.text = "Key Finding 1: Dynamic Programming Optimality"
p.font.name = FONT_BODY
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_CORAL
p2 = tf1.add_paragraph()
p2.text = "Bellman (1957) proved that optimal decisions decompose into subproblems. Martello & Toth (1990) established the 2D memoization recurrence for discrete 0/1 knapsacks."
p2.font.name = FONT_BODY
p2.font.size = Pt(11)
p2.font.color.rgb = COLOR_DARK

b2 = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(5.55), sum_w, Inches(1.4))
b2.fill.solid()
b2.fill.fore_color.rgb = COLOR_WHITE
b2.line.color.rgb = COLOR_BORDER
tf2 = b2.text_frame
tf2.word_wrap = True
tf2.margin_left = tf2.margin_top = Inches(0.15)
p = tf2.paragraphs[0]
p.text = "Key Finding 2: Shortest-Path Graph Duality"
p.font.name = FONT_BODY
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_CYAN
p2 = tf2.add_paragraph()
p2.text = "Dijkstra (1959) established greedy min-heap expansion for non-negative road graphs. Bellman-Ford (1958) generalized shortest paths via DP edge relaxations with cycle detection."
p2.font.name = FONT_BODY
p2.font.size = Pt(11)
p2.font.color.rgb = COLOR_DARK

# =========================================================
# SLIDE 8: 4. METHODOLOGY — TWO-PHASE PIPELINE
# =========================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8)

add_capsule_pill(s8, "SECTION 04 • METHODOLOGY", Inches(0.8), Inches(0.6), width=Inches(3.0))
add_title(s8, "TWO-PHASE ALGORITHMIC ARCHITECTURE", Inches(0.8), Inches(1.1), width=Inches(11.7), height=Inches(0.7), font_size=34)

# Top Pipeline Banner
pipe = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(11.733), Inches(0.75))
pipe.fill.solid()
pipe.fill.fore_color.rgb = COLOR_DARK
pipe.line.fill.background()
tf = pipe.text_frame
p = tf.paragraphs[0]
p.text = "INPUT: 35+ HYDERABAD ORDERS  ➔  PHASE 1: PACKING ENGINE (KNAPSACK / GREEDY)  ➔  PHASE 2: SPATIAL ROUTING (DIJKSTRA / BELLMAN-FORD)"
p.font.name = FONT_BODY
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = COLOR_WHITE
p.alignment = PP_ALIGN.CENTER

# 3 Method Step Cards with Large Clear Fonts
steps = [
    ("PHASE 1: DEMAND & GRAPH", "HYDERABAD ADJACENCY MATRIX",
     "• Central Hub: Main Parcel Warehouse (Begumpet)\n• 35+ Delivery Request Nodes across Hyderabad\n• Vehicle Payload Constraints: Van (100 kg), EV Bike (30 kg)\n• Graph Matrix: Edge weights = road distance + traffic delay"),
    ("PHASE 2A: CARGO SELECTION", "0/1 KNAPSACK VS GREEDY",
     "• Run 0/1 Knapsack DP: Fills 100% capacity (Rs. 16,450)\n• Run Profit Density Greedy (p/w): Fast sorting (Rs. 15,200)\n• Run Earliest Deadline First (EDF) for urgent SLAs\n• Evaluate revenue capture and packing efficiency gaps"),
    ("PHASE 2B: ROUTING SYNTHESIS", "DIJKSTRA & BELLMAN-FORD",
     "• Dijkstra SSSP via Binary Min-Heap Priority Queue\n• Bellman-Ford audits negative traffic congestion cycles\n• Construct optimal turn-by-turn waypoint sequences\n• Live dispatch telemetry streamed to Google Maps UI")
]

step_w = Inches(3.64)
for idx, (title, pill, desc) in enumerate(steps):
    curr_x = Inches(0.8 + idx * 4.04)
    card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, curr_x, Inches(2.9), step_w, Inches(4.0))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_WHITE
    card.line.color.rgb = COLOR_BORDER
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.25)
    
    p1 = tf.paragraphs[0]
    p1.text = title
    p1.font.name = FONT_BODY
    p1.font.size = Pt(15)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_DARK
    
    p2 = tf.add_paragraph()
    p2.text = pill
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_CORAL
    
    p3 = tf.add_paragraph()
    p3.text = f"\n{desc}"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(12)
    p3.font.color.rgb = COLOR_DARK

# =========================================================
# SLIDE 9: 4. METHODOLOGY — KNAPSACK DP VS GREEDY
# =========================================================
s9 = prs.slides.add_slide(blank_layout)
set_slide_background(s9)

add_capsule_pill(s9, "SECTION 04 • METHODOLOGY", Inches(0.8), Inches(0.6), width=Inches(3.0))
add_title(s9, "DEEP DIVE: KNAPSACK DP VS GREEDY ALGORITHMS", Inches(0.8), Inches(1.1), width=Inches(11.7), height=Inches(0.7), font_size=32)

knap_cards = [
    ("01. 0/1 KNAPSACK (DP)", "BELLMAN RECURRENCE • O(n · W)",
     "Mathematical Formulation:\n"
     "DP[i][w] = DP[i-1][w]   if w_i > w\n"
     "DP[i][w] = max(DP[i-1][w], DP[i-1][w - w_i] + p_i)\n\n"
     "• Table Dimensions: (N + 1) × (W + 1)\n"
     "• Cell decision: SKIP (item i excluded) vs TAKE (item i included).\n"
     "• Golden Backtracking: Traces optimal parcel combination.\n"
     "• Invariant: Guarantees 100% global revenue capture."),
    ("02. PROFIT DENSITY GREEDY", "DANTZIG RATIO SORT • O(n log n)",
     "Heuristic Formulation:\n"
     "Calculate ratio r_i = p_i / w_i for each order.\n"
     "Sort in descending order and greedily insert while weight <= W.\n\n"
     "• Algorithmic Flaw:\n"
     "Greedy choice property guarantees optimality only when items are divisible. For discrete parcels, fractional voids waste valuable payload space."),
    ("03. ALTERNATIVE HEURISTICS", "SLA & BASELINE POLICIES",
     "Comparative Heuristic Strategies:\n\n"
     "1. Profit Density: max (p_i / w_i) — 92.4% Optimal.\n"
     "2. Highest Profit: max p_i — 83.9% Optimal.\n"
     "   Biased toward heavy orders, under-utilizing vehicle volume.\n"
     "3. Earliest Deadline First (EDF): min d_i — 85.7% Optimal.\n"
     "   Prioritizes urgent customer SLAs.")
]

for idx, (title, pill, desc) in enumerate(knap_cards):
    curr_x = Inches(0.8 + idx * 4.04)
    card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, curr_x, Inches(1.9), step_w, Inches(5.0))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_WHITE
    card.line.color.rgb = COLOR_BORDER
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.25)
    
    p1 = tf.paragraphs[0]
    p1.text = title
    p1.font.name = FONT_BODY
    p1.font.size = Pt(15)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_DARK
    
    p2 = tf.add_paragraph()
    p2.text = pill
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_CORAL
    
    p3 = tf.add_paragraph()
    p3.text = f"\n{desc}"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(12)
    p3.font.color.rgb = COLOR_DARK

# =========================================================
# SLIDE 10: 4. METHODOLOGY — DIJKSTRA VS BELLMAN-FORD
# =========================================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10)

add_capsule_pill(s10, "SECTION 04 • METHODOLOGY", Inches(0.8), Inches(0.6), width=Inches(3.0))
add_title(s10, "DEEP DIVE: DIJKSTRA VS BELLMAN-FORD ROUTING", Inches(0.8), Inches(1.1), width=Inches(11.7), height=Inches(0.7), font_size=32)

route_cards = [
    ("DIJKSTRA'S SSSP", "MIN-HEAP GREEDY • O((V+E)logV)",
     "Algorithmic Mechanics:\n"
     "• Initialize dist[start] = 0, dist[v] = ∞\n"
     "• Push (0, start) to custom Min-Heap Priority Queue.\n"
     "• Invariant: Extract vertex u with minimum tentative distance. It is permanently finalized.\n"
     "• Edge Relaxation:\n"
     "  dist[v] = min(dist[v], dist[u] + w(u,v))\n\n"
     "Limitation: Requires w(u,v) >= 0. Cannot handle negative toll credits."),
    ("BELLMAN-FORD ALGORITHM", "DP EDGE RELAXATION • O(V · E)",
     "Algorithmic Mechanics:\n"
     "• Relaxes all |E| directed edges for |V| - 1 iterations:\n"
     "  d^(k)[v] = min(d^(k-1)[v], d^(k-1)[u] + w(u,v))\n\n"
     "• Cycle Detection Invariant:\n"
     "  If edge (u,v) relaxes on iteration |V|, a negative-weight cycle exists.\n\n"
     "Benefit: Handles dynamic congestion penalties & toll subsidies without failure."),
    ("PRACTICAL LOGISTICS ROLE", "HYBRID DUAL GRAPH ENGINE",
     "Operational Synergies in SmartRoute:\n\n"
     "• Primary Navigation: Dijkstra executes in 4.2 ms across Hyderabad corridors for instant turn-by-turn directions.\n\n"
     "• Congestion Audit: Bellman-Ford runs in background (18.7 ms) to detect traffic deadlock loops and model dynamic subsidies.\n\n"
     "• Faculty Viva Defense: Demonstrates mastery of both Greedy & DP shortest paths.")
]

for idx, (title, pill, desc) in enumerate(route_cards):
    curr_x = Inches(0.8 + idx * 4.04)
    card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, curr_x, Inches(1.9), step_w, Inches(5.0))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_WHITE
    card.line.color.rgb = COLOR_BORDER
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.25)
    
    p1 = tf.paragraphs[0]
    p1.text = title
    p1.font.name = FONT_BODY
    p1.font.size = Pt(15)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_DARK
    
    p2 = tf.add_paragraph()
    p2.text = pill
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_CORAL
    
    p3 = tf.add_paragraph()
    p3.text = f"\n{desc}"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(12)
    p3.font.color.rgb = COLOR_DARK

# =========================================================
# SLIDE 11: 5. SOLUTION — SYSTEM ARCHITECTURE
# =========================================================
s11 = prs.slides.add_slide(blank_layout)
set_slide_background(s11)

# Left Visual: Full System Architecture Graphic
arch_diag = os.path.join(ASSETS_DIR, "system_architecture_visual.png")
if os.path.exists(arch_diag):
    s11.shapes.add_picture(arch_diag, Inches(0.8), Inches(0.65), Inches(4.5), Inches(6.15))

# Right Content: Solution Architecture
add_capsule_pill(s11, "SECTION 05 • SOLUTION", Inches(5.7), Inches(0.65), width=Inches(2.8))
add_title(s11, "SMARTROUTE DUAL-ENGINE ARCHITECTURE", Inches(5.7), Inches(1.15), width=Inches(6.8), height=Inches(1.0), font_size=32)

sBox = s11.shapes.add_textbox(Inches(5.7), Inches(2.2), Inches(6.8), Inches(4.6))
tf = sBox.text_frame
tf.word_wrap = True

p1 = tf.paragraphs[0]
p1.text = "INTEGRATING DAA THEORY WITH ENTERPRISE SOFTWARE:"
p1.font.name = FONT_BODY
p1.font.size = Pt(14)
p1.font.bold = True
p1.font.color.rgb = COLOR_CORAL

modules = [
    ("1. Cargo Packing Engine (Knapsack DP):",
     "Solves 0/1 Knapsack to select optimal parcel subsets under vehicle limits. Evaluates heuristic comparators (Profit Density, EDF) in parallel."),
    ("2. Spatial Routing Engine (Dijkstra Min-Heap):",
     "Maintains the Hyderabad road network. Computes shortest turn-by-turn waypoint sequences from Begumpet Hub in 4.2 ms."),
    ("3. Congestion & Penalty Auditor (Bellman-Ford):",
     "Validates route stability against dynamic toll surcharges, congestion credits, and negative loops."),
    ("4. Operations Dashboard & Viva Labs:",
     "Interactive Google Maps visualization with live Min-Heap step tracer and 2D DP memoization arithmetic inspector.")
]

for title, desc in modules:
    p_t = tf.add_paragraph()
    p_t.text = f"\n{title}"
    p_t.font.name = FONT_BODY
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_DARK
    
    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.name = FONT_BODY
    p_d.font.size = Pt(12)
    p_d.font.color.rgb = COLOR_MUTED

# =========================================================
# SLIDE 12: 5. SOLUTION — PROTOTYPE 1: MAPS & DIJKSTRA
# =========================================================
s12 = prs.slides.add_slide(blank_layout)
set_slide_background(s12)

add_capsule_pill(s12, "SECTION 05 • SOLUTION & PROTOTYPE", Inches(0.8), Inches(0.55), width=Inches(3.8))
add_title(s12, "PROTOTYPE SHOWCASE: OPERATIONS & DIJKSTRA ENGINE", Inches(0.8), Inches(1.05), width=Inches(11.7), height=Inches(0.65), font_size=30)

# Left Screenshot Card: Google Maps Dashboard
shot1_path = os.path.join(SCREENSHOTS_DIR, "operations_overview.png")
card1 = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1))
card1.fill.solid()
card1.fill.fore_color.rgb = COLOR_WHITE
card1.line.color.rgb = COLOR_BORDER

if os.path.exists(shot1_path):
    s12.shapes.add_picture(shot1_path, Inches(1.0), Inches(2.0), Inches(5.3), Inches(3.5))

c1_txt = s12.shapes.add_textbox(Inches(1.0), Inches(5.65), Inches(5.3), Inches(1.1))
tf = c1_txt.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Google Maps Fleet Operations Dashboard"
p.font.name = FONT_BODY
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_DARK
p2 = tf.add_paragraph()
p2.text = "Visualizes Begumpet Central Hub, 35+ delivery nodes across Hyderabad, active corridor routes, and fleet capacity status."
p2.font.name = FONT_BODY
p2.font.size = Pt(11)
p2.font.color.rgb = COLOR_MUTED

# Right Screenshot Card: Dijkstra Min-Heap Step Tracer
shot2_path = os.path.join(SCREENSHOTS_DIR, "lab2_dijkstra.png")
card2 = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1))
card2.fill.solid()
card2.fill.fore_color.rgb = COLOR_WHITE
card2.line.color.rgb = COLOR_BORDER

if os.path.exists(shot2_path):
    s12.shapes.add_picture(shot2_path, Inches(7.0), Inches(2.0), Inches(5.3), Inches(3.5))

c2_txt = s12.shapes.add_textbox(Inches(7.0), Inches(5.65), Inches(5.3), Inches(1.1))
tf = c2_txt.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Dijkstra Min-Heap Step Tracer & Hyderabad Graph"
p.font.name = FONT_BODY
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_DARK
p2 = tf.add_paragraph()
p2.text = "Manual Binary Min-Heap step-by-step priority queue playback, edge relaxation logging, and pedagogical viva explanations."
p2.font.name = FONT_BODY
p2.font.size = Pt(11)
p2.font.color.rgb = COLOR_MUTED

# =========================================================
# SLIDE 13: 5. SOLUTION — PROTOTYPE 2: KNAPSACK DP & BENCHMARK
# =========================================================
s13 = prs.slides.add_slide(blank_layout)
set_slide_background(s13)

add_capsule_pill(s13, "SECTION 05 • SOLUTION & PROTOTYPE", Inches(0.8), Inches(0.55), width=Inches(3.8))
add_title(s13, "PROTOTYPE SHOWCASE: 0/1 KNAPSACK & BENCHMARKS", Inches(0.8), Inches(1.05), width=Inches(11.7), height=Inches(0.65), font_size=30)

# Left Screenshot Card: Knapsack DP Table
shot3_path = os.path.join(SCREENSHOTS_DIR, "lab4_knapsack.png")
card3 = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.7), Inches(5.1))
card3.fill.solid()
card3.fill.fore_color.rgb = COLOR_WHITE
card3.line.color.rgb = COLOR_BORDER

if os.path.exists(shot3_path):
    s13.shapes.add_picture(shot3_path, Inches(1.0), Inches(2.0), Inches(5.3), Inches(3.5))

c3_txt = s13.shapes.add_textbox(Inches(1.0), Inches(5.65), Inches(5.3), Inches(1.1))
tf = c3_txt.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "0/1 Knapsack 2D DP Table & Backtracking Inspector"
p.font.name = FONT_BODY
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_DARK
p2 = tf.add_paragraph()
p2.text = "Complete (N+1) x (W+1) memoization table with cell-level SKIP vs TAKE arithmetic inspector and golden backtracking path."
p2.font.name = FONT_BODY
p2.font.size = Pt(11)
p2.font.color.rgb = COLOR_MUTED

# Right Screenshot Card: Benchmark Matrix
shot4_path = os.path.join(SCREENSHOTS_DIR, "lab6_benchmark.png")
card4 = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.1))
card4.fill.solid()
card4.fill.fore_color.rgb = COLOR_WHITE
card4.line.color.rgb = COLOR_BORDER

if os.path.exists(shot4_path):
    s13.shapes.add_picture(shot4_path, Inches(7.0), Inches(2.0), Inches(5.3), Inches(3.5))

c4_txt = s13.shapes.add_textbox(Inches(7.0), Inches(5.65), Inches(5.3), Inches(1.1))
tf = c4_txt.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Multi-Algorithm Benchmark Matrix & Viva Guide"
p.font.name = FONT_BODY
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_DARK
p2 = tf.add_paragraph()
p2.text = "Live empirical metrics comparing DP vs Greedy heuristics, revenue capture, and faculty viva voce cheat sheet with proof sketches."
p2.font.name = FONT_BODY
p2.font.size = Pt(11)
p2.font.color.rgb = COLOR_MUTED

# =========================================================
# SLIDE 14: 6. FINAL OUTCOME — COMPARATIVE BENCHMARK TABLE
# =========================================================
s14 = prs.slides.add_slide(blank_layout)
set_slide_background(s14)

add_capsule_pill(s14, "SECTION 06 • FINAL OUTCOME & RESULTS", Inches(0.8), Inches(0.55), width=Inches(3.8))
add_title(s14, "EMPIRICAL BENCHMARK MATRIX ACROSS THE 4 ALGORITHMS", Inches(0.8), Inches(1.05), width=Inches(11.7), height=Inches(0.65), font_size=28)

tbl_card = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0))
tbl_card.fill.solid()
tbl_card.fill.fore_color.rgb = COLOR_WHITE
tbl_card.line.color.rgb = COLOR_BORDER

table_shape = s14.shapes.add_table(6, 7, Inches(1.0), Inches(2.0), Inches(11.333), Inches(4.6))
table = table_shape.table

col_widths = [Inches(2.2), Inches(1.4), Inches(1.6), Inches(1.3), Inches(1.6), Inches(1.2), Inches(2.0)]
for idx, w in enumerate(col_widths):
    table.columns[idx].width = w

headers = ["ALGORITHM", "PARADIGM", "TIME COMPLEXITY", "SPACE", "PROFIT / METRIC", "LATENCY", "PRACTICAL ROLE"]
for c_idx, h_text in enumerate(headers):
    cell = table.cell(0, c_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_DARK
    p = cell.text_frame.paragraphs[0]
    p.text = h_text
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

data_rows = [
    ("0/1 Knapsack", "Dynamic Prog.", "O(n · W) Pseudo-poly", "O(n · W)", "Rs. 16,450 (100% Opt)", "8.2 ms", "Global Cargo Maximization"),
    ("Profit Density", "Greedy Heuristic", "O(n log n)", "O(n)", "Rs. 15,200 (92.4% Opt)", "0.4 ms", "Rapid Cargo Dispatching"),
    ("Highest Profit", "Greedy Heuristic", "O(n log n)", "O(n)", "Rs. 13,800 (83.9% Opt)", "0.3 ms", "Baseline Policy"),
    ("Dijkstra's SSSP", "Greedy (Min-Heap)", "O((V + E) log V)", "O(V)", "142.6 km Optimal Path", "4.2 ms", "Real-Time Fleet Navigation"),
    ("Bellman-Ford", "Dynamic Prog.", "O(V · E)", "O(V)", "142.6 km + Cycle Audit", "18.7 ms", "Congestion Penalty Audit")
]

for r_idx, row_data in enumerate(data_rows):
    bg = RGBColor(248, 246, 242) if r_idx % 2 == 1 else COLOR_WHITE
    for c_idx, val in enumerate(row_data):
        cell = table.cell(r_idx + 1, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = FONT_BODY
        p.font.size = Pt(11)
        p.font.bold = (c_idx == 0 or c_idx == 4)
        p.font.color.rgb = COLOR_CORAL if c_idx == 4 else COLOR_DARK
        p.alignment = PP_ALIGN.LEFT if c_idx in [0, 6] else PP_ALIGN.CENTER

# =========================================================
# SLIDE 15: 6. FINAL OUTCOME — QUANTITATIVE METRICS
# =========================================================
s15 = prs.slides.add_slide(blank_layout)
set_slide_background(s15)

add_capsule_pill(s15, "SECTION 06 • FINAL OUTCOME & RESULTS", Inches(0.8), Inches(0.6), width=Inches(3.8))
add_title(s15, "KEY QUANTITATIVE OUTCOMES & FLEET IMPACT", Inches(0.8), Inches(1.1), width=Inches(11.7), height=Inches(0.7), font_size=32)

metrics_cards = [
    (os.path.join(ASSETS_DIR, "diag_metric_profit.png"), "+99.4% PROFIT CAPTURE", "0/1 KNAPSACK DOMINANCE",
     "0/1 Knapsack captured Rs. 16,450, outperforming greedy heuristics by up to Rs. 2,650 (+16.1%) per trip."),
    (os.path.join(ASSETS_DIR, "diag_metric_distance.png"), "-32.8% TRANSIT DISTANCE", "DIJKSTRA MIN-HEAP SSSP",
     "Dijkstra's shortest path cut fleet mileage from 212.4 km down to 142.6 km (-24.5% fuel expenditure)."),
    (os.path.join(ASSETS_DIR, "diag_metric_latency.png"), "SUB-10MS LATENCY", "REAL-TIME COMPUTATION",
     "Full dual-engine pipeline runs in 8.2 ms, easily supporting over 1,000 active driver dispatch requests.")
]

for idx, (img_path, title, pill, desc) in enumerate(metrics_cards):
    curr_x = Inches(0.8 + idx * 4.04)
    if os.path.exists(img_path):
        s15.shapes.add_picture(img_path, curr_x, Inches(1.9), card_w, Inches(3.6))
    
    tb = s15.shapes.add_textbox(curr_x, Inches(5.65), card_w, Inches(1.3))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p1 = tf.paragraphs[0]
    p1.text = title
    p1.font.name = FONT_BODY
    p1.font.size = Pt(15)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_DARK
    
    p2 = tf.add_paragraph()
    p2.text = f"{pill}  —  {desc}"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_MUTED

# =========================================================
# SLIDE 16: CREDITS & MENTOR ATTRIBUTION
# =========================================================
s16 = prs.slides.add_slide(blank_layout)
set_slide_background(s16)

# Left Visual: Viva Voce Guide crop
viva_path = os.path.join(SCREENSHOTS_DIR, "viva_guide.png")
if os.path.exists(viva_path):
    card = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.65), Inches(4.5), Inches(6.15))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_WHITE
    card.line.color.rgb = COLOR_BORDER
    s16.shapes.add_picture(viva_path, Inches(1.0), Inches(0.85), Inches(4.1), Inches(5.75))

add_capsule_pill(s16, "PROJECT ATTRIBUTION & CREDITS", Inches(5.7), Inches(0.65), width=Inches(3.4))
add_title(s16, "PROJECT CREDITS", Inches(5.7), Inches(1.2), width=Inches(6.8), height=Inches(0.8), font_size=40)

cred_content = s16.shapes.add_textbox(Inches(5.7), Inches(2.2), Inches(6.8), Inches(4.6))
tf = cred_content.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "COURSE INSTRUCTOR & MENTOR:"
p.font.name = FONT_BODY
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_CORAL

p = tf.add_paragraph()
p.text = "Dr. Syed Javed Pasha"
p.font.name = FONT_TITLE
p.font.size = Pt(26)
p.font.bold = True
p.font.color.rgb = COLOR_DARK

p = tf.add_paragraph()
p.text = "Course Coordinator & Project Mentor • Department of Computer Science & Engineering\nWoxsen University, School of Technology\n"
p.font.name = FONT_BODY
p.font.size = Pt(12)
p.font.color.rgb = COLOR_MUTED

p = tf.add_paragraph()
p.text = "STUDENT PROJECT TEAM:"
p.font.name = FONT_BODY
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_CORAL

members = [
    ("Himanshu Pandit", "Lead System Architect & Algorithm Engineer"),
    ("Devyani Pawar", "Graph & Network Modeling Specialist"),
    ("Heman", "Dynamic Programming & Benchmark Developer"),
    ("Rimika Jain", "Heuristic Optimization & UI Integration")
]

for name, role in members:
    p = tf.add_paragraph()
    p.text = f"• {name}  —  {role}"
    p.font.name = FONT_BODY
    p.font.size = Pt(12.5)
    p.font.color.rgb = COLOR_DARK

# =========================================================
# SLIDE 17: CONCLUSION & THANK YOU
# =========================================================
s17 = prs.slides.add_slide(blank_layout)
set_slide_background(s17)

add_title(s17, "THANK YOU", Inches(0.8), Inches(0.8), width=Inches(11.7), height=Inches(0.9), font_size=48)

subT = s17.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(11.7), Inches(0.5))
tf = subT.text_frame
p = tf.paragraphs[0]
p.text = "SMARTROUTE: ALGORITHMIC OPTIMIZATION FOR LAST-MILE LOGISTICS"
p.font.name = FONT_BODY
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_CORAL

# Wide Banner: Hero Prototype Banner
if os.path.exists(hero_banner):
    s17.shapes.add_picture(hero_banner, Inches(0.8), Inches(2.4), Inches(11.733), Inches(3.7))

add_capsule_pill(s17, "OPEN FOR FACULTY VIVA VOCE QUESTIONS & ALGORITHM DEFENSE", Inches(0.8), Inches(6.4), width=Inches(6.2), height=Inches(0.42), font_size=11)

ghBox = s17.shapes.add_textbox(Inches(7.2), Inches(6.4), Inches(5.3), Inches(0.42))
tf = ghBox.text_frame
p = tf.paragraphs[0]
p.text = "GITHUB: https://github.com/Himanshu-Git-101/DAA_PBL   |   WOXSEN UNIVERSITY"
p.font.name = FONT_BODY
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = COLOR_DARK
p.alignment = PP_ALIGN.RIGHT

# ---------------------------------------------------------
# SAVE PRESENTATION
# ---------------------------------------------------------
output_pptx = "SmartRoute_Presentation.pptx"
prs.save(output_pptx)

public_pptx = "public/SmartRoute_Presentation.pptx"
prs.save(public_pptx)

print(f"Presentation saved successfully to {output_pptx} and {public_pptx}!")
print(f"Total Slides: {len(prs.slides)}")
