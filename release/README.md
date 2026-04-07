# Release (Windows standalone bundle)

Maintainer and handoff notes for the `release/` folder inside the development repository.

**Traditional Chinese:** [README.zh-TW.md](README.zh-TW.md)

This `release/` tree holds the **PyInstaller output** folder `verify_image_text\`, copied from `source\dist\` by the sync script, for delivery to PCs **without Python**.

---

## Maintainer: populate the bundle

1. **Build and sync (recommended)** — from the repo:

   ```powershell
   cd <project-root>\tool
   .\build_pyinstaller_release.ps1 -SyncToRelease
   ```

2. **Sync only** — if you already built `source\dist\verify_image_text`:

   ```powershell
   cd <project-root>\release
   .\sync_from_dev_build.ps1
   ```

   Uses **robocopy /MIR**; you do not need to delete `verify_image_text` first (reduces “file in use” failures).

3. After **CLI changes** (e.g. new flags like `--extract`), **rebuild** the exe. Old `verify_image_text.exe` may show `unrecognized arguments: …`.

4. Confirm `release\verify_image_text\verify_image_text.exe` exists before committing the bundle to Git or zipping for delivery.

---

## What to give “clean” / offline Windows PCs

- **Ship the whole folder**: zip **`release\verify_image_text\` in full**. Root must include `verify_image_text.exe`, `_internal\`, `README.txt`, and **`scripts\`**, **`config\`**, **`doc\`**. **Without `_internal\` or with only the exe extracted, the app will not run.**
- **You do not need to ship**: full repo source, Python, or venv (unless the recipient develops).
- **Other 64-bit Windows 10/11 machines** usually run the same build as-is. Very old systems missing VC++ runtimes may need [Microsoft VC++ Redistributable](https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist) (follow on-screen errors).
- **Offline**:
  - **Local image paths** work; models are inside the bundle—**no download at runtime**.
  - Avoid **`http(s)://`** image URLs when offline.

If `.gitignore` excludes `release/verify_image_text/`, `git clone` **does not include the exe**. Share the zipped folder via **Release assets**, internal file share, or similar.

---

## Repository strategy (pick one)

- **Single repo**: commit the whole project including `release/`. To avoid large binaries in Git, add `release/verify_image_text/` to the **root** `.gitignore`.
- **Separate remote**: `git init` under `release/` only for publish payloads; be careful not to delete the parent repo’s `.git`.

---

## Size and Git

The bundle is large (ONNX Runtime, OpenCV, etc.). If the remote is unsuitable for binaries, use **Git LFS**, **GitHub Releases attachments**, or keep `release/verify_image_text/` ignored and distribute **zip** only.

---

## End users (already have the `verify_image_text` folder or zip)

Open **cmd** in the bundle root (same folder as `verify_image_text.exe`):

```bat
cd verify_image_text
verify_image_text.exe "D:\photo.png" --dump-json
scripts\run_ocr.bat "D:\photo.png" --dump-json
```

**Layout**: `scripts\` shortcuts; `config\` sample extract JSON; `doc\` detailed notes; root `README.txt` index.

**TR7-style temperature / humidity**:

```bat
scripts\extract_tr7.cmd "D:\screenshot.png"
```

**Custom extract**: copy `config\extract_config.example.json`, edit, then:

```bat
scripts\extract_with_config.cmd config\my_config.json "D:\screenshot.png"
```

Inside the bundle, **`README.txt`** and **`doc\OCR_README_FOR_USERS.txt`** are **English-first** with a **Traditional Chinese supplement** at the end. Sample JSON may include `description` (English) and optional `description_zh_TW`.

Project docs: repository root **`README.md`** (English) and **`README.zh-TW.md`** (Traditional Chinese).
