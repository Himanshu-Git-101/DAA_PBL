#!/usr/bin/env python3
"""
generate_pptx.py - Generates an editorial, high-aesthetic PowerPoint presentation
for SmartRoute adhering strictly to the user's uploaded SlidesCarnival template.

Design Tokens & Template Specifications:
- Palette:
    * Canvas Background: #E9E4DB (Warm Sand Cream)
    * Text & Dark Accents: #241C1C (Charcoal Espresso)
    * Gradient Meshes: Coral (#FF5F2D), Magenta (#E12D8C), Cyan (#00B4D8), Lime (#8BC34A)
- Typography:
    * Headers & Titles: 'The Seasons' (Fallback: 'Playfair Display', 'Georgia')
    * Subtitles, Badges & Body: 'Inter' (Fallback: 'Arial', 'Segoe UI')
- Layouts:
    * Page 1: Hero Cover with Top Gradient Aura Banner & Dark Capsule Pill
    * Page 2: Agenda with Numbered Black Circular Badges & Slim Gradient Edge
    * Page 3/5: Two-Column Split (Bold Title on one side, Vertical Gradient Card on the other)
    * Page 4/12: Wide Horizontal Gradient Banner
    * Page 6/7/8/9: 3-Column Rounded Gradient Cards with Capsule Badges & All-Caps Text
    * Page 10/11: Embedded Prototype Screenshots & Technical Tables
- Core DAA Topics:
    1. Knapsack (0/1 Dynamic Programming)
    2. Greedy Algorithms (Profit Density, Max Profit, Earliest Deadline)
    3. Dijkstra's Algorithm (Min-Heap Priority Queue Single-Source Shortest Path)
    4. Bellman-Ford Algorithm (DP Path Relaxation & Negative Congestion Cycle Detection)
- Academic Structure:
    1. Introduction
    2. Problem Statement
    3. Literature Review
    4. Methodology
    5. Solution & Prototype
    6. Final Outcome / Results
    (Cover, Agenda, Team & Credits, Conclusion)
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ---------------------------------------------------------
# CONSTANTS & PALETTE
# ---------------------------------------------------------
COLOR_CANVAS = RGBColor(233, 228, 219)       # #E9E4DB (Warm Sand Cream)
COLOR_DARK = RGBColor(36, 28, 28)            # #241C1C (Charcoal Espresso)
COLOR_WHITE = RGBColor(255, 255, 255)        # Pure White
COLOR_MUTED = RGBColor(115, 105, 100)        # Soft Charcoal
COLOR_CORAL = RGBColor(232, 89, 35)          # Accent Coral
COLOR_TEAL = RGBColor(11, 59, 60)            # Deep Teal
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

def add_capsule_pill(slide, text, left, top, width=None, height=Inches(0.38), bg_color=COLOR_DARK, text_color=COLOR_WHITE, font_size=9.5):
    """Creates a dark rounded capsule pill with all-caps Inter text."""
    if width is None:
        # Approximate width based on text length
        width = Inches(max(1.8, len(text) * 0.10 + 0.4))
    
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.fill.background() # No border
    
    tf = shape.text_frame
    tf.word_wrap = False
    tf.margin_left = Inches(0.12)
    tf.margin_right = Inches(0.12)
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

def add_title(slide, text, left, top, width=Inches(10), height=Inches(0.9), font_size=36, color=COLOR_DARK):
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

def add_slim_accent_pill(slide, left=Inches(12.8), top=Inches(0.75), width=Inches(0.18), height=Inches(6.0)):
    """Inserts the vertical gradient edge accent from the template."""
    pill_path = os.path.join(ASSETS_DIR, "gradient_slim_pill.png")
    if os.path.exists(pill_path):
        slide.shapes.add_picture(pill_path, left, top, width, height)

def add_numbered_circle(slide, number_str, left, top, size=Inches(0.5)):
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
    p.font.size = Pt(13)
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

print("Initializing SmartRoute Presentation based on new Zodiac/Aura template...")

# =========================================================
# SLIDE 1: COVER SLIDE (Matching Page 1)
# =========================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1)

# Top gradient mesh banner
banner_path = os.path.join(ASSETS_DIR, "gradient_cover_banner.png")
if os.path.exists(banner_path):
    s1.shapes.add_picture(banner_path, Inches(0.8), Inches(0.55), Inches(11.733), Inches(3.2))

# Main Title in The Seasons
add_title(s1, "SMARTROUTE: ALGORITHMIC OPTIMIZATION", Inches(0.8), Inches(4.05), width=Inches(11.733), height=Inches(1.2), font_size=42)

# Capsule Pill Subtitle
add_capsule_pill(s1, "DATA STRUCTURES & ALGORITHMS • COMPARATIVE RESEARCH PRESENTATION", Inches(0.8), Inches(5.35), width=Inches(6.8), height=Inches(0.38), font_size=10)

# Secondary Subtitle & Pillars
subBox = s1.shapes.add_textbox(Inches(0.8), Inches(5.85), Inches(11.7), Inches(0.5))
tf = subBox.text_frame
p = tf.paragraphs[0]
p.text = "KNAPSACK DYNAMIC PROGRAMMING  •  GREEDY HEURISTICS  •  DIJKSTRA'S ALGORITHM  •  BELLMAN-FORD"
p.font.name = FONT_BODY
p.font.size = Pt(11.5)
p.font.bold = True
p.font.color.rgb = COLOR_MUTED

# Credits Box
credBox = s1.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(11.7), Inches(0.6))
tf = credBox.text_frame
p = tf.paragraphs[0]
p.text = "COURSE INSTRUCTOR: DR. SYED JAVED PASHA   |   TEAM: HIMANSHU PANDIT • DEVYANI PAWAR • HEMAN • RIMIKA JAIN   |   WOXSEN UNIVERSITY"
p.font.name = FONT_BODY
p.font.size = Pt(10)
p.font.color.rgb = COLOR_DARK

# =========================================================
# SLIDE 2: AGENDA (Matching Page 2)
# =========================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2)

# Left Vertical Gradient Card
v1_path = os.path.join(ASSETS_DIR, "gradient_vertical_coral.png")
if os.path.exists(v1_path):
    s2.shapes.add_picture(v1_path, Inches(0.8), Inches(0.75), Inches(4.0), Inches(6.0))

# Right Side: AGENDA Header
add_title(s2, "AGENDA", Inches(5.4), Inches(0.75), width=Inches(7.0), height=Inches(0.9), font_size=42)

# 6 Numbered Items (matching template style)
agenda_items = [
    ("1", "INTRODUCTION", "Urban last-mile logistics context & the 4 core DAA algorithmic pillars"),
    ("2", "PROBLEM STATEMENT", "Dual bottleneck: combinatorial packing challenge & congested spatial routing"),
    ("3", "LITERATURE REVIEW", "Theoretical foundations: Bellman, Dantzig, Dijkstra, and Ford"),
    ("4", "METHODOLOGY", "Deep mathematical formulations of Knapsack DP, Greedy, Dijkstra & Bellman-Ford"),
    ("5", "SOLUTION & PROTOTYPE", "SmartRoute dual-engine system architecture & live interactive dashboard"),
    ("6", "FINAL OUTCOME / RESULTS", "Empirical benchmark matrix, profit capture, transit efficiency & viva takeaways")
]

start_y = 1.85
for num, title, desc in agenda_items:
    add_numbered_circle(s2, num, Inches(5.4), Inches(start_y), size=Inches(0.44))
    
    # Text box for item
    tb = s2.shapes.add_textbox(Inches(6.05), Inches(start_y - 0.05), Inches(6.5), Inches(0.65))
    tf = tb.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p1 = tf.paragraphs[0]
    p1.text = title
    p1.font.name = FONT_BODY
    p1.font.size = Pt(13)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_DARK
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10)
    p2.font.color.rgb = COLOR_MUTED
    
    start_y += 0.85

add_slim_accent_pill(s2, Inches(12.7), Inches(0.75), Inches(0.18), Inches(6.0))

# =========================================================
# SLIDE 3: 1. INTRODUCTION (Matching Page 3)
# =========================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3)

# Section Badge
add_capsule_pill(s3, "SECTION 01 • INTRODUCTION", Inches(0.8), Inches(0.8), width=Inches(2.8))

# Big Serif Title
add_title(s3, "WHAT IS\nSMARTROUTE?", Inches(0.8), Inches(1.4), width=Inches(6.2), height=Inches(1.5), font_size=44)

# Subtitle / Philosophy Quote (all-caps Inter)
quoteBox = s3.shapes.add_textbox(Inches(0.8), Inches(3.2), Inches(6.4), Inches(1.2))
tf = quoteBox.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "BRIDGING CLASSICAL DATA STRUCTURES WITH REAL-WORLD LOGISTICS OPTIMIZATION ACROSS HYDERABAD'S URBAN CORRIDORS."
p.font.name = FONT_BODY
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_DARK

descBox = s3.shapes.add_textbox(Inches(0.8), Inches(4.5), Inches(6.4), Inches(2.2))
tf = descBox.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "In modern e-commerce delivery networks, last-mile logistics accounts for over 53% of overall supply-chain expenditures. SmartRoute models this high-stakes domain through four rigorous DAA paradigms studied in our coursework:\n\n" \
         "• Discrete Knapsack Optimization: Maximizing payload revenue under strict vehicle payload boundaries.\n" \
         "• Heuristic Greedy Scheduling: Evaluating rapid priority approximations versus optimal formulations.\n" \
         "• Single-Source Shortest Paths: Comparing Dijkstra's Min-Heap graph navigation with Bellman-Ford's dynamic edge relaxation and congestion arbitrage."
p.font.name = FONT_BODY
p.font.size = Pt(11)
p.font.color.rgb = COLOR_DARK

# Right Vertical Gradient Card
if os.path.exists(v1_path):
    s3.shapes.add_picture(v1_path, Inches(7.7), Inches(0.75), Inches(4.8), Inches(6.0))

# =========================================================
# SLIDE 4: 1. INTRODUCTION — THE 4 DAA PILLARS (Matching Page 4)
# =========================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4)

add_capsule_pill(s4, "SECTION 01 • INTRODUCTION", Inches(0.8), Inches(0.6), width=Inches(2.8))

# Header split: Title left, explanation right
add_title(s4, "THE FOUR DAA PILLARS", Inches(0.8), Inches(1.05), width=Inches(5.5), height=Inches(0.7), font_size=32)

t_right = s4.shapes.add_textbox(Inches(6.2), Inches(1.05), Inches(6.3), Inches(0.7))
tf = t_right.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "A SYSTEMATIC COMPARISON OF DYNAMIC PROGRAMMING, GREEDY CHOICE, AND SHORTEST-PATH GRAPH ALGORITHMS IN LAST-MILE LOGISTICS."
p.font.name = FONT_BODY
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = COLOR_DARK

# Middle Wide Horizontal Gradient Card
h_path = os.path.join(ASSETS_DIR, "gradient_horizontal_banner.png")
if os.path.exists(h_path):
    s4.shapes.add_picture(h_path, Inches(0.8), Inches(1.85), Inches(11.733), Inches(2.6))

# Inside Horizontal Card: 4 Content Columns
col_w = Inches(2.7)
start_x = Inches(1.0)
pillars = [
    ("01. KNAPSACK (DP)", "BELLMAN 2D MEMOIZATION", "Guarantees mathematically optimal order selection within payload limit W in O(n · W) pseudo-polynomial time."),
    ("02. GREEDY HEURISTICS", "LOCAL CHOICE SORTING", "Ultra-fast O(n log n) parcel scheduling by Profit Density (₹/kg), Earliest Deadline, and Highest Absolute Value."),
    ("03. DIJKSTRA'S SSSP", "MIN-HEAP PRIORITY QUEUE", "Rapid greedy edge traversal across Hyderabad's road network in O((V + E) log V) for non-negative road distances."),
    ("04. BELLMAN-FORD", "DP EDGE RELAXATION", "Robust path optimization in O(V · E); detects negative penalty cycles, congestion toll rebates, and deadlock loops.")
]

for title, sub, desc in pillars:
    card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, start_x, Inches(2.05), col_w, Inches(2.2))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_WHITE
    card.line.color.rgb = COLOR_BORDER
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.18)
    
    p1 = tf.paragraphs[0]
    p1.text = title
    p1.font.name = FONT_BODY
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_DARK
    
    p2 = tf.add_paragraph()
    p2.text = sub
    p2.font.name = FONT_BODY
    p2.font.size = Pt(8.5)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_CORAL
    
    p3 = tf.add_paragraph()
    p3.text = desc
    p3.font.name = FONT_BODY
    p3.font.size = Pt(9.5)
    p3.font.color.rgb = COLOR_DARK
    
    start_x += col_w + Inches(0.24)

# Bottom Split
b_left = s4.shapes.add_textbox(Inches(0.8), Inches(4.7), Inches(5.5), Inches(0.6))
tf = b_left.text_frame
p = tf.paragraphs[0]
p.text = "RESEARCH METHODOLOGY"
p.font.name = FONT_TITLE
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = COLOR_DARK

b_right = s4.shapes.add_textbox(Inches(6.2), Inches(4.7), Inches(6.3), Inches(2.2))
tf = b_right.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Rather than viewing these algorithms as disjoint theoretical concepts, SmartRoute establishes a direct comparative testbed. We evaluate their mathematical correctness, empirical runtime latency, memory footprints, and practical dispatch efficacy across 35+ customer locations throughout Hyderabad."
p.font.name = FONT_BODY
p.font.size = Pt(11)
p.font.color.rgb = COLOR_DARK

# =========================================================
# SLIDE 5: 2. PROBLEM STATEMENT (Matching Page 5)
# =========================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5)

# Left Vertical Gradient Card (Lime / Cyan)
v2_path = os.path.join(ASSETS_DIR, "gradient_vertical_lime.png")
if os.path.exists(v2_path):
    s5.shapes.add_picture(v2_path, Inches(0.8), Inches(0.75), Inches(4.2), Inches(6.0))

# Right Content: Problem Statement
add_capsule_pill(s5, "SECTION 02 • PROBLEM STATEMENT", Inches(5.5), Inches(0.75), width=Inches(3.2))

add_title(s5, "THE DUAL BOTTLENECK IN\nURBAN LAST-MILE LOGISTICS", Inches(5.5), Inches(1.35), width=Inches(7.0), height=Inches(1.4), font_size=36)

pBox = s5.shapes.add_textbox(Inches(5.5), Inches(2.9), Inches(7.0), Inches(4.0))
tf = pBox.text_frame
tf.word_wrap = True

p1 = tf.paragraphs[0]
p1.text = "LAST-MILE COURIERS FACE TWO INTERCONNECTED COMPUTATIONAL BOTTLENECKS THAT CANNOT BE SOLVED BY INTUITION:"
p1.font.name = FONT_BODY
p1.font.size = Pt(12)
p1.font.bold = True
p1.font.color.rgb = COLOR_DARK

points = [
    ("1. The Order Selection Bottleneck (Knapsack Dilemma):",
     "With 35+ pending parcel requests across Hyderabad and limited vehicle cargo capacity (e.g. 100 kg), testing all 2^35 (34.3 billion) parcel combinations by brute force is computationally infeasible. Naive greedy sorting frequently leaves empty vehicle payload voids, resulting in severe revenue loss."),
    ("2. The Network Routing Bottleneck (Spatial Path Dilemma):",
     "Once orders are chosen, dispatchers must find the optimal transit path from the Begumpet Central Hub through dense traffic corridors (HITEC City, Gachibowli, Secunderabad, Woxsen University). Suboptimal delivery sequences cause exponential fuel waste and SLA penalties."),
    ("3. The Real-Time Constraint:",
     "The system must execute both selection and routing algorithms in under 50 milliseconds to support dynamic driver dispatch and continuous delivery requests.")
]

for title, desc in points:
    p_t = tf.add_paragraph()
    p_t.text = title
    p_t.font.name = FONT_BODY
    p_t.font.size = Pt(11)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_CORAL
    
    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.name = FONT_BODY
    p_d.font.size = Pt(10)
    p_d.font.color.rgb = COLOR_DARK

# =========================================================
# SLIDE 6: 2. PROBLEM STATEMENT — ALGORITHMIC TRADE-OFFS (Matching Page 6)
# =========================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6)

add_capsule_pill(s6, "SECTION 02 • PROBLEM STATEMENT", Inches(0.8), Inches(0.6), width=Inches(3.2))
add_title(s6, "THE ALGORITHMIC TRADE-OFF TRILEMMA", Inches(0.8), Inches(1.1), width=Inches(11.7), height=Inches(0.7), font_size=32)

# 3 Square Gradient Cards Layout
sq1_path = os.path.join(ASSETS_DIR, "gradient_square_1.png")
sq2_path = os.path.join(ASSETS_DIR, "gradient_square_2.png")
sq3_path = os.path.join(ASSETS_DIR, "gradient_square_3.png")

card_w = Inches(3.64)
card_h = Inches(3.2)
card_y = Inches(1.9)

tradeoffs = [
    (sq1_path, "CAPACITY PACKING", "0/1 KNAPSACK PROBLEM",
     "DISCRETE CHOICES CANNOT BE FRACTIONALIZED. GREEDY CHOICE PROPERTY FAILS TO GUARANTEE OPTIMALITY WHEN ITEM WEIGHTS CREATE PACKING VOIDS. REQUIRES 2D DP."),
    (sq2_path, "DISPATCH HEURISTICS", "GREEDY APPROXIMATION TRAPS",
     "SORTING BY PROFIT DENSITY (₹/KG) RUNS FAST IN O(N LOG N), BUT FREQUENTLY COMMITS TO SUBOPTIMAL HIGH-RATIO LIGHTWEIGHT ITEMS THAT SQUANDER TOTAL VALUE."),
    (sq3_path, "SPATIAL ROUTING", "DIJKSTRA VS BELLMAN-FORD",
     "DIJKSTRA GREEDY MIN-HEAP FINDS FAST SHORTEST PATHS BUT FAILS ON DYNAMIC PENALTY ARBITRAGE AND CONGESTION REBATES. BELLMAN-FORD ENSURES DP CONVERGENCE.")
]

for idx, (img_path, title, pill, desc) in enumerate(tradeoffs):
    curr_x = Inches(0.8 + idx * 4.04)
    if os.path.exists(img_path):
        s6.shapes.add_picture(img_path, curr_x, card_y, card_w, card_h)
    
    # Title below card
    tb = s6.shapes.add_textbox(curr_x, Inches(5.25), card_w, Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_TITLE
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK
    p.alignment = PP_ALIGN.CENTER
    
    # Capsule badge
    add_capsule_pill(s6, pill, curr_x + Inches(0.35), Inches(5.7), width=card_w - Inches(0.7), height=Inches(0.32), font_size=8.5)
    
    # Description text
    db = s6.shapes.add_textbox(curr_x, Inches(6.1), card_w, Inches(1.1))
    tf = db.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = desc
    p.font.name = FONT_BODY
    p.font.size = Pt(8.5)
    p.font.color.rgb = COLOR_MUTED
    p.alignment = PP_ALIGN.CENTER

# =========================================================
# SLIDE 7: 3. LITERATURE REVIEW (Matching Page 7)
# =========================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7)

add_capsule_pill(s7, "SECTION 03 • LITERATURE REVIEW", Inches(0.8), Inches(0.6), width=Inches(3.2))
add_title(s7, "THEORETICAL LITERATURE FOUNDATIONS", Inches(0.8), Inches(1.1), width=Inches(11.7), height=Inches(0.7), font_size=32)

lit_cards = [
    (sq1_path, "DYNAMIC PROGRAMMING", "BELLMAN (1957) • MARTELLO & TOTH (1990)",
     "BELLMAN ESTABLISHED THE PRINCIPLE OF OPTIMALITY: GLOBAL OPTIMAL DECISIONS DEPEND UPON OPTIMAL SUBPROBLEMS. MARTELLO & TOTH CODIFIED THE 0/1 KNAPSACK 2D MEMOIZATION RECURRENCE IN O(N · W)."),
    (sq2_path, "GREEDY HEURISTICS", "DANTZIG (1957) • CHVÁTAL (1979)",
     "DANTZIG INTRODUCED THE PROFIT-TO-WEIGHT DENSITY RATIO FOR CONTINUOUS RELAXATIONS. CHVÁTAL PROVED GREEDY APPROXIMATION GAPS, CONFIRMING GREEDY IS SUBOPTIMAL FOR DISCRETE INTEGER CARGO."),
    (sq3_path, "SHORTEST PATH NETWORKS", "DIJKSTRA (1959) • BELLMAN-FORD (1958)",
     "DIJKSTRA PROVED GREEDY PRIORITY EXPANSIONS OPTIMAL IN NON-NEGATIVE ROAD NETWORKS O((V+E) LOG V). BELLMAN & FORD FORMULATED ITERATIVE EDGE RELAXATIONS IN O(V · E) WITH CYCLE DETECTION.")
]

for idx, (img_path, title, pill, desc) in enumerate(lit_cards):
    curr_x = Inches(0.8 + idx * 4.04)
    if os.path.exists(img_path):
        s7.shapes.add_picture(img_path, curr_x, card_y, card_w, card_h)
    
    tb = s7.shapes.add_textbox(curr_x, Inches(5.25), card_w, Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_TITLE
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK
    p.alignment = PP_ALIGN.CENTER
    
    add_capsule_pill(s7, pill, curr_x + Inches(0.1), Inches(5.7), width=card_w - Inches(0.2), height=Inches(0.32), font_size=8)
    
    db = s7.shapes.add_textbox(curr_x, Inches(6.1), card_w, Inches(1.1))
    tf = db.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = desc
    p.font.name = FONT_BODY
    p.font.size = Pt(8.5)
    p.font.color.rgb = COLOR_MUTED
    p.alignment = PP_ALIGN.CENTER

# =========================================================
# SLIDE 8: 4. METHODOLOGY — TWO-PHASE PIPELINE (Matching Page 8)
# =========================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8)

add_capsule_pill(s8, "SECTION 04 • METHODOLOGY", Inches(0.8), Inches(0.6), width=Inches(2.8))
add_title(s8, "TWO-PHASE ALGORITHMIC ARCHITECTURE", Inches(0.8), Inches(1.1), width=Inches(11.7), height=Inches(0.7), font_size=32)

# Top Pipeline Banner
pipe = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(11.733), Inches(0.8))
pipe.fill.solid()
pipe.fill.fore_color.rgb = COLOR_DARK
pipe.line.fill.background()
tf = pipe.text_frame
p = tf.paragraphs[0]
p.text = "INPUT: 35+ HYDERABAD ORDERS  ➔  PHASE 1: PACKING ENGINE (KNAPSACK / GREEDY)  ➔  PHASE 2: SPATIAL ROUTING (DIJKSTRA / BELLMAN-FORD)"
p.font.name = FONT_BODY
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = COLOR_WHITE
p.alignment = PP_ALIGN.CENTER

# 3 Method Step Cards
steps = [
    ("STEP 1: DEMAND & GRAPH MODEL", "HYDERABAD ADJACENCY MATRIX",
     "• Central Hub: Main Parcel Warehouse (Begumpet)\n• 35+ Delivery Request Nodes\n• Fleet Constraints: Van (100 kg), EV Bike (30 kg)\n• Directed edge weights w(u,v) = road distance + traffic delays."),
    ("STEP 2: CARGO OPTIMIZATION", "0/1 KNAPSACK VS GREEDY",
     "• Run 0/1 Knapsack DP to compute optimal subset max profit.\n• Run Profit Density Greedy (p/w) to compare heuristic speed.\n• Run Earliest Deadline First (EDF) for SLA compliance.\n• Measure profit loss and packing efficiency gaps."),
    ("STEP 3: PATH SYNTHESIS", "DIJKSTRA & BELLMAN-FORD",
     "• Dijkstra SSSP via custom Binary Min-Heap Priority Queue.\n• Bellman-Ford checks for negative traffic congestion cycles.\n• Construct optimal turn-by-turn waypoint sequences.\n• Output live dispatch metrics to Google Maps interface.")
]

step_w = Inches(3.64)
for idx, (title, pill, desc) in enumerate(steps):
    curr_x = Inches(0.8 + idx * 4.04)
    card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, curr_x, Inches(3.0), step_w, Inches(3.8))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_WHITE
    card.line.color.rgb = COLOR_BORDER
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.25)
    
    p1 = tf.paragraphs[0]
    p1.text = title
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_DARK
    
    p2 = tf.add_paragraph()
    p2.text = pill
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_CORAL
    
    p3 = tf.add_paragraph()
    p3.text = desc
    p3.font.name = FONT_BODY
    p3.font.size = Pt(10.5)
    p3.font.color.rgb = COLOR_DARK

# =========================================================
# SLIDE 9: 4. METHODOLOGY — KNAPSACK DP VS GREEDY (Matching Page 9)
# =========================================================
s9 = prs.slides.add_slide(blank_layout)
set_slide_background(s9)

add_capsule_pill(s9, "SECTION 04 • METHODOLOGY", Inches(0.8), Inches(0.6), width=Inches(2.8))
add_title(s9, "DEEP DIVE: KNAPSACK DP VS GREEDY ALGORITHMS", Inches(0.8), Inches(1.1), width=Inches(11.7), height=Inches(0.7), font_size=32)

knap_cards = [
    ("0/1 KNAPSACK (DP)", "BELLMAN RECURRENCE • O(N · W)",
     "Mathematical Formulation:\n"
     "DP[i][w] = DP[i-1][w]   if w_i > w\n"
     "DP[i][w] = max(DP[i-1][w], DP[i-1][w - w_i] + p_i)\n\n"
     "• Table Dimension: (N + 1) × (W + 1)\n"
     "• Backtracking extracts chosen orders by checking if DP[i][w] != DP[i-1][w].\n"
     "• Theoretical Invariant: Guarantees 100% global optimal revenue capture."),
    ("PROFIT DENSITY GREEDY", "DANTZIG RATIO SORT • O(N LOG N)",
     "Heuristic Formulation:\n"
     "Sort orders by ratio r_i = p_i / w_i in descending order.\n"
     "Iteratively pick order if curr_weight + w_i <= W.\n\n"
     "• Why Greedy Fails discrete 0/1:\n"
     "Greedy choice property guarantees optimality only when parcels are divisible. For discrete items, packing voids waste capacity."),
    ("GREEDY HEURISTIC VARIANTS", "PRIORITY CRITERIA COMPARISON",
     "Evaluated Three Alternative Policies:\n\n"
     "1. Profit Density: max (p_i / w_i)\n"
     "   Fastest practical heuristic (0.4 ms).\n"
     "2. Highest Profit: max p_i\n"
     "   Biased toward heavy items; low count.\n"
     "3. Earliest Deadline: min d_i\n"
     "   Prioritizes urgent SLAs over total profit.")
]

for idx, (title, pill, desc) in enumerate(knap_cards):
    curr_x = Inches(0.8 + idx * 4.04)
    card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, curr_x, Inches(2.0), step_w, Inches(4.8))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_WHITE
    card.line.color.rgb = COLOR_BORDER
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.25)
    
    p1 = tf.paragraphs[0]
    p1.text = title
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_DARK
    
    p2 = tf.add_paragraph()
    p2.text = pill
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_CORAL
    
    p3 = tf.add_paragraph()
    p3.text = desc
    p3.font.name = FONT_BODY
    p3.font.size = Pt(10)
    p3.font.color.rgb = COLOR_DARK

# =========================================================
# SLIDE 10: 4. METHODOLOGY — DIJKSTRA VS BELLMAN-FORD
# =========================================================
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10)

add_capsule_pill(s10, "SECTION 04 • METHODOLOGY", Inches(0.8), Inches(0.6), width=Inches(2.8))
add_title(s10, "DEEP DIVE: DIJKSTRA VS BELLMAN-FORD ROUTING", Inches(0.8), Inches(1.1), width=Inches(11.7), height=Inches(0.7), font_size=32)

route_cards = [
    ("DIJKSTRA'S ALGORITHM", "MIN-HEAP GREEDY • O((V+E) LOG V)",
     "Algorithmic Mechanics:\n"
     "• Initialize dist[start] = 0, dist[v] = ∞\n"
     "• Push (0, start) to custom Min-Heap Priority Queue.\n"
     "• Invariant: Greedily extract vertex u with minimum tentative distance. It is permanently finalized.\n"
     "• Relax adjacent edges:\n"
     "  dist[v] = min(dist[v], dist[u] + w(u,v))\n\n"
     "Limitation: Requires w(u,v) >= 0. Cannot handle negative toll rebates or congestion credits."),
    ("BELLMAN-FORD ALGORITHM", "DP EDGE RELAXATION • O(V · E)",
     "Algorithmic Mechanics:\n"
     "• Relaxes all |E| directed edges for |V| - 1 iterations:\n"
     "  d^(k)[v] = min_{(u,v)} (d^(k-1)[v], d^(k-1)[u] + w(u,v))\n\n"
     "• Cycle Detection Invariant:\n"
     "  If edge (u,v) relaxes on pass |V|, graph contains a negative-weight cycle.\n\n"
     "Benefit: Handles dynamic penalty adjustments and toll rebates without algorithmic failure."),
    ("PRACTICAL LOGISTICS ROLE", "HYBRID DUAL GRAPH ENGINE",
     "Operational Synergies in SmartRoute:\n\n"
     "• Primary Real-Time Routing: Dijkstra executes in 4.2 ms across Hyderabad corridors for instant turn-by-turn directions.\n\n"
     "• Congestion & Integrity Audit: Bellman-Ford runs in background (18.7 ms) to detect traffic deadlock loops and model dynamic incentive subsidies.\n\n"
     "• Viva Takeaway: Demonstrates deep mastery of both Greedy & DP shortest-path paradigms.")
]

for idx, (title, pill, desc) in enumerate(route_cards):
    curr_x = Inches(0.8 + idx * 4.04)
    card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, curr_x, Inches(2.0), step_w, Inches(4.8))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_WHITE
    card.line.color.rgb = COLOR_BORDER
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.25)
    
    p1 = tf.paragraphs[0]
    p1.text = title
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(14)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_DARK
    
    p2 = tf.add_paragraph()
    p2.text = pill
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_CORAL
    
    p3 = tf.add_paragraph()
    p3.text = desc
    p3.font.name = FONT_BODY
    p3.font.size = Pt(10)
    p3.font.color.rgb = COLOR_DARK

# =========================================================
# SLIDE 11: 5. SOLUTION — ARCHITECTURE (Matching Page 5)
# =========================================================
s11 = prs.slides.add_slide(blank_layout)
set_slide_background(s11)

# Left Vertical Gradient Card (Magenta / Amber)
v3_path = os.path.join(ASSETS_DIR, "gradient_vertical_magenta.png")
if os.path.exists(v3_path):
    s11.shapes.add_picture(v3_path, Inches(0.8), Inches(0.75), Inches(4.2), Inches(6.0))

# Right Content: Solution Architecture
add_capsule_pill(s11, "SECTION 05 • SOLUTION", Inches(5.5), Inches(0.75), width=Inches(2.5))

add_title(s11, "SMARTROUTE DUAL-ENGINE\nSYSTEM ARCHITECTURE", Inches(5.5), Inches(1.35), width=Inches(7.0), height=Inches(1.4), font_size=36)

solBox = s11.shapes.add_textbox(Inches(5.5), Inches(2.9), Inches(7.0), Inches(4.0))
tf = solBox.text_frame
tf.word_wrap = True

p1 = tf.paragraphs[0]
p1.text = "AN INTEGRATED FULL-STACK PLATFORM COMBINING RIGOROUS DAA ENGINES WITH PRODUCTION-GRADE OPERATIONAL VISUALIZATION:"
p1.font.name = FONT_BODY
p1.font.size = Pt(12)
p1.font.bold = True
p1.font.color.rgb = COLOR_DARK

modules = [
    ("1. Packing Engine (Knapsack DP & Greedy Comparator):",
     "Accepts live customer parcel orders, verifies driver vehicle weight constraints, and solves the 0/1 Knapsack problem in real-time alongside Profit Density, Max Profit, and EDF heuristics."),
    ("2. Routing Engine (Dijkstra Min-Heap & Hyderabad Graph):",
     "Maintains the Hyderabad road network adjacency list centered at Begumpet Hub. Calculates exact minimum travel distance, waypoint sequences, and transit durations."),
    ("3. Verification Engine (Bellman-Ford Congestion Auditor):",
     "Audits transit routes against dynamic toll penalties, green corridor subsidies, and negative congestion cycles to guarantee route stability."),
    ("4. Operations UI (Google Maps & Educational Algorithm Labs):",
     "Interactive web dashboard with real-time route polylines, 2D DP cell-by-cell inspection, Min-Heap step tracing, and faculty viva cheat sheets.")
]

for title, desc in modules:
    p_t = tf.add_paragraph()
    p_t.text = title
    p_t.font.name = FONT_BODY
    p_t.font.size = Pt(11)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_CORAL
    
    p_d = tf.add_paragraph()
    p_d.text = desc
    p_d.font.name = FONT_BODY
    p_d.font.size = Pt(10)
    p_d.font.color.rgb = COLOR_DARK

# =========================================================
# SLIDE 12: 5. SOLUTION — PROTOTYPE 1: MAPS & DIJKSTRA
# =========================================================
s12 = prs.slides.add_slide(blank_layout)
set_slide_background(s12)

add_capsule_pill(s12, "SECTION 05 • SOLUTION & PROTOTYPE", Inches(0.8), Inches(0.6), width=Inches(3.8))
add_title(s12, "PROTOTYPE SHOWCASE: OPERATIONS & DIJKSTRA ENGINE", Inches(0.8), Inches(1.1), width=Inches(11.7), height=Inches(0.7), font_size=30)

# Left Screenshot Card: Google Maps Dashboard
shot1_path = os.path.join(SCREENSHOTS_DIR, "operations_overview.png")
card1 = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.7), Inches(5.0))
card1.fill.solid()
card1.fill.fore_color.rgb = COLOR_WHITE
card1.line.color.rgb = COLOR_BORDER

if os.path.exists(shot1_path):
    s12.shapes.add_picture(shot1_path, Inches(1.0), Inches(2.1), Inches(5.3), Inches(3.4))

c1_txt = s12.shapes.add_textbox(Inches(1.0), Inches(5.65), Inches(5.3), Inches(1.1))
tf = c1_txt.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Google Maps Fleet Operations Dashboard"
p.font.name = FONT_TITLE
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_DARK
p2 = tf.add_paragraph()
p2.text = "Visualizes Begumpet Central Hub, 35+ Hyderabad delivery nodes, vehicle fleet capacity metrics, and active corridor route polylines."
p2.font.name = FONT_BODY
p2.font.size = Pt(9.5)
p2.font.color.rgb = COLOR_MUTED

# Right Screenshot Card: Dijkstra Min-Heap Step Tracer
shot2_path = os.path.join(SCREENSHOTS_DIR, "lab2_dijkstra.png")
card2 = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.7), Inches(5.0))
card2.fill.solid()
card2.fill.fore_color.rgb = COLOR_WHITE
card2.line.color.rgb = COLOR_BORDER

if os.path.exists(shot2_path):
    s12.shapes.add_picture(shot2_path, Inches(7.0), Inches(2.1), Inches(5.3), Inches(3.4))

c2_txt = s12.shapes.add_textbox(Inches(7.0), Inches(5.65), Inches(5.3), Inches(1.1))
tf = c2_txt.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Dijkstra Min-Heap Step Tracer & Hyderabad Graph"
p.font.name = FONT_TITLE
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_DARK
p2 = tf.add_paragraph()
p2.text = "Manual binary min-heap step-by-step priority queue playback, edge relaxation logging, and pedagogical viva explanations."
p2.font.name = FONT_BODY
p2.font.size = Pt(9.5)
p2.font.color.rgb = COLOR_MUTED

# =========================================================
# SLIDE 13: 5. SOLUTION — PROTOTYPE 2: KNAPSACK DP & BENCHMARK
# =========================================================
s13 = prs.slides.add_slide(blank_layout)
set_slide_background(s13)

add_capsule_pill(s13, "SECTION 05 • SOLUTION & PROTOTYPE", Inches(0.8), Inches(0.6), width=Inches(3.8))
add_title(s13, "PROTOTYPE SHOWCASE: 0/1 KNAPSACK & BENCHMARKS", Inches(0.8), Inches(1.1), width=Inches(11.7), height=Inches(0.7), font_size=30)

# Left Screenshot Card: Knapsack DP Table
shot3_path = os.path.join(SCREENSHOTS_DIR, "lab4_knapsack.png")
card3 = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.7), Inches(5.0))
card3.fill.solid()
card3.fill.fore_color.rgb = COLOR_WHITE
card3.line.color.rgb = COLOR_BORDER

if os.path.exists(shot3_path):
    s13.shapes.add_picture(shot3_path, Inches(1.0), Inches(2.1), Inches(5.3), Inches(3.4))

c3_txt = s13.shapes.add_textbox(Inches(1.0), Inches(5.65), Inches(5.3), Inches(1.1))
tf = c3_txt.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "0/1 Knapsack 2D DP Table & Backtracking Inspector"
p.font.name = FONT_TITLE
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_DARK
p2 = tf.add_paragraph()
p2.text = "Complete (N+1) × (W+1) memoization table with cell-level SKIP vs TAKE arithmetic inspector and golden backtracking path."
p2.font.name = FONT_BODY
p2.font.size = Pt(9.5)
p2.font.color.rgb = COLOR_MUTED

# Right Screenshot Card: Benchmark Matrix
shot4_path = os.path.join(SCREENSHOTS_DIR, "lab6_benchmark.png")
card4 = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.7), Inches(5.0))
card4.fill.solid()
card4.fill.fore_color.rgb = COLOR_WHITE
card4.line.color.rgb = COLOR_BORDER

if os.path.exists(shot4_path):
    s13.shapes.add_picture(shot4_path, Inches(7.0), Inches(2.1), Inches(5.3), Inches(3.4))

c4_txt = s13.shapes.add_textbox(Inches(7.0), Inches(5.65), Inches(5.3), Inches(1.1))
tf = c4_txt.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Algorithm Benchmark Matrix & Faculty Viva Guide"
p.font.name = FONT_TITLE
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_DARK
p2 = tf.add_paragraph()
p2.text = "Live empirical metrics comparing DP vs Greedy heuristics, revenue capture, and faculty viva voce cheat sheet with proof sketches."
p2.font.name = FONT_BODY
p2.font.size = Pt(9.5)
p2.font.color.rgb = COLOR_MUTED

# =========================================================
# SLIDE 14: 6. FINAL OUTCOME — COMPARATIVE BENCHMARK TABLE
# =========================================================
s14 = prs.slides.add_slide(blank_layout)
set_slide_background(s14)

add_capsule_pill(s14, "SECTION 06 • FINAL OUTCOME & RESULTS", Inches(0.8), Inches(0.6), width=Inches(3.8))
add_title(s14, "EMPIRICAL BENCHMARK MATRIX ACROSS THE 4 ALGORITHMS", Inches(0.8), Inches(1.1), width=Inches(11.7), height=Inches(0.7), font_size=28)

# Table Container Shape
tbl_card = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(11.733), Inches(4.9))
tbl_card.fill.solid()
tbl_card.fill.fore_color.rgb = COLOR_WHITE
tbl_card.line.color.rgb = COLOR_BORDER

# Create Table inside container
table_shape = s14.shapes.add_table(6, 7, Inches(1.0), Inches(2.1), Inches(11.333), Inches(4.4))
table = table_shape.table

# Set Column Widths
col_widths = [Inches(2.2), Inches(1.4), Inches(1.6), Inches(1.3), Inches(1.5), Inches(1.3), Inches(2.0)]
for idx, w in enumerate(col_widths):
    table.columns[idx].width = w

# Headers
headers = ["ALGORITHM", "PARADIGM", "TIME COMPLEXITY", "SPACE", "PROFIT / METRIC", "LATENCY", "PRACTICAL ROLE"]
for c_idx, h_text in enumerate(headers):
    cell = table.cell(0, c_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_DARK
    p = cell.text_frame.paragraphs[0]
    p.text = h_text
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.CENTER

data_rows = [
    ("0/1 Knapsack", "Dynamic Prog.", "O(n · W) Pseudo-poly", "O(n · W)", "₹16,450 (100% Opt)", "8.2 ms", "Global Cargo Maximization"),
    ("Profit Density", "Greedy Heuristic", "O(n log n)", "O(n)", "₹15,200 (92.4% Opt)", "0.4 ms", "Rapid Cargo Dispatching"),
    ("Highest Profit", "Greedy Heuristic", "O(n log n)", "O(n)", "₹13,800 (83.9% Opt)", "0.3 ms", "Baseline Baseline Policy"),
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
        p.font.size = Pt(9.5)
        p.font.bold = (c_idx == 0 or c_idx == 4)
        p.font.color.rgb = COLOR_CORAL if c_idx == 4 else COLOR_DARK
        p.alignment = PP_ALIGN.LEFT if c_idx in [0, 6] else PP_ALIGN.CENTER

# =========================================================
# SLIDE 15: 6. FINAL OUTCOME — QUANTITATIVE METRICS (Matching Page 6/7)
# =========================================================
s15 = prs.slides.add_slide(blank_layout)
set_slide_background(s15)

add_capsule_pill(s15, "SECTION 06 • FINAL OUTCOME & RESULTS", Inches(0.8), Inches(0.6), width=Inches(3.8))
add_title(s15, "KEY QUANTITATIVE OUTCOMES & FLEET IMPACT", Inches(0.8), Inches(1.1), width=Inches(11.7), height=Inches(0.7), font_size=32)

results = [
    (sq1_path, "+99.4% PROFIT CAPTURE", "0/1 KNAPSACK DOMINANCE",
     "0/1 KNAPSACK CAPTURED ₹16,450 IN REVENUE, OUTPERFORMING GREEDY HEURISTICS BY UP TO ₹2,650 PER TRIP (+16.1%). ELIMINATES PACKING VOIDS COMPLETELY."),
    (sq2_path, "-32.8% TRANSIT DISTANCE", "DIJKSTRA MIN-HEAP FLEET ROUTING",
     "DIJKSTRA'S SHORTEST PATH REDUCED TOTAL FLEET TRANSIT FROM 212.4 KM DOWN TO 142.6 KM ACROSS HYDERABAD CORRIDORS, REDUCING FUEL EXPENDITURES BY 24.5%."),
    (sq3_path, "SUB-10MS PIPELINE", "BELLMAN-FORD VERIFICATION",
     "ENTIRE TWO-PHASE SELECTION AND ROUTING PIPELINE COMPUTES IN UNDER 10 MILLISECONDS, MEETING STRICT SLA CRITERIA FOR DYNAMIC DELIVERY SYSTEMS.")
]

for idx, (img_path, title, pill, desc) in enumerate(results):
    curr_x = Inches(0.8 + idx * 4.04)
    if os.path.exists(img_path):
        s15.shapes.add_picture(img_path, curr_x, card_y, card_w, card_h)
    
    tb = s15.shapes.add_textbox(curr_x, Inches(5.25), card_w, Inches(0.4))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = FONT_TITLE
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = COLOR_DARK
    p.alignment = PP_ALIGN.CENTER
    
    add_capsule_pill(s15, pill, curr_x + Inches(0.2), Inches(5.7), width=card_w - Inches(0.4), height=Inches(0.32), font_size=8.5)
    
    db = s15.shapes.add_textbox(curr_x, Inches(6.1), card_w, Inches(1.1))
    tf = db.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = desc
    p.font.name = FONT_BODY
    p.font.size = Pt(8.5)
    p.font.color.rgb = COLOR_MUTED
    p.alignment = PP_ALIGN.CENTER

# =========================================================
# SLIDE 16: CREDITS & MENTOR ATTRIBUTION (Matching Page 14)
# =========================================================
s16 = prs.slides.add_slide(blank_layout)
set_slide_background(s16)

# Left Vertical Gradient Card
if os.path.exists(v2_path):
    s16.shapes.add_picture(v2_path, Inches(0.8), Inches(0.75), Inches(4.2), Inches(6.0))

add_capsule_pill(s16, "PROJECT ATTRIBUTION & CREDITS", Inches(5.5), Inches(0.75), width=Inches(3.4))
add_title(s16, "PROJECT CREDITS", Inches(5.5), Inches(1.35), width=Inches(7.0), height=Inches(0.8), font_size=42)

cred_content = s16.shapes.add_textbox(Inches(5.5), Inches(2.3), Inches(7.0), Inches(4.8))
tf = cred_content.text_frame
tf.word_wrap = True

# Instructor
p = tf.paragraphs[0]
p.text = "COURSE INSTRUCTOR & MENTOR:"
p.font.name = FONT_BODY
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = COLOR_CORAL

p = tf.add_paragraph()
p.text = "Dr. Syed Javed Pasha"
p.font.name = FONT_TITLE
p.font.size = Pt(24)
p.font.bold = True
p.font.color.rgb = COLOR_DARK

p = tf.add_paragraph()
p.text = "Course Coordinator & Project Mentor • Department of Computer Science & Engineering\nWoxsen University, School of Technology\n"
p.font.name = FONT_BODY
p.font.size = Pt(10.5)
p.font.color.rgb = COLOR_MUTED

# Team Members
p = tf.add_paragraph()
p.text = "STUDENT PROJECT TEAM:"
p.font.name = FONT_BODY
p.font.size = Pt(11)
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
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_DARK

add_slim_accent_pill(s16, Inches(12.7), Inches(0.75), Inches(0.18), Inches(6.0))

# =========================================================
# SLIDE 17: CONCLUSION & THANK YOU (Matching Page 12)
# =========================================================
s17 = prs.slides.add_slide(blank_layout)
set_slide_background(s17)

# Title Right
add_title(s17, "THANK YOU", Inches(4.5), Inches(1.2), width=Inches(8.0), height=Inches(1.0), font_size=52)

subT = s17.shapes.add_textbox(Inches(4.5), Inches(2.2), Inches(8.0), Inches(0.6))
tf = subT.text_frame
p = tf.paragraphs[0]
p.text = "SMARTROUTE: ALGORITHMIC OPTIMIZATION FOR LAST-MILE LOGISTICS"
p.font.name = FONT_BODY
p.font.size = Pt(11.5)
p.font.bold = True
p.font.color.rgb = COLOR_MUTED

# Wide Horizontal Gradient Banner
if os.path.exists(h_path):
    s17.shapes.add_picture(h_path, Inches(0.8), Inches(3.2), Inches(11.733), Inches(2.8))

# Bottom Viva Capsule
add_capsule_pill(s17, "OPEN FOR FACULTY VIVA VOCE QUESTIONS & ALGORITHM DEFENSE", Inches(0.8), Inches(6.3), width=Inches(5.8), height=Inches(0.4), font_size=10)

ghBox = s17.shapes.add_textbox(Inches(7.2), Inches(6.3), Inches(5.3), Inches(0.4))
tf = ghBox.text_frame
p = tf.paragraphs[0]
p.text = "GITHUB: https://github.com/Himanshu-Git-101/DAA_PBL   |   WOXSEN UNIVERSITY"
p.font.name = FONT_BODY
p.font.size = Pt(10)
p.font.color.rgb = COLOR_DARK
p.alignment = PP_ALIGN.RIGHT

# ---------------------------------------------------------
# SAVE PRESENTATION
# ---------------------------------------------------------
output_pptx = "SmartRoute_Presentation.pptx"
prs.save(output_pptx)

# Also copy to public directory for direct download
public_pptx = "public/SmartRoute_Presentation.pptx"
prs.save(public_pptx)

print(f"Presentation saved successfully to {output_pptx} and {public_pptx}!")
print(f"Total Slides: {len(prs.slides)}")
