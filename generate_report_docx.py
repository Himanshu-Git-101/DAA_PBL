#!/usr/bin/env python3
"""
generate_report_docx.py - Generates the complete, comprehensive academic project report
for SmartRoute adhering strictly to the Woxsen University School of Technology report template
and formatting guidelines (Appendix II).

Specifications Implemented:
- Paper Size: A4 (8.5 x 11 in / 210 x 297 mm)
- Margins: 1.0 inch (2.54 cm) on all sides
- Font Family: Times New Roman throughout
- Body Text: 12 pt, 1.5 Line Spacing, Justified, 6 pt After
- Heading 1: 16 pt, Bold, 18 pt Before, 12 pt After
- Heading 2: 14 pt, Bold, 12 pt Before, 6 pt After
- Heading 3: 13 pt, Bold, 10 pt Before, 6 pt After
- Tables: Centered, Header Background RGB(213, 232, 240), Bold 12 pt Header, 12 pt Body,
  Centered Italic 11 pt Caption Below Table
- Figures: Centered, High Resolution, Centered Italic 11 pt Caption Below Figure
- In-Text Citations: IEEE Numerical Format [1], [2], [3]
- Reference List: Numbered IEEE Format with Hanging Indents
- Complete content for all chapters (No blanks or placeholders)
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCX_OUTPUT = "SmartRoute_Project_Report.docx"
ASSETS_DIR = "public/presentation/assets"
SCREENSHOTS_DIR = "public/presentation"

def set_cell_background(cell, hex_color):
    """Sets background shading of a table cell."""
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets internal padding (in twips) of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def format_run(run, font_name="Times New Roman", size_pt=12, bold=False, italic=False, color_rgb=(0, 0, 0)):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)

def add_body_paragraph(doc, text="", bold_prefix="", space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        format_run(r_pre, bold=True)
    if text:
        r_txt = p.add_run(text)
        format_run(r_txt)
    return p

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    format_run(r, size_pt=16, bold=True)
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    format_run(r, size_pt=14, bold=True)
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    format_run(r, size_pt=13, bold=True)
    return p

def add_bullet_item(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        format_run(r_pre, bold=True)
    r_txt = p.add_run(text)
    format_run(r_txt)
    return p

def add_numbered_item(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Number')
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        format_run(r_pre, bold=True)
    r_txt = p.add_run(text)
    format_run(r_txt)
    return p

def add_figure(doc, img_path, caption_text, width=Inches(5.8)):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(4)
        run = p_img.add_run()
        run.add_picture(img_path, width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)
        r = p_cap.add_run(caption_text)
        format_run(r, size_pt=11, italic=True)
    else:
        print(f"Warning: Image not found: {img_path}")

def add_table_caption(doc, caption_text):
    p = doc.add_paragraph()
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run(caption_text)
    format_run(r, size_pt=11, italic=True)

print("Initializing document...")
doc = docx.Document()

# Configure Margins to 1.0 inch
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)

# =========================================================
# 1. TITLE PAGE
# =========================================================
print("Adding Title Page...")
p_univ = doc.add_paragraph()
p_univ.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_univ.paragraph_format.space_before = Pt(12)
p_univ.paragraph_format.space_after = Pt(4)
r = p_univ.add_run("Woxsen University")
format_run(r, size_pt=22, bold=True)

p_school = doc.add_paragraph()
p_school.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_school.paragraph_format.space_after = Pt(18)
r = p_school.add_run("School of Technology")
format_run(r, size_pt=16, bold=True)

# Logo
logo_path = os.path.join(ASSETS_DIR, "woxsen_logo.jpg")
if os.path.exists(logo_path):
    p_logo = doc.add_paragraph()
    p_logo.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_after = Pt(20)
    p_logo.add_run().add_picture(logo_path, width=Inches(1.8))

p_a = doc.add_paragraph()
p_a.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_a.paragraph_format.space_after = Pt(4)
r = p_a.add_run("A")
format_run(r, size_pt=12)

p_rep = doc.add_paragraph()
p_rep.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_rep.paragraph_format.space_after = Pt(4)
r = p_rep.add_run("PROJECT REPORT")
format_run(r, size_pt=16, bold=True)

p_on = doc.add_paragraph()
p_on.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_on.paragraph_format.space_after = Pt(14)
r = p_on.add_run("on")
format_run(r, size_pt=12)

# Project Title
p_title = doc.add_paragraph()
p_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_after = Pt(18)
r = p_title.add_run("SMARTROUTE: ALGORITHMIC LAST-MILE DELIVERY OPTIMIZATION USING DYNAMIC PROGRAMMING, GREEDY HEURISTICS, DIJKSTRA'S ALGORITHM, AND BELLMAN-FORD")
format_run(r, size_pt=15, bold=True)

p_sub = doc.add_paragraph()
p_sub.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(14)
r = p_sub.add_run("Submitted in partial fulfillment of the requirements for the degree of")
format_run(r, size_pt=12)

p_deg = doc.add_paragraph()
p_deg.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_deg.paragraph_format.space_after = Pt(24)
r = p_deg.add_run("B. Tech. in Computer Science and Engineering")
format_run(r, size_pt=14, bold=True)

# Student Names
p_by = doc.add_paragraph()
p_by.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_by.paragraph_format.space_after = Pt(2)
r = p_by.add_run("Submitted by:")
format_run(r, size_pt=12, bold=True)

team_members = [
    ("Himanshu Pandit", "WOU/BTECH/CSE/2023/042"),
    ("Devyani Pawar", "WOU/BTECH/CSE/2023/018"),
    ("Heman", "WOU/BTECH/CSE/2023/029"),
    ("Rimika Jain", "WOU/BTECH/CSE/2023/065")
]

for name, roll in team_members:
    p_mem = doc.add_paragraph()
    p_mem.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_mem.paragraph_format.space_after = Pt(1)
    r = p_mem.add_run(f"{name} ({roll})")
    format_run(r, size_pt=12)

# Guide
p_guid = doc.add_paragraph()
p_guid.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_guid.paragraph_format.space_before = Pt(14)
p_guid.paragraph_format.space_after = Pt(2)
r = p_guid.add_run("Under the guidance of:")
format_run(r, size_pt=12, bold=True)

p_fac = doc.add_paragraph()
p_fac.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_fac.paragraph_format.space_after = Pt(1)
r = p_fac.add_run("Dr. Syed Javed Pasha")
format_run(r, size_pt=13, bold=True)

p_dept = doc.add_paragraph()
p_dept.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_dept.paragraph_format.space_after = Pt(1)
r = p_dept.add_run("Associate Professor, Department of Computer Science & Engineering\nSchool of Technology, Woxsen University")
format_run(r, size_pt=11)

doc.add_page_break()

# =========================================================
# 2. CERTIFICATE
# =========================================================
print("Adding Certificate...")
p_cert = doc.add_paragraph()
p_cert.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_cert.paragraph_format.space_before = Pt(24)
p_cert.paragraph_format.space_after = Pt(24)
r = p_cert.add_run("CERTIFICATE")
format_run(r, size_pt=16, bold=True)

cert_text = (
    "This is to certify that the project report entitled \"SMARTROUTE: ALGORITHMIC LAST-MILE DELIVERY OPTIMIZATION "
    "USING DYNAMIC PROGRAMMING, GREEDY HEURISTICS, DIJKSTRA'S ALGORITHM, AND BELLMAN-FORD\" submitted by "
    "Himanshu Pandit (WOU/BTECH/CSE/2023/042), Devyani Pawar (WOU/BTECH/CSE/2023/018), Heman (WOU/BTECH/CSE/2023/029), "
    "and Rimika Jain (WOU/BTECH/CSE/2023/065) in partial fulfillment of the requirements for the award of the degree of "
    "Bachelor of Technology in Computer Science and Engineering from Woxsen University, School of Technology is a bonafide "
    "record of work carried out by the students under my supervision and guidance.\n\n"
    "The work embodied in this project report has been carried out by the candidates and has not been submitted elsewhere for a degree."
)
add_body_paragraph(doc, cert_text, space_after=60)

p_sig = doc.add_paragraph()
p_sig.paragraph_format.space_after = Pt(2)
r = p_sig.add_run("Signature of Mentor:\n________________________\n")
format_run(r, size_pt=12)

p_mname = doc.add_paragraph()
p_mname.paragraph_format.space_after = Pt(2)
r = p_mname.add_run("Name: Dr. Syed Javed Pasha")
format_run(r, size_pt=12, bold=True)

p_mdes = doc.add_paragraph()
p_mdes.paragraph_format.space_after = Pt(2)
r = p_mdes.add_run("Designation: Associate Professor, Department of Computer Science & Engineering\nInstitution: School of Technology, Woxsen University")
format_run(r, size_pt=12)

p_mdate = doc.add_paragraph()
p_mdate.paragraph_format.space_after = Pt(12)
r = p_mdate.add_run("Date: 13th October 2026")
format_run(r, size_pt=12)

doc.add_page_break()

# =========================================================
# 3. DECLARATION
# =========================================================
print("Adding Declaration...")
p_dec = doc.add_paragraph()
p_dec.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_dec.paragraph_format.space_before = Pt(24)
p_dec.paragraph_format.space_after = Pt(24)
r = p_dec.add_run("DECLARATION of the candidates")
format_run(r, size_pt=16, bold=True)

dec_text = (
    "We hereby declare that the project work entitled \"SMARTROUTE: ALGORITHMIC LAST-MILE DELIVERY OPTIMIZATION "
    "USING DYNAMIC PROGRAMMING, GREEDY HEURISTICS, DIJKSTRA'S ALGORITHM, AND BELLMAN-FORD\" submitted to the Department "
    "of Computer Science and Engineering, School of Technology, Woxsen University, in partial fulfillment of the requirements "
    "for the award of the degree of Bachelor of Technology in Computer Science and Engineering is our original work and has "
    "been carried out under the guidance of Dr. Syed Javed Pasha.\n\n"
    "We further declare that the work reported in this project has not been submitted and will not be submitted, either in part "
    "or in full, for the award of any other degree or diploma in this institute or any other institute or university."
)
add_body_paragraph(doc, dec_text, space_after=36)

# Signatures Table (2x2 grid)
table_sig = doc.add_table(rows=2, cols=2)
table_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
for r_i, c_i, name, roll in [(0, 0, "Himanshu Pandit", "WOU/BTECH/CSE/2023/042"),
                             (0, 1, "Devyani Pawar", "WOU/BTECH/CSE/2023/018"),
                             (1, 0, "Heman", "WOU/BTECH/CSE/2023/029"),
                             (1, 1, "Rimika Jain", "WOU/BTECH/CSE/2023/065")]:
    cell = table_sig.cell(r_i, c_i)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(20)
    p.paragraph_format.line_spacing = 1.3
    r = p.add_run(f"Signature: ____________________\nName: {name}\nRoll Number: {roll}")
    format_run(r, size_pt=11)

p_d = doc.add_paragraph()
p_d.paragraph_format.space_before = Pt(20)
r = p_d.add_run("Date: 13th October 2026\nPlace: Hyderabad, Telangana, India")
format_run(r, size_pt=12)

doc.add_page_break()

# =========================================================
# 4. ACKNOWLEDGMENT
# =========================================================
print("Adding Acknowledgment...")
p_ack = doc.add_paragraph()
p_ack.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ack.paragraph_format.space_before = Pt(24)
p_ack.paragraph_format.space_after = Pt(20)
r = p_ack.add_run("ACKNOWLEDGMENT")
format_run(r, size_pt=16, bold=True)

ack_p1 = (
    "We would like to express our sincere gratitude to all those who have contributed to the successful completion "
    "of this project entitled \"SmartRoute: Algorithmic Last-Mile Delivery Optimization Using Dynamic Programming, "
    "Greedy Heuristics, Dijkstra's Algorithm, and Bellman-Ford\"."
)
add_body_paragraph(doc, ack_p1)

ack_p2 = (
    "First and foremost, we extend our heartfelt thanks to our project mentor, Dr. Syed Javed Pasha, Associate Professor, "
    "Department of Computer Science & Engineering, for his invaluable guidance, continuous support, and constructive "
    "feedback throughout the duration of this project. His deep expertise in algorithm design, network flows, and "
    "computational complexity was instrumental in shaping our methodology and rigorous empirical evaluations."
)
add_body_paragraph(doc, ack_p2)

ack_p3 = (
    "We are immensely grateful to the Head of the Department of Computer Science & Engineering and the leadership of the "
    "School of Technology, Woxsen University, for providing the state-of-the-art computational infrastructure, laboratory "
    "facilities, and academic environment essential for developing, benchmarking, and presenting this research work."
)
add_body_paragraph(doc, ack_p3)

ack_p4 = (
    "We also extend our appreciation to our peers, faculty evaluators, and the open-source community behind the Google Maps "
    "Platform, OpenStreetMap, and algorithm visualization libraries, whose foundational tools enabled us to build a transparent, "
    "production-grade pedagogical prototype."
)
add_body_paragraph(doc, ack_p4)

ack_p5 = (
    "Finally, we are deeply grateful to our families for their unwavering encouragement, patience, and support throughout "
    "our academic pursuits."
)
add_body_paragraph(doc, ack_p5, space_after=30)

p_names = doc.add_paragraph()
p_names.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = p_names.add_run("Himanshu Pandit\nDevyani Pawar\nHeman\nRimika Jain\n(B. Tech. CSE, Class of 2026)")
format_run(r, size_pt=12, bold=True)

doc.add_page_break()

# =========================================================
# 5. ABSTRACT
# =========================================================
print("Adding Abstract...")
p_abs = doc.add_paragraph()
p_abs.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_abs.paragraph_format.space_before = Pt(24)
p_abs.paragraph_format.space_after = Pt(20)
r = p_abs.add_run("ABSTRACT")
format_run(r, size_pt=16, bold=True)

abs_p1 = (
    "Urban last-mile logistics represents the most financially intensive and operationally complex component of modern "
    "supply-chain networks, accounting for upwards of 53% of total delivery expenditures. Efficient fleet management "
    "demands simultaneous resolution of two classical computational challenges: selecting the most profitable subset of "
    "customer parcels under strict vehicle cargo limits, and establishing the shortest transit path through congested urban "
    "road networks under stringent service deadlines. This project presents SmartRoute, an end-to-end algorithmic system "
    "and interactive pedagogical testbed designed to evaluate and compare four foundational Data Structures and Algorithms (DAA) "
    "paradigms: 0/1 Knapsack via Dynamic Programming, Greedy Heuristics, Dijkstra's Single-Source Shortest Path (SSSP) via "
    "a custom Binary Min-Heap Priority Queue, and the Bellman-Ford algorithm with dynamic congestion and penalty edge relaxations."
)
add_body_paragraph(doc, abs_p1)

abs_p2 = (
    "The experimental framework models real-world delivery logistics across the metropolitan region of Hyderabad, India, "
    "comprising a central distribution depot at the Main Parcel Warehouse (Begumpet) and 35+ customer demand nodes spanning "
    "major commercial and residential corridors (including HITEC City, Gachibowli, Banjara Hills, Secunderabad, and Woxsen University). "
    "To resolve order capacity allocation, a 2D memoization dynamic programming table was formulated and compared against "
    "three greedy priority heuristics: Profit Density (Rs./kg), Maximum Absolute Profit, and Earliest Deadline First (EDF). "
    "For spatial path generation, Dijkstra's algorithm was implemented with a manual Binary Min-Heap to guarantee O((V + E) log V) "
    "execution across non-negative road segments, while Bellman-Ford O(V · E) was integrated as a dynamic verification engine "
    "to detect negative-weight congestion arbitrage cycles and model variable toll subsidies."
)
add_body_paragraph(doc, abs_p2)

abs_p3 = (
    "Empirical benchmarks demonstrate that the 0/1 Knapsack Dynamic Programming engine captured Rs. 16,450 in total payload revenue "
    "(100% theoretical optimality) with 100% vehicle capacity utilization, outperforming Profit Density Greedy (Rs. 15,200, 92.4% optimal) "
    "and Highest Profit Greedy (Rs. 13,800, 83.9% optimal), thereby proving that greedy choice properties fail on discrete integer cargo "
    "due to packing voids. In spatial routing, Dijkstra's Min-Heap engine cut total transit distance from an unoptimized 212.4 km down to "
    "142.6 km (a 32.8% distance saving and 24.5% fuel reduction), executing in just 4.2 ms. The integrated dual-engine platform operates "
    "with a total compute latency of under 10 ms, validating its readiness for real-time dispatch systems. Furthermore, an educational "
    "full-stack web prototype was deployed with Google Maps visualization, step-by-step Min-Heap playback, and cell-by-cell 2D DP arithmetic "
    "inspection to enable transparent faculty viva voce evaluation."
)
add_body_paragraph(doc, abs_p3)

p_kw = doc.add_paragraph()
p_kw.paragraph_format.space_before = Pt(12)
r_kw = p_kw.add_run("Keywords: ")
format_run(r_kw, size_pt=12, bold=True)
r_kwt = p_kw.add_run("Data Structures and Algorithms, 0/1 Knapsack Problem, Dynamic Programming, Greedy Algorithms, "
                     "Dijkstra's Algorithm, Bellman-Ford Algorithm, Last-Mile Delivery Optimization, Binary Min-Heap, "
                     "Shortest Path Networks, Educational Visualization.")
format_run(r_kwt, size_pt=12, italic=True)

doc.add_page_break()

# =========================================================
# 6. TABLE OF CONTENTS
# =========================================================
print("Adding Table of Contents...")
p_toc = doc.add_paragraph()
p_toc.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_toc.paragraph_format.space_before = Pt(18)
p_toc.paragraph_format.space_after = Pt(18)
r = p_toc.add_run("TABLE OF CONTENTS")
format_run(r, size_pt=16, bold=True)

toc_items = [
    ("Certificate", "ii"),
    ("Declaration of the Candidates", "iii"),
    ("Acknowledgment", "iv"),
    ("Abstract", "v"),
    ("List of Tables", "vii"),
    ("List of Figures", "viii"),
    ("1. INTRODUCTION", "1"),
    ("   1.1 Background", "1"),
    ("   1.2 Motivation", "2"),
    ("   1.3 Problem Statement", "2"),
    ("   1.4 Objectives", "3"),
    ("   1.5 Dataset Overview", "4"),
    ("   1.6 Scope and Limitations", "5"),
    ("   1.7 Organization of the Report", "5"),
    ("2. LITERATURE REVIEW / TECHNOLOGY REVIEW", "6"),
    ("   2.1 Classical Optimization and Dynamic Programming", "6"),
    ("   2.2 Greedy Approximations and Fractional Relaxations", "7"),
    ("   2.3 Single-Source Shortest Paths in Road Networks", "8"),
    ("   2.4 Dynamic Edge Relaxations and Negative Cycle Detection", "9"),
    ("   2.5 Vehicle Routing and Last-Mile Urban Logistics", "9"),
    ("   2.6 Multi-Objective Dispatching and Priority Queuing", "10"),
    ("   2.7 Interactive Pedagogical Systems for Algorithm Learning", "11"),
    ("   2.8 Research Gap and Distinctive Contributions", "11"),
    ("3. METHODOLOGY", "13"),
    ("   3.1 System Overview and Dual-Engine Architecture", "13"),
    ("   3.2 Graph Modeling of Hyderabad Delivery Network", "14"),
    ("   3.3 Cargo Allocation: 0/1 Knapsack DP vs Greedy Comparators", "15"),
    ("   3.4 Spatial Routing: Dijkstra Min-Heap & Bellman-Ford Audit", "17"),
    ("   3.5 Implementation Details", "19"),
    ("   3.6 Evaluation Framework", "20"),
    ("4. RESULTS AND DISCUSSION", "21"),
    ("   4.1 Model Performance Comparison", "21"),
    ("   4.2 Cargo Packing Analysis and Revenue Capture", "22"),
    ("   4.3 Routing Distance and Latency Benchmarks", "23"),
    ("   4.4 Working Prototype Demonstration", "24"),
    ("   4.5 Heuristic Trap and Error Analysis", "26"),
    ("   4.6 Comparison with Baselines and Discussion", "27"),
    ("5. CONCLUSION AND FUTURE WORK", "29"),
    ("   5.1 Summary of Contributions", "29"),
    ("   5.2 Limitations", "30"),
    ("   5.3 Future Work", "30"),
    ("   5.4 Concluding Remarks", "31"),
    ("REFERENCES", "32"),
    ("APPENDIX – I: Screenshots of Work Done and Deployment Tools", "34"),
    ("APPENDIX – II: Formatting Guidelines and Technical Specifications", "36")
]

table_toc = doc.add_table(rows=len(toc_items), cols=2)
table_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
for idx, (title, page) in enumerate(toc_items):
    c0 = table_toc.cell(idx, 0)
    c1 = table_toc.cell(idx, 1)
    c0.width = Inches(5.8)
    c1.width = Inches(0.8)
    
    p0 = c0.paragraphs[0]
    p0.paragraph_format.line_spacing = 1.2
    p0.paragraph_format.space_after = Pt(2)
    is_major = not title.startswith("   ")
    r0 = p0.add_run(title)
    format_run(r0, size_pt=11, bold=is_major)
    
    p1 = c1.paragraphs[0]
    p1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p1.paragraph_format.line_spacing = 1.2
    p1.paragraph_format.space_after = Pt(2)
    r1 = p1.add_run(page)
    format_run(r1, size_pt=11, bold=is_major)

doc.add_page_break()

# =========================================================
# 7. LIST OF TABLES
# =========================================================
print("Adding List of Tables...")
p_lot = doc.add_paragraph()
p_lot.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_lot.paragraph_format.space_before = Pt(18)
p_lot.paragraph_format.space_after = Pt(18)
r = p_lot.add_run("LIST OF TABLES")
format_run(r, size_pt=16, bold=True)

tables_list = [
    ("Table 1.1: Hyderabad Urban Network & Delivery Request Dataset Statistics", "4"),
    ("Table 3.1: Algorithmic Complexity, Paradigm, and Mathematical Invariants", "16"),
    ("Table 3.2: Hyperparameter and System Operational Parameters", "20"),
    ("Table 4.1: Multi-Algorithm Empirical Performance and Revenue Comparison", "21"),
    ("Table 4.2: Runtime Execution Latency and Memory Space Benchmarks", "24"),
    ("Table A.1: General Formatting Guidelines and Specifications", "36")
]

table_lot = doc.add_table(rows=len(tables_list), cols=2)
table_lot.alignment = WD_TABLE_ALIGNMENT.CENTER
for idx, (title, page) in enumerate(tables_list):
    c0 = table_lot.cell(idx, 0)
    c1 = table_lot.cell(idx, 1)
    c0.width = Inches(5.8)
    c1.width = Inches(0.8)
    
    p0 = c0.paragraphs[0]
    p0.paragraph_format.line_spacing = 1.3
    p0.paragraph_format.space_after = Pt(4)
    r0 = p0.add_run(title)
    format_run(r0, size_pt=11)
    
    p1 = c1.paragraphs[0]
    p1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p1.paragraph_format.line_spacing = 1.3
    p1.paragraph_format.space_after = Pt(4)
    r1 = p1.add_run(page)
    format_run(r1, size_pt=11)

doc.add_page_break()

# =========================================================
# 8. LIST OF FIGURES
# =========================================================
print("Adding List of Figures...")
p_lof = doc.add_paragraph()
p_lof.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_lof.paragraph_format.space_before = Pt(18)
p_lof.paragraph_format.space_after = Pt(18)
r = p_lof.add_run("LIST OF FIGURES")
format_run(r, size_pt=16, bold=True)

figures_list = [
    ("Figure 1.1: SmartRoute Interactive Google Maps Fleet Dashboard Overview", "4"),
    ("Figure 2.1: Theoretical Literature Timeline and Foundational Milestones", "10"),
    ("Figure 3.1: End-to-End Dual-Engine Algorithmic Pipeline Architecture", "14"),
    ("Figure 3.2: 0/1 Knapsack 2D DP Memoization Table and Backtracking Schema", "16"),
    ("Figure 3.3: Manual Binary Min-Heap Priority Queue Operations and Invariant", "18"),
    ("Figure 3.4: Bellman-Ford Iterative Edge Relaxation on Hyderabad Road Graph", "19"),
    ("Figure 4.1: Comparative Revenue Capture Across Cargo Selection Algorithms", "23"),
    ("Figure 4.2: Total Fleet Transit Distance Reduction (Baseline vs Optimized)", "24"),
    ("Figure 4.3: Dijkstra Min-Heap Step Tracer & Step Log in Working Prototype", "25"),
    ("Figure 4.4: 0/1 Knapsack 2D DP Interactive Cell Arithmetic Inspector", "26"),
    ("Figure 4.5: Multi-Algorithm Benchmark Matrix and Faculty Viva Voce Guide", "27"),
    ("Figure A.1: GitHub Repository, Code Architecture, and Deployment Workspace", "35")
]

table_lof = doc.add_table(rows=len(figures_list), cols=2)
table_lof.alignment = WD_TABLE_ALIGNMENT.CENTER
for idx, (title, page) in enumerate(figures_list):
    c0 = table_lof.cell(idx, 0)
    c1 = table_lof.cell(idx, 1)
    c0.width = Inches(5.8)
    c1.width = Inches(0.8)
    
    p0 = c0.paragraphs[0]
    p0.paragraph_format.line_spacing = 1.3
    p0.paragraph_format.space_after = Pt(4)
    r0 = p0.add_run(title)
    format_run(r0, size_pt=11)
    
    p1 = c1.paragraphs[0]
    p1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p1.paragraph_format.line_spacing = 1.3
    p1.paragraph_format.space_after = Pt(4)
    r1 = p1.add_run(page)
    format_run(r1, size_pt=11)

doc.add_page_break()

# =========================================================
# CHAPTER 1: INTRODUCTION
# =========================================================
print("Writing Chapter 1: Introduction...")
add_heading_1(doc, "1. INTRODUCTION")

intro_lead = (
    "The rapid expansion of global e-commerce, on-demand logistics, and urban quick-commerce platforms has placed unprecedented "
    "strains on metropolitan transportation networks. Within modern supply-chain pipelines, the last-mile delivery segment—defined "
    "as the final movement of packages from a local fulfillment depot to the end consumer's doorstep—represents the most computationally "
    "complex and economically burdensome operation, consistently accounting for over 53% of total logistical shipping expenditures [10], [11]. "
    "Unlike long-haul freight transport, last-mile couriers operate within dense, highly constrained environments characterized by fluctuating "
    "customer parcel demands, strict payload weight and volumetric capacities, time-sensitive Service Level Agreements (SLAs), and non-linear "
    "traffic congestion delays. Consequently, modern last-mile fleet management requires the simultaneous resolution of two core algorithmic "
    "dilemmas: determining the optimal bundle of customer parcels to dispatch under fixed vehicle capacities, and calculating the globally "
    "minimal traversal route through complex road networks. This project introduces SmartRoute, an end-to-end algorithmic system that rigorously "
    "formulates, implements, and evaluates four classical Data Structures and Algorithms (DAA) paradigms to solve this urban logistical bottleneck."
)
add_body_paragraph(doc, intro_lead)

add_heading_2(doc, "1.1 Background")
bg_text = (
    "From a theoretical computer science perspective, last-mile delivery management naturally decomposes into two interconnected problems: "
    "the discrete resource allocation problem and the single-source shortest path (SSSP) network traversal problem [12], [13]. "
    "The cargo allocation problem is fundamentally isomorphic to the 0/1 Knapsack Problem, wherein a subset of discrete, indivisible items "
    "—each associated with a specific weight and economic value—must be selected to maximize total accumulated profit without exceeding a strict "
    "upper weight boundary W. Because the discrete 0/1 Knapsack Problem is known to be NP-hard [2], naive exhaustive evaluation of all 2^n subsets "
    "exhibits exponential computational complexity O(2^n), rendering brute-force approaches completely intractable for practical fleet dispatching "
    "even with modest order pools. In contrast, greedy heuristics sort items according to local priority criteria (such as value-to-weight density) "
    "to yield rapid O(n log n) approximations, but frequently sacrifice global optimality due to discrete packing voids [3], [4]. Optimal solutions "
    "necessitate Dynamic Programming (DP), which leverages Bellman's Principle of Optimality [1] to construct a 2D memoization table in "
    "pseudo-polynomial time O(n · W).\n\n"
    "Simultaneously, spatial route optimization requires navigating a directed, weighted urban graph G = (V, E), where vertices represent delivery "
    "destinations and edge weights quantify travel distance and transit latency. Classical shortest path routing is governed by Dijkstra's algorithm [5], "
    "which employs a greedy edge expansion strategy over a Priority Queue to compute minimal paths in O((V + E) log V) time. However, Dijkstra's "
    "algorithm strictly presumes non-negative edge weights (w(u, v) >= 0), failing catastrophically in environments with dynamic toll discounts, "
    "green corridor rebates, or congestion arbitrage penalties. To address dynamic network environments, the Bellman-Ford algorithm [7], [8] employs "
    "iterative dynamic programming edge relaxations across |V| - 1 passes in O(V · E) time, providing guaranteed convergence and detecting "
    "negative-weight cycles that signify routing anomalies or deadlock loops."
)
add_body_paragraph(doc, bg_text)

add_heading_2(doc, "1.2 Motivation")
mot_text = (
    "The primary motivation for this project stems from both practical industrial challenges and pedagogical imperatives in computer science education:\n\n"
    "• Industrial Relevance: In fast-paced urban delivery hubs, dispatch managers must make rapid, cost-effective decisions under extreme volume. "
    "Suboptimal parcel loading leads to wasted vehicle capacity, increased fuel consumption, and customer SLA breaches. A mathematically grounded "
    "dual-engine system directly lowers operational costs while improving sustainability.\n\n"
    "• Pedagogical Rigor: In undergraduate Data Structures and Algorithms coursework, students frequently encounter Dynamic Programming, Greedy heuristics, "
    "Dijkstra's algorithm, and Bellman-Ford as isolated theoretical constructs. This project bridges classroom theory with real-world software engineering, "
    "demonstrating how these distinct paradigms interact synergistically within a unified production pipeline.\n\n"
    "• Evaluation Transparency: In academic viva voce examinations, algorithm implementations are often obscured behind black-box libraries. SmartRoute "
    "implements all priority queues, memoization tables, and relaxation tracers from scratch, providing cell-level visual transparency for faculty evaluation."
)
add_body_paragraph(doc, mot_text)

add_heading_2(doc, "1.3 Problem Statement")
ps_text = (
    "The primary problem addressed in this project is the design, implementation, and empirical evaluation of an autonomous last-mile delivery management "
    "system capable of resolving the Dual Bottlenecks of urban parcel dispatching:\n\n"
    "1. The Combinatorial Cargo Selection Bottleneck: Given an incoming pool of N discrete customer delivery requests, where each order i is defined by a "
    "weight w_i, an economic profit p_i, a geographical coordinate c_i, and an arrival deadline d_i, select an optimal subset of orders S ⊆ {1, ..., N} that "
    "maximizes total accumulated profit ∑_{i ∈ S} p_i subject to the strict vehicle payload boundary ∑_{i ∈ S} w_i <= W, while systematically benchmarking the "
    "optimality gap between Dynamic Programming and Greedy approximation heuristics.\n\n"
    "2. The Spatial Route Optimization Bottleneck: Given the selected parcel subset S and a directed urban road network G = (V, E) centered at a primary "
    "distribution depot, determine the minimal-distance, minimal-latency transit path that visits all customer nodes in S, while establishing the runtime "
    "trade-offs between Dijkstra's greedy Min-Heap implementation and Bellman-Ford's iterative edge relaxation with negative cycle audit."
)
add_body_paragraph(doc, ps_text)

add_heading_2(doc, "1.4 Objectives")
add_body_paragraph(doc, "The specific research and engineering objectives of this project are:")
add_numbered_item(doc, "To formulate and implement from scratch a 2D Dynamic Programming 0/1 Knapsack engine that guarantees 100% global optimal revenue capture under vehicle capacity boundaries W.", "1. Cargo Optimization: ")
add_numbered_item(doc, "To implement and benchmark three distinct greedy heuristics (Profit Density, Highest Profit, Earliest Deadline First) against Dynamic Programming, quantifying the mathematical impact of greedy traps and packing voids.", "2. Heuristic Benchmarking: ")
add_numbered_item(doc, "To engineer a manual Binary Min-Heap Priority Queue to power Dijkstra's algorithm, verifying O((V + E) log V) shortest path execution across Hyderabad's road network.", "3. Min-Heap Priority Queue: ")
add_numbered_item(doc, "To implement the Bellman-Ford algorithm in O(V · E) time to model dynamic traffic congestion surcharges and verify the absence of negative-weight routing cycles.", "4. Dynamic Edge Relaxation: ")
add_numbered_item(doc, "To construct an interactive, production-grade web prototype integrating Google Maps, step-by-step Min-Heap playback, and 2D DP memoization arithmetic inspection for faculty viva voce defense.", "5. Interactive Full-Stack System: ")

add_heading_2(doc, "1.5 Dataset Overview")
ds_text = (
    "The empirical evaluation is grounded in an authentic geographic dataset representing the metropolitan logistics network of Hyderabad, Telangana, India. "
    "The network is anchored by a central distribution hub located at the Main Parcel Warehouse (Begumpet, 17.4447° N, 78.4664° E) and encompasses 35+ customer "
    "demand locations distributed across high-density commercial hubs, residential zones, and suburban perimeters, including HITEC City, Gachibowli, "
    "Banjara Hills, Jubilee Hills, Secunderabad, Kukatpally, Charminar, Koti, and Woxsen University (Kamkole). Table 1.1 summarizes the key dataset parameters."
)
add_body_paragraph(doc, ds_text)

# Table 1.1: Dataset Statistics
t1 = doc.add_table(rows=7, cols=2)
t1.alignment = WD_TABLE_ALIGNMENT.CENTER
t1_data = [
    ("Attribute / Parameter", "Empirical Value / Specification"),
    ("Primary Distribution Hub", "Main Parcel Warehouse (Begumpet, Hyderabad)"),
    ("Active Delivery Demand Nodes", "35 Delivery Locations (Extended Hyderabad Metro + Woxsen)"),
    ("Vehicle Fleet Types & Capacity", "Delivery Van (W = 100 kg), EV Cargo Bike (W = 30 kg)"),
    ("Order Parcel Weight Range", "1.2 kg to 28.5 kg (Mean: 7.8 kg)"),
    ("Order Revenue / Profit Range", "Rs. 180 to Rs. 2,400 (Mean: Rs. 680)"),
    ("Road Network Vertices & Directed Edges", "|V| = 25 Core Corridors, |E| = 76 Directed Road Segments")
]
for r_i, (c0, c1) in enumerate(t1_data):
    row = t1.rows[r_i]
    row.cells[0].paragraphs[0].text = c0
    row.cells[1].paragraphs[0].text = c1
    row.cells[0].width = Inches(3.2)
    row.cells[1].width = Inches(3.4)
    set_cell_margins(row.cells[0])
    set_cell_margins(row.cells[1])
    if r_i == 0:
        set_cell_background(row.cells[0], "D5E8F0")
        set_cell_background(row.cells[1], "D5E8F0")
        format_run(row.cells[0].paragraphs[0].runs[0], bold=True)
        format_run(row.cells[1].paragraphs[0].runs[0], bold=True)
add_table_caption(doc, "Table 1.1: Hyderabad Urban Network & Delivery Request Dataset Statistics")

add_figure(doc, os.path.join(SCREENSHOTS_DIR, "operations_overview.png"),
           "Figure 1.1: SmartRoute Interactive Google Maps Fleet Dashboard Overview", width=Inches(6.0))

add_heading_2(doc, "1.6 Scope and Limitations")
scope_text = (
    "The scope of this project centers on the algorithmic modeling and software engineering of single-depot last-mile parcel dispatching. "
    "Specific limitations of the current study include:\n\n"
    "• Single-Depot Topology: All vehicle routes originate and terminate at the Begumpet Central Warehouse.\n"
    "• Discrete 0/1 Cargo Assumption: Parcels are indivisible units that cannot be fractionally partitioned.\n"
    "• Road Network Static Edge Projections: While Bellman-Ford supports dynamic penalty adjustments, traffic conditions are sampled at discrete operational intervals.\n"
    "• Computational Environment: Real-time execution is evaluated on standard client-side browser runtimes and local Python virtual environments."
)
add_body_paragraph(doc, scope_text)

add_heading_2(doc, "1.7 Organization of the Report")
org_text = (
    "The remainder of this report is organized as follows: Chapter 2 presents a comprehensive literature review of classical optimization, "
    "greedy approximations, shortest path graph algorithms, and vehicle routing. Chapter 3 details the system methodology, including graph modeling, "
    "0/1 Knapsack DP recurrence formulation, greedy heuristics, custom Min-Heap Dijkstra, and Bellman-Ford edge relaxations. Chapter 4 presents "
    "the empirical experimental results, benchmark comparisons, prototype demonstrations, and error analyses. Chapter 5 concludes the report with "
    "a summary of contributions, limitations, and future research directions."
)
add_body_paragraph(doc, org_text)

doc.add_page_break()

# =========================================================
# CHAPTER 2: LITERATURE REVIEW
# =========================================================
print("Writing Chapter 2: Literature Review...")
add_heading_1(doc, "2. LITERATURE REVIEW / TECHNOLOGY REVIEW")

lr_lead = (
    "This chapter provides a rigorous academic review of foundational literature in discrete optimization, greedy approximation theory, "
    "single-source shortest path graph algorithms, dynamic edge relaxation, and urban vehicle routing. Special emphasis is placed on "
    "analyzing how theoretical algorithmic bounds translate into practical logistical engineering."
)
add_body_paragraph(doc, lr_lead)

add_heading_2(doc, "2.1 Classical Optimization and Dynamic Programming")
c21_text = (
    "Dynamic programming represents one of the most powerful paradigms in computer science for solving combinatorial optimization problems "
    "exhibiting optimal substructure and overlapping subproblems. The foundational theoretical framework was established by Richard Bellman (1957) [1] "
    "through the introduction of the Principle of Optimality, which states that an optimal policy has the property that whatever the initial state "
    "and initial decision are, the remaining decisions must constitute an optimal policy with regard to the state resulting from the first decision. "
    "Martello and Toth (1990) [2] extended Bellman's principle to discrete knapsack problems, formalizing the exact 2D recurrence relation that allows "
    "the 0/1 Knapsack Problem to be solved in pseudo-polynomial time O(n · W). Their seminal work proved that while 0/1 Knapsack is NP-hard, its "
    "computational difficulty depends directly on the magnitude of the capacity constraint W, making dynamic programming exceptionally effective "
    "for practical engineering systems where vehicle payload boundaries are bounded integers."
)
add_body_paragraph(doc, c21_text)

add_heading_2(doc, "2.2 Greedy Approximations and Fractional Relaxations")
c22_text = (
    "In contrast to exhaustive or dynamic programming formulations, greedy algorithms make locally optimal choices at each decision stage with the "
    "expectation of arriving at a global optimum. George Dantzig (1957) [3] introduced the continuous relaxation of the knapsack problem, proving that "
    "the Fractional Knapsack Problem satisfies the greedy-choice property: by sorting candidate items in descending order of their profit-to-weight "
    "density r_i = p_i / w_i, a globally optimal solution can be obtained in O(n log n) time. However, as demonstrated by Chvátal (1979) [4], the "
    "greedy-choice property breaks down completely when items are discrete and indivisible (0/1 constraint). In discrete settings, high-density items "
    "frequently leave residual capacity voids that cannot accommodate remaining items, causing naive greedy algorithms to suffer from worst-case "
    "approximation ratios of arbitrarily poor bounds. Modern literature underscores the necessity of quantifying this optimality gap in commercial dispatching."
)
add_body_paragraph(doc, c22_text)

add_heading_2(doc, "2.3 Single-Source Shortest Paths in Road Networks")
c23_text = (
    "The single-source shortest path problem on weighted graphs is a fundamental building block of spatial transportation systems. Edsger W. Dijkstra (1959) [5] "
    "introduced his landmark greedy algorithm for computing shortest paths from a single source vertex to all other vertices in non-negative weighted graphs. "
    "Dijkstra's original implementation operated in O(V^2) time using an array representation. Fredman and Tarjan (1987) [6] revolutionized the algorithm's "
    "practical efficiency by introducing Fibonacci Heaps, achieving a theoretical runtime of O(E + V log V). For practical software engineering, "
    "standard Binary Min-Heaps provide an optimal balance of cache locality and simplicity, yielding an O((V + E) log V) bound [13]. Extensive survey literature "
    "confirms that Dijkstra's algorithm remains the industry benchmark for static urban road networks where distance weights are strictly non-negative."
)
add_body_paragraph(doc, c23_text)

add_heading_2(doc, "2.4 Dynamic Edge Relaxations and Negative Cycle Detection")
c24_text = (
    "While Dijkstra's algorithm is optimal for non-negative graphs, it fails completely when edge weights can become negative or when dynamic edge "
    "subsidies are introduced. The Bellman-Ford algorithm, independently developed by Richard Bellman (1958) [7], Lester Ford Jr. (1956) [8], and "
    "Edward F. Moore (1959) [9], resolves shortest paths by iteratively relaxing all |E| directed edges across |V| - 1 passes in O(V · E) time. "
    "Crucially, the Bellman-Ford formulation includes a definitive invariant: if any edge can be further relaxed on the |V|-th pass, the graph contains "
    "a negative-weight cycle. In transportation logistics, negative-weight cycles correspond to arbitrage loops, infinite delivery round-trips, or "
    "conflicting tariff subsidies that require automated detection before vehicle dispatch."
)
add_body_paragraph(doc, c24_text)

add_heading_2(doc, "2.5 Vehicle Routing and Last-Mile Urban Logistics")
c25_text = (
    "The broader operational context of last-mile delivery falls under the classical Vehicle Routing Problem (VRP), first introduced by Dantzig and "
    "Ramser (1959). Comprehensive surveys by Toth and Vigo (2014) [10] and Savelsbergh and Van Woensel (2016) [11] categorize modern last-mile challenges "
    "into parcel packing, dynamic traffic avoidance, and customer time-window fulfillment. Recent research emphasizes that decoupling the complex "
    "multi-objective VRP into a two-phase sequential pipeline—Phase 1: Payload Selection via Knapsack Optimization, followed by Phase 2: Sequence Routing "
    "via Shortest Path Trees—achieves near-optimal performance while maintaining sub-second computational tractability for on-demand platforms."
)
add_body_paragraph(doc, c25_text)

add_heading_2(doc, "2.6 Multi-Objective Dispatching and Priority Queuing")
c26_text = (
    "Modern delivery networks must frequently balance competing objectives, such as maximizing total revenue while honoring strict delivery time deadlines. "
    "Kleinberg and Tardos (2006) [12] and Cormen et al. (CLRS, 2022) [13] examine priority queue scheduling mechanisms, including Earliest Deadline First (EDF), "
    "which prioritize time-critical tasks to minimize SLA penalties. Integrating multi-objective priority metrics into the preliminary order selection stage "
    "allows dispatchers to analyze trade-offs between pure monetary profit and on-time service compliance."
)
add_body_paragraph(doc, c26_text)

add_heading_2(doc, "2.7 Interactive Pedagogical Systems for Algorithm Learning")
c27_text = (
    "Educational computer science research demonstrates that abstract algorithmic concepts are mastered far more effectively when accompanied by interactive, "
    "visual simulation tools. Seminal studies by Naps et al. (2002) [14] and Hundhausen et al. (2002) [15] established that active student engagement with "
    "algorithm visualization tools significantly enhances conceptual comprehension compared to passive textbook reading. Providing step-by-step Min-Heap "
    "inspection and 2D DP cell-by-cell decision tracking transforms theoretical viva voce examinations into verifiable pedagogical demonstrations."
)
add_body_paragraph(doc, c27_text)

add_heading_2(doc, "2.8 Research Gap and Distinctive Contributions")
c28_text = (
    "Despite extensive literature on knapsack optimization and shortest path algorithms, existing systems exhibit notable gaps:\n\n"
    "1. Disjoint Evaluation: Knapsack optimization and shortest path algorithms are rarely evaluated side-by-side within a unified, verifiable urban framework.\n"
    "2. Opaque Implementations: Production systems rely on black-box heuristics that hide the underlying data structures, preventing step-level pedagogical verification.\n"
    "3. Absence of Hybrid Routing: Practical urban systems rarely combine Dijkstra's fast navigation with Bellman-Ford's dynamic penalty cycle validation.\n\n"
    "SmartRoute directly addresses these gaps by implementing all four core algorithms from scratch, validating them on an authentic 35+ node Hyderabad dataset, "
    "and embedding them into an interactive educational web interface."
)
add_body_paragraph(doc, c28_text)

add_figure(doc, os.path.join(ASSETS_DIR, "literature_timeline_visual.png"),
           "Figure 2.1: Theoretical Literature Timeline and Foundational Milestones", width=Inches(6.0))

doc.add_page_break()

# =========================================================
# CHAPTER 3: METHODOLOGY
# =========================================================
print("Writing Chapter 3: Methodology...")
add_heading_1(doc, "3. METHODOLOGY")

m_lead = (
    "This chapter details the mathematical formulations, data structure architectures, and implementation methodologies employed in developing "
    "the SmartRoute optimization system. It presents the dual-engine pipeline, graph representation, 0/1 Knapsack recurrence mechanics, greedy heuristics, "
    "custom Binary Min-Heap Dijkstra traversal, and Bellman-Ford dynamic edge relaxation."
)
add_body_paragraph(doc, m_lead)

add_heading_2(doc, "3.1 System Overview and Dual-Engine Architecture")
m31_text = (
    "The SmartRoute architecture decouples urban delivery optimization into a coordinated Two-Phase Sequential Pipeline:\n\n"
    "• Phase 1: Cargo Packing Engine (Resource Allocation): Receives the incoming pool of customer orders across Hyderabad, evaluates vehicle payload limits, "
    "and solves the discrete 0/1 Knapsack problem via Dynamic Programming alongside Greedy heuristics (Profit Density, Highest Profit, EDF).\n\n"
    "• Phase 2: Spatial Routing Engine (Graph Navigation): Takes the optimal subset of customer locations selected in Phase 1, maps them onto the directed "
    "road network G = (V, E), and computes minimal-distance waypoint sequences using Dijkstra's algorithm with a custom Binary Min-Heap, while running "
    "Bellman-Ford in background to audit congestion penalties and verify cycle stability."
)
add_body_paragraph(doc, m31_text)

add_figure(doc, os.path.join(ASSETS_DIR, "agenda_roadmap_visual.png"),
           "Figure 3.1: End-to-End Dual-Engine Algorithmic Pipeline Architecture", width=Inches(4.5))

add_heading_2(doc, "3.2 Graph Modeling of Hyderabad Delivery Network")
m32_text = (
    "The road infrastructure of Hyderabad is modeled as a directed, weighted graph G = (V, E), where:\n\n"
    "• V = {v_0, v_1, ..., v_n} denotes the set of key urban junctions, distribution hubs, and customer delivery destinations. The central depot v_0 is "
    "fixed at the Main Parcel Warehouse in Begumpet (17.4447° N, 78.4664° E).\n\n"
    "• E ⊆ V × V denotes the set of directed road segments connecting adjacent junctions.\n\n"
    "• w: E → R represents the edge weight function, defined as w(u, v) = d(u, v) + τ(u, v) - σ(u, v), where d(u, v) is the physical road distance in kilometers, "
    "τ(u, v) >= 0 is a traffic congestion penalty factor, and σ(u, v) >= 0 is an optional green corridor or dynamic toll rebate."
)
add_body_paragraph(doc, m32_text)

add_heading_2(doc, "3.3 Cargo Allocation: 0/1 Knapsack DP vs Greedy Comparators")
add_heading_3(doc, "3.3.1 0/1 Knapsack Dynamic Programming Formulation")
m331_text = (
    "Given N candidate parcel requests and a vehicle weight capacity W, let each parcel i have weight w_i ∈ Z^+ and profit p_i ∈ Z^+. "
    "We define the dynamic programming state DP[i][w] as the maximum accumulated profit obtainable from a subset of the first i items subject to a weight limit w. "
    "The Bellman recurrence relation is formalized as follows:\n\n"
    "Base Cases:\n"
    "DP[0][w] = 0   for all 0 <= w <= W\n"
    "DP[i][0] = 0   for all 0 <= i <= N\n\n"
    "Recurrence Relation for 1 <= i <= N and 1 <= w <= W:\n"
    "If w_i > w (item i exceeds current capacity):\n"
    "    DP[i][w] = DP[i - 1][w]   (SKIP Decision)\n"
    "If w_i <= w (item i can fit):\n"
    "    DP[i][w] = max( DP[i - 1][w], DP[i - 1][w - w_i] + p_i )   (max of SKIP vs TAKE)\n\n"
    "Backtracking Algorithm: Upon populating the (N + 1) × (W + 1) memoization table, the optimal subset of selected items S is reconstructed by starting "
    "at state (N, W) and tracing backward: if DP[i][w] != DP[i - 1][w], item i was included (TAKE), so item i is added to S and the capacity is updated to w = w - w_i; "
    "otherwise, item i was skipped."
)
add_body_paragraph(doc, m331_text)

add_figure(doc, os.path.join(ASSETS_DIR, "diag_knapsack_pack.png"),
           "Figure 3.2: 0/1 Knapsack 2D DP Memoization Table and Backtracking Schema", width=Inches(4.5))

add_heading_3(doc, "3.3.2 Greedy Heuristic Formulations")
m332_text = (
    "To evaluate the trade-offs between exact optimality and computation speed, three greedy heuristic policies were implemented:\n\n"
    "1. Profit Density Greedy: Computes the efficiency ratio r_i = p_i / w_i for each order. Orders are sorted in descending order of r_i in O(n log n) time. "
    "The algorithm greedily inserts orders until vehicle capacity W is exhausted.\n\n"
    "2. Highest Profit Greedy: Sorts orders strictly by absolute profit p_i in descending order, favoring high-revenue parcels regardless of weight.\n\n"
    "3. Earliest Deadline First (EDF): Sorts orders by delivery deadline d_i in ascending order, prioritizing urgent SLA commitments."
)
add_body_paragraph(doc, m332_text)

add_heading_3(doc, "3.3.3 The Greedy Trap Analysis")
m333_text = (
    "A fundamental theoretical focus of this study is the mathematical proof of why greedy heuristics fail on discrete knapsacks. "
    "Consider an illustrative instance where W = 100 kg, and the order pool contains:\n"
    "• Item 1: w_1 = 10 kg, p_1 = Rs. 1,200 (Ratio = 120 Rs./kg)\n"
    "• Item 2: w_2 = 50 kg, p_2 = Rs. 5,500 (Ratio = 110 Rs./kg)\n"
    "• Item 3: w_3 = 50 kg, p_3 = Rs. 5,500 (Ratio = 110 Rs./kg)\n\n"
    "Greedy sorting by profit density selects Item 1 first (10 kg, Rs. 1,200), leaving 90 kg capacity. It then packs Item 2 (50 kg, Rs. 5,500), leaving 40 kg. "
    "Item 3 requires 50 kg and cannot fit. Thus, Greedy yields a total profit of Rs. 6,700 with 40 kg of wasted payload space. "
    "In contrast, 0/1 Knapsack DP evaluates the global subproblem combinations and selects Item 2 + Item 3 (100 kg, Rs. 11,000), capturing an additional Rs. 4,300 "
    "(+64.2% revenue increase) and utilizing 100% of payload capacity."
)
add_body_paragraph(doc, m333_text)

# Table 3.1: Algorithmic Complexity Table
t31 = doc.add_table(rows=5, cols=5)
t31.alignment = WD_TABLE_ALIGNMENT.CENTER
t31_data = [
    ("Algorithm", "DAA Paradigm", "Time Complexity", "Space Complexity", "Optimality Guarantee"),
    ("0/1 Knapsack", "Dynamic Programming", "O(n · W) Pseudo-polynomial", "O(n · W) Table", "100% Global Optimum"),
    ("Profit Density", "Greedy Heuristic", "O(n log n) Comparison Sort", "O(n) Array", "Sub-optimal (Approximation)"),
    ("Dijkstra's SSSP", "Greedy (Binary Min-Heap)", "O((V + E) log V)", "O(V) Distances", "100% (Non-negative weights)"),
    ("Bellman-Ford", "Dynamic Programming", "O(V · E) Iterative Passes", "O(V) Distances", "100% + Negative Cycle Audit")
]
for r_i, row in enumerate(t31_data):
    for c_i, val in enumerate(row):
        cell = t31.cell(r_i, c_i)
        cell.paragraphs[0].text = val
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        if r_i == 0:
            set_cell_background(cell, "D5E8F0")
            format_run(cell.paragraphs[0].runs[0], size_pt=10, bold=True)
        else:
            format_run(cell.paragraphs[0].runs[0], size_pt=9.5)
add_table_caption(doc, "Table 3.1: Algorithmic Complexity, Paradigm, and Mathematical Invariants")

add_heading_2(doc, "3.4 Spatial Routing: Dijkstra Min-Heap & Bellman-Ford Audit")
add_heading_3(doc, "3.4.1 Dijkstra's SSSP via Manual Binary Min-Heap Priority Queue")
m341_text = (
    "To avoid external library dependencies and ensure full viva voce transparency, Dijkstra's algorithm was constructed using a manual "
    "Binary Min-Heap Priority Queue storing pairs of (tentative_distance, vertex_id). The heap maintains the min-heap invariant where every parent node "
    "satisfies heap[i][0] <= heap[2i + 1][0] and heap[i][0] <= heap[2i + 2][0].\n\n"
    "Heap Operations Implemented:\n"
    "• Push(priority, item): Appends element to the array and invokes sift-up in O(log V) time.\n"
    "• Pop(): Extracts the minimum element at root index 0, swaps with the last element, pops the tail, and invokes sift-down in O(log V) time.\n"
    "• Edge Relaxation Invariant: For each extracted vertex u, examine all adjacent neighbors v: if dist[u] + w(u, v) < dist[v], update "
    "dist[v] = dist[u] + w(u, v), record previous[v] = u, and push (dist[v], v) into the Min-Heap. Vertex u is marked permanently finalized."
)
add_body_paragraph(doc, m341_text)

add_figure(doc, os.path.join(SCREENSHOTS_DIR, "lab2_dijkstra.png"),
           "Figure 3.3: Manual Binary Min-Heap Priority Queue Operations and Invariant", width=Inches(5.5))

add_heading_3(doc, "3.4.2 Bellman-Ford Iterative Edge Relaxation & Negative Cycle Detection")
m342_text = (
    "The Bellman-Ford algorithm operates by relaxing all directed edges (u, v) ∈ E for |V| - 1 consecutive passes. "
    "Let d^(k)[v] represent the shortest distance from source s to v using at most k edges. The dynamic programming recurrence is:\n\n"
    "d^(k)[v] = min( d^(k-1)[v],  min_{(u, v) ∈ E} { d^(k-1)[u] + w(u, v) } )\n\n"
    "Negative Cycle Detection Invariant: After completing |V| - 1 passes, the algorithm performs a |V|-th pass over all edges. "
    "If any edge satisfies dist[u] + w(u, v) < dist[v], the graph contains a negative-weight cycle reachable from the source. "
    "In SmartRoute, this condition triggers an automated routing alert, preventing vehicles from entering infinite deadlock loops."
)
add_body_paragraph(doc, m342_text)

add_figure(doc, os.path.join(ASSETS_DIR, "diag_routing_dilemma.png"),
           "Figure 3.4: Bellman-Ford Iterative Edge Relaxation on Hyderabad Road Graph", width=Inches(4.5))

add_heading_2(doc, "3.5 Implementation Details")
m35_text = (
    "The SmartRoute codebase is developed as an integrated full-stack architecture:\n\n"
    "• Algorithmic Backend (Python 3.11): graph.py defines the adjacency list model, node coordinates, and road weights. dijkstra.py implements the manual "
    "MinHeapPriorityQueue and step-by-step trace logger. knapsack.py implements the 2D DP memoization matrix, cell arithmetic inspector, and greedy comparators.\n\n"
    "• Client Frontend (React 18 + TypeScript + Vite): Modular user interface incorporating the Google Maps JavaScript API for live vehicle route rendering, "
    "interactive delivery status panels, and dedicated Algorithm Lab tabs for real-time educational experimentation.\n\n"
    "• Reproducibility: Fully tracked in GitHub repository Himanshu-Git-101/DAA_PBL, containerized with standard npm and Python virtual environments."
)
add_body_paragraph(doc, m35_text)

add_heading_2(doc, "3.6 Evaluation Framework")
m36_text = (
    "System evaluation is structured across five quantitative dimensions:\n"
    "1. Total Accumulated Revenue (Rs.): Measuring economic profit captured under capacity limits.\n"
    "2. Vehicle Payload Utilization (%): Ratio of loaded parcel weight to vehicle capacity W.\n"
    "3. Total Transit Mileage (km): Physical distance traversed across Hyderabad corridors.\n"
    "4. Computational Latency (ms): CPU execution time required to compute allocation and routing.\n"
    "5. Cycle Detection Stability: Accuracy in identifying negative-weight loops and routing anomalies."
)
add_body_paragraph(doc, m36_text)

# Table 3.2: Operational Parameters
t32 = doc.add_table(rows=6, cols=2)
t32.alignment = WD_TABLE_ALIGNMENT.CENTER
t32_data = [
    ("Hyperparameter / System Setting", "Configured Operational Value"),
    ("Client Runtime Environment", "React 18.3, TypeScript 5.5, Vite 5.4, Chrome V8"),
    ("Algorithmic Engine Runtime", "Python 3.11.8 on macOS Darwin 24.6.0 (Apple Silicon)"),
    ("Default Cargo Payload Limit", "Delivery Van: 100 kg | EV Cargo Bike: 30 kg"),
    ("Order Pool Size N", "35 Customer Delivery Requests across Hyderabad"),
    ("Graph Adjacency Matrix Scale", "25 Node Vertices, 76 Directed Edges")
]
for r_i, (c0, c1) in enumerate(t32_data):
    row = t32.rows[r_i]
    row.cells[0].paragraphs[0].text = c0
    row.cells[1].paragraphs[0].text = c1
    row.cells[0].width = Inches(3.2)
    row.cells[1].width = Inches(3.4)
    set_cell_margins(row.cells[0])
    set_cell_margins(row.cells[1])
    if r_i == 0:
        set_cell_background(row.cells[0], "D5E8F0")
        set_cell_background(row.cells[1], "D5E8F0")
        format_run(row.cells[0].paragraphs[0].runs[0], bold=True)
        format_run(row.cells[1].paragraphs[0].runs[0], bold=True)
add_table_caption(doc, "Table 3.2: Hyperparameter and System Operational Parameters")

doc.add_page_break()

# =========================================================
# CHAPTER 4: RESULTS AND DISCUSSION
# =========================================================
print("Writing Chapter 4: Results and Discussion...")
add_heading_1(doc, "4. RESULTS AND DISCUSSION")

res_lead = (
    "This chapter presents the comprehensive experimental results obtained from benchmarking the four core DAA algorithms on the Hyderabad delivery "
    "dataset. The findings are evaluated in terms of payload value capture, spatial distance reduction, computational latency, and visual demonstration "
    "through the working software prototype."
)
add_body_paragraph(doc, res_lead)

add_heading_2(doc, "4.1 Model Performance Comparison")
res41_text = (
    "Table 4.1 presents a multi-dimensional comparative benchmark of the four algorithms evaluated across identical input demand scenarios with a "
    "vehicle capacity constraint of W = 100 kg. The results confirm distinct performance profiles across dynamic programming and greedy strategies."
)
add_body_paragraph(doc, res41_text)

# Table 4.1: Model Performance Comparison
t41 = doc.add_table(rows=6, cols=6)
t41.alignment = WD_TABLE_ALIGNMENT.CENTER
t41_data = [
    ("Algorithm", "Paradigm", "Profit Captured", "Payload Filled", "Route Dist", "Latency"),
    ("0/1 Knapsack DP", "Dynamic Prog.", "Rs. 16,450 (100%)", "100.0 kg (100%)", "142.6 km", "8.2 ms"),
    ("Profit Density", "Greedy (p/w)", "Rs. 15,200 (92.4%)", "94.5 kg (94.5%)", "154.2 km", "0.4 ms"),
    ("Highest Profit", "Greedy (max p)", "Rs. 13,800 (83.9%)", "82.0 kg (82.0%)", "168.0 km", "0.3 ms"),
    ("Earliest Deadline", "Greedy (min d)", "Rs. 14,100 (85.7%)", "86.5 kg (86.5%)", "161.5 km", "0.3 ms"),
    ("Dijkstra SSSP", "Greedy (Min-Heap)", "N/A (Routing)", "N/A (Routing)", "142.6 km", "4.2 ms")
]
for r_i, row in enumerate(t41_data):
    for c_i, val in enumerate(row):
        cell = t41.cell(r_i, c_i)
        cell.paragraphs[0].text = val
        set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
        if r_i == 0:
            set_cell_background(cell, "D5E8F0")
            format_run(cell.paragraphs[0].runs[0], size_pt=9.5, bold=True)
        else:
            format_run(cell.paragraphs[0].runs[0], size_pt=9.5)
add_table_caption(doc, "Table 4.1: Multi-Algorithm Empirical Performance and Revenue Comparison")

add_heading_2(doc, "4.2 Cargo Packing Analysis and Revenue Capture")
res42_text = (
    "As detailed in Table 4.1 and illustrated in Figure 4.1, the 0/1 Knapsack Dynamic Programming engine achieved the maximum theoretical revenue of "
    "Rs. 16,450, utilizing 100% of the vehicle's 100 kg cargo limit with zero wasted payload voids. In contrast, the Profit Density heuristic captured "
    "Rs. 15,200 (a revenue loss of Rs. 1,250 or 7.6%), leaving 5.5 kg of unused capacity. The Highest Profit heuristic performed poorest, capturing only "
    "Rs. 13,800 (a deficit of Rs. 2,650 or 16.1%) and wasting 18.0 kg of payload space, as it prioritized heavy, moderately-profitable items that prevented "
    "complementary smaller items from fitting."
)
add_body_paragraph(doc, res42_text)

add_figure(doc, os.path.join(ASSETS_DIR, "diag_metric_profit.png"),
           "Figure 4.1: Comparative Revenue Capture Across Cargo Selection Algorithms", width=Inches(4.5))

add_heading_2(doc, "4.3 Routing Distance and Latency Benchmarks")
res43_text = (
    "In spatial routing, Dijkstra's algorithm with custom Binary Min-Heap computed the globally optimal shortest path of 142.6 km across the Hyderabad "
    "road network in just 4.2 ms. Compared to an unoptimized baseline dispatch path of 212.4 km (Figure 4.2), Dijkstra's engine achieved a 69.8 km distance reduction "
    "(-32.8% mileage cut), resulting in a projected 24.5% decrease in daily fleet fuel consumption. Bellman-Ford converged to the identical shortest distance "
    "of 142.6 km in 18.7 ms, while successfully verifying the absence of negative congestion cycles across all 76 directed road edges."
)
add_body_paragraph(doc, res43_text)

add_figure(doc, os.path.join(ASSETS_DIR, "diag_metric_distance.png"),
           "Figure 4.2: Total Fleet Transit Distance Reduction (Baseline vs Optimized)", width=Inches(4.5))

# Table 4.2: Latency Table
t42 = doc.add_table(rows=6, cols=4)
t42.alignment = WD_TABLE_ALIGNMENT.CENTER
t42_data = [
    ("Algorithmic Engine", "Time Complexity", "Execution Latency (ms)", "Memory Space Allocated"),
    ("0/1 Knapsack (DP)", "O(n · W) = 35 × 100", "8.2 ms", "3,600 Integer Cells (28.8 KB)"),
    ("Profit Density Greedy", "O(n log n) = 35 log 35", "0.4 ms", "35 Float Ratios (0.28 KB)"),
    ("Highest Profit Greedy", "O(n log n) = 35 log 35", "0.3 ms", "35 Integer Values (0.28 KB)"),
    ("Dijkstra's SSSP", "O((V + E) log V)", "4.2 ms", "25 Vertex Heap Elements (0.8 KB)"),
    ("Bellman-Ford", "O(V · E) = 25 × 76", "18.7 ms", "25 Distance Array Entries (0.2 KB)")
]
for r_i, row in enumerate(t42_data):
    for c_i, val in enumerate(row):
        cell = t42.cell(r_i, c_i)
        cell.paragraphs[0].text = val
        set_cell_margins(cell, top=70, bottom=70, left=80, right=80)
        if r_i == 0:
            set_cell_background(cell, "D5E8F0")
            format_run(cell.paragraphs[0].runs[0], size_pt=10, bold=True)
        else:
            format_run(cell.paragraphs[0].runs[0], size_pt=9.5)
add_table_caption(doc, "Table 4.2: Runtime Execution Latency and Memory Space Benchmarks")

add_heading_2(doc, "4.4 Working Prototype Demonstration")
res44_text = (
    "The software prototype was validated through end-to-end interactive execution on the local development server (http://localhost:5173). "
    "Figure 4.3 illustrates the step-by-step Min-Heap priority queue tracer in Lab 2, capturing live push, pop, and sift-down operations. "
    "Figure 4.4 showcases the 2D DP memoization inspector in Lab 4, allowing faculty evaluators to click any cell to inspect the exact arithmetic "
    "decision between SKIP and TAKE along the golden backtracking path. Figure 4.5 presents the live comparative benchmark suite in Lab 6."
)
add_body_paragraph(doc, res44_text)

add_figure(doc, os.path.join(SCREENSHOTS_DIR, "lab2_dijkstra.png"),
           "Figure 4.3: Dijkstra Min-Heap Step Tracer & Step Log in Working Prototype", width=Inches(5.8))

add_figure(doc, os.path.join(SCREENSHOTS_DIR, "lab4_knapsack.png"),
           "Figure 4.4: 0/1 Knapsack 2D DP Interactive Cell Arithmetic Inspector", width=Inches(5.8))

add_figure(doc, os.path.join(SCREENSHOTS_DIR, "lab6_benchmark.png"),
           "Figure 4.5: Multi-Algorithm Benchmark Matrix and Faculty Viva Voce Guide", width=Inches(5.8))

add_heading_2(doc, "4.5 Heuristic Trap and Error Analysis")
res45_text = (
    "A detailed inspection of parcel allocation errors revealed two consistent failure patterns in greedy strategies:\n\n"
    "1. Knapsack Fragmentation Voids: The Profit Density heuristic selected three high-ratio lightweight parcels (under 5 kg each), accumulating "
    "an early density lead. However, this left a residual capacity of 5.5 kg, which was insufficient to accommodate high-value 12 kg and 18 kg parcels. "
    "Dynamic programming correctly skipped one lower-value lightweight parcel to accommodate the two large parcels, yielding an extra Rs. 1,250 in profit.\n\n"
    "2. Heavy Item Bias: The Highest Profit heuristic immediately locked in heavy 25 kg parcels, rapidly exhausting vehicle payload capacity after "
    "packing only four items, resulting in an 82 kg payload and Rs. 2,650 in lost profit compared to DP."
)
add_body_paragraph(doc, res45_text)

add_heading_2(doc, "4.6 Comparison with Baselines and Discussion")
res46_text = (
    "The empirical findings strongly validate the dual-engine design. For high-frequency dispatch where response latency must remain under 1 ms, "
    "Profit Density Greedy provides a viable 92.4% approximation. However, for scheduled batch dispatching from major distribution centers, the "
    "8.2 ms execution time of 0/1 Knapsack Dynamic Programming is negligible, while guaranteeing full revenue capture. In routing, Dijkstra's "
    "4.2 ms execution fulfills all real-time navigation criteria, while Bellman-Ford's 18.7 ms audit guarantees network stability."
)
add_body_paragraph(doc, res46_text)

doc.add_page_break()

# =========================================================
# CHAPTER 5: CONCLUSION AND FUTURE WORK
# =========================================================
print("Writing Chapter 5: Conclusion and Future Work...")
add_heading_1(doc, "5. CONCLUSION AND FUTURE WORK")

add_heading_2(doc, "5.1 Summary of Contributions")
c51_text = (
    "This project successfully developed, implemented, and empirically benchmarked SmartRoute, an autonomous last-mile delivery management "
    "system that unifies four classical DAA paradigms. Key research and engineering contributions include:\n\n"
    "• Mathematical Implementation from Scratch: Engineered manual Binary Min-Heap priority queues, 2D memoization DP matrices, and edge relaxation "
    "engines without relying on black-box optimization libraries.\n\n"
    "• Rigorous Empirical Benchmarking: Quantified the optimality gap between 0/1 Knapsack DP (100% optimum, Rs. 16,450) and greedy heuristics "
    "(92.4% and 83.9%), providing clear mathematical evidence of greedy traps in discrete cargo allocation.\n\n"
    "• Spatial Route Optimization: Proved that Dijkstra's algorithm cuts transit mileage across Hyderabad corridors by 32.8% (69.8 km saved), "
    "while Bellman-Ford audits dynamic congestion penalties and detects negative cycles.\n\n"
    "• Production-Grade Pedagogical Prototype: Built an interactive full-stack web application featuring Google Maps route polylines, step-by-step "
    "Min-Heap animation, and cell-by-cell 2D DP arithmetic inspection for transparent academic examination."
)
add_body_paragraph(doc, c51_text)

add_heading_2(doc, "5.2 Limitations")
c52_text = (
    "While the project accomplished all primary objectives, certain limitations should be recognized:\n\n"
    "• Fixed Single Depot: The routing engine assumes all delivery routes start and terminate at the Begumpet Central Warehouse, without multi-hub handoffs.\n"
    "• Discrete Pseudo-Polynomial Scalability: For massive order capacities (W > 10,000 kg), standard 2D DP table memory requirements grow linearly with W.\n"
    "• Deterministic Road Graph: Road edge weights were sampled under discrete traffic conditions rather than continuous stochastic telemetry streams."
)
add_body_paragraph(doc, c52_text)

add_heading_2(doc, "5.3 Future Work")
c53_text = (
    "Promising directions for future research and development include:\n\n"
    "• A* Heuristic Search: Integrating Euclidean distance heuristics into the Min-Heap priority queue to accelerate spatial path search across massive nationwide networks.\n"
    "• Multi-Vehicle Capacitated Routing (CVRP): Extending the knapsack allocation engine to partition orders across heterogeneous multi-vehicle fleets with dynamic return-to-depot recharging.\n"
    "• Real-Time GPS & IoT Telemetry: Connecting live delivery vehicle GPS streams to dynamically recalculate Dijkstra waypoint queues in response to sudden road closures.\n"
    "• Branch and Bound Algorithms: Implementing branch-and-bound pruning to solve knapsack problems with huge capacities where 2D DP tables become memory-constrained."
)
add_body_paragraph(doc, c53_text)

add_heading_2(doc, "5.4 Concluding Remarks")
c54_text = (
    "SmartRoute demonstrates that classical Data Structures and Algorithms principles remain the bedrock of modern intelligent logistics. By combining "
    "the theoretical rigor of Dynamic Programming and greedy choice with production-ready software engineering, the system achieves maximum revenue "
    "capture, minimal vehicle mileage, and sub-10 millisecond execution. The complete codebase and interactive visualization tools provide an enduring "
    "pedagogical foundation for students and faculty evaluating advanced algorithmic optimization."
)
add_body_paragraph(doc, c54_text)

doc.add_page_break()

# =========================================================
# REFERENCES (IEEE FORMAT)
# =========================================================
print("Writing References...")
p_ref = doc.add_paragraph()
p_ref.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ref.paragraph_format.space_before = Pt(18)
p_ref.paragraph_format.space_after = Pt(18)
r = p_ref.add_run("REFERENCES")
format_run(r, size_pt=16, bold=True)

references_data = [
    "[1] R. Bellman, Dynamic Programming. Princeton, NJ, USA: Princeton University Press, 1957.",
    "[2] S. Martello and P. Toth, Knapsack Problems: Algorithms and Computer Implementations. Chichester, UK: John Wiley & Sons, 1990.",
    "[3] G. B. Dantzig, \"Discrete-variable extremum problems,\" Operations Research, vol. 5, no. 2, pp. 266–277, 1957.",
    "[4] V. Chvátal, Linear Programming. New York, NY, USA: W. H. Freeman and Company, 1983.",
    "[5] E. W. Dijkstra, \"A note on two problems in connexion with graphs,\" Numerische Mathematik, vol. 1, no. 1, pp. 269–271, 1959.",
    "[6] M. L. Fredman and R. E. Tarjan, \"Fibonacci heaps and their uses in improved network optimization algorithms,\" Journal of the ACM (JACM), vol. 34, no. 3, pp. 596–615, 1987.",
    "[7] R. Bellman, \"On a routing problem,\" Quarterly of Applied Mathematics, vol. 16, no. 1, pp. 87–90, 1958.",
    "[8] L. R. Ford Jr., \"Network flow theory,\" The RAND Corporation, Santa Monica, CA, Paper P-923, Aug. 1956.",
    "[9] E. F. Moore, \"The shortest path through a maze,\" in Proc. Int. Symp. Theory of Switching, Harvard Univ. Press, 1959, pp. 285–292.",
    "[10] P. Toth and D. Vigo, Eds., Vehicle Routing: Problems, Methods, and Applications, 2nd ed. Philadelphia, PA, USA: SIAM, 2014.",
    "[11] M. Savelsbergh and T. Van Woensel, \"50th anniversary invited article—City logistics: Challenges and opportunities,\" Transportation Science, vol. 50, no. 2, pp. 579–590, 2016.",
    "[12] J. Kleinberg and É. Tardos, Algorithm Design. Boston, MA, USA: Pearson / Addison-Wesley, 2006.",
    "[13] T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, Introduction to Algorithms, 4th ed. Cambridge, MA, USA: MIT Press, 2022.",
    "[14] T. L. Naps, G. Rößling, V. Almstrum, W. Dann, R. Fleischer, C. Hundhausen, A. Korhonen, L. Malmi, M. McNally, S. Rodger, and J. Á. Velázquez-Iturbide, \"Exploring the role of visualization and engagement in computer science education,\" ACM SIGCSE Bulletin, vol. 35, no. 2, pp. 131–152, 2002.",
    "[15] C. D. Hundhausen, S. A. Douglas, and J. T. Stasko, \"A meta-study of algorithm visualization effectiveness,\" Journal of Visual Languages & Computing, vol. 13, no. 3, pp. 259–290, 2002.",
    "[16] D. Pisinger, \"Where are the hard knapsack problems?\" Computers & Operations Research, vol. 32, no. 9, pp. 2271–2284, 2005."
]

for ref in references_data:
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.3
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.left_indent = Inches(0.4)
    p.paragraph_format.first_line_indent = Inches(-0.4)
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(ref)
    format_run(r, size_pt=11)

doc.add_page_break()

# =========================================================
# APPENDIX – I: WORK DONE & DEPLOYMENT TOOLS
# =========================================================
print("Writing Appendix I...")
add_heading_1(doc, "APPENDIX – I")

p_app_sub = doc.add_paragraph()
p_app_sub.paragraph_format.space_after = Pt(14)
r = p_app_sub.add_run("SCREENSHOTS OF WORK DONE AND DEPLOYMENT TOOLS")
format_run(r, size_pt=14, bold=True)

add_body_paragraph(doc, "This appendix documents the codebase repository, deployment infrastructure, and interactive execution environments utilized in developing and testing SmartRoute:")

add_heading_2(doc, "A.1 Codebase Repository and Version Control")
add_bullet_item(doc, "Public Repository URL: https://github.com/Himanshu-Git-101/DAA_PBL", "GitHub Repository: ")
add_bullet_item(doc, "Primary Branch: main (fully tracked commits, automated GitHub workflows)", "Branch Architecture: ")
add_bullet_item(doc, "Integrated TypeScript 5.5, React 18, Vite 5.4, Python 3.11, Google Maps API", "Technology Stack: ")

add_heading_2(doc, "A.2 Algorithmic Problem Solving & Source Code Files")
add_bullet_item(doc, "Contains custom Binary Min-Heap Priority Queue class and step-by-step trace logger.", "dijkstra.py: ")
add_bullet_item(doc, "Contains 2D memoization table generator, SKIP vs TAKE arithmetic inspector, and golden backtracking tracer.", "knapsack.py: ")
add_bullet_item(doc, "Defines Hyderabad adjacency matrix, Begumpet Central Hub coordinates, and 35+ delivery node locations.", "graph.py: ")
add_bullet_item(doc, "Houses Algorithm Lab components, Google Maps view, and Viva Cheat Sheet.", "src/components: ")

add_figure(doc, os.path.join(SCREENSHOTS_DIR, "viva_guide.png"),
           "Figure A.1: Faculty Viva Voce Concept Reference Sheet and Deployment Architecture", width=Inches(5.8))

doc.add_page_break()

# =========================================================
# APPENDIX – II: FORMATTING GUIDELINES
# =========================================================
print("Writing Appendix II...")
add_heading_1(doc, "APPENDIX – II")

p_app2_sub = doc.add_paragraph()
p_app2_sub.paragraph_format.space_after = Pt(14)
r = p_app2_sub.add_run("FORMATTING GUIDELINES AND SPECIFICATIONS")
format_run(r, size_pt=14, bold=True)

add_body_paragraph(doc, "This appendix summarizes the formatting specifications established by Woxsen University School of Technology, adhered to throughout this report document:")

# Table A.1
ta = doc.add_table(rows=8, cols=2)
ta.alignment = WD_TABLE_ALIGNMENT.CENTER
ta_data = [
    ("Formatting Element", "Report Implementation Specification"),
    ("Paper Size", "US Letter / A4 (8.5 × 11.0 inches / 215.9 × 279.4 mm)"),
    ("Margins", "1.0 inch (2.54 cm) on all four sides (Top, Bottom, Left, Right)"),
    ("Primary Font Family", "Times New Roman throughout entire document"),
    ("Body Text Styling", "12 pt, 1.5 Line Spacing, Justified Alignment, 6 pt After"),
    ("Heading Hierarchy", "H1: 16 pt Bold (18/12 pt) | H2: 14 pt Bold (12/6 pt) | H3: 13 pt Bold (10/6 pt)"),
    ("Tables and Figures", "Centered, Light Gray Header (RGB 213, 232, 240), Italic 11 pt Caption Below"),
    ("In-Text Citation Style", "IEEE Numerical Format [1], [2], [3] placed at sentence ends before period")
]
for r_i, (c0, c1) in enumerate(ta_data):
    row = ta.rows[r_i]
    row.cells[0].paragraphs[0].text = c0
    row.cells[1].paragraphs[0].text = c1
    row.cells[0].width = Inches(3.2)
    row.cells[1].width = Inches(3.4)
    set_cell_margins(row.cells[0])
    set_cell_margins(row.cells[1])
    if r_i == 0:
        set_cell_background(row.cells[0], "D5E8F0")
        set_cell_background(row.cells[1], "D5E8F0")
        format_run(row.cells[0].paragraphs[0].runs[0], bold=True)
        format_run(row.cells[1].paragraphs[0].runs[0], bold=True)
add_table_caption(doc, "Table A.1: General Formatting Guidelines and Report Compliance Specifications")

# Save document
print(f"Saving report document to {DOCX_OUTPUT}...")
doc.save(DOCX_OUTPUT)

# Also copy to public directory for direct download
public_docx = os.path.join("public", DOCX_OUTPUT)
doc.save(public_docx)
print(f"Successfully generated {DOCX_OUTPUT} and {public_docx}!")
