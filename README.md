# AI Contract Risk Analysis Agent

Production-ready AI pipeline for identifying legal and financial risks in construction and IT contracts.

## 🎯 Features

- **Automated Risk Detection**: Identifies 7+ types of contract risks
- **Structured Output**: Pydantic-validated JSON responses
- **Interactive UI**: Simple Streamlit interface for uploads and analysis# AI Contract Risk Analysis Agent

Production-ready AI pipeline for identifying legal and financial risks in construction and IT contracts, powered by **Google Gemini**.

## 🎯 Features

- **Automated Risk Detection**: Identifies 7+ types of contract risks
- **Structured Output**: Pydantic-validated JSON responses
- **Interactive UI**: Simple Streamlit interface for uploads and analysis
- **Gemini-Powered**: Uses Google's latest Gemini 2.0 Flash for intelligent analysis
- **Fast Processing**: PyMuPDF for efficient text extraction
- **Free Tier Available**: Generous free quota with Google AI

## 🏗️ Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   PDF File  │ -> │ PyMuPDF      │ -> │ Google      │
│   Upload    │    │ Text Extract │    │ Gemini API  │
└─────────────┘    └──────────────┘    └─────────────┘
                                              │
                                              v
                                       ┌──────────────┐
                                       │   Pydantic   │
                                       │  Validation  │
                                       └──────────────┘
                                              │
                                              v
                                       ┌──────────────┐
                                       │  Streamlit   │
                                       │  Interface   │
                                       └──────────────┘
```

### Tech Stack

- **Python 3.11+** with `uv` dependency management
- **PyMuPDF**: Fast PDF text extraction
- **Pydantic 2**: Type-safe structured outputs
- **Google Gemini 2.0**: Latest LLM for risk analysis
- **Streamlit**: Rapid UI development

## 🚀 Quick Start

### Prerequisites

```bash
# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Get Google AI API Key (FREE)
# Visit: https://aistudio.google.com/apikey
```

### Installation

```bash
# Clone repository
git clone https://github.com/pedroarthuralvesdeoliveira/ai-challenge.git
cd ai-challenge

# Install dependencies with uv
uv sync

# Set up API key
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### Run

```bash
# Start Streamlit app
uv run streamlit run src/app.py

# The app will open at http://localhost:8501
```

## 📋 Usage

1. **Get API Key**: Visit https://aistudio.google.com/apikey (free, no credit card)
2. **Upload Contract**: Drag & drop PDF file
3. **Configure**: Enter API key in sidebar
4. **Analyze**: Click "Analyze Contract with Gemini" button
5. **Review**: Examine identified risks with explanations
6. **Export**: Download results as JSON or Markdown

### Gemini Model Options

| Model | Speed | Accuracy | Cost | Best For |
|-------|-------|----------|------|----------|
| **Gemini 2.0 Flash** | ⚡⚡⚡ | ⭐⭐⭐ | Free tier | Quick analysis, most contracts |
| **Gemini 1.5 Pro** | ⚡ | ⭐⭐⭐⭐⭐ | Pay-per-use | Complex contracts, thorough review |
| **Gemini 1.5 Flash** | ⚡⚡ | ⭐⭐⭐⭐ | Free tier | Balanced option |

### Detected Risk Types

- ⚠️ Vague payment terms
- ⚠️ Uncapped liability
- ⚠️ Ambiguous scope of work
- ⚠️ Missing termination terms
- ⚠️ Missing insurance requirements
- ⚠️ Broad indemnification clauses
- ⚠️ Overly unilateral terms

## 📊 Output Schema

```json
{
  "risks": [
    {
      "risk_type": "Uncapped Liability",
      "clause_text": "...exact clause from contract...",
      "explanation": "Why this is problematic...",
      "remediation_suggestion": "How to fix it..."
    }
  ]
}
```

## 🧪 Testing

```bash
# Run on sample contracts
uv run pytest

# Test with provided assets
uv run streamlit run src/app.py
# Upload files from assets/ folder
```

## 📁 Project Structure

```
ai-challenge/
├── src/
│   ├── models.py          # Pydantic schemas
│   ├── parser.py          # PDF text extraction
│   ├── analyzer.py        # Gemini integration
│   └── app.py             # Streamlit UI
├── assets/                # Sample contracts
├── tests/                 # Unit tests
│   ├── test_parser.py     # Parser tests
│   └── test_analyzer.py   # Analyzer tests
├── pyproject.toml         # Dependencies (managed by uv)
├── .env.example           # Environment variables template
└── README.md
```

## 🐳 Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files
COPY . .

# Install dependencies
RUN uv sync

# Expose Streamlit port
EXPOSE 8501

# Run application
CMD ["uv", "run", "streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t ai-challenge .
docker run -p 8501:8501 -e GOOGLE_API_KEY=your_key ai-challenge
```

## 📝 Technical Notes

### Current Limitations

1. **Text-Only PDFs**: Requires native text; OCR not implemented in MVP
2. **Single Document**: Doesn't cross-reference multiple contracts yet
3. **English Only**: Optimized for English-language contracts
4. **Manual Review**: AI suggestions should be verified by legal counsel

### Future Improvements

1. **OCR Integration**: Add Tesseract for scanned documents
2. **Multi-Document Analysis**: Cross-check data across related contracts
3. **Vector Database**: RAG for legal precedent lookup
4. **Batch Processing**: Analyze multiple contracts simultaneously
5. **Custom Rules**: Allow user-defined risk criteria
6. **Integration API**: REST endpoints for backend systems

### Why This Stack?

- **PyMuPDF**: 10x faster than alternatives, robust text extraction
- **Pydantic**: Production-ready validation, self-documenting schemas
- **Google Gemini**: Best free tier, excellent JSON mode, fast response times
- **Streamlit**: 4-hour constraint demands rapid UI development

### Gemini Advantages

✅ **Generous Free Tier**: 60 requests/minute for Flash models  
✅ **JSON Mode**: Native structured output support  
✅ **Fast**: Gemini 2.0 Flash is among the fastest LLMs  
✅ **Multimodal**: Future support for image-based PDFs  
✅ **No Credit Card**: Free tier doesn't require payment method  

## 🔑 API Key Setup

### Option 1: Environment Variable (Recommended)
```bash
export GOOGLE_API_KEY="your_api_key_here"
uv run streamlit run src/app.py
```

### Option 2: .env File
```bash
echo "GOOGLE_API_KEY=your_api_key_here" > .env
uv run streamlit run src/app.py
```

### Option 3: Streamlit UI
- Enter API key directly in the sidebar
- Key is stored only for the session


## 📊 Performance Benchmarks

- **PDF Extraction**: ~1-2 seconds per 50-page document
- **Gemini Analysis**: ~3-8 seconds (Flash) / ~10-15 seconds (Pro)
- **Total**: ~10-20 seconds per contract

## 🆘 Troubleshooting

### "API key not valid"
- Get a new key at https://aistudio.google.com/apikey
- Make sure you copied the entire key
- Check for extra spaces

### "Resource exhausted" or "Quota exceeded"
- You've hit the rate limit (60 req/min for free tier)
- Wait a moment and try again
- Consider using Gemini Flash instead of Pro

### "Very little text extracted"
- Your PDF might be scanned/image-based
- OCR support coming soon
- Try a text-based PDF first

## 📄 License

MIT License - Assessment Project

## 👤 Author

[Pedro Oliveira] - Backend AI Engineer Candidate