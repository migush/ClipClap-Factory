# Autonomous Short-Form Video Factory with n8n + GPT

An end-to-end automation pipeline that creates and publishes vertical videos (Reels/Shorts/TikToks) across multiple social media platforms with zero human intervention.

## 🎯 Project Overview

This project implements a fully automated content creation system that:
- Scrapes trending AI/tech content from TLDR.tech
- Generates engaging video scripts using AI
- Creates vertical videos with voice-overs, music, and captions
- Publishes to Instagram, TikTok, and YouTube Shorts
- Operates completely autonomously

## 🏗️ Architecture

The system consists of:
- **n8n**: Workflow automation platform
- **crawl4ai**: Web scraping service
- **Ollama**: Local AI model for content generation
- **Docker**: Containerized deployment
- **Colima**: Local Docker environment for macOS

## 📋 Prerequisites

- macOS with Docker support
- [Colima](https://github.com/abiosoft/colima)
- [Docker](https://docs.docker.com/get-docker/)
- At least 4GB RAM available for containers

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd team_2
```

### 2. Start Colima Environment

```bash
chmod +x start_colima.sh
./start_colima.sh
```

This script:
- Stops any running Colima instance
- Starts a new Colima environment with 2 CPUs and 4GB RAM
- Mounts your project directories for file sharing

### 3. Start the Services

```bash
docker-compose up -d
```

This will start:
- **n8n** on `http://localhost:5678`
- **crawl4ai** on `http://localhost:11235`

### 4. Access n8n

1. Open your browser and navigate to `http://localhost:5678`
2. Complete the initial n8n setup
3. Import the workflow from `first_attempt.json`

### 5. Configure API Keys

Create a `.env` file in the project root:

```env
# RunwayML API Key (for video generation)
RUNWAY_API_KEY=your_runway_api_key_here

# Social Media API Keys (for posting)
INSTAGRAM_ACCESS_TOKEN=your_instagram_token
TIKTOK_ACCESS_TOKEN=your_tiktok_token
YOUTUBE_API_KEY=your_youtube_api_key

# Optional: OpenAI API Key (alternative to Ollama)
OPENAI_API_KEY=your_openai_key
```

## 📁 Project Structure

```
team_2/
├── docker-compose.yml          # Container orchestration
├── start_colima.sh            # Colima startup script
├── first_attempt.json         # Main workflow
├── first_test.json            # Test workflow
├── runway_api_key.txt         # RunwayML API key
├── files/                     # Generated content storage (mouted)
│   └── 2025-06-22.md         # Sample video script
└── .n8n/                      # n8n configuration (mounted)
```

## 🔧 Current Workflow

The existing workflow (`first_attempt.json`) performs:

1. **Content Discovery**: Scrapes AI news from TLDR.tech
2. **AI Processing**: Uses Ollama to generate video scripts
3. **Content Storage**: Saves generated scripts to `files/` directory

### Workflow Nodes:

- **Manual Trigger**: Starts the workflow
- **Edit Fields**: Sets target URL for scraping
- **HTTP Request**: Calls crawl4ai service
- **AI Agent**: Processes content with Ollama
- **Convert to File**: Converts AI output to file format
- **Read/Write Files**: Saves content to disk

## 🎬 Usage

### Running the Current Workflow

1. Open n8n at `http://localhost:5678`
2. Navigate to the imported workflow
3. Click "Execute Workflow"
4. Check the `files/` directory for generated content

### Generated Content

The workflow creates markdown files with video scripts like:
- Title and concept
- Detailed script with timing
- Visual style guidelines
- Hashtag recommendations

## 🚧 Development Roadmap

### Level 1 (Current) ✅
- [x] Content scraping from TLDR.tech
- [x] AI-powered script generation
- [x] Basic file management

### Level 2 (In Progress)
- [ ] Video generation with RunwayML
- [ ] Text-to-speech integration
- [ ] Background music generation
- [ ] Caption overlay system

### Level 3 (Planned)
- [ ] Instagram posting automation
- [ ] TikTok posting automation
- [ ] YouTube Shorts posting automation

### Level 4 (Future)
- [ ] Fully automated content chain
- [ ] Multi-platform optimization
- [ ] Performance analytics

### Level 5 (Advanced)
- [ ] Trending topic discovery
- [ ] Autonomous content ideation
- [ ] Viral prediction algorithms

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `RUNWAY_API_KEY` | RunwayML API key for video generation | Yes |
| `INSTAGRAM_ACCESS_TOKEN` | Instagram Graph API token | For Level 3+ |
| `TIKTOK_ACCESS_TOKEN` | TikTok API access token | For Level 3+ |
| `YOUTUBE_API_KEY` | YouTube Data API key | For Level 3+ |
| `OPENAI_API_KEY` | OpenAI API key (alternative to Ollama) | Optional |

### n8n Settings

The workflow uses these n8n nodes:
- **Manual Trigger**: Workflow initiation
- **Set**: Data manipulation
- **HTTP Request**: API calls
- **AI Agent**: LangChain integration
- **Ollama Chat Model**: Local AI processing
- **Convert to File**: File format conversion
- **Read/Write Files**: File system operations

## 🐛 Troubleshooting

### Common Issues

1. **Colima won't start**
   ```bash
   # Check if Docker is running
   docker ps
   
   # Restart Colima
   colima stop
   colima start --cpu 2 --memory 4
   ```

2. **n8n not accessible**
   ```bash
   # Check if containers are running
   docker-compose ps
   
   # Restart services
   docker-compose down
   docker-compose up -d
   ```

3. **Workflow fails**
   - Check n8n execution logs
   - Verify API keys are set correctly
   - Ensure crawl4ai service is running

### Logs

View container logs:
```bash
# n8n logs
docker-compose logs n8n

# crawl4ai logs
docker-compose logs crawl4ai
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

### Development Setup

1. Fork the repository
2. Clone your fork locally
3. Follow the Quick Start instructions
4. Create a feature branch: `git checkout -b feature/amazing-feature`

### Development Guidelines

- **Code Style**: Follow existing patterns
- **Testing**: Test workflows in n8n before committing
- **Documentation**: Update README.md for new features
- **Commits**: Use descriptive commit messages

### Adding New Features

1. **New Workflow Nodes**: Document in README.md
2. **API Integrations**: Add environment variables
3. **Dependencies**: Update docker-compose.yml
4. **Configuration**: Update setup instructions

### Pull Request Process

1. Ensure your code follows the project guidelines
2. Test your changes thoroughly
3. Update documentation as needed
4. Submit a pull request with a clear description

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [n8n](https://n8n.io/) for workflow automation
- [crawl4ai](https://github.com/unclecode/crawl4ai) for web scraping
- [Ollama](https://ollama.ai/) for local AI processing
- [TLDR.tech](https://tldr.tech/) for content inspiration

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review n8n documentation
3. Open an issue on GitHub
4. Check the project discussions

---

**Happy automating! 🚀** 