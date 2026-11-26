import os
import re
import subprocess
import sys

import markdown_it


def format_math_blocks(text: str) -> str:
    """Convert markdown math callouts into clean styled HTML callout cards."""
    return re.sub(
        r'> \*\*(Softmax|Hallucination Risk|Math):\*\* `([^`]+)`',
        r'<div class="math-card"><strong>\1:</strong> <code>\2</code></div>',
        text,
    )


def generate_academic_pdf() -> None:
    workspace = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.join(workspace, "TRUTHLENS_AI_PROJECT_REPORT.md")
    html_path = os.path.join(workspace, "TRUTHLENS_AI_PROJECT_REPORT.html")
    pdf_path = os.path.join(workspace, "TRUTHLENS_AI_PROJECT_REPORT.pdf")

    if not os.path.exists(md_path):
        print(f"Error: {md_path} not found!")
        sys.exit(1)

    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    processed_md = format_math_blocks(md_content)
    md = markdown_it.MarkdownIt().enable("table")
    raw_html = md.render(processed_md)

    # Clean section page breaks matching the reference academic layout
    page_break_headers = [
        "Declaration",
        "Chapter 1: Introduction",
        "Chapter 2: Literature Survey",
        "Chapter 3: System Design",
        "Chapter 4: Implementation",
        "Chapter 5: Tools and Technologies Required",
        "Chapter 6: Software Requirements Specification (SRS)",
        "Chapter 7: Results and Discussion",
        "Chapter 8: Conclusion and Future Scope",
    ]

    for header in page_break_headers:
        for tag in ("h1", "h2"):
            pattern = re.compile(rf'(<{tag}>\s*{re.escape(header)}\s*</{tag}>)', re.IGNORECASE)
            raw_html = pattern.sub(r'<div class="page-break"></div>\1', raw_html)

    # Style figure captions italicized below diagrams/tables cleanly
    raw_html = re.sub(
        r'<p><em>((?:Figure|Table) [^<]+)</em></p>',
        r'<p class="caption">\1</p>',
        raw_html,
    )

    academic_css = """
    <style>
        @page {
            size: A4 portrait;
            margin: 19mm 17mm 19mm 17mm;
            @top-left {
                content: "TruthLens AI: Hallucination Detection in LLM-Generated Answers Using Semantic Entailment Scoring";
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 7.5pt;
                color: #64748b;
            }
            @bottom-right {
                content: "Page " counter(page) " of " counter(pages);
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 8pt;
                color: #64748b;
            }
        }

        @page :first {
            @top-left {
                content: none;
            }
        }

        body {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Arial, sans-serif;
            color: #1f2937;
            background-color: #ffffff;
            line-height: 1.56;
            font-size: 10pt;
            margin: 0;
            padding: 0;
        }

        .page-break {
            page-break-before: always;
            break-before: page;
        }

        h1 {
            font-family: Georgia, 'Times New Roman', serif;
            color: #111827;
            font-size: 18pt;
            font-weight: 700;
            line-height: 1.25;
            margin-top: 8pt;
            margin-bottom: 10pt;
            page-break-after: avoid;
        }

        body > h1:first-of-type {
            font-size: 21pt;
            margin-top: 0;
            margin-bottom: 10pt;
        }

        h2 {
            font-family: Georgia, 'Times New Roman', serif;
            color: #111827;
            font-size: 12.5pt;
            font-weight: 700;
            margin-top: 14pt;
            margin-bottom: 6pt;
            page-break-after: avoid;
        }

        h3 {
            color: #1f2937;
            font-size: 10.5pt;
            font-weight: 700;
            margin-top: 10pt;
            margin-bottom: 4pt;
            page-break-after: avoid;
        }

        p {
            margin-top: 0;
            margin-bottom: 7pt;
            text-align: left;
        }

        ul, ol {
            margin-top: 4pt;
            margin-bottom: 8pt;
            padding-left: 18pt;
        }

        li {
            margin-bottom: 3pt;
        }

        .caption {
            font-style: italic;
            font-size: 9pt;
            color: #374151;
            margin-top: 4pt;
            margin-bottom: 10pt;
        }

        .math-card {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-left: 3px solid #64748b;
            padding: 7pt 10pt;
            margin: 8pt 0;
            font-size: 9.5pt;
            color: #0f172a;
            border-radius: 3pt;
            page-break-inside: avoid;
        }

        .math-card code {
            background: transparent;
            color: #0f172a;
            font-size: 9.5pt;
            padding: 0;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10pt 0;
            font-size: 8.8pt;
            page-break-inside: avoid;
        }

        th {
            background-color: #f1f5f9;
            color: #111827;
            font-weight: 600;
            text-align: left;
            padding: 6pt 8pt;
            border: 1px solid #cbd5e1;
        }

        td {
            padding: 5.5pt 8pt;
            border: 1px solid #cbd5e1;
            vertical-align: top;
        }

        pre {
            background-color: #f8fafc;
            color: #111827;
            padding: 9pt 11pt;
            border-radius: 4pt;
            border: 1px solid #e2e8f0;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 8pt;
            line-height: 1.42;
            margin: 8pt 0;
            page-break-inside: avoid;
            white-space: pre-wrap;
        }

        code {
            font-family: 'Consolas', 'Courier New', monospace;
            background-color: #f1f5f9;
            color: #0f172a;
            padding: 1pt 3pt;
            border-radius: 2pt;
            font-size: 8.8pt;
        }

        pre code {
            background-color: transparent;
            color: inherit;
            padding: 0;
            font-size: inherit;
        }

        hr {
            border: 0;
            height: 1px;
            background: #cbd5e1;
            margin: 12pt 0;
        }
    </style>
    """

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>TruthLens AI - Individual Project Report</title>
    {academic_css}
</head>
<body>
    {raw_html}
</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    ]
    browser_bin = next((p for p in edge_paths if os.path.exists(p)), None)
    if not browser_bin:
        print("Error: No Chromium/Edge browser found for PDF generation.")
        sys.exit(1)

    cmd = [
        browser_bin,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        print(f"PDF renderer failed ({result.returncode}): {result.stderr}")
        sys.exit(result.returncode)

    if os.path.exists(pdf_path):
        size_kb = os.path.getsize(pdf_path) / 1024
        print(f"Generated {pdf_path} ({size_kb:.1f} KB)")
    else:
        print("Error: PDF output file was not created.")
        sys.exit(1)


if __name__ == "__main__":
    generate_academic_pdf()
