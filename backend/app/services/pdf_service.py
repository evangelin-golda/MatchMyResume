import io
import pymupdf
from fastapi import HTTPException

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extracts structured text from raw PDF bytes in-memory using PyMuPDF.
    Ensures zero permanent file storage on disk.
    """
    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="Empty PDF file uploaded.")
    
    try:
        # Open PDF from in-memory stream
        doc = pymupdf.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid or corrupted PDF file. Please upload a standard text PDF: {str(e)}"
        )
    
    if len(doc) == 0:
        doc.close()
        raise HTTPException(status_code=400, detail="The uploaded PDF contains no pages.")
    
    extracted_text_chunks = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        if text:
            extracted_text_chunks.append(text)
            
    doc.close()
    
    full_text = "\n".join(extracted_text_chunks).strip()
    
    # Check if PDF contains selectable text (not a scanned image)
    if len(full_text) < 50:
        raise HTTPException(
            status_code=400,
            detail="The uploaded PDF appears to be a scanned image or empty. Please upload a text-selectable PDF."
        )
        
    return full_text
