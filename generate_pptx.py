"""
generate_pptx.py - Generates an authentic, creative, pastel-themed PowerPoint presentation (.pptx)
for SmartRoute: Last-Mile Delivery Operations & Algorithmic Optimization Engine.
Inspired by the SlidesCarnival creative template with winding road motifs, 8-point starbursts,
florets, pastel containers, and embedded high-resolution prototype screenshots.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# 1. Color Palette Definitions (from uploaded template)
CREAM_BG = RGBColor(244, 239, 234)       # #F4EFEA - Warm canvas
DARK_TEAL = RGBColor(11, 59, 60)         # #0B3B3C - Deep Spruce
ORANGE = RGBColor(232, 89, 35)           # #E85923 - Terracotta
LIME_GREEN = RGBColor(132, 204, 22)      # #84CC16 - Spring Chartreuse
PASTEL_PEACH = RGBColor(248, 182, 141)   # #F8B68D - Soft Peach
WHITE = RGBColor(255, 255, 255)          # #FFFFFF - Crisp White
SLATE_DARK = RGBColor(30, 41, 59)        # #1E293B - Body text dark
SLATE_MUTED = RGBColor(100, 116, 139)    # #64748B - Muted caption
CARD_BG = RGBColor(255, 255, 255)        # Pure white card
PASTEL_GREEN_BG = RGBColor(241, 248, 233)# Light green tint
PASTEL_ORANGE_BG = RGBColor(255, 243, 235)# Light orange tint

FONT_TITLE = "Tenor Sans"
FONT_BODY = "Arial"

def set_slide_background(slide, color):
    """Sets a solid colored background rectangle covering the entire slide."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background() # No border
    return bg

def add_header(slide, section_tag, title_text, dark_mode=False):
    """Adds a stylish header with section badge and main title."""
    # Badge
    badge_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8), Inches(0.4))
    tf_b = badge_box.text_frame
    tf_b.word_wrap = True
    p_b = tf_b.paragraphs[0]
    p_b.text = f"●  {section_tag.upper()}"
    p_b.font.name = FONT_BODY
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = LIME_GREEN if dark_mode else ORANGE

    # Main Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.5), Inches(0.8))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = FONT_TITLE
    p_t.font.size = Pt(28)
    p_t.font.bold = True
    p_t.font.color.rgb = WHITE if dark_mode else DARK_TEAL

def add_starburst(slide, left, top, size, color):
    """Adds an 8-point geometric starburst badge."""
    star = slide.shapes.add_shape(MSO_SHAPE.STAR_8_POINT, left, top, size, size)
    star.fill.solid()
    star.fill.fore_color.rgb = color
    star.line.fill.background()
    return star

def add_floret(slide, left, top, size, color):
    """Adds an 12-point scalloped starburst."""
    floret = slide.shapes.add_shape(MSO_SHAPE.STAR_12_POINT, left, top, size, size)
    floret.fill.solid()
    floret.fill.fore_color.rgb = color
    floret.line.fill.background()
    return floret

def add_curved_road_motif(slide, color=ORANGE, position="bottom"):
    """Adds dynamic road/wave ribbons matching the template design."""
    if position == "bottom":
        # Wavy bottom ribbon
        ribbon = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(-1), Inches(6.2), Inches(15.333), Inches(1.5))
        ribbon.fill.solid()
        ribbon.fill.fore_color.rgb = color
        ribbon.line.fill.background()
        ribbon.rotation = 2
    elif position == "top_right":
        ribbon = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(9), Inches(-0.5), Inches(5), Inches(8.5))
        ribbon.fill.solid()
        ribbon.fill.fore_color.rgb = color
        ribbon.line.fill.background()
        ribbon.rotation = 90

def add_card(slide, left, top, width, height, title, body_text="", bg_color=WHITE, border_color=None, star_color=None):
    """Adds a rounded rectangular card with optional starburst icon and text."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
    else:
        card.line.fill.background()

    # Starburst accent
    if star_color:
        star_size = Inches(0.4)
        add_starburst(slide, left + Inches(0.2), top + Inches(0.2), star_size, star_color)
        text_left = left + Inches(0.7)
        text_width = width - Inches(0.9)
    else:
        text_left = left + Inches(0.3)
        text_width = width - Inches(0.6)

    tb = slide.shapes.add_textbox(text_left, top + Inches(0.2), text_width, height - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    
    # Title
    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.name = FONT_TITLE
    p_title.font.size = Pt(15)
    p_title.font.bold = True
    p_title.font.color.rgb = DARK_TEAL

    # Body
    if body_text:
        p_body = tf.add_paragraph()
        p_body.text = body_text
        p_body.font.name = FONT_BODY
        p_body.font.size = Pt(11.5)
        p_body.font.color.rgb = SLATE_DARK
        p_body.space_before = Pt(8)

    return card

def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    assets_dir = "/Users/himanshu/Documents/Daa PBL/public/presentation"

    # =========================================================================
    # SLIDE 1: Title Slide (Cover)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s1, CREAM_BG)

    # Wavy graphic ribbons (Lime green & Terracotta)
    w1 = s1.shapes.add_shape(MSO_SHAPE.OVAL, Inches(-2), Inches(4.5), Inches(17), Inches(5))
    w1.fill.solid()
    w1.fill.fore_color.rgb = ORANGE
    w1.line.fill.background()

    w2 = s1.shapes.add_shape(MSO_SHAPE.OVAL, Inches(4), Inches(2.5), Inches(11), Inches(6))
    w2.fill.solid()
    w2.fill.fore_color.rgb = LIME_GREEN
    w2.line.fill.background()

    # Starburst accents
    add_starburst(s1, Inches(1.2), Inches(0.8), Inches(1.4), ORANGE)
    add_floret(s1, Inches(10.8), Inches(0.8), Inches(1.2), DARK_TEAL)

    # Main Big Title
    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11), Inches(3.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "SMARTROUTE"
    p0.font.name = FONT_TITLE
    p0.font.size = Pt(54)
    p0.font.bold = True
    p0.font.color.rgb = DARK_TEAL

    p1 = tf1.add_paragraph()
    p1.text = "Last-Mile Delivery Operations & Algorithmic Optimization Engine"
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(12)

    p2 = tf1.add_paragraph()
    p2.text = "Design and Analysis of Algorithms (DAA - PBL) | University Final Defense"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(13)
    p2.font.color.rgb = CREAM_BG
    p2.space_before = Pt(8)

    # Academic Credentials Box (Bottom Left & Right)
    box_inst = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(5.2), Inches(5.2), Inches(1.6))
    box_inst.fill.solid()
    box_inst.fill.fore_color.rgb = WHITE
    box_inst.line.fill.background()
    tf_inst = box_inst.text_frame
    tf_inst.word_wrap = True
    p_i1 = tf_inst.paragraphs[0]
    p_i1.text = "FACULTY GUIDE & COURSE INSTRUCTOR"
    p_i1.font.name = FONT_BODY
    p_i1.font.size = Pt(10)
    p_i1.font.bold = True
    p_i1.font.color.rgb = ORANGE
    p_i2 = tf_inst.add_paragraph()
    p_i2.text = "Dr. Syed Javed Pasha"
    p_i2.font.name = FONT_TITLE
    p_i2.font.size = Pt(18)
    p_i2.font.bold = True
    p_i2.font.color.rgb = DARK_TEAL
    p_i3 = tf_inst.add_paragraph()
    p_i3.text = "Department of Computer Science & Engineering"
    p_i3.font.name = FONT_BODY
    p_i3.font.size = Pt(11)
    p_i3.font.color.rgb = SLATE_MUTED

    box_team = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(5.2), Inches(5.3), Inches(1.6))
    box_team.fill.solid()
    box_team.fill.fore_color.rgb = WHITE
    box_team.line.fill.background()
    tf_team = box_team.text_frame
    tf_team.word_wrap = True
    p_t1 = tf_team.paragraphs[0]
    p_t1.text = "PROJECT DEVELOPMENT TEAM"
    p_t1.font.name = FONT_BODY
    p_t1.font.size = Pt(10)
    p_t1.font.bold = True
    p_t1.font.color.rgb = LIME_GREEN
    p_t2 = tf_team.add_paragraph()
    p_t2.text = "Himanshu Pandit  •  Devyani Pawar\nHeman  •  Rimika Jain"
    p_t2.font.name = FONT_TITLE
    p_t2.font.size = Pt(14)
    p_t2.font.bold = True
    p_t2.font.color.rgb = DARK_TEAL
    p_t3 = tf_team.add_paragraph()
    p_t3.text = "Greater Hyderabad & Woxsen University NH65 Corridor"
    p_t3.font.name = FONT_BODY
    p_t3.font.size = Pt(11)
    p_t3.font.color.rgb = SLATE_MUTED

    # =========================================================================
    # SLIDE 2: Table of Contents (Template Slide 3 Style)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s2, CREAM_BG)
    add_header(s2, "Executive Agenda", "Table of Contents")

    # Three large geometric badges
    # 1. Lime Green Floret
    add_floret(s2, Inches(1.2), Inches(2.2), Inches(3.4), LIME_GREEN)
    tb_c1 = s2.shapes.add_textbox(Inches(1.5), Inches(3.0), Inches(2.8), Inches(1.8))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    p_c1_t = tf_c1.paragraphs[0]
    p_c1_t.text = "01. Foundations"
    p_c1_t.font.name = FONT_TITLE
    p_c1_t.font.size = Pt(18)
    p_c1_t.font.bold = True
    p_c1_t.font.color.rgb = WHITE
    p_c1_t.alignment = PP_ALIGN.CENTER
    p_c1_b = tf_c1.add_paragraph()
    p_c1_b.text = "• Introduction\n• 53% Cost Bottleneck\n• Problem Statement\n• CVRPTW Constraints"
    p_c1_b.font.name = FONT_BODY
    p_c1_b.font.size = Pt(11)
    p_c1_b.font.color.rgb = WHITE
    p_c1_b.alignment = PP_ALIGN.CENTER
    p_c1_b.space_before = Pt(8)

    # 2. Terracotta Starburst
    add_starburst(s2, Inches(5.0), Inches(2.0), Inches(3.6), ORANGE)
    tb_c2 = s2.shapes.add_textbox(Inches(5.3), Inches(2.9), Inches(3.0), Inches(2.0))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    p_c2_t = tf_c2.paragraphs[0]
    p_c2_t.text = "02. Core Algorithms"
    p_c2_t.font.name = FONT_TITLE
    p_c2_t.font.size = Pt(18)
    p_c2_t.font.bold = True
    p_c2_t.font.color.rgb = WHITE
    p_c2_t.alignment = PP_ALIGN.CENTER
    p_c2_b = tf_c2.add_paragraph()
    p_c2_b.text = "• Literature Review\n• Two-Tier Solution\n• Graph & Min-Heap\n• 0/1 Knapsack DP\n• Invariant Scheduling"
    p_c2_b.font.name = FONT_BODY
    p_c2_b.font.size = Pt(11)
    p_c2_b.font.color.rgb = WHITE
    p_c2_b.alignment = PP_ALIGN.CENTER
    p_c2_b.space_before = Pt(8)

    # 3. Dark Teal Rosette
    add_floret(s2, Inches(8.9), Inches(2.2), Inches(3.4), DARK_TEAL)
    tb_c3 = s2.shapes.add_textbox(Inches(9.2), Inches(3.0), Inches(2.8), Inches(1.8))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True
    p_c3_t = tf_c3.paragraphs[0]
    p_c3_t.text = "03. Demonstration"
    p_c3_t.font.name = FONT_TITLE
    p_c3_t.font.size = Pt(18)
    p_c3_t.font.bold = True
    p_c3_t.font.color.rgb = WHITE
    p_c3_t.alignment = PP_ALIGN.CENTER
    p_c3_b = tf_c3.add_paragraph()
    p_c3_b.text = "• Prototype Screenshots\n• Algorithm Lab Trace\n• Benchmark Matrix\n• Faculty Viva Defense"
    p_c3_b.font.name = FONT_BODY
    p_c3_b.font.size = Pt(11)
    p_c3_b.font.color.rgb = WHITE
    p_c3_b.alignment = PP_ALIGN.CENTER
    p_c3_b.space_before = Pt(8)

    # =========================================================================
    # SLIDE 3: Section 01 Divider - INTRODUCTION (Template Slide 4 Style)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s3, LIME_GREEN)

    # Starburst cutouts in cream
    add_starburst(s3, Inches(-1.5), Inches(1.5), Inches(4.5), CREAM_BG)
    add_floret(s3, Inches(10.5), Inches(1.5), Inches(4.5), CREAM_BG)

    tb_s3 = s3.shapes.add_textbox(Inches(2.5), Inches(2.8), Inches(8.333), Inches(1.8))
    tf_s3 = tb_s3.text_frame
    p_s3 = tf_s3.paragraphs[0]
    p_s3.text = "01. INTRODUCTION"
    p_s3.font.name = FONT_TITLE
    p_s3.font.size = Pt(46)
    p_s3.font.bold = True
    p_s3.font.color.rgb = DARK_TEAL
    p_s3.alignment = PP_ALIGN.CENTER

    p_s3_sub = tf_s3.add_paragraph()
    p_s3_sub.text = "The Urban Logistics Dilemma & Educational Scope"
    p_s3_sub.font.name = FONT_BODY
    p_s3_sub.font.size = Pt(16)
    p_s3_sub.font.color.rgb = WHITE
    p_s3_sub.alignment = PP_ALIGN.CENTER
    p_s3_sub.space_before = Pt(10)

    # =========================================================================
    # SLIDE 4: Introduction - The 53% Cost Bottleneck & Hyderabad Scope
    # =========================================================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s4, CREAM_BG)
    add_header(s4, "Context & Motivation", "The Urban Last-Mile Logistics Crisis")
    add_curved_road_motif(s4, LIME_GREEN, "bottom")

    # 3 Pastel Cards with Starbursts
    add_card(s4, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.0),
             "1. The 53% Cost Trap",
             "Last-mile dispatching accounts for over 53% of overall supply chain expenditure. Erratic driver routing and suboptimal package selection bleed operating capital through wasted fuel and missed SLAs.",
             WHITE, border_color=ORANGE, star_color=ORANGE)

    add_card(s4, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.0),
             "2. The Hyderabad Corridor",
             "Rapid urbanization connects dense tech corridors (Hitec City, Gachibowli) with distant highway universities (Woxsen University on NH65). Fixed delivery promises require guaranteed non-Euclidean road paths.",
             WHITE, border_color=LIME_GREEN, star_color=LIME_GREEN)

    add_card(s4, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.0),
             "3. The Pedagogical Goal",
             "Bridge classical DAA coursework with realistic software engineering. Provide transparent visualizations of Min-Heaps, Bellman DP tables, and route invariants for comprehensive faculty viva defense.",
             WHITE, border_color=DARK_TEAL, star_color=DARK_TEAL)

    # =========================================================================
    # SLIDE 5: Problem Statement - Multi-Constraint Dispatch Challenge
    # =========================================================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s5, CREAM_BG)
    add_header(s5, "Problem Definition", "The Multi-Constrained Dispatch Challenge")

    # 4 Grid Cards
    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.2),
             "📦 Payload Capacity Constraint",
             "The fleet operates under physical mass limits (e.g., 75 kg for Van V-101, 120 kg for Truck V-102). Overloading breaches transportation safety laws; underloading damages profit margins.",
             WHITE, border_color=ORANGE)

    add_card(s5, Inches(6.8), Inches(1.8), Inches(5.6), Inches(2.2),
             "⏱️ Strict SLA Arrival Deadlines",
             "Each package has a customer delivery window (e.g. 180 to 380 mins). A single late arrival triggers financial chargebacks, customer churn, and dispatch failure.",
             WHITE, border_color=ORANGE)

    add_card(s5, Inches(0.8), Inches(4.4), Inches(5.6), Inches(2.2),
             "🗺️ Non-Euclidean Road Topology",
             "Straight-line distance approximations fail across urban flyovers and arterial bottlenecks. Turn-by-turn shortest paths must be computed using realistic weighted road edges.",
             WHITE, border_color=LIME_GREEN)

    add_card(s5, Inches(6.8), Inches(4.4), Inches(5.6), Inches(2.2),
             "🧩 Discrete 0/1 Indivisibility",
             "Parcels are atomic units. Drivers cannot deliver 50% of an electronic item or medical shipment. The decision space is strictly discrete: {0, 1}.",
             WHITE, border_color=LIME_GREEN)

    # =========================================================================
    # SLIDE 6: Section 02 Divider - LITERATURE REVIEW
    # =========================================================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s6, ORANGE)

    add_starburst(s6, Inches(1.0), Inches(0.8), Inches(2.5), WHITE)
    add_floret(s6, Inches(10.0), Inches(4.2), Inches(3.0), DARK_TEAL)

    tb_s6 = s6.shapes.add_textbox(Inches(2.5), Inches(2.8), Inches(8.333), Inches(1.8))
    tf_s6 = tb_s6.text_frame
    p_s6 = tf_s6.paragraphs[0]
    p_s6.text = "02. LITERATURE REVIEW"
    p_s6.font.name = FONT_TITLE
    p_s6.font.size = Pt(46)
    p_s6.font.bold = True
    p_s6.font.color.rgb = WHITE
    p_s6.alignment = PP_ALIGN.CENTER

    p_s6_sub = tf_s6.add_paragraph()
    p_s6_sub.text = "Classical Heuristics, Mathematical Bounds & Identified Gaps"
    p_s6_sub.font.name = FONT_BODY
    p_s6_sub.font.size = Pt(16)
    p_s6_sub.font.color.rgb = CREAM_BG
    p_s6_sub.alignment = PP_ALIGN.CENTER
    p_s6_sub.space_before = Pt(10)

    # =========================================================================
    # SLIDE 7: Literature Review & Gap Analysis
    # =========================================================================
    s7 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s7, CREAM_BG)
    add_header(s7, "State of the Art", "Algorithmic Survey & Literature Review")

    add_card(s7, Inches(0.8), Inches(1.8), Inches(3.6), Inches(3.2),
             "1. Clarke-Wright Savings",
             "Pioneered greedy tour merging based on distance savings: s(i,j) = c(d,i) + c(d,j) - c(i,j).\n\nLimitation: Ignores heterogeneous parcel profitability and hard delivery cutoffs.",
             WHITE, border_color=DARK_TEAL, star_color=DARK_TEAL)

    add_card(s7, Inches(4.8), Inches(1.8), Inches(3.6), Inches(3.2),
             "2. Dijkstra Shortest Paths",
             "Non-negative edge relaxation with Binary Min-Heap Priority Queue runs in O((V + E) log V).\n\nLimitation: Solves single point-to-point shortest paths; does not select optimal parcel combinations.",
             WHITE, border_color=LIME_GREEN, star_color=LIME_GREEN)

    add_card(s7, Inches(8.8), Inches(1.8), Inches(3.6), Inches(3.2),
             "3. 0/1 Knapsack DP",
             "Bellman recurrence constructs 2D memoization table in pseudo-polynomial O(n · C) time.\n\nLimitation: Classical knapsack assumes static capacity, ignoring transit time and spatial stop sequences.",
             WHITE, border_color=ORANGE, star_color=ORANGE)

    # Highlight box for the gap
    box_gap = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.3), Inches(11.6), Inches(1.5))
    box_gap.fill.solid()
    box_gap.fill.fore_color.rgb = PASTEL_ORANGE_BG
    box_gap.line.color.rgb = ORANGE
    tf_gap = box_gap.text_frame
    tf_gap.word_wrap = True
    p_g1 = tf_gap.paragraphs[0]
    p_g1.text = "🎯 IDENTIFIED RESEARCH GAP ADDRESSED BY SMARTROUTE"
    p_g1.font.name = FONT_BODY
    p_g1.font.size = Pt(11)
    p_g1.font.bold = True
    p_g1.font.color.rgb = ORANGE
    p_g2 = tf_gap.add_paragraph()
    p_g2.text = "Existing models isolate parcel selection from spatial vehicle routing. SmartRoute integrates them into a Two-Tier Decoupled Pipeline with proactive feasibility repair: optimal parcel selection via 0/1 DP, routed along Dijkstra graph paths, with automated trimming of bottleneck stops."
    p_g2.font.name = FONT_BODY
    p_g2.font.size = Pt(11.5)
    p_g2.font.color.rgb = DARK_TEAL
    p_g2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 8: Solution - Two-Tier Decoupled Architecture (Timeline Road Motif)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s8, CREAM_BG)
    add_header(s8, "Proposed Solution", "Two-Tier Decoupled Architecture")

    # Dark Asphalt Highway Road Motif (Template Slide 8 Style)
    road = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.5), Inches(11.7), Inches(0.9))
    road.fill.solid()
    road.fill.fore_color.rgb = DARK_TEAL
    road.line.fill.background()

    # Dashed divider line
    for i in range(12):
        dash = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2 + i * 0.95), Inches(3.9), Inches(0.5), Inches(0.08))
        dash.fill.solid()
        dash.fill.fore_color.rgb = LIME_GREEN
        dash.line.fill.background()

    # 4 Milestone Cards above and below the road
    # Step 1: Request Pool
    add_card(s8, Inches(0.8), Inches(1.6), Inches(2.6), Inches(1.6),
             "1. Pool Ingestion",
             "35 candidate orders across Hyderabad filtered for vehicle payload limit.",
             WHITE, border_color=ORANGE)
    add_starburst(s8, Inches(1.9), Inches(3.2), Inches(0.4), ORANGE)

    # Step 2: Knapsack DP
    add_card(s8, Inches(3.8), Inches(4.7), Inches(2.6), Inches(1.8),
             "2. Tier 1: 0/1 DP",
             "Bellman memoization table optimizes subset profit within payload capacity (O(n · C)).",
             WHITE, border_color=LIME_GREEN)
    add_starburst(s8, Inches(4.9), Inches(4.1), Inches(0.4), LIME_GREEN)

    # Step 3: Dijkstra Routing
    add_card(s8, Inches(6.8), Inches(1.6), Inches(2.6), Inches(1.6),
             "3. Tier 2: Dijkstra",
             "Binary Min-Heap computes turn-by-turn road paths (O((V+E) log V)).",
             WHITE, border_color=ORANGE)
    add_starburst(s8, Inches(7.9), Inches(3.2), Inches(0.4), ORANGE)

    # Step 4: Feasibility Repair
    add_card(s8, Inches(9.8), Inches(4.7), Inches(2.6), Inches(1.8),
             "4. Feasible Dispatch",
             "Verifies SLA deadlines; systematically defers bottlenecks for 100% on-time delivery.",
             WHITE, border_color=DARK_TEAL)
    add_starburst(s8, Inches(10.9), Inches(4.1), Inches(0.4), DARK_TEAL)

    # =========================================================================
    # SLIDE 9: Methodology Part A - Graph & Dijkstra Min-Heap
    # =========================================================================
    s9 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s9, CREAM_BG)
    add_header(s9, "Methodology: Graph Network", "Urban Graph & Dijkstra Min-Heap Engine")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "📍 Hyderabad Logistics Road Network",
             "• Representation: Undirected weighted graph G = (V, E) stored as an Adjacency List (Map<string, Edge[]>).\n\n"
             "• Vertices (|V| = 22): Central Depot at Main Parcel Warehouse (Begumpet), Ameerpet, Secunderabad, Hitec City, Gachibowli, Kukatpally, Miyapur, Patancheru, Sangareddy, and Woxsen University.\n\n"
             "• Edges (|E| = 34): Real metropolitan arterial roads and NH65 corridor with true distance weights.\n\n"
             "• Spatial Efficiency: Consumes O(V + E) memory rather than O(V²) dense matrices.",
             WHITE, border_color=DARK_TEAL, star_color=DARK_TEAL)

    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "⚡ Binary Min-Heap Priority Queue",
             "• Core Complexity: O((|V| + |E|) · log |V|).\n\n"
             "• Motivation: Unsorted array scanning takes O(V²) because finding the minimum unvisited node requires O(V) scans. The Binary Min-Heap extracts min in O(1) and reheapifies in O(log V).\n\n"
             "• Edge Relaxation Condition:\n"
             "  if dist[u] + weight(u, v) < dist[v]:\n"
             "      dist[v] = dist[u] + weight(u, v)\n"
             "      parent[v] = u\n"
             "      minHeap.push((dist[v], v))\n\n"
             "• Sub-millisecond Execution: Reconstructs exact turn-by-turn paths in < 0.2 ms.",
             WHITE, border_color=ORANGE, star_color=ORANGE)

    # =========================================================================
    # SLIDE 10: Methodology Part B - 0/1 Knapsack Dynamic Programming
    # =========================================================================
    s10 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s10, CREAM_BG)
    add_header(s10, "Methodology: Optimization", "0/1 Knapsack Dynamic Programming Formulation")

    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "📐 Bellman Recurrence Formulation",
             "Let DP[i][c] be maximum profit with first i packages and capacity c:\n\n"
             "  DP[i][c] = max(\n"
             "      DP[i-1][c],                  // Choice 0: SKIP\n"
             "      DP[i-1][c - w_i] + p_i        // Choice 1: TAKE\n"
             "  )\n\n"
             "• Optimal Substructure: Global optimal schedule consists of optimal sub-solutions.\n\n"
             "• Overlapping Subproblems: Stored in a 2D memoization table across all capacity increments.\n\n"
             "• Time Complexity: O(n · C) pseudo-polynomial runtime.",
             WHITE, border_color=LIME_GREEN, star_color=LIME_GREEN)

    add_card(s10, Inches(6.8), Inches(1.8), Inches(5.6), Inches(4.8),
             "🔍 Backtracking Trail & Greedy Flaws",
             "• Backtracking Extraction:\n"
             "  Starting at DP[n][C], if DP[i][w] != DP[i-1][w], parcel i is added to the manifest and capacity w -= weight[i].\n\n"
             "• Why Greedy Heuristic Fails:\n"
             "  Greedy sorting by density (p/w) is mathematically optimal only for continuous (fractional) items.\n\n"
             "• Discrete Package Reality:\n"
             "  Greedy accepts low-weight packages first and leaves awkward capacity gaps, missing high-value shipments.",
             WHITE, border_color=ORANGE, star_color=ORANGE)

    # =========================================================================
    # SLIDE 11: Methodology Part C - Route Scheduling & Invariant Repair
    # =========================================================================
    s11 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s11, CREAM_BG)
    add_header(s11, "Methodology: Scheduling", "Route Invariants & SLA Feasibility Repair")

    add_card(s11, Inches(0.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "1. Precedence Invariant",
             "• Invariant: Pickup(i) ≺ Drop(i).\n\n"
             "• State Tracking: Scheduler tracks 'pickedUp' and 'delivered' sets.\n\n"
             "• Action Gating: Drop stop is mathematically forbidden from candidate queue until physical pickup has occurred.",
             WHITE, border_color=ORANGE, star_color=ORANGE)

    add_card(s11, Inches(4.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "2. Payload Safety",
             "• Invariant: 0 ≤ Load(s) ≤ C at every single route leg.\n\n"
             "• Dynamic Tracking: Starts at 0 kg at Depot. At pickup: load += w. At drop: load -= w.\n\n"
             "• Telematics Safety: Overweight stops are pruned before dispatch.",
             WHITE, border_color=LIME_GREEN, star_color=LIME_GREEN)

    add_card(s11, Inches(8.8), Inches(1.8), Inches(3.6), Inches(4.8),
             "3. SLA Feasibility Repair",
             "• Invariant: Arrival(i) ≤ Deadline(i).\n\n"
             "• Bottleneck Pruning: If a delivery arrives late, scheduler identifies the lowest-margin offender.\n\n"
             "• Guaranteed Punctuality: Recalibrates route until 100% on-time delivery is achieved.",
             WHITE, border_color=DARK_TEAL, star_color=DARK_TEAL)

    # =========================================================================
    # SLIDE 12: Section 03 Divider - PROTOTYPE & RESULTS
    # =========================================================================
    s12 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s12, DARK_TEAL)

    add_starburst(s12, Inches(1.5), Inches(1.2), Inches(2.5), LIME_GREEN)
    add_floret(s12, Inches(10.2), Inches(4.0), Inches(2.8), ORANGE)

    tb_s12 = s12.shapes.add_textbox(Inches(2.5), Inches(2.8), Inches(8.333), Inches(1.8))
    tf_s12 = tb_s12.text_frame
    p_s12 = tf_s12.paragraphs[0]
    p_s12.text = "03. PROTOTYPE & RESULTS"
    p_s12.font.name = FONT_TITLE
    p_s12.font.size = Pt(46)
    p_s12.font.bold = True
    p_s12.font.color.rgb = WHITE
    p_s12.alignment = PP_ALIGN.CENTER

    p_s12_sub = tf_s12.add_paragraph()
    p_s12_sub.text = "Live Operations Platform, Algorithm Labs & Empirical Benchmarks"
    p_s12_sub.font.name = FONT_BODY
    p_s12_sub.font.size = Pt(16)
    p_s12_sub.font.color.rgb = CREAM_BG
    p_s12_sub.alignment = PP_ALIGN.CENTER
    p_s12_sub.space_before = Pt(10)

    # =========================================================================
    # SLIDE 13: Prototype Walkthrough - Operations Dashboard (Screenshot)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s13, CREAM_BG)
    add_header(s13, "Live Demonstration", "Interactive Operations Dashboard & Google Maps")

    # Image on Left
    img_ops = os.path.join(assets_dir, "operations_overview.png")
    if os.path.exists(img_ops):
        s13.shapes.add_picture(img_ops, Inches(0.8), Inches(1.8), Inches(6.8), Inches(4.8))

    # Notes Card on Right
    add_card(s13, Inches(7.8), Inches(1.8), Inches(4.7), Inches(4.8),
             "🚀 Key Operational Capabilities",
             "• Authentic Google Maps Layer:\n  Renders live Roadmap & Satellite tiles with pan/zoom and Google logo.\n\n"
             "• NH65 Corridor Routing:\n  Calculates complete route across Hyderabad to Woxsen University (Kamkole).\n\n"
             "• Real-Time Telematics:\n  Tracks live vehicle load progression (0kg → 4kg → 12kg → 44kg).\n\n"
             "• Financial Performance:\n  ₹10,190 realized profit across 12 scheduled orders with zero SLA late penalties.",
             WHITE, border_color=ORANGE, star_color=ORANGE)

    # =========================================================================
    # SLIDE 14: Prototype Walkthrough - Lab 2 Dijkstra (Screenshot)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s14, CREAM_BG)
    add_header(s14, "Algorithm Lab Trace", "Lab 2: Dijkstra & Min-Heap Step Tracer")

    img_dijk = os.path.join(assets_dir, "lab2_dijkstra.png")
    if os.path.exists(img_dijk):
        s14.shapes.add_picture(img_dijk, Inches(0.8), Inches(1.8), Inches(6.8), Inches(4.8))

    add_card(s14, Inches(7.8), Inches(1.8), Inches(4.7), Inches(4.8),
             "🔍 Step-by-Step Pedagogical Visualizer",
             "• Arbitrary Hub Selection:\n  Select any source hub (Main Parcel Warehouse) and destination (Woxsen University).\n\n"
             "• Execution Playhead (Step 1 of 49):\n  Step forward, backward, or auto-play through edge relaxations.\n\n"
             "• Live Min-Heap Inspection:\n  Visualizes root extractions in O(1) and heap sift-ups in O(log V).\n\n"
             "• Shortest Path Reconstruction:\n  Begumpet → Ameerpet → Kukatpally → Miyapur → Patancheru → Sangareddy → Woxsen (70 km, 131 mins).",
             WHITE, border_color=LIME_GREEN, star_color=LIME_GREEN)

    # =========================================================================
    # SLIDE 15: Prototype Walkthrough - Lab 4 Knapsack DP (Screenshot)
    # =========================================================================
    s15 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s15, CREAM_BG)
    add_header(s15, "Algorithm Lab Trace", "Lab 4: 0/1 Knapsack 2D DP Memoization Matrix")

    img_knap = os.path.join(assets_dir, "lab4_knapsack.png")
    if os.path.exists(img_knap):
        s15.shapes.add_picture(img_knap, Inches(0.8), Inches(1.8), Inches(6.8), Inches(4.8))

    add_card(s15, Inches(7.8), Inches(1.8), Inches(4.7), Inches(4.8),
             "📊 Dynamic Programming Transparency",
             "• Complete 2D Table (35 × 75):\n  Rows represent parcel requests; columns represent incremental capacity from 0 to 75 kg.\n\n"
             "• Interactive Cell Arithmetic:\n  Clicking any cell reveals the exact Bellman decision: SKIP vs TAKE.\n\n"
             "• Golden Backtracking Trail:\n  Vibrant green highlight traces which exact packages compose the global optimum.\n\n"
             "• Theoretical Optimum:\n  ₹18,290 maximum achievable profit before spatial deadlines are applied.",
             WHITE, border_color=ORANGE, star_color=ORANGE)

    # =========================================================================
    # SLIDE 16: Key Performance Statistics (Template Slide 14 Style)
    # =========================================================================
    s16 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s16, CREAM_BG)
    add_header(s16, "Empirical Validation", "Key Performance Telematics & Delivery Metrics")
    add_curved_road_motif(s16, LIME_GREEN, "bottom")

    # Three large Starburst Metrics (Template Slide 14 style)
    # Metric 1: 100% Punctuality
    add_starburst(s16, Inches(1.2), Inches(2.2), Inches(3.4), ORANGE)
    tb_m1 = s16.shapes.add_textbox(Inches(1.5), Inches(2.8), Inches(2.8), Inches(1.8))
    tf_m1 = tb_m1.text_frame
    p_m1_val = tf_m1.paragraphs[0]
    p_m1_val.text = "100%"
    p_m1_val.font.name = FONT_TITLE
    p_m1_val.font.size = Pt(38)
    p_m1_val.font.bold = True
    p_m1_val.font.color.rgb = WHITE
    p_m1_val.alignment = PP_ALIGN.CENTER
    p_m1_lbl = tf_m1.add_paragraph()
    p_m1_lbl.text = "On-Time Fulfillment\nZero SLA Breaches"
    p_m1_lbl.font.name = FONT_BODY
    p_m1_lbl.font.size = Pt(12)
    p_m1_lbl.font.color.rgb = WHITE
    p_m1_lbl.alignment = PP_ALIGN.CENTER

    # Metric 2: ₹10,190 Profit
    add_starburst(s16, Inches(5.0), Inches(2.2), Inches(3.4), LIME_GREEN)
    tb_m2 = s16.shapes.add_textbox(Inches(5.3), Inches(2.8), Inches(2.8), Inches(1.8))
    tf_m2 = tb_m2.text_frame
    p_m2_val = tf_m2.paragraphs[0]
    p_m2_val.text = "₹10,190"
    p_m2_val.font.name = FONT_TITLE
    p_m2_val.font.size = Pt(32)
    p_m2_val.font.bold = True
    p_m2_val.font.color.rgb = WHITE
    p_m2_val.alignment = PP_ALIGN.CENTER
    p_m2_lbl = tf_m2.add_paragraph()
    p_m2_lbl.text = "Net Dispatched Profit\n+25.5% Over Greedy"
    p_m2_lbl.font.name = FONT_BODY
    p_m2_lbl.font.size = Pt(12)
    p_m2_lbl.font.color.rgb = WHITE
    p_m2_lbl.alignment = PP_ALIGN.CENTER

    # Metric 3: 230 km Route
    add_starburst(s16, Inches(8.9), Inches(2.2), Inches(3.4), DARK_TEAL)
    tb_m3 = s16.shapes.add_textbox(Inches(9.2), Inches(2.8), Inches(2.8), Inches(1.8))
    tf_m3 = tb_m3.text_frame
    p_m3_val = tf_m3.paragraphs[0]
    p_m3_val.text = "230 km"
    p_m3_val.font.name = FONT_TITLE
    p_m3_val.font.size = Pt(34)
    p_m3_val.font.bold = True
    p_m3_val.font.color.rgb = WHITE
    p_m3_val.alignment = PP_ALIGN.CENTER
    p_m3_lbl = tf_m3.add_paragraph()
    p_m3_lbl.text = "Total Route Distance\nOptimal Road Sequence"
    p_m3_lbl.font.name = FONT_BODY
    p_m3_lbl.font.size = Pt(12)
    p_m3_lbl.font.color.rgb = WHITE
    p_m3_lbl.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 17: Empirical Benchmark Table (Greedy vs DP)
    # =========================================================================
    s17 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s17, CREAM_BG)
    add_header(s17, "Comparative Evaluation", "Benchmark Matrix: Greedy vs. 0/1 Knapsack Pipeline")

    # Table Shape
    rows = 6
    cols = 4
    left = Inches(0.8)
    top = Inches(1.8)
    width = Inches(11.7)
    height = Inches(4.8)

    table_shape = s17.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(2.8)
    table.columns[2].width = Inches(2.8)
    table.columns[3].width = Inches(2.9)

    headers = ["Dimension", "Greedy Density (p/w)", "Greedy Deadline (EDF)", "SmartRoute DP Pipeline"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_TEAL
        for p in cell.text_frame.paragraphs:
            p.font.name = FONT_BODY
            p.font.bold = True
            p.font.size = Pt(12)
            p.font.color.rgb = WHITE

    data = [
        ["Theoretical Packing Profit", "₹18,960", "₹14,200", "₹18,290 (Globally Optimal)"],
        ["Dispatched Feasible Profit", "₹8,120 (4 SLA breaches)", "₹7,540", "₹10,190 (+25.5% Revenue)"],
        ["Vehicle Payload Utilization", "74.5 / 75 kg (99.3%)", "38.0 / 75 kg (50.6%)", "44.0 / 75 kg (58.7% Feasible)"],
        ["Orders Dispatched", "20 accepted (unverified)", "9 orders", "12 orders dispatched"],
        ["Deadline Verification", "FAILED (4 Late Deliveries)", "100% Punctual", "100% Punctual (Zero Late)"]
    ]

    for r_idx, row in enumerate(data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else PASTEL_ORANGE_BG
            for p in cell.text_frame.paragraphs:
                p.font.name = FONT_BODY
                p.font.size = Pt(11)
                p.font.color.rgb = SLATE_DARK
                if c_idx == 3:
                    p.font.bold = True
                    p.font.color.rgb = ORANGE

    # =========================================================================
    # SLIDE 18: Faculty Viva Voce Defense Guide
    # =========================================================================
    s18 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s18, CREAM_BG)
    add_header(s18, "Faculty Viva Voce", "Academic Defense: Core Algorithmic Q&A")

    add_card(s18, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.4),
             "Q1: Why not pure DP for full VRP?",
             "Answer: Exact multi-stop VRP with Time Windows requires tracking the visited subset in DP state (Held-Karp). This incurs O(n² · 2ⁿ) exponential states. For 35 orders, 2³⁵ ≈ 34 billion states! Decoupling into Knapsack DP + Dijkstra heuristic executes in 12 ms.",
             WHITE, border_color=ORANGE)

    add_card(s18, Inches(6.8), Inches(1.8), Inches(5.6), Inches(2.4),
             "Q2: Why use a Binary Min-Heap?",
             "Answer: Without a Min-Heap, finding the next unvisited vertex requires an O(V) linear scan, giving O(V²) total runtime. A Binary Min-Heap provides O(1) root lookup and O(log V) sift operations, reducing complexity to O((V+E) log V).",
             WHITE, border_color=ORANGE)

    add_card(s18, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.4),
             "Q3: When does Greedy match DP?",
             "Answer: Greedy is optimal for Fractional Knapsack (divisible items). In discrete 0/1 Knapsack, Greedy is optimal only when item weights divide capacity evenly with identical profit densities. Otherwise, Greedy leaves capacity fragments.",
             WHITE, border_color=LIME_GREEN)

    add_card(s18, Inches(6.8), Inches(4.5), Inches(5.6), Inches(2.4),
             "Q4: How enforce Pickup-Before-Drop?",
             "Answer: The scheduler maintains 'pickedUp' and 'delivered' hash sets. A DROP action is strictly locked until its package ID exists in 'pickedUp'. Furthermore, vehicle load invariants (0 ≤ load ≤ C) are verified at every stop.",
             WHITE, border_color=LIME_GREEN)

    # =========================================================================
    # SLIDE 19: Team Members & Faculty Acknowledgements (Template Slide 10 Style)
    # =========================================================================
    s19 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s19, CREAM_BG)
    add_header(s19, "Project Team", "Course Instructor & Student Developers")

    # Wavy Orange Ribbon across bottom (Template Slide 10 style)
    ribbon_team = s19.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(5.2), Inches(13.333), Inches(2.3))
    ribbon_team.fill.solid()
    ribbon_team.fill.fore_color.rgb = ORANGE
    ribbon_team.line.fill.background()

    # 4 Team Members cards with Starburst Badges
    members = [
        ("Himanshu Pandit", "Algorithmic Core & Architecture", LIME_GREEN),
        ("Devyani Pawar", "Graph & Dijkstra Min-Heap", DARK_TEAL),
        ("Heman", "0/1 Knapsack DP Optimization", LIME_GREEN),
        ("Rimika Jain", "Empirical Benchmarks & Telematics", DARK_TEAL)
    ]

    for idx, (name, role, star_col) in enumerate(members):
        col_left = Inches(0.8 + idx * 2.95)
        # Photo card
        card_m = s19.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, col_left, Inches(2.0), Inches(2.7), Inches(3.2))
        card_m.fill.solid()
        card_m.fill.fore_color.rgb = WHITE
        card_m.line.color.rgb = LIME_GREEN
        card_m.line.width = Pt(2)

        # Starburst accent on top right
        add_starburst(s19, col_left + Inches(2.1), Inches(1.8), Inches(0.55), star_col)

        # Avatar representation
        avatar = s19.shapes.add_shape(MSO_SHAPE.OVAL, col_left + Inches(0.65), Inches(2.3), Inches(1.4), Inches(1.4))
        avatar.fill.solid()
        avatar.fill.fore_color.rgb = PASTEL_PEACH
        avatar.line.fill.background()

        # Name & Role inside card
        tb_m = s19.shapes.add_textbox(col_left + Inches(0.1), Inches(3.9), Inches(2.5), Inches(1.2))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        p_nm = tf_m.paragraphs[0]
        p_nm.text = name
        p_nm.font.name = FONT_TITLE
        p_nm.font.size = Pt(14)
        p_nm.font.bold = True
        p_nm.font.color.rgb = DARK_TEAL
        p_nm.alignment = PP_ALIGN.CENTER

        p_rl = tf_m.add_paragraph()
        p_rl.text = role
        p_rl.font.name = FONT_BODY
        p_rl.font.size = Pt(10)
        p_rl.font.color.rgb = SLATE_MUTED
        p_rl.alignment = PP_ALIGN.CENTER
        p_rl.space_before = Pt(4)

    # Faculty Banner on Orange Ribbon
    tb_fac = s19.shapes.add_textbox(Inches(1.0), Inches(5.5), Inches(11.333), Inches(1.4))
    tf_fac = tb_fac.text_frame
    tf_fac.word_wrap = True
    p_f1 = tf_fac.paragraphs[0]
    p_f1.text = "GUIDED BY: DR. SYED JAVED PASHA"
    p_f1.font.name = FONT_TITLE
    p_f1.font.size = Pt(18)
    p_f1.font.bold = True
    p_f1.font.color.rgb = WHITE
    p_f1.alignment = PP_ALIGN.CENTER

    p_f2 = tf_fac.add_paragraph()
    p_f2.text = "Department of Computer Science & Engineering • Design & Analysis of Algorithms"
    p_f2.font.name = FONT_BODY
    p_f2.font.size = Pt(12)
    p_f2.font.color.rgb = CREAM_BG
    p_f2.alignment = PP_ALIGN.CENTER
    p_f2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 20: Conclusion & Future Scope (Template Slide 21 Style)
    # =========================================================================
    s20 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s20, CREAM_BG)

    # Central Cross / Floret in Lime Green (Template Slide 21 style)
    add_floret(s20, Inches(4.9), Inches(1.5), Inches(3.5), LIME_GREEN)

    tb_s20 = s20.shapes.add_textbox(Inches(3.0), Inches(2.2), Inches(7.333), Inches(2.2))
    tf_s20 = tb_s20.text_frame
    tf_s20.word_wrap = True
    p_end = tf_s20.paragraphs[0]
    p_end.text = "THANK YOU!"
    p_end.font.name = FONT_TITLE
    p_end.font.size = Pt(44)
    p_end.font.bold = True
    p_end.font.color.rgb = DARK_TEAL
    p_end.alignment = PP_ALIGN.CENTER

    p_end_sub = tf_s20.add_paragraph()
    p_end_sub.text = "SmartRoute: Last-Mile Delivery Operations Engine"
    p_end_sub.font.name = FONT_BODY
    p_end_sub.font.size = Pt(15)
    p_end_sub.font.color.rgb = WHITE
    p_end_sub.alignment = PP_ALIGN.CENTER
    p_end_sub.space_before = Pt(6)

    # 2 Summary Cards at bottom
    add_card(s20, Inches(0.8), Inches(4.5), Inches(5.6), Inches(2.2),
             "🏆 Summary of Achievements",
             "• Mathematical optimality on payload packing (0/1 DP).\n"
             "• 100% on-time delivery across 22 Hyderabad hubs.\n"
             "• Full corridor coverage including Woxsen University on NH65.\n"
             "• Complete viva transparency via Algorithm Lab.",
             WHITE, border_color=ORANGE)

    add_card(s20, Inches(6.8), Inches(4.5), Inches(5.6), Inches(2.2),
             "🔭 Future Research Horizons",
             "• Multi-Vehicle Fleet Partitioning (Genetic K-Means).\n"
             "• Dynamic Time-Dependent Traffic Edge Weights.\n"
             "• EV Battery State-of-Charge & Charging Insertions.\n"
             "• Real-Time Dispatching with stochastic cancellations.",
             WHITE, border_color=DARK_TEAL)

    # Save presentation
    output_path = "/Users/himanshu/Documents/Daa PBL/SmartRoute_Presentation.pptx"
    prs.save(output_path)
    print(f"Successfully generated PowerPoint presentation at {output_path}")

if __name__ == "__main__":
    main()
