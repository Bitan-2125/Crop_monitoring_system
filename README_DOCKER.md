# 🐳 Harvestify - Docker Deployment

> AI-powered agricultural recommendation system - Now fully Dockerized!

## 🚀 Quick Start (30 seconds)

```bash
# 1. Set up environment
cp app/.env.example app/.env
# Edit app/.env with your API keys

# 2. Run with Docker Compose
docker-compose up -d

# 3. Access app
# Open http://localhost:8000
```

That's it! 🎉

## 📋 What You Need

1. **Docker** - [Install Docker](https://docs.docker.com/get-docker/)
2. **API Keys** (free):
   - [OpenWeatherMap](https://openweathermap.org/api)
   - [Groq](https://console.groq.com/)
   - [Tavily](https://tavily.com/)

## 🎯 Deployment Options

### Option 1: Local Development (Docker Compose)

```bash
docker-compose up -d
```

**Pros:** Easy, fast, perfect for testing
**Access:** http://localhost:8000

### Option 2: Render (Recommended for Production)

1. Push to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Create Web Service → Connect repo → Select Docker
4. Add environment variables
5. Deploy!

**Pros:** Free tier, auto-deploy, SSL included
**Time:** 5 minutes

### Option 3: Railway (Fastest Deployment)

```bash
railway login
railway init
railway up
```

**Pros:** Fastest, great DX, simple CLI
**Time:** 2 minutes

### Option 4: Fly.io (Global Edge)

```bash
fly launch
fly deploy
```

**Pros:** Global deployment, low latency
**Time:** 3 minutes

## 📁 Project Structure

```
harvestify/
├── 🐳 Docker Files
│   ├── Dockerfile              # Main Docker image
│   ├── docker-compose.yml      # Local development
│   ├── .dockerignore          # Build optimization
│   └── start-docker.sh/bat    # Quick start scripts
│
├── ☁️ Deployment Configs
│   ├── render-docker.yaml     # Render deployment
│   ├── railway.json           # Railway deployment
│   └── fly.toml               # Fly.io deployment
│
├── 📚 Documentation
│   ├── DOCKER_QUICK_START.md  # Start here!
│   ├── DOCKER_DEPLOYMENT.md   # Detailed guide
│   ├── DEPLOYMENT_COMPARISON.md # Platform comparison
│   ├── DEPLOYMENT_SUMMARY.md  # Complete summary
│   └── COMMANDS.md            # Command reference
│
└── 🚀 Application
    └── app/
        ├── app.py             # Main Flask app
        ├── requirements.txt   # Dependencies
        ├── .env.example       # Environment template
        ├── models/            # ML models
        ├── Data/              # Data files
        ├── static/            # Assets
        ├── templates/         # HTML templates
        └── utils/             # Utilities
```

## 🔑 Environment Variables

Create `app/.env`:

```env
WEATHER_API_KEY=your_openweathermap_key
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
```

## 🎨 Features

- 🌾 **Crop Recommendation** - ML-based crop suggestions
- 🦠 **Disease Detection** - Image-based plant disease identification
- 🧪 **Fertilizer Suggestion** - NPK-based fertilizer recommendations
- 💰 **Market Price Insight** - Real-time market price analysis
- 📅 **Smart Crop Planning** - AI-powered crop planning with charts

## 🛠️ Common Commands

```bash
# Start app
docker-compose up -d

# View logs
docker-compose logs -f

# Stop app
docker-compose down

# Rebuild
docker-compose up -d --build

# Check status
docker ps
```

## 📊 Platform Comparison

| Platform | Free Tier | Difficulty | Deploy Time |
|----------|-----------|------------|-------------|
| **Render** | ✅ 750hrs/mo | ⭐ Easy | 5 min |
| **Railway** | ✅ $5 credit | ⭐ Easy | 2 min |
| **Fly.io** | ✅ 3 VMs | ⭐⭐ Medium | 3 min |
| **Heroku** | ✅ Limited | ⭐ Easy | 5 min |

See `DEPLOYMENT_COMPARISON.md` for detailed comparison.

## 🔧 Troubleshooting

### Port already in use
```bash
docker-compose down
# Or use different port in docker-compose.yml
```

### Container won't start
```bash
docker logs harvestify-app
```

### Environment variables not working
```bash
# Check if .env exists
ls -la app/.env

# Verify in container
docker exec harvestify-app env | grep API_KEY
```

### Build fails
```bash
docker system prune -a
docker-compose build --no-cache
```

## 📚 Documentation

- **🚀 Quick Start**: `DOCKER_QUICK_START.md`
- **📖 Detailed Guide**: `DOCKER_DEPLOYMENT.md`
- **⚖️ Platform Comparison**: `DEPLOYMENT_COMPARISON.md`
- **📝 Command Reference**: `COMMANDS.md`
- **✅ Summary**: `DEPLOYMENT_SUMMARY.md`

## 🎓 Deployment Workflow

```
1. Test Locally
   ↓
   docker-compose up -d
   Test at localhost:8000
   
2. Push to GitHub
   ↓
   git push
   
3. Deploy to Cloud
   ↓
   Choose platform (Render recommended)
   Connect repository
   Add environment variables
   
4. Monitor & Iterate
   ↓
   Check logs
   Test features
   Fix issues
```

## ✅ Pre-Deployment Checklist

- [ ] Docker installed and running
- [ ] `app/.env` created with API keys
- [ ] Tested locally with Docker
- [ ] Model files present in `app/models/`
- [ ] Data files present in `app/Data/`
- [ ] Code pushed to GitHub
- [ ] Platform account created (Render/Railway/Fly.io)

## 🎯 Recommended Path

1. **Start Local**: Test with `docker-compose up -d`
2. **Deploy to Render**: Free tier, easy setup
3. **Monitor**: Check logs and test features
4. **Scale**: Upgrade or move to Railway/Fly.io when needed

## 💡 Pro Tips

- ✅ Always test locally first
- ✅ Use Docker Compose for development
- ✅ Monitor logs after deployment
- ✅ Keep API keys secure
- ✅ Update dependencies regularly
- ✅ Set up automated backups
- ✅ Use specific version tags in production

## 🆘 Need Help?

1. Check `DOCKER_QUICK_START.md` for quick solutions
2. See `DOCKER_DEPLOYMENT.md` for detailed troubleshooting
3. Review `COMMANDS.md` for command reference
4. Check platform-specific documentation

## 🌟 Success Criteria

Your deployment is successful when:
- ✅ App accessible via URL
- ✅ All pages load correctly
- ✅ Crop recommendation works
- ✅ Disease detection works
- ✅ Fertilizer suggestion works
- ✅ Market price insight works
- ✅ Crop planning works
- ✅ No errors in logs

## 📈 Next Steps

After successful deployment:

1. **Custom Domain**: Add your own domain
2. **Monitoring**: Set up error tracking (Sentry)
3. **Analytics**: Add Google Analytics
4. **CI/CD**: Automate deployments
5. **Scaling**: Configure auto-scaling
6. **Backup**: Set up automated backups
7. **Security**: Add rate limiting, CORS

## 🎉 You're Ready!

Everything is configured. Choose your deployment method:

- **Quick Test**: `docker-compose up -d`
- **Production**: Deploy to Render (easiest)
- **Fast Deploy**: Use Railway CLI
- **Global**: Deploy to Fly.io

Good luck! 🚀

---

**Made with ❤️ for farmers and developers**
