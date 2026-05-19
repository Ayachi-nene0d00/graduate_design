# Agent Guide — Bird Classifier

- **Path baseline**: Always work under `BASE_DIR = r"F:\Python-program\111"`; raw CUB-200 lives in `bird_species_raw/CUB_200_2011/images/`.
- **Data flow (classification)**: raw folders → `convert_dataset.py` splits into `datasets/birds/{train,val}/class/` → `augment_dataset.py` copies + 3× aug to `datasets/birds_augmented/` (224×224 crops) → training outputs `runs/classify/bird_cls_final_stable/weights/best.pt` → ONNX copied to `static/bird_cls_final_stable.onnx`.

## Critical workflows
- **Initial Training/Transfer Learning**: `retrain_better.py` loads `yolov8n-cls.pt` by default. For fine-tuning, update the `YOLO()` path to a trained `best.pt` (e.g., `runs/classify/bird_cls_final_stable/weights/best.pt`).
- **Prep dataset**: `python convert_dataset.py` creates `datasets/birds/`. `python augment_dataset.py` optionally copies + 3× aug to `datasets/birds_augmented/` (224×224 crops). Note: Currently `retrain_better.py` reads from `datasets/birds`, not `birds_augmented`.
- **[Optional] Merge Semi-BD200 classes**: If you want to expand CUB-200_2011 with Semi-BD200, run `python tools/merge_semi_bd200_to_cub.py --dry-run --limit 5` to preview, then `python tools/merge_semi_bd200_to_cub.py` for the full merge. This script is idempotent and only adds new classes not already present. Always run this before dataset conversion/augmentation if using Semi-BD200.
- **Train + export (Windows/GPU tuned)**: run `python retrain_better.py`; env set inside for stability (`OMP_NUM_THREADS=4`, `TORCHDYNAMO_DISABLE=1`, `CUDNN_BENCHMARK=1`). Uses `yolov8n-cls.pt`, imgsz 224, auto_augment="randaugment", mixed precision, batch auto-chosen (>=4GB GPUs default to 16). Exports ONNX (opset 12, simplify=True) and copies to `static/`.
- **Evaluate quickly**: `python test_model_bird.py` picks 5 samples from `datasets/birds/val`, auto-discovers latest `best.pt` under `runs/**/best.pt`, compares folder name to top1.
- **Interactive PC check**: `python test_UI.py` Tkinter app auto-finds newest `best.pt`; resizes preview only; inference at 224.
- **Class name export**: `python get_names.py` reads latest `best.pt` and dumps ordered names array for UniApp `birdNames`.
- **FastAPI Local Backend**: Run `python backend/main.py` (or similar entrypoint). Runs a local server using `uvicorn` listening on `0.0.0.0:8000`. Receives image uploads via HTTP POST, runs YOLO inference, and returns JSON predictions. Intended for local intranet demo (phone and PC on the same WiFi).
- **AI Q&A endpoint**: The backend exposes a POST `/api/aiqa` endpoint for bird-related questions, using an external AI API. Requires an API key in `API.txt` or as an environment variable (`SILICONFLOW_API_KEY` or `DEEPSEEK_API_KEY`). All questions and answers are logged to the `ai_chat_log` table if available.
- **Meta endpoint**: The backend provides a `/api/meta` endpoint returning the base URL and a QR code (base64) for LAN access.
- **GPU sanity**: `python check_gpu.py` before training if CUDA issues arise.

## Intranet FastAPI Architecture
- **Role**: Serves as a local HTTP API for end-to-end classification demo over Wi-Fi. No external internet or cloud deployment required.
- **Frontend (UniApp)**: Sends standard HTTP POST requests with multipart form data (image) to `http://<PC_IP>:8000/predict`.
- **Backend (Python)**: Uses FastAPI and `uvicorn` to host endpoints locally. Loads the `.pt` model and processes the uploaded byte stream in-memory.
- **Data Flow**: UniApp `uni.uploadFile` -> PC FastAPI -> YOLO Model Predict -> JSON return `{"bird_name": "...", "confidence": ...}`.

### Additional API Endpoints (since 2026-05)
- **/api/quiz**: Returns a set of 5 quiz questions about birds, dynamically generated from the MySQL `bird` table. Used for educational or quiz features in the frontend.
- **/api/recommend**: Returns a list of bird species relevant to a given region/city, based on the MySQL `bird` table. Used for location-based recommendations.
- **/api/bird**: Bird encyclopedia list/search endpoint with pagination and fuzzy search by keyword (name, english_name, family, region). Supports page and page_size query params.
- **/api/bird/{bird_id}**: Bird detail endpoint returning full info for a specific bird by ID.
- Both endpoints require a running MySQL instance with the `bird_classification_app` database and a populated `bird` table (fields: `name`, `family`, `protect_level`, `region`, `habit`, `feature`, etc.).

## Conventions & patterns
- **Paths**: prefer raw strings (e.g., `r"F:\\Python-program\\111"`) to avoid backslash escapes.
- **Model lookup**: pick the newest `best.pt` by mtime (sort desc or `max(..., key=os.path.getmtime)`), as in `backend/main.py`, `test_model_bird.py`, `get_names.py`, `test_UI.py`.
- **Image policy**: training expects RGB 224×224, JPG/PNG; augmentations already embedded, do not add YOLO detection-style params.
- **Hardware tuning**: keep `compile=False`, `half=True`, `amp=True`; `workers=8`; patience=15; warmup_epochs=3; weight_decay=5e-4.

### Backend conventions (FastAPI)
- **API Framework**: FastAPI for lightweight, high-performance routing.
- **Host & Port**: Bind to `0.0.0.0` to allow external network (LAN) requests, typical port `8000`.
- **Image handling**: Do not save uploaded images to disk unless debugging. Read directly from `UploadFile` via PIL/BytesIO, pass to YOLO.
- **MySQL dependency**: The backend expects a MySQL server running locally with user `root` and database `bird_classification_app`. The `bird` table must exist and be populated for `/api/quiz` and `/api/recommend` to function.
- **Intranet connectivity**: Automatically detects local IP using socket and generates QR code for easy mobile access on the same LAN. Install `qrcode[pil]` for QR functionality.
- **AI API key management**: Place your AI API key in `API.txt` or set as an environment variable (`SILICONFLOW_API_KEY` or `DEEPSEEK_API_KEY`). The backend will use this key to authenticate requests to the AI Q&A service.

## UniApp / ONNX integration (App focus)
- **Model artifact**: front-end consumes `/static/bird_cls_final_stable.onnx`; ensure `static/` ships with app build.
- **ONNX runtime**: app pages (`app.vue`, `app2.vue`, `app3.vue`) load `onnxruntime-web@1.14.0` via script tag; inference uses WebGL EP. Canvas/WebGL checks gate UI status.
- **Preprocess expectation**: resize to 224; current front-end either letterboxes (app.vue/app2.vue) or direct resize (app3.vue); normalize with ImageNet mean/std and reorder to CHW float32.
- **Platform guards**: `APP-PLUS` only; non-app platforms short-circuit with unsupported messages. If using nvue (no DOM), ONNX-WebGL will fail; keep pages as Vue/H5-rendered views.
- **Project variants**: Full UniApp project structures for app2.vue and app3.vue implementations are located in `Uni_app_relation/Test2` and `Uni_app_relation/Test2_2` respectively.

## Common pitfalls
- Wrong base path → use raw string and forward slashes in scripts; otherwise file not found on Windows.
- Using Semi-BD200 but skipping merge → run the merge script before `convert_dataset.py` if you want to include Semi-BD200 classes; otherwise, they will not appear in the training/validation sets.
- Missing augmented data → run convert + augment; training currently uses `datasets/birds` directly instead of `datasets/birds_augmented` in `retrain_better.py`.
- ONNX mismatch → ensure export ran after latest training; replace stale `/static/bird_cls_final_stable.onnx` when retraining.
- Class list drift → rerun `get_names.py` after retrain and paste into UniApp `birdNames` array.
