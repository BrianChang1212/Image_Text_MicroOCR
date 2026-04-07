Image Text OCR — Windows release bundle
========================================

Layout
------
  verify_image_text.exe + _internal/   Main program (do not separate)
  README.txt                         This file
  config/                            Edit JSON extract rules here (sample inside)
  doc/                               Full user notes
  scripts/                           Shortcuts: .cmd / .bat / .ps1

Quick start (open cmd at this folder — the bundle root)
---------------------------------------------------------
  scripts\ocr_plain.bat "D:\picture.png"
  scripts\run_ocr.bat "D:\picture.png" --dump-json
  scripts\extract_tr7.cmd "D:\screenshot.png"
  scripts\extract_with_config.cmd config\extract_config.example.json "D:\picture.png"
  verify_image_text.exe "D:\picture.png" --extract tr7-monitor

You may also run verify_image_text.exe from this folder; see doc\ for options.
