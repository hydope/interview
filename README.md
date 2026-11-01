# 🎯 StealthInterview

**The world's most advanced, open-source, real-time AI interview copilot.**

> Outperform every commercial solution. Get the ultimate edge in job interviews. Minimize detection risks.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Discord](https://img.shields.io/badge/Join-Discord-7289DA.svg)](https://discord.gg/stealthinterview)

---

## 🚀 Mission

StealthInterview is an open-source real-time AI interview assistant that listens to interview audio, generates instant answers using state-of-the-art speech-to-text and LLMs, and renders them as a stealthy transparent overlay over your video conferencing app — undetectable by screen-sharing software.

We believe every candidate deserves an equal shot. StealthInterview levels the playing field while protecting your privacy and integrity.

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| **Real-Time Transcription** | Whisper/DeepSpeech STT converts interview audio to text instantly |
| **AI Answer Generation** | Ollama/LLaMA generates contextual, interview-ready answers in seconds |
| **Stealth Mode** | Transparent overlay hooks over Zoom, Teams, Google Meet, and more — invisible to screen sharing |
| **Resume Integration** | Auto-parse your resume to pre-populate experience, skills, and projects |
| **Mock Practice Simulator** | Practice with real-world questions from LeetCode, Glassdoor, and behavioral databases |
| **Customizable Workflows** | Behavioral, coding, and system design formats with adjustable speed, length, and detail |
| **RESTful API** | Integrate with calendar schedulers, resume builders, and third-party services |
| **Privacy-First** | No identifiable logging, optional encryption, user anonymity by default |

---

## 🗺️ Technical Roadmap

### Phase 1 (0-4 weeks) — Foundation ✅
- [x] GitHub repository with documentation (README.md, LICENSE)
- [x] Basic speech-to-text using Whisper
- [x] Lightweight LLM integration via Ollama/LLaMA

### Phase 2 (4-8 weeks) — Stealth & Practice 🔨
- [ ] System-level display hooks for stealth mode (Windows, macOS, Linux)
- [ ] Resume parser (PDF, DOCX, TXT)
- [ ] Mock interview simulator with question databases
- [ ] Multi-platform video conferencing support

### Phase 3 (8-12 weeks) — Scale & API 📋
- [ ] Domain-specific fine-tuning (tech, finance, healthcare, etc.)
- [ ] Customizable workflows and response settings
- [ ] RESTful API endpoints (Swagger/OpenAPI)
- [ ] Security audits & anti-detection measures

### Phase 4 (12+ weeks) — Community & Growth 🌍
- [ ] Open beta with community feedback loop
- [ ] Multi-language support
- [ ] User-submitted question/answer training data
- [ ] Expanded platform support

---

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- [Ollama](https://ollama.ai) installed and running (for LLM)
- CUDA-capable GPU recommended (optional, CPU works)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/stealthinterview/stealthinterview.git
cd stealthinterview

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Copy configuration
cp examples/config.example.yaml config/config.yaml

# Pull an LLM model (via Ollama)
ollama pull llama3.2:3b

# Run the application
python -m src.api.main
```

### Docker (Coming Soon)

```bash
docker build -t stealthinterview .
docker run -p 8000:8000 stealthinterview
```

---

## 🎮 Usage

### Real-Time Interview Mode

```python
from src.stt.whisper_engine import WhisperEngine
from src.llm.ollama_client import OllamaClient
from src.generator.answer_generator import AnswerGenerator

# Initialize components
stt = WhisperEngine(model="base", device="cpu")
llm = OllamaClient(model="llama3.2:3b", base_url="http://localhost:11434")
generator = AnswerGenerator(stt=stt, llm=llm, config_path="config/config.yaml")

# Start listening and generating answers
generator.start_interview_session()
```

### CLI

```bash
# Start interview assistant
stealthinterview --mode interview --format behavioral

# Run mock interview
stealthinterview --mode mock --difficulty medium --questions 10

# Start API server
stealthinterview --api --port 8000
```

### REST API

Start the server:

```bash
python -m src.api.main
```

Then visit `http://localhost:8000/docs` for interactive Swagger documentation.

Example request:

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"question": "Tell me about yourself", "format": "behavioral", "resume_data": {...}}'
```

---

## 🛡️ Stealth Mode

StealthInterview renders AI-generated answers as a transparent, click-through overlay that sits on top of your video conferencing window. It uses system-level display hooks so screen-sharing software cannot capture the overlay text.

### Supported Platforms

| Platform | Status | Notes |
|----------|--------|-------|
| Windows | Planned (Phase 2) | Uses Win32 API / PyQt6 |
| macOS | Planned (Phase 2) | Uses PyObjC / Quartz |
| Linux | Planned (Phase 2) | Uses X11 / Wayland |

### Detection Resistance

- Transparent window with click-through enabled
- Always-on-top without taskbar presence
- No window title or process name leakage
- Configurable opacity and position

> **Warning:** Use responsibly. StealthInterview is designed to assist, not to guarantee undetectability. Always follow your potential employer's interview policies.

---

## 📄 Resume Integration

Parse your resume to auto-populate your experience:

```python
from src.resume.parser import ResumeParser

parser = ResumeParser()
data = parser.parse("path/to/resume.pdf")

print(data.skills)        # ['Python', 'React', 'AWS', ...]
print(data.experience)    # [{'company': '...', 'role': '...', 'years': 3}, ...]
print(data.education)     # [{'degree': '...', 'school': '...'}, ...]
```

Supported formats: PDF, DOCX, TXT, MD

---

## 🎭 Mock Interview Simulator

Practice before the real thing:

```python
from src.mock.simulator import MockSimulator

sim = MockSimulator(question_bank="leetcode", difficulty="medium")
session = sim.start_session(format="coding", num_questions=5)

for q in session.questions:
    answer = input(f"Q: {q}\nYour answer: ")
    feedback = sim.evaluate(answer, q)
    print(feedback)
```

---

## 🔌 API Documentation

Full REST API documentation is hosted on SwaggerHub and available locally at:

```
http://localhost:8000/docs   # Swagger UI
http://localhost:8000/redoc  # ReDoc
```

OpenAPI spec: `docs/SWAGGER.yaml`

Key endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/generate` | POST | Generate an answer from a question |
| `/transcribe` | POST | Transcribe audio to text |
| `/resume/parse` | POST | Parse resume file |
| `/mock/start` | POST | Start a mock interview session |
| `/config` | GET | Get current configuration |
| `/health` | GET | Health check |

---

## 🔒 Security & Privacy

- **No identifiable logging:** We do not log your name, email, or personal data
- **Optional encryption:** End-to-end encryption available for data in transit
- **Local-first:** All STT and LLM processing can run entirely on your machine
- **Anomaly detection:** Regular updates to anti-detection measures
- **Data ownership:** You own all data generated by StealthInterview

---

## 🤝 Contributing

We welcome contributions! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on:

- Setting up your development environment
- Code style and standards
- Pull request process
- Code review guidelines

### Quick Contribute

```bash
# Fork the repo, then:
git checkout -b feature/your-feature-name
# Make your changes
git commit -m "feat: add your feature"
git push origin feature/your-feature-name
# Open a pull request
```

---

## 📣 Community

- **Discord:** https://discord.gg/stealthinterview — Support, updates, feedback
- **GitHub Issues:** Bug reports and feature requests
- **Discussions:** General questions and ideas

---

## 📄 License

This project is licensed under the **GPLv3** — see [LICENSE](LICENSE) for details.

This ensures StealthInterview remains open-source forever while allowing commercial use under GPLv3 conditions.

---

## ⚠️ Disclaimer

StealthInterview is provided as-is, without warranty of any kind. Use at your own risk. The authors are not responsible for any consequences of using this software in interview settings. Always respect employer policies and local laws.

---

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) — Speech-to-text
- [Ollama](https://ollama.ai) — Local LLM inference
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) — Cross-platform UI
- [FastAPI](https://fastapi.tiangolo.com/) — REST API framework
- All contributors and the open-source community

---

**Built with ❤️ by the StealthInterview community. Star this repo if you believe in open, fair interviews for everyone.**