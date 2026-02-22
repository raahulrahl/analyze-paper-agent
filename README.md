<p align="center">
  <img src="https://raw.githubusercontent.com/getbindu/create-bindu-agent/refs/heads/main/assets/light.svg" alt="bindu Logo" width="200">
</p>

<h1 align="center">Analyze Paper Agent</h1>

<p align="center">
  <strong>AI-powered research paper analysis with evidence-based evaluation</strong>
</p>

<p align="center">
  <a href="https://github.com/raahulrahl/analyze-paper-agent/actions/workflows/main.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/raahulrahl/analyze-paper-agent/main.yml?branch=main" alt="Build status">
  </a>
  <a href="https://img.shields.io/github/license/raahulrahl/analyze-paper-agent">
    <img src="https://img.shields.io/github/license/raahulrahl/analyze-paper-agent" alt="License">
  </a>
</p>

---

## 📖 Overview

An intelligent agent that analyzes research papers by extracting truth claims, evaluating evidence, identifying logical fallacies, and providing balanced assessments with quality ratings. Built on the [Bindu Agent Framework](https://github.com/getbindu/bindu) for the Internet of Agents.

**Key Capabilities:**
- 🔍 Extracts and evaluates truth claims from research papers
- ✅ Provides supporting and refuting evidence with verifiable references
- 🚨 Identifies logical fallacies with examples
- 📊 Assigns quality ratings (A-F scale) to claims
- ⚖️ Generates balanced, centrist-oriented analysis

-> [Postman Collection link](https://raahul-1409c5b4-717533.postman.co/workspace/getbindu's-Workspace~44eb7cfe-a752-4114-8a1a-631395f07bf1/collection/50606358-a4c51dab-a869-4ece-b820-c109485b00af?action=share&creator=50606358)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager
- API keys for OpenRouter and Mem0 (both have free tiers)

### Installation

```bash
# Clone the repository
git clone https://github.com/raahulrahl/analyze-paper-agent.git
cd analyze-paper-agent

# Create virtual environment
uv venv --python 3.12.9
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync

# Configure environment
cp .env.example .env
```

### Configuration

Edit `.env` and add your API keys:

| Key | Get It From | Required |
|-----|-------------|----------|
| `OPENROUTER_API_KEY` | [OpenRouter](https://openrouter.ai/keys) | ✅ Yes |
| `MEM0_API_KEY` | [Mem0 Dashboard](https://app.mem0.ai/dashboard/api-keys) | If you want to use Mem0 tools |

### Run the Agent

```bash
# Start the agent
uv run python -m analyze_paper_agent

# Agent will be available at http://localhost:3773
```

---

## 💡 Usage

### Example Queries

```bash
# Analyze a research paper
"concise summary https://arxiv.org/abs/1706.03762"

# Evaluate arguments and evidence
"Evaluate the methodology and evidence in this medical study"

# Identify logical fallacies
"Identify logical fallacies in this economic policy paper"
```

### Input Formats

**Plain Text:**
```
Analyze this paper: [paste your research paper text here]
```

**JSON:**
```json
{
  "content": "Research paper text or argument",
  "focus": "claims"
}
```

### Output Structure

The agent returns structured analysis with:
- **Argument Summary**: Brief overview (< 30 words)
- **Truth Claims**: Each claim with:
  - Supporting evidence with references
  - Refuting evidence with references
  - Logical fallacies identified
  - Quality rating (A-F)
  - Characterization labels
- **Overall Score**: Lowest, highest, and average claim scores
- **Overall Analysis**: Summary with actionable recommendations

### Real Example: Transformer Paper Analysis

**Input Query:**
```
Identify logical fallacies in this paper https://arxiv.org/abs/1706.03762
```

**Output Sample:**

```markdown
## ARGUMENT SUMMARY:
Self-attention alone can replace recurrence and convolution while achieving
superior translation performance with greater efficiency.

## TRUTH CLAIMS:

### CLAIM 1
#### CLAIM:
Self-attention architectures outperform recurrent and convolutional models
for machine translation.

#### CLAIM SUPPORT EVIDENCE:
- Higher BLEU scores on WMT 2014 English–German and English–French tasks
- Vaswani et al. (2017) report BLEU 28.4 (En-De) exceeding prior benchmarks
- Results reproduced and extended in subsequent work

**References:**
- Vaswani et al., 2017, *Attention Is All You Need*, arXiv:1706.03762
- Gehring et al., 2017, *Convolutional Sequence to Sequence Learning*

#### CLAIM REFUTATION EVIDENCE:
- Performance gains depend on hyperparameter tuning, dataset size, and compute
- Hybrid models and improved RNNs can match or exceed early Transformer results
- BLEU improvements were modest and within variance ranges

**References:**
- Britz et al., 2017, *Massive Exploration of Neural Machine Translation*
- Melis et al., 2018, *On the State of the Art of Evaluation in Neural Language Models*

#### LOGICAL FALLACIES:
- **Overgeneralization**: "We propose a new simple network architecture…
  that relies solely on attention mechanisms."
- **Selection Bias**: Focus on benchmarks where Transformers perform best.

#### CLAIM RATING:
**B (High)**

#### LABELS:
Empirically supported, overgeneralized, benchmark-dependent

---

### CLAIM 2
#### CLAIM:
Recurrence and convolution are unnecessary for modeling sequence dependencies.

#### LOGICAL FALLACIES:
- **False Dichotomy**: "Without recurrence or convolution…" implies
  exclusivity where hybrids exist.
- **Scope Overshoot**: Generalizing from translation to all sequence modeling.

#### CLAIM RATING:
**C (Medium)**

#### LABELS:
Reductionist, overextended, architectural absolutism
```

**Key Features Demonstrated:**
- ✅ ArxivTools integration for automatic paper retrieval
- ✅ Both supporting AND refuting evidence with verifiable references
- ✅ Logical fallacy identification with quoted examples
- ✅ A-F quality ratings per claim
- ✅ Characterization labels for balanced assessment

---

## 🔌 API Usage

The agent exposes a RESTful API when running. Default endpoint: `http://localhost:3773`

### Quick Start

For complete API documentation, request/response formats, and examples, visit:

📚 **[Bindu API Reference - Send Message to Agent](https://docs.getbindu.com/api-reference/all-the-tasks/send-message-to-agent)**


### Additional Resources

- 📖 [Full API Documentation](https://docs.getbindu.com/api-reference/all-the-tasks/send-message-to-agent)
- 📦 [Postman Collections](https://github.com/GetBindu/Bindu/tree/main/postman/collections)
- 🔧 [API Reference](https://docs.getbindu.com)

---

## 🎯 Skills

### analyze-paper (v1.0.0)

**Primary Capability:**
- Analyzes truth claims and arguments with evidence-based evaluation
- Extracts verifiable claims from research papers
- Provides balanced perspectives with both supporting and refuting evidence

**Features:**
- Evidence verification with external sources
- Logical fallacy detection
- Quality scoring system (A-F scale)
- Comprehensive claim characterization
- Balanced, centrist-oriented analysis

**Best Used For:**
- Evaluating research papers for claim validity
- Fact-checking academic arguments
- Peer review assistance
- Getting balanced perspectives on controversial claims

**Not Suitable For:**
- Simple summarization (use a summarization skill instead)
- Creative writing or content generation
- Real-time fact-checking without verification time

**Performance:**
- Average processing time: ~5 seconds
- Max concurrent requests: 5
- Memory per request: 512MB

---

## 🐳 Docker Deployment

### Local Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up --build

# Agent will be available at http://localhost:3773
```

### Docker Configuration

The agent runs on port `3773` and requires:
- `OPENROUTER_API_KEY` environment variable
- `MEM0_API_KEY` environment variable

Configure these in your `.env` file before running.

### Production Deployment

```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🌐 Deploy to bindus.directory

Make your agent discoverable worldwide and enable agent-to-agent collaboration.

### Setup GitHub Secrets

```bash
# Authenticate with GitHub
gh auth login

# Set deployment secrets
gh secret set BINDU_API_TOKEN --body "<your-bindu-api-key>"
gh secret set DOCKERHUB_TOKEN --body "<your-dockerhub-token>"
```

Get your keys:
- **Bindu API Key**: [bindus.directory](https://bindus.directory) dashboard
- **Docker Hub Token**: [Docker Hub Security Settings](https://hub.docker.com/settings/security)

### Deploy

```bash
# Push to trigger automatic deployment
git push origin main
```

GitHub Actions will automatically:
1. Build your agent
2. Create Docker container
3. Push to Docker Hub
4. Register on bindus.directory

---

## 🛠️ Development

### Project Structure

```
analyze-paper-agent/
├── analyze_paper_agent/
│   ├── skills/
│   │   └── analyze-paper/
│   │       ├── skill.yaml          # Skill configuration
│   │       └── __init__.py
│   ├── __init__.py
│   ├── __main__.py
│   ├── main.py                     # Agent entry point
│   └── agent_config.json           # Agent configuration
├── tests/
│   └── test_main.py
├── .env.example
├── docker-compose.yml
├── Dockerfile.agent
└── pyproject.toml
```

### Running Tests

```bash
make test              # Run all tests
make test-cov          # With coverage report
```

### Code Quality

```bash
make format            # Format code with ruff
make lint              # Run linters
make check             # Format + lint + test
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
uv run pre-commit install

# Run manually
uv run pre-commit run -a
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Powered by Bindu

Built with the [Bindu Agent Framework](https://github.com/getbindu/bindu)

**Why Bindu?**
- 🌐 **Internet of Agents**: A2A, AP2, X402 protocols for agent collaboration
- ⚡ **Zero-config setup**: From idea to production in minutes
- 🛠️ **Production-ready**: Built-in deployment, monitoring, and scaling

**Build Your Own Agent:**
```bash
uvx cookiecutter https://github.com/getbindu/create-bindu-agent.git
```

---

## 📚 Resources

- 📖 [Full Documentation](https://raahulrahl.github.io/analyze-paper-agent/)
- 💻 [GitHub Repository](https://github.com/raahulrahl/analyze-paper-agent/)
- 🐛 [Report Issues](https://github.com/raahulrahl/analyze-paper-agent/issues)
- 💬 [Join Discord](https://discord.gg/3w5zuYUuwt)
- 🌐 [Agent Directory](https://bindus.directory)
- 📚 [Bindu Documentation](https://docs.getbindu.com)

---

<p align="center">
  <strong>Built with 💛 by the team from Amsterdam 🌷</strong>
</p>

<p align="center">
  <a href="https://github.com/raahulrahl/analyze-paper-agent">⭐ Star this repo</a> •
  <a href="https://discord.gg/3w5zuYUuwt">💬 Join Discord</a> •
  <a href="https://bindus.directory">🌐 Agent Directory</a>
</p>
