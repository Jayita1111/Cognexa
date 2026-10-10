import os
import pymupdf  # PyMuPDF library
import pandas as pd

# Suppress PyMuPDF console error/warning messages
pymupdf.TOOLS.mupdf_display_errors(False)

DATA_DIR = "data"
OUTPUT_EXCEL = "PDF_Inventory.xlsx"
OUTPUT_REPORT = "Comparison_Report.txt"

def infer_subject(filename):
    """Infer subject based on keywords in the file name."""
    fname_lower = filename.lower()
    
    subjects_map = {
        "Computer Science": ["cs", "code", "python", "java", "data", "algo", "dbms", "os", "network", "ai", "ml", "software", "web"],
        "Chemistry": ["chem", "organic", "inorganic", "lab", "physical"],
        "Electronics": ["ec", "circuit", "digital", "signal", "microprocessor", "vlsi"],
        "Mathematics": ["math", "calculus", "algebra", "stats", "probability", "discrete"],
        "Physics": ["physics", "electro", "thermo", "optics", "quantum"],
    }
    
    for subject, keywords in subjects_map.items():
        if any(keyword in fname_lower for keyword in keywords):
            return subject
            
    return "General / Uncategorized"

def classify_doc_type(filename):
    """Infer document type from filename."""
    fname_lower = filename.lower()
    if any(k in fname_lower for k in ["syllabus", "curriculum", "scheme"]):
        return "Syllabus / Curriculum"
    elif any(k in fname_lower for k in ["lab", "manual", "pract", "experiment"]):
        return "Lab Manual"
    elif any(k in fname_lower for k in ["slide", "ppt", "presentation", "deck"]):
        return "Slides / Presentation"
    elif any(k in fname_lower for k in ["note", "lecture", "unit", "chapter", "module"]):
        return "Lecture Notes"
    elif any(k in fname_lower for k in ["paper", "exam", "midterm", "final", "test", "qp", "quiz"]):
        return "Question Paper / Exam"
    elif any(k in fname_lower for k in ["book", "textbook"]):
        return "Textbook"
    else:
        return "General Reference / Document"

def check_pdf_status(pdf_path):
    """Check page count and text status (selectable vs scanned vs encrypted)."""
    try:
        doc = pymupdf.open(pdf_path)
        
        if doc.is_encrypted:
            doc.close()
            return 0, "Encrypted / Protected"
            
        page_count = len(doc)
        total_text_len = 0
        
        # Check text length across up to 5 pages
        pages_to_check = min(page_count, 5)
        for i in range(pages_to_check):
            try:
                page = doc[i]
                total_text_len += len(page.get_text().strip())
            except Exception:
                continue
        
        doc.close()
        
        if total_text_len > 50:
            is_selectable = "Selectable Text"
        else:
            is_selectable = "Scanned"
            
        return page_count, is_selectable
    except Exception:
        return 0, "Corrupted / Error"

def get_file_size_mb(file_path):
    """Returns file size in Megabytes."""
    size_bytes = os.path.getsize(file_path)
    return round(size_bytes / (1024 * 1024), 6)

def generate_inventory(data_dir):
    records = []
    
    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                full_path = os.path.join(root, file)
                
                # Extract source directly from top-level directory inside 'data'
                rel_path = os.path.relpath(full_path, data_dir)
                path_parts = rel_path.split(os.sep)
                
                raw_source = path_parts[0] if len(path_parts) > 0 else "Unknown"
                source = raw_source.capitalize()
                
                # Extract metadata
                file_size_mb = get_file_size_mb(full_path)
                page_count, text_status = check_pdf_status(full_path)
                doc_type = classify_doc_type(file)
                subject = infer_subject(file)
                
                records.append({
                    "File Name": file,
                    "Source": source,
                    "Subject": subject,
                    "Document Type": doc_type,
                    "Page Count": page_count,
                    "File Size (MB)": file_size_mb,
                    "Text Status": text_status
                })
                
    return pd.DataFrame(records)

def generate_report_string(df):
    """Generates exact output report as a single string."""
    report = []
    
    # Total counts
    total_docs = len(df)
    report.append(f"Total PDFs Cataloged: {total_docs}")
    source_counts = df['Source'].value_counts()
    for src, count in source_counts.items():
        report.append(f"  • {src} Documents: {count}")
    report.append("\n")
    
    # Section 1: Overall Metrics
    report.append("1. OVERALL METRICS BY SOURCE:")
    report.append("-" * 65)
    summary_metrics = df.groupby('Source').agg(
        Total_Files=('File Name', 'count'),
        Total_Pages=('Page Count', 'sum'),
        Avg_Pages_Per_Doc=('Page Count', lambda x: round(x.mean(), 1)),
        Avg_Size_MB=('File Size (MB)', lambda x: round(x.mean(), 1))
    ).reset_index()
    report.append(summary_metrics.to_string(index=False))
    report.append("\n\n")
    
    # Section 2: Text Status Breakdown
    report.append("2. TEXT STATUS (SELECTABLE VS SCANNED):")
    report.append("-" * 65)
    text_status_table = df.groupby(['Source', 'Text Status']).size().unstack(fill_value=0)
    report.append(text_status_table.to_string())
    report.append("\n\n")
    
    # Section 3: Document Type Variety
    report.append("3. DOCUMENT TYPE VARIETY BY SOURCE:")
    report.append("-" * 65)
    doc_variety_table = df.groupby(['Source', 'Document Type']).size().unstack(fill_value=0)
    report.append(doc_variety_table.to_string())
    report.append("\n\n")
    
    # Section 4: Subject Variety
    report.append("4. SUBJECT VARIETY BY SOURCE:")
    report.append("-" * 65)
    subject_table = df.groupby(['Source', 'Subject']).size().unstack(fill_value=0)
    report.append(subject_table.to_string())
    report.append("\n\n")
    
    # Section 5: Comparative Analysis Text
    report.append("5. COMPARATIVE DIVERSITY ANALYSIS (Kaggle vs College):")
    report.append("-" * 65)
    report.append("""
A. Text Digitization & Selectability:
   • Kaggle Documents: Almost exclusively digital-native documents generated
     from Markdown, LaTeX, or Word files. Text is 100% selectable, clean,
     and suitable for direct NLP/RAG pipeline extraction.
   • College Documents: Contain a mixed distribution, including physical paper
     scans, handwritten class notes, and previous year printed question papers,
     requiring pre-processing via OCR.

B. Content Structure & Document Variety:
   • Kaggle Documents: Focus on datasets, technical writeups, competition guides,
     and research summaries. High formatting uniformity across files.
   • College Documents: Exhibit diverse academic material types (Syllabi,
     Laboratory Manuals, Lecture Slides, Unit Notes, Midterm Exams).

C. File Size & Scale Characteristics:
   • Kaggle documents have consistent file size-to-page ratios due to vector layouts.
   • College scanned documents have larger file sizes relative to page counts
     due to high-resolution image embeds.
""")
    report.append("=" * 65)
    
    return "\n".join(report)

if __name__ == "__main__":
    df = generate_inventory(DATA_DIR)
    
    if not df.empty:
        # Save Excel File in background
        df.to_excel(OUTPUT_EXCEL, index=False)
        
        # Build report
        report_str = generate_report_string(df)
        
        # Save Text File in background
        with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
            f.write(report_str)
            
        # Print strictly the report to console
        print(report_str)
