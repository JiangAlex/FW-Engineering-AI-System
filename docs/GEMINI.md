# 🚀 FW Engineering AI System Instructions

## 🏗️ System Architecture
- **Core**: Modular Python backend with FastAPI.
- **Data**: SQLite FTS5 for efficient knowledge retrieval.
- **Frontend**: Single-page web dashboard.
- **Pipeline**: Mail (.msg) -> Markdown (.md) -> SQLite FTS5.

## 📜 Coding Conventions
- **Structure**: Core logic in `src/core/`, high-level services in `src/services/`.
- **Language**: Technical explanations in **Traditional Chinese**.
- **Code**: All code elements (variables, functions, comments) in **English**.
- **Fallback**: Always provide a non-AI fallback path for data processing.

## 🛠️ Feature Status
- [x] Refactored Pipeline (Core/Services)
- [x] AI QA & Search
- [x] FW Timeline & Comparison
- [x] API Server & Web UI
- [x] Mail to MD Conversion
- [x] Weekly Report
