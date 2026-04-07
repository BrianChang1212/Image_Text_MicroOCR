Image Text OCR — Windows bundle (detail)
==========================================

No Python. Do not separate verify_image_text.exe from _internal\.

Folder layout
-------------
  verify_image_text.exe, _internal\  — main program (bundle root)
  README.txt                         — short index
  config\                            — sample JSON for --extract-config
  doc\                               — this file
  scripts\                           — .cmd / .bat / .ps1 helpers

Run from bundle root (folder that contains verify_image_text.exe)
------------------------------------------------------------------
  scripts\ocr_plain.bat "C:\path\to\image.png"
  scripts\run_ocr.bat "C:\path\to\image.png" --dump-json
  scripts\extract_tr7.cmd "C:\path\to\screenshot.png"
  scripts\extract_with_config.cmd config\extract_config.example.json "C:\path\to\image.png"

Or cd to bundle root and call exe directly:
  verify_image_text.exe -p "C:\path\to\image.png"

Paths in the helpers above may be relative to the bundle root (e.g. demo.png next to .exe).

Exit codes: 0 ok, 1 verify/extract failed, 2 bad install.

Notes: quote paths with spaces. In PowerShell use .\verify_image_text.exe from bundle root.
First run may be slow if antivirus scans the folder.
