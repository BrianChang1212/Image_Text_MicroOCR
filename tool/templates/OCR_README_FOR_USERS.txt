Image Text OCR — Windows bundle (user guide)
==============================================

English (primary)
-----------------

No Python on the target PC. Do not move verify_image_text.exe away from _internal\.

Folder layout
-------------
  verify_image_text.exe, _internal\  — application (bundle root)
  README.txt                         — short index
  config\                            — sample JSON for --extract-config
  doc\                               — this file
  scripts\                           — .cmd / .bat / .ps1 helpers

Run from bundle root (the folder that contains verify_image_text.exe)
----------------------------------------------------------------------
  scripts\ocr_plain.bat "C:\path\to\image.png"
  scripts\run_ocr.bat "C:\path\to\image.png" --dump-json
  scripts\extract_tr7.cmd "C:\path\to\screenshot.png"
  scripts\extract_with_config.cmd config\extract_config.example.json "C:\path\to\image.png"

Or from the same folder:
  verify_image_text.exe -p "C:\path\to\image.png"
  verify_image_text.exe "C:\path\to\image.png" --extract tr7-monitor

Relative paths are resolved from the bundle root (e.g. image.png next to the exe).

Exit codes
----------
  0 — Success (OCR ran; verification or extract rules passed as applicable)
  1 — Verification failed, or extract could not read required fields
  2 — Bad install (e.g. missing runtime files); reinstall the full folder

Scripting: structured JSON from --extract / --extract-config is printed to stdout.
RapidOCR INFO logs go to stderr — redirect or discard stderr when parsing JSON.

Tips: Quote paths that contain spaces. In PowerShell run .\verify_image_text.exe from the bundle root.
First run may be slow if antivirus scans the folder.

================================================================================
Traditional Chinese — supplement (繁體中文補充)
================================================================================

重點
----
  目標電腦不需安裝 Python。請勿把 verify_image_text.exe 與 _internal\ 分開。

目錄
----
  verify_image_text.exe、_internal\  主程式（套件根目錄）
  README.txt                         簡短索引
  config\                            --extract-config 用 JSON 範例
  doc\                               本說明檔
  scripts\                           捷徑：.cmd / .bat / .ps1

使用方式（在含 exe 的資料夾開 cmd）
----------------------------------
  scripts\ocr_plain.bat "圖片路徑"
  scripts\run_ocr.bat "圖片路徑" --dump-json
  scripts\extract_tr7.cmd "截圖路徑"
  scripts\extract_with_config.cmd config\extract_config.example.json "圖片路徑"
  verify_image_text.exe -p "圖片路徑"
  verify_image_text.exe "圖片路徑" --extract tr7-monitor

相對路徑以套件根目錄為準。

結束碼
------
  0 成功（OCR 執行完成；驗證或擷取規則通過）
  1 驗證失敗，或擷取欄位未滿足必填
  2 安裝不完整（缺執行檔案）；請重新解壓整包

若使用 --extract / --extract-config，結構化 JSON 在 stdout；RapidOCR 的 INFO 在 stderr，
串接程式時請只解析 stdout 或將 stderr 導掉。

路徑含空白請加引號。PowerShell 請在套件根執行 .\verify_image_text.exe。
防毒首次掃描可能讓啟動變慢。
