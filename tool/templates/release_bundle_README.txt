Image Text OCR — Windows release bundle
========================================

Layout
------
  verify_image_text.exe + _internal/   Main program (do not separate from exe)
  README.txt                         This file (English primary; Chinese supplement below)
  config/                            Sample JSON for --extract-config (edit copies)
  doc/                               Detailed user notes (OCR_README_FOR_USERS.txt)
  scripts/                           Shortcuts: .cmd / .bat / .ps1

Quick start (open cmd in this folder — the bundle root)
---------------------------------------------------------
  scripts\ocr_plain.bat "D:\picture.png"
  scripts\run_ocr.bat "D:\picture.png" --dump-json
  scripts\extract_tr7.cmd "D:\screenshot.png"
  scripts\extract_with_config.cmd config\extract_config.example.json "D:\picture.png"
  verify_image_text.exe "D:\picture.png" --extract tr7-monitor

You may pass any CLI flags to verify_image_text.exe or scripts\run_ocr.bat. See doc\ for more.

================================================================================
Traditional Chinese — supplement (繁體中文補充)
================================================================================

目錄說明
--------
  verify_image_text.exe 與 _internal\ 為主程式，請勿拆開。
  README.txt           本檔（英文為主，本段為補充）。
  config\              擷取規則 JSON 範例，請複製後自訂。
  doc\                 較完整說明（OCR_README_FOR_USERS.txt）。
  scripts\             捷徑：.cmd / .bat / .ps1。

快速指令（請在「含 exe 的那個資料夾」開 cmd）
--------------------------------------------
  scripts\ocr_plain.bat "圖片路徑"
  scripts\run_ocr.bat "圖片路徑" --dump-json
  scripts\extract_tr7.cmd "截圖路徑"
  scripts\extract_with_config.cmd config\extract_config.example.json "圖片路徑"
  verify_image_text.exe "圖片路徑" --extract tr7-monitor

詳見 doc\OCR_README_FOR_USERS.txt。
