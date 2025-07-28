#!/usr/bin/env python3
"""
Competition-ready PDF analyzer wrapper for Docker execution.
Processes all PDFs from /app/input and outputs JSON files to /app/output.
"""

import os
import json
import time
import logging
from pdf_analyzer import PDFAnalyzer

def main():
    input_dir = "/app/input" if os.path.exists("/app/input") else "input_pdfs"
    output_dir = "/app/output" if os.path.exists("/app/output") else "."
    os.makedirs(output_dir, exist_ok=True)

    log_level = logging.WARNING if input_dir == "/app/input" else logging.INFO
    logging.basicConfig(level=log_level, format='%(message)s')

    if not os.path.exists(input_dir):
        print(f"Input directory {input_dir} does not exist")
        return

    pdf_files = [f for f in os.listdir(input_dir) if f.endswith('.pdf')]
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return

    print(f"Found {len(pdf_files)} PDF files to process")
    analyzer = PDFAnalyzer()

    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        start_time = time.time()

        print(f"\n{'='*60}")
        print(f"Processing: {pdf_file}")
        print(f"{'='*60}")

        try:
            result = analyzer.pd_analyser(pdf_path)  # <-- FIXED method name
            processing_time = time.time() - start_time

            if result:
                print(f"✓ Completed in {processing_time:.2f}s")
                print(f"Title: {result.get('title', 'N/A')}")
                print(f"Found {len(result.get('outline', []))} headings:")

                for i, heading in enumerate(result.get('outline', []), 1):
                    indent = "  " * (int(heading.get('level', 'L1')[1]) - 1)
                    print(f"  {i:2d}. {indent}{heading['level']}: {heading['text']} (page {heading['page']})")

                output_file = os.path.join(output_dir, f"{os.path.splitext(pdf_file)[0]}.json")
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"\nSaved result to: {output_file}")

            else:
                print("✗ No result returned")

        except Exception as e:
            processing_time = time.time() - start_time
            print(f"✗ Error after {processing_time:.2f}s: {str(e)}")

if __name__ == "__main__":
    main()
