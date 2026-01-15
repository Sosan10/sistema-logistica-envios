#!/usr/bin/env python
# Test script to verify fpdf2 installation

print("Testing fpdf2 installation...")

try:
    from fpdf import FPDF, XPos, YPos 
    print("✅ SUCCESS: All imports worked!")
    print(f"   - FPDF: {FPDF}")
    print(f"   - XPos: {XPos}")
    print(f"   - YPos: {YPos}")
    print(f"   - FPDF_AVAILABLE would be: True")
except ImportError as e:
    print(f"❌ FAILED: ImportError occurred")
    print(f"   - Error: {e}")
    print(f"   - FPDF_AVAILABLE would be: False")
