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

- [Docker](https://docs.docker.com/get-docker/)
- [Colima (Only for MacOS)](https://github.com/abiosoft/colima)

At least 4GB RAM available for containers

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone git@github.com:migush/ClipClap-Factory.git
cd ClipClap-Factory
```

### 2. Start n8n and crawl4ai

#### MacOS Users: Use Colima
```bash
chmod +x start_colima.sh
./start_colima.sh
```

This script:
- Stops any running Colima instance
- Starts a new Colima environment with 2 CPUs and 4GB RAM
- Mounts your project directories for file sharing

### 3. Windows/Linux

```bash
docker-compose up -d
```


This will start:
- **n8n** on `http://localhost:5678`
- **crawl4ai** on `http://localhost:11235`

### 4. Access n8n

1. Open your browser and navigate to `http://localhost:5678`
2. Complete the initial n8n setup
3. Import the workflow from `workflow.json`

### 5. Configure API Keys (Not Implemented Yet)

[//]: # (Create a `.env` file in the project root:)

[//]: # ()
[//]: # (```env)

[//]: # (# RunwayML API Key &#40;for video generation&#41;)

[//]: # (RUNWAY_API_KEY=your_runway_api_key_here)

[//]: # ()
[//]: # (# Social Media API Keys &#40;for posting&#41;)

[//]: # (INSTAGRAM_ACCESS_TOKEN=your_instagram_token)

[//]: # (TIKTOK_ACCESS_TOKEN=your_tiktok_token)

[//]: # (YOUTUBE_API_KEY=your_youtube_api_key)

[//]: # ()
[//]: # (# Optional: OpenAI API Key &#40;alternative to Ollama&#41;)

[//]: # (OPENAI_API_KEY=your_openai_key)

[//]: # (```)

## 📁 Project Structure

```
ClipClap-Factory/
├── docker-compose.yml           # Container orchestration
├── start_colima.sh              # Colima startup script
├── workflow.json                # Main workflow
├── files/                       # Generated content storage (mouted)
└── .n8n/                        # n8n configuration (mounted)
```

## 🔧 Current Workflow

The existing workflow (`workflow.json`) performs:

1. **Content Discovery**: Scrapes AI news from TLDR.tech
2. **AI Processing**: Uses Ollama to generate video scripts
3. **Content Storage**: Saves generated scripts to `files/` directory

## 🎬 Usage

### Running the Current Workflow

1. Open n8n at `http://localhost:5678`
2. Create a new workflow and import `workflow.json`
3. Navigate to the imported workflow
4. Make necessary adjustments (e.g., API keys)
5. Execute Workflow
6. Check the `files/` directory for generated content


## 🚧 Development Roadmap

### Phase 1: Foundation & Content Discovery ✅
- [x] **Infrastructure Setup**: Docker containers for n8n and crawl4ai
- [x] **Content Scraping**: Automated scraping from TLDR.tech AI section
- [x] **AI Integration**: Ollama local AI model for content processing
- [x] **Workflow Automation**: n8n workflow for content discovery and processing
- [x] **File Management**: Automated file generation and storage system

### Phase 2: Content Generation & Processing ✅
- [x] **AI-Powered Script Generation**: Automated script creation from scraped content
- [x] **Image Generation**: AI-generated images for video content (OpenAI API integration)
- [x] **Video Generation**: Automated video creation with Kling AI
- [x] **Content Processing Pipeline**: End-to-end content transformation workflow

### Phase 3: Video Enhancement & Production 🔄
- [ ] **Text-to-Speech Integration**: Automated voice-over generation
- [ ] **Background Music**: AI-generated or curated background music
- [ ] **Caption Overlay System**: Automated subtitle generation and placement
- [ ] **Video Editing**: Automated trimming, transitions, and effects
- [ ] **Quality Optimization**: Video compression and format optimization

### Phase 4: Multi-Platform Publishing 🎯
- [ ] **Instagram Integration**: Automated posting to Instagram Reels
- [ ] **TikTok API Integration**: Automated posting to TikTok
- [ ] **YouTube Shorts**: Automated posting to YouTube Shorts
- [ ] **Cross-Platform Optimization**: Platform-specific video formatting
- [ ] **Scheduling System**: Intelligent posting time optimization

### Phase 5: Advanced Automation & Intelligence 🚀
- [ ] **Trending Topic Discovery**: AI-powered trend analysis
- [ ] **Content Performance Analytics**: Automated performance tracking
- [ ] **Viral Prediction**: AI algorithms for content virality prediction
- [ ] **A/B Testing**: Automated content variation testing
- [ ] **Audience Engagement**: Automated response and interaction management

### Phase 6: Enterprise Features & Scaling 🌟
- [ ] **Multi-Account Management**: Support for multiple social media accounts
- [ ] **Content Calendar**: Advanced scheduling and content planning
- [ ] **Team Collaboration**: Multi-user workflow management
- [ ] **Advanced Analytics**: Comprehensive reporting and insights
- [ ] **API Integration**: Third-party service integrations

### Current Status: Phase 2 Complete ✅
The system currently successfully:
- Scrapes trending AI content from TLDR.tech
- Generates AI-powered scripts using Ollama
- Creates AI-generated images using OpenAI
- Produces videos using Kling AI
- Stores all generated content automatically

**Next Milestone**: Phase 3 - Adding audio, music, and caption features to complete the video production pipeline.

## 🔧 Configuration (Not Implemented Yet)

### Environment Variables (Not Implemented Yet)

|----------|-------------|----------|
| Variable | Description | Required |
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

#### Colima won't start
   ```bash
   # Check if Docker is running
   docker ps
   
   # Restart Colima
   colima stop
   colima start --cpu 2 --memory 4
   ```

#### n8n not accessible
   ```bash
   # Check if containers are running
   docker-compose ps
   
   # Restart services
   docker-compose down
   docker-compose up -d
   ```

### Logs

View container logs:
```bash
# n8n logs
docker-compose logs n8n

# crawl4ai logs
docker-compose logs crawl4ai
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [n8n](https://n8n.io/) for workflow automation
- [crawl4ai](https://github.com/unclecode/crawl4ai) for web scraping
- [Ollama](https://ollama.ai/) for local AI processing
- [Docker](https://www.docker.com/) for containerization
- [Colima](https://github.com/abiosoft/colima) for local Docker on macOS


## 📞 Support

For questions or issues:
1. Review n8n documentation
2. Review crawl4ai documentation
3. Review Ollama documentation
4. Review Docker documentation
5. Review Colima documentation
6. Open an issue on GitHub

---

**Happy automating! 🚀** 