# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**C# Code Reviewer** is an AI-powered code review automation tool designed for offline VDI environments. It uses Phi-3-mini LLM (via Ollama) to analyze C# code and generate improvement suggestions across 6 review categories.

### Core Objectives
- **100% Offline**: No internet connection required, fully local execution
- **No Admin Rights**: Portable EXE that runs without installation
- **AI-Powered**: Phi-3-mini (3.8B parameters, 2.3GB GGUF) for intelligent code analysis
- **6 Review Categories**: Null reference, Exception handling, Resource disposal, Performance, Security, Naming conventions

### Tech Stack
- **Backend**: Python 3.11+, Ollama SDK (LLM client)
- **Frontend**: PySide6 (Qt6 Python bindings) - LGPL licensed
- **LLM**: Phi-3-mini via Ollama (localhost:11434)
- **Markdown**: python-markdown, Pygments (syntax highlighting)
- **Diagrams**: Mermaid CLI (converted to PNG)
- **Packaging**: PyInstaller (Python → EXE)

---

## Development Commands

### Initial Setup

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Ollama and pull model
brew install ollama  # macOS
ollama serve  # Start server (runs on localhost:11434)
ollama pull phi3:mini  # Download Phi-3-mini model (2.3GB)
```

### Running the Application

```bash
# Development mode (when implemented)
python app/main.py

# With debug logging
python app/main.py --debug

# Start Ollama server (separate terminal)
ollama serve
```

### Testing

```bash
# Run all tests
pytest

# With coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_ollama_client.py -v

# UI tests (pytest-qt)
pytest tests/test_ui/ -v
```

### Building Portable Package

```bash
# Build EXE with PyInstaller
python scripts/build_exe.py

# Bundle Ollama + model
python scripts/bundle_ollama.py

# Create distributable package (~/2.5GB, compressed ~1.5GB)
python scripts/package_portable.py
```

---

## Architecture Overview

### 3-Layer Architecture

```
┌─────────────────────────────────────┐
│    Presentation Layer (PySide6)     │
│  - Main Window (menu, toolbar)      │
│  - Before/After Split Editor        │
│  - Result Panel (Markdown viewer)   │
│  - File Upload / Folder Select UI   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    Business Logic Layer             │
│  - Code Analyzer (orchestration)    │
│  - Prompt Builder (6 templates)     │
│  - Report Generator (Markdown)      │
│  - Diagram Converter (Mermaid→PNG)  │
│  - Syntax Highlighter (C# lexer)    │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│    LLM Integration Layer            │
│  - Ollama Client (HTTP API)         │
│  - Streaming Response Handler       │
│  - Retry Logic (3 attempts)         │
│  - Response Caching                 │
└─────────────────────────────────────┘
```

### Data Flow: Text Analysis Mode

```
1. User pastes C# code → Before Editor
2. Click "Analyze" button
3. Prompt Builder creates LLM prompt (6 review categories)
4. Ollama Client sends POST /api/generate (streaming)
5. Report Generator parses LLM response → Markdown
6. Diagram Converter extracts Mermaid → PNG (mmdc CLI)
7. Markdown Renderer converts to HTML (Pygments highlighting)
8. UI updates: After Editor + Result Panel
```

### Key Components

#### Prompt Template Structure
- Main prompt: 6 review categories with detailed instructions
- Few-shot examples: 3 example code reviews
- Output format: Markdown with sections (Summary, Issues, Improvements, Diagram, After Code)
- Token optimization: Target <1500 tokens per prompt

#### Ollama Client Configuration
```python
{
  "model": "phi3:mini",
  "stream": true,
  "options": {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "num_predict": 2048
  }
}
```

#### C# Syntax Highlighter (QSyntaxHighlighter)
- Keywords: Blue (#569CD6)
- Strings: Orange (#CE9178)
- Comments: Green (#6A9955)
- Numbers: Light green (#B5CEA8)
- Classes: Cyan (#4EC9B0)

---

## File Structure

```
app/
├── main.py                      # Application entry point
├── ui/
│   ├── main_window.py           # Main window with menu/toolbar
│   ├── before_after_editor.py   # Split editor with sync scroll
│   ├── file_upload_widget.py    # File upload + drag-and-drop
│   ├── folder_select_widget.py  # Tree view for folder selection
│   └── result_panel.py          # QTextBrowser for Markdown
├── core/
│   ├── analyzer.py              # Orchestrates analysis workflow
│   ├── ollama_client.py         # Ollama API client (streaming)
│   ├── prompt_builder.py        # Template-based prompt generation
│   ├── report_generator.py      # Markdown report creation
│   └── diagram_converter.py     # Mermaid CLI wrapper (mmdc)
├── utils/
│   ├── syntax_highlighter.py    # QSyntaxHighlighter for C#
│   ├── markdown_renderer.py     # Markdown→HTML (python-markdown)
│   └── file_handler.py          # File I/O with UTF-8 encoding
└── config/
    └── settings.py              # App settings (Ollama host, theme, etc.)

resources/
├── icons/                       # App and UI icons
├── styles/
│   ├── dark_theme.qss           # Qt stylesheet (dark mode)
│   └── github_markdown.css      # GitHub-style Markdown rendering
└── templates/
    └── report_template.md       # Markdown report template

scripts/
├── build_exe.py                 # PyInstaller build script
├── bundle_ollama.py             # Bundle Ollama + Phi-3-mini
└── package_portable.py          # Create portable package

tests/
├── test_ollama_client.py        # LLM client tests (mocked)
├── test_prompt_builder.py       # Prompt generation tests
├── test_report_generator.py     # Report parsing tests
├── test_diagram_converter.py    # Mermaid conversion tests
└── test_ui/                     # pytest-qt UI tests
```

---

## Development Workflow

### Phase 1: MVP (Weeks 1-2) - Text Editor Mode
- Before/After split editor with C# syntax highlighting
- Ollama integration with streaming responses
- 6 review categories (Null, Exception, Resource, Performance, Security, Naming)
- Markdown report generation with Pygments
- Mermaid diagram PNG conversion

### Phase 2: File Upload (Week 3)
- Single/multiple file selection with drag-and-drop
- Progress dialog for batch analysis
- Per-file report generation
- Report history (SQLite DB)

### Phase 3: Folder Selection (Week 4)
- Recursive folder traversal with tree view
- Batch processing (10 files at a time)
- Project-wide summary report with charts
- File count limit (50 files max)

### Phase 4: Portable Packaging (Week 5)
- PyInstaller EXE build (--onefile, --windowed)
- Ollama portable bundling (auto-start subprocess)
- VDI environment testing (Windows 11, no admin, no internet)
- UPX compression

### Phase 5: Testing & Optimization (Week 6)
- Unit tests with >80% coverage (pytest, pytest-qt)
- Integration tests for full workflows
- Performance optimization (response caching, async file I/O)
- Memory management (QThread cleanup)

---

## Testing Strategy

### Unit Tests (pytest)
```bash
# Test LLM client with mocked responses
tests/test_ollama_client.py

# Test prompt template generation
tests/test_prompt_builder.py

# Test Markdown parsing and report structure
tests/test_report_generator.py

# Test Mermaid→PNG conversion
tests/test_diagram_converter.py
```

### UI Tests (pytest-qt)
```bash
# Test button clicks, text input, dialogs
tests/test_ui/test_main_window.py

# Test file drag-and-drop
tests/test_ui/test_file_upload.py
```

### Performance Benchmarks
- 10 lines: <2 seconds
- 100 lines: <5 seconds
- 500 lines: <20 seconds
- Memory usage: <3GB (including model)

---

## Configuration

### settings.json Structure
```json
{
  "ollama": {
    "host": "http://localhost:11434",
    "model": "phi3:mini",
    "timeout": 30,
    "temperature": 0.7
  },
  "ui": {
    "theme": "dark",
    "font_family": "Consolas",
    "font_size": 12,
    "sync_scroll": true
  },
  "analysis": {
    "check_null_reference": true,
    "check_exception": true,
    "check_resource": true,
    "check_performance": true,
    "check_security": true,
    "check_naming": true,
    "generate_comments": true,
    "generate_diagram": true
  },
  "files": {
    "max_file_size_mb": 1,
    "max_file_count": 50
  }
}
```

---

## Error Handling

### Custom Exception Hierarchy
```python
class CodeReviewerError(Exception):
    """Base exception"""
    pass

class OllamaConnectionError(CodeReviewerError):
    """Ollama server unreachable"""
    pass

class ModelNotFoundError(CodeReviewerError):
    """Phi-3-mini model not available"""
    pass

class PromptTooLongError(CodeReviewerError):
    """Prompt exceeds context window (4096 tokens)"""
    pass

class DiagramConversionError(CodeReviewerError):
    """Mermaid CLI (mmdc) failed"""
    pass
```

### Retry Logic
- Ollama API calls: 3 retries with exponential backoff (1s, 2s, 4s)
- File I/O errors: Skip file and log error
- Mermaid conversion failure: Fallback to text representation

---

## Optimization Techniques

### Response Caching
```python
# Cache LLM responses by code hash (MD5)
# Prevents re-analysis of identical code
cache_key = hashlib.md5(code.encode()).hexdigest()
```

### Asynchronous Processing (QThread)
```python
# Prevent UI freeze during LLM analysis
class AnalysisThread(QThread):
    progress_updated = Signal(int)
    result_ready = Signal(dict)
    error_occurred = Signal(str)
```

### Memory Management
- Release file contents after analysis
- Clear QThread resources on completion
- Batch processing with 1-second delay between batches

---

## Dependencies

### Core Dependencies
```
PySide6>=6.6.0           # Qt6 GUI framework (LGPL)
ollama>=0.1.0            # Ollama Python SDK
markdown>=3.5.0          # Markdown to HTML conversion
Pygments>=2.17.0         # Syntax highlighting
pytest>=7.4.0            # Testing framework
pytest-qt>=4.2.0         # Qt testing support
pytest-cov>=4.1.0        # Coverage reporting
PyInstaller>=6.3.0       # EXE packaging
```

### External Dependencies
- **Ollama**: Required for LLM inference (localhost:11434)
- **Mermaid CLI (mmdc)**: Required for diagram conversion
  ```bash
  npm install -g @mermaid-js/mermaid-cli
  ```

---

## Portable Package Structure

```
CodeReviewer_Portable/         (~2.5GB uncompressed, ~1.5GB compressed)
├── CodeReviewer.exe           # PyInstaller bundled executable (~50-100MB)
├── ollama_portable/
│   ├── ollama.exe             # Ollama Windows binary (~100MB)
│   └── models/
│       └── phi3-mini.gguf     # Phi-3-mini Q4_K_M quantized (2.3GB)
├── config/
│   └── settings.json          # User preferences
├── logs/                      # Application logs
└── README.txt                 # Quick start guide
```

### Auto-Start Ollama
```python
# CodeReviewer.exe automatically starts Ollama subprocess
subprocess.Popen(
    ["ollama_portable/ollama.exe", "serve"],
    env={"OLLAMA_MODELS": "./ollama_portable/models"}
)
```

---

## Known Limitations & Workarounds

### QTextBrowser Markdown Rendering
- **Limitation**: No native Mermaid support
- **Workaround**: Convert Mermaid to PNG using mmdc CLI

### PyInstaller Bundle Size
- **Issue**: PySide6 increases EXE size to ~100MB
- **Mitigation**: UPX compression, exclude unused Qt plugins

### Phi-3-mini Performance on Low-End CPUs
- **Issue**: Slow inference on 4-core CPUs (>10s per response)
- **Mitigation**: Optimize prompt length, use Q4_K_M quantization

### VDI Port Conflicts
- **Issue**: Port 11434 may be in use
- **Mitigation**: Check and use alternative port (11435, 11436, etc.)

---

## Troubleshooting

### "Ollama server not responding"
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Manually start Ollama
ollama serve

# Check firewall settings (VDI environments)
```

### "Model not found: phi3:mini"
```bash
# Pull model
ollama pull phi3:mini

# Verify model exists
ollama list
```

### "mmdc: command not found"
```bash
# Install Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Or use fallback (skip diagrams)
# Set generate_diagram: false in settings.json
```

---

## Project Status

**Current Phase**: Planning & Documentation (Pre-Week 1)

- [x] Project plan (PROJECT_PLAN.md)
- [x] Development timeline (DEVELOPMENT_TIMELINE.md)
- [x] Technical specification (TECHNICAL_SPECIFICATION.md)
- [x] README documentation
- [ ] Project structure implementation (Week 1, Day 1)
- [ ] Ollama integration (Week 1, Day 2)
- [ ] MVP completion target: End of Week 2
- [ ] Full release target: Week 6 (6 weeks from project start)

---

## Additional Resources

- **Project Plan**: See [PROJECT_PLAN.md](PROJECT_PLAN.md) for complete feature specification
- **Development Timeline**: See [DEVELOPMENT_TIMELINE.md](DEVELOPMENT_TIMELINE.md) for detailed daily tasks
- **Technical Spec**: See [TECHNICAL_SPECIFICATION.md](TECHNICAL_SPECIFICATION.md) for architecture diagrams and API details
- **Ollama Docs**: https://ollama.com/library/phi3
- **PySide6 Docs**: https://doc.qt.io/qtforpython-6/
- **Mermaid Syntax**: https://mermaid.js.org/
