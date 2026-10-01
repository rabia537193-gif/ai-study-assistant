import os

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
except ImportError:
    os.system("pip install reportlab")
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

def create_pdf(filename, title, content):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, title)
    c.setFont("Helvetica", 12)
    
    y = 710
    for line in content.split("\n"):
        c.drawString(50, y, line)
        y -= 20
    c.save()

chapters = {
    "Chapter1_Introduction.pdf": (
        "Chapter 1: Introduction to Python",
        "Python is a high-level, interpreted programming language.\n"
        "It is easy to learn, highly readable, and widely used in AI, web development, and data science."
    ),
    "Chapter2_Variables.pdf": (
        "Chapter 2: Variables and Data Types",
        "Variables in Python store data values.\n"
        "Common data types include Integer, Float, String, Boolean, List, Tuple, and Dictionary."
    ),
    "Chapter3_Conditionals.pdf": (
        "Chapter 3: Conditional Statements",
        "Conditional statements control program execution flow using if, elif, and else keywords.\n"
        "They allow decision making based on Boolean conditions."
    ),
    "Chapter4_Loops.pdf": (
        "Chapter 4: Loops in Python",
        "Loops repeat code blocks. Python supports for loops and while loops.\n"
        "A for loop iterates over a sequence like a list, tuple, or range."
    ),
    "Chapter5_Functions.pdf": (
        "Chapter 5: Functions in Python",
        "Functions are reusable blocks of code defined using the def keyword.\n"
        "Functions take input arguments and can return output values using the return statement."
    )
}

print("Generating 5 Sample PDFs...")
for fname, (title, text) in chapters.items():
    create_pdf(fname, title, text)
    print(f"Created: {fname}")

print("\nDone! 5 PDFs created successfully in your project folder.")