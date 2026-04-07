# Release（Windows 免安裝發行包）

本目錄位於**開發專案內**（`release/`），用來放置 PyInstaller 建置後要交付給「乾淨 Windows」使用者的 `verify_image_text` 資料夾（由同步腳本從 `source\dist\` 複製而來）。

## 維護者：填入發行檔

1. 在專案根目錄的上一層進入 `tool` 建置並同步（建議）：

   ```powershell
   cd <專案根>\tool
   .\build_pyinstaller_release.ps1 -SyncToRelease
   ```

2. 或僅同步（已建置過 `source\dist\verify_image_text`）：

   ```powershell
   cd <專案根>\release
   .\sync_from_dev_build.ps1
   ```

   同步使用 **robocopy /MIR**，不必先刪除整個 `verify_image_text`（較不易因檔案被鎖而失敗）。

3. **變更 CLI（例如新增 `--extract`）後務必重新建置**，否則舊版 `verify_image_text.exe` 會出現 `unrecognized arguments: --extract`。

4. 確認 `release\verify_image_text\verify_image_text.exe` 存在後，再決定是否納入 Git／打包 zip。

## 交付給「乾淨電腦／別台 PC／離線」時要給什麼

- **請給整包資料夾**：`release\verify_image_text\` **整個目錄**打成 zip（根目錄須含 `verify_image_text.exe`、`_internal\`、`README.txt`，以及 **`scripts\`、`config\`、`doc\`**）。少 `_internal` 或只抽 exe **無法執行**。
- **不必給**：整份 `20260407_Image_Text_MicroOCR` 原始碼、Python、venv（除非對方要開發）。
- **乾淨 Windows、與你電腦不同**：只要同為常見 **64-bit Windows 10/11**，一般可直接跑；極舊環境若缺 VC 執行庫，才可能需安裝 [Microsoft VC++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist)（視實機錯誤訊息而定）。
- **沒有網路**：
  - **本機圖檔路徑**：可離線使用；模型已打在套件內，執行時**不需要**再下載。
  - **不要用** `http(s)://` 當圖片路徑（離線會失敗）。

若 Git 忽略了 `release/verify_image_text/`，別人 `git clone` 只會拿到說明與腳本，**沒有 exe**；此時請改以 **zip／內部檔案伺服器／Release 附件** 傳遞上述整包資料夾。

## 版本庫策略（擇一）

- **單一 repo**：整個 `20260407_Image_Text_MicroOCR` 含 `release/` 一併提交。若不想追蹤大二進位，在**專案根** `.gitignore` 加入 `release/verify_image_text/`。
- **獨立遠端**：僅推送發行內容時，可在本目錄另執行 `git init` 並設定 remote（子目錄獨立 repo）；與主專案並存時注意不要誤刪對方 `.git`。

## Git 與體積

發行目錄含 ONNX、OpenCV 等**體積大**。若遠端不適合存大二進位：使用 **Git LFS**、**Releases 附件**，或忽略 `release/verify_image_text/` 僅以 zip 內部分享。

## 使用者（已取得 `verify_image_text` 資料夾或 zip）

套件根目錄（與 `verify_image_text.exe` 同層）開 cmd：

```bat
cd verify_image_text
verify_image_text.exe "D:\圖片.png" --dump-json
scripts\run_ocr.bat "D:\圖片.png" --dump-json
```

**目錄分類（精簡）**：`scripts\` 捷徑；`config\` 擷取規則範例 JSON；`doc\` 詳細說明；根目錄 `README.txt` 為索引。

**溫溼度擷取（TR7 類截圖）**：

```bat
scripts\extract_tr7.cmd "D:\截圖.png"
```

**自訂擷取**：複製 `config\extract_config.example.json` 為自訂檔後：

```bat
scripts\extract_with_config.cmd config\my_config.json "D:\截圖.png"
```

詳見 `doc\OCR_README_FOR_USERS.txt` 與專案 `README.md`。
