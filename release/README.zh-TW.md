# 發行（Windows 獨立套件）

開發用 repo 內 **`release/`** 目錄的維護與交付說明。

**English:** [README.md](README.md)

本 `release/` 底下放的是 **PyInstaller 建置產物**資料夾 `verify_image_text\`，通常由同步腳本從 `source\dist\` 複製而來，用來交給**未安裝 Python**的 Windows 使用者。

---

## 維護者：如何產出／更新套件

1. **建置並同步（建議）** — 在 repo 內：

   ```powershell
   cd <專案根>\tool
   .\build_pyinstaller_release.ps1 -SyncToRelease
   ```

2. **僅同步** — 若已在 `source\dist\verify_image_text` 建置完成：

   ```powershell
   cd <專案根>\release
   .\sync_from_dev_build.ps1
   ```

   使用 **robocopy /MIR**；不必先手動刪除 `verify_image_text`（可減少「檔案使用中」失敗）。

3. **CLI 有變更**（例如新增 `--extract` 等參數）時務必**重建 exe**；舊的 `verify_image_text.exe` 可能出現 `unrecognized arguments: …`。

4. 若要將整包納入 Git 或以 zip 交付，請先確認 `release\verify_image_text\verify_image_text.exe` 存在。

---

## 交付給「乾淨」／離線的 Windows 電腦

- **請 zip 整個資料夾**：**完整**打包 **`release\verify_image_text\`**。根目錄須含 `verify_image_text.exe`、`_internal\`、`README.txt`，以及 **`scripts\`**、**`config\`**、**`doc\`**。**若缺少 `_internal\`，或只抽出 exe，程式無法執行。**
- **不必交付**：完整 repo 原始碼、Python、venv（除非對方要開發）。
- **其他 64 位元 Windows 10/11** 多半可直接執行同一建置；極舊環境若缺 VC++ 執行庫，可能需要 [Microsoft VC++ 可轉散發套件](https://learn.microsoft.com/zh-tw/cpp/windows/latest-supported-vc-redist)（依畫面錯誤訊息處理）。
- **離線**：
  - **本機圖片路徑**可用；模型已在套件內—**執行時不必下載**。
  - 離線時避免使用 **`http(s)://`** 圖片網址。

若根目錄 `.gitignore` 排除 `release/verify_image_text/`，他人 **`git clone` 不會拿到 exe**。請改以 **zip、Release 附件**或內部檔案分享傳遞。

---

## Repo 策略（擇一）

- **單一 repo**：整個專案含 `release/` 一併版控。若不想把大型二進位塞進 Git，請在**根目錄** `.gitignore` 加入 `release/verify_image_text/`。
- **獨立遠端**：僅在 `release/` 下 `git init` 發布 payload；注意不要誤刪上層專案的 `.git`。

---

## 體積與 Git

套件體積大（ONNX Runtime、OpenCV 等）。若遠端不適合放二進位，可改用 **Git LFS**、**GitHub Releases 附件**，或持續忽略 `release/verify_image_text/`、**只發 zip**。

---

## 使用者（已取得 `verify_image_text` 資料夾或 zip）

在套件根目錄（與 `verify_image_text.exe` 同層）開 **cmd**：

```bat
cd verify_image_text
verify_image_text.exe "D:\photo.png" --dump-json
scripts\run_ocr.bat "D:\photo.png" --dump-json
```

**目錄**：`scripts\` 捷徑；`config\` 範例抽取 JSON；`doc\` 詳細說明；根目錄 `README.txt` 索引。

**TR7 風格溫濕度**：

```bat
scripts\extract_tr7.cmd "D:\screenshot.png"
```

**自訂抽取**：複製 `config\extract_config.example.json` 編輯後：

```bat
scripts\extract_with_config.cmd config\my_config.json "D:\screenshot.png"
```

套件內 **`README.txt`**、**`doc\OCR_README_FOR_USERS.txt`** 為**英文為主、文末繁體中文補充**；範例 JSON 可有英文 `description` 與選填 `description_zh_TW`。

完整開發文件見專案根目錄 **`README.md`**（英文）與 **`README.zh-TW.md`**（繁體中文）。
