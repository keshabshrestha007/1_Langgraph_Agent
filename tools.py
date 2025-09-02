import os
from langchain.tools import tool
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

from langchain_community.tools import DuckDuckGoSearchRun

DUCK_REGION = os.getenv("DUCK_REGION", "us")
DUCK_SAFESEARCH = os.getenv("DUCK_SAFESEARCH", "Moderate")
DUCK_TIME_RANGE = os.getenv("DUCK_TIME_RANGE", "y")

search_tool = DuckDuckGoSearchRun(region=DUCK_REGION, safesearch=DUCK_SAFESEARCH, time_range=DUCK_TIME_RANGE)
search_tool.name = "duckduckgo_search"

@tool
def write_to_file(filename: str, content: str) -> str:
    """Writes given content to a file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return f"✅ Content written to {filename}"

@tool
def read_file(filename: str) -> str:
    """Reads content from a file."""
    if not os.path.exists(filename):
        return "❌ File does not exist."
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()
@tool
def append_to_file(filename: str, content: str) -> str:
    """Appends given content to a file. Creates the file if it does not exist."""
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(content + "\n")
        return f"✅ Content appended to {filename}"
    except Exception as e:
        return f"❌ Failed to append: {str(e)}"

@tool
def read_pdf(filename: str) -> str:
    """Extracts text from a PDF file."""
    if not os.path.exists(filename):
        return "❌ PDF not found"
    reader = PdfReader(filename)
    text = ""
    for page in reader.pages:
        
        extracted = page.extract_text() or ""
        text += extracted + "\\n"
    return text.strip()

@tool
def write_pdf(filename: str, text: str) -> str:
    """Creates a simple PDF with given text."""
    writer = PdfWriter()

    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
  
    c.drawString(72, 750, text[:2000])  
    c.save()

    packet.seek(0)
    new_pdf = PdfReader(packet)
    writer.add_page(new_pdf.pages[0])

    with open(filename, "wb") as f:
        writer.write(f)
    return f"✅ PDF created: {filename}"

@tool
def search_arxiv(query: str, max_results: int = 3) -> str:
    """Searches Arxiv for research papers and returns top results with title, authors, and link."""
    try:
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )

        results = []
        for result in search.results():
            paper_info = f"📄 {result.title}\n👨‍🔬 Authors: {', '.join(a.name for a in result.authors)}\n🔗 {result.entry_id}\n"
            results.append(paper_info)

        if not results:
            return "❌ No papers found."

        return "\n".join(results)

    except Exception as e:
        return f"❌ Arxiv search failed: {str(e)}"
