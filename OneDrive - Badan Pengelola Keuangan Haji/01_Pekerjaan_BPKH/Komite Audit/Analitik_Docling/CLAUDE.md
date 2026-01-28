# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Batch document converter that uses IBM's **Docling** library to convert office documents (PDF, DOCX, PPTX, XLSX, etc.) into structured JSON. Used by BPKH (Badan Pengelola Keuangan Haji) Komite Audit for document analytics.

- **Python version:** 3.11
- **Platform:** Windows (developed on Windows 10/11)
- **Language:** Code comments are in Indonesian (Bahasa Indonesia)

## Commands

```bash
# Setup
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

# Run the converter (processes all supported files in CWD, outputs to hasil_konversi/)
python tes_docling.py
```

There is no test suite, linter, or build system.

## Architecture

This is a single-script project: **`tes_docling.py`** is the entire application.

**Conversion flow:**
1. Scans the current working directory for supported files (`.pdf`, `.docx`, `.doc`, `.pptx`, `.ppt`, `.xlsx`, `.xls`)
2. Converts each file using `DocumentConverter` from Docling
3. On failure, retries with table structure pipeline disabled (`do_table_structure=False`) as a fallback
4. Exports results as JSON to `hasil_konversi/` directory

**Key functions:**
- `make_converter(disable_table_structure)` — Creates a `DocumentConverter` with optional PDF table structure bypass
- `safe_convert(converter, file_path)` — Thin wrapper around `converter.convert()`
- `main()` — Batch processing loop with fallback error handling

**Output format:** Docling's `DoclingDocument` schema (v1.8.0) — structured JSON containing `body`, `texts`, `tables`, `pictures`, `pages`, `groups`, `key_value_items`, and `form_items`.

## Dependencies

The `numpy<2` constraint in `requirements.txt` is critical — NumPy 2.x breaks compatibility with scipy/sklearn used by Docling's ML pipeline. Do not remove this constraint.

Docling pulls in heavy ML dependencies (PyTorch, TensorFlow, HuggingFace transformers). Expect high memory usage during conversion.

## Environment Variables

Set automatically in `tes_docling.py`:
- `TF_CPP_MIN_LOG_LEVEL=2` — Suppresses TensorFlow debug/info logs
- `TF_ENABLE_ONEDNN_OPTS=0` — Disables oneDNN optimization logs
