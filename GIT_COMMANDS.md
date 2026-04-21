# 📦 Git Commands for Deployment

## 🚀 Quick Deploy (Copy & Paste)

```bash
# Add all changes
git add .

# Commit with message
git commit -m "Add Docker deployment configuration"

# Push to GitHub
git push
```

That's it! Now connect your repo to Render/Railway/Fly.io.

## 📋 Detailed Git Workflow

### First Time Setup

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit with Docker deployment"

# Add remote repository (replace with your URL)
git remote add origin https://github.com/yourusername/harvestify.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Regular Updates

```bash
# Check what changed
git status

# Add specific files
git add Dockerfile docker-compose.yml

# Or add all changes
git add .

# Commit with descriptive message
git commit -m "Update Docker configuration"

# Push to GitHub
git push
```

## 📝 Good Commit Messages

### For Docker Setup
```bash
git commit -m "Add Docker deployment configuration

- Add Dockerfile with Python 3.11.9
- Add docker-compose.yml for local development
- Add deployment configs for Render, Railway, Fly.io
- Update Python version and dependencies
- Fix file paths for Docker compatibility"
```

### For Bug Fixes
```bash
git commit -m "Fix matplotlib compatibility issue

- Update matplotlib from 3.7.5 to 3.8.4
- Fix Python version to 3.11.9
- Resolve SafeConfigParser error"
```

### For Features
```bash
git commit -m "Add market price insight feature

- Implement Tavily search integration
- Add Groq vision analysis
- Create market price result page"
```

## 🔍 Check Before Committing

```bash
# See what changed
git status

# See detailed changes
git diff

# See changes in specific file
git diff app/app.py

# See staged changes
git diff --staged
```

## ⚠️ Important: Don't Commit Secrets!

### Check .gitignore includes:
```bash
# View .gitignore
cat .gitignore

# Should include:
# .env
# *.env
# app/.env
```

### If you accidentally committed .env:
```bash
# Remove from git but keep locally
git rm --cached app/.env

# Commit the removal
git commit -m "Remove .env from git"

# Push
git push
```

## 🌿 Branch Management

### Create Feature Branch
```bash
# Create and switch to new branch
git checkout -b docker-deployment

# Make changes, then commit
git add .
git commit -m "Add Docker configuration"

# Push branch to GitHub
git push -u origin docker-deployment
```

### Merge to Main
```bash
# Switch to main
git checkout main

# Merge feature branch
git merge docker-deployment

# Push to GitHub
git push

# Delete feature branch (optional)
git branch -d docker-deployment
```

## 🔄 Sync with Remote

### Pull Latest Changes
```bash
# Pull from GitHub
git pull

# Or fetch and merge separately
git fetch
git merge origin/main
```

### Handle Conflicts
```bash
# If there are conflicts after pull
# 1. Open conflicted files
# 2. Resolve conflicts manually
# 3. Add resolved files
git add .

# 4. Commit the merge
git commit -m "Resolve merge conflicts"

# 5. Push
git push
```

## 🔙 Undo Changes

### Undo Local Changes (Not Committed)
```bash
# Discard changes in specific file
git checkout -- app/app.py

# Discard all local changes
git checkout -- .
```

### Undo Last Commit (Keep Changes)
```bash
# Undo commit but keep changes
git reset --soft HEAD~1

# Make more changes, then commit again
git add .
git commit -m "Better commit message"
```

### Undo Last Commit (Discard Changes)
```bash
# WARNING: This deletes changes!
git reset --hard HEAD~1
```

### Undo Pushed Commit
```bash
# Create reverse commit
git revert HEAD

# Push the revert
git push
```

## 📊 View History

```bash
# View commit history
git log

# View compact history
git log --oneline

# View last 5 commits
git log -5

# View changes in each commit
git log -p

# View commits by author
git log --author="Your Name"
```

## 🏷️ Tags (For Releases)

```bash
# Create tag
git tag -a v1.0.0 -m "Version 1.0.0 - Docker deployment"

# Push tag to GitHub
git push origin v1.0.0

# Push all tags
git push --tags

# List tags
git tag

# Delete tag
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
```

## 🔧 Configuration

### Set Your Identity
```bash
# Set name
git config --global user.name "Your Name"

# Set email
git config --global user.email "your.email@example.com"

# View config
git config --list
```

### Useful Aliases
```bash
# Create shortcuts
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit

# Now you can use:
git st    # instead of git status
git co    # instead of git checkout
git br    # instead of git branch
git ci    # instead of git commit
```

## 🚨 Emergency Commands

### Forgot to Add Files
```bash
# Add forgotten files
git add forgotten-file.txt

# Amend last commit
git commit --amend --no-edit

# Force push (if already pushed)
git push --force
```

### Wrong Branch
```bash
# Move uncommitted changes to new branch
git stash
git checkout correct-branch
git stash pop
```

### Accidentally Deleted Files
```bash
# Restore deleted file
git checkout HEAD -- deleted-file.txt
```

## 📦 For Deployment

### Deploy to Render
```bash
# Just push to main branch
git push

# Render auto-deploys from main
```

### Deploy to Railway
```bash
# Push to GitHub first
git push

# Then use Railway CLI
railway up
```

### Deploy to Fly.io
```bash
# Commit changes
git add .
git commit -m "Update for Fly.io"

# Deploy with Fly CLI
fly deploy
```

## ✅ Pre-Push Checklist

Before pushing to GitHub:

```bash
# 1. Check status
git status

# 2. Check what you're committing
git diff

# 3. Make sure .env is not included
git status | grep .env
# Should show nothing or "Untracked files"

# 4. Test locally
docker-compose up -d
# Test at http://localhost:8000

# 5. If all good, push
git push
```

## 🎯 Complete Deployment Workflow

```bash
# 1. Make changes to your code
# ... edit files ...

# 2. Test locally
docker-compose up -d
# Test at http://localhost:8000
docker-compose down

# 3. Check changes
git status
git diff

# 4. Stage changes
git add .

# 5. Commit with good message
git commit -m "Add new feature: market price insight"

# 6. Push to GitHub
git push

# 7. Deploy to platform
# Render: Auto-deploys from GitHub
# Railway: railway up
# Fly.io: fly deploy
```

## 📚 Learn More

```bash
# Get help for any command
git help <command>
git help commit
git help push

# Or use --help flag
git commit --help
```

## 🆘 Common Issues

### "Permission denied (publickey)"
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Add public key to GitHub
cat ~/.ssh/id_ed25519.pub
# Copy output and add to GitHub Settings → SSH Keys
```

### "Repository not found"
```bash
# Check remote URL
git remote -v

# Update remote URL
git remote set-url origin https://github.com/yourusername/harvestify.git
```

### "Failed to push"
```bash
# Pull first
git pull --rebase

# Then push
git push
```

### "Merge conflict"
```bash
# See conflicted files
git status

# Open files and resolve conflicts
# Look for <<<<<<< HEAD markers

# After resolving
git add .
git commit -m "Resolve merge conflicts"
git push
```

## 💡 Pro Tips

1. **Commit often**: Small, frequent commits are better
2. **Write good messages**: Explain what and why
3. **Test before pushing**: Always test locally first
4. **Use branches**: For new features or experiments
5. **Pull before push**: Avoid conflicts
6. **Never commit secrets**: Use .env and .gitignore
7. **Tag releases**: Use semantic versioning (v1.0.0)

## 🎉 Ready to Deploy!

```bash
# Final deployment commands
git add .
git commit -m "Add Docker deployment configuration"
git push

# Then deploy to your chosen platform!
```

---

**Quick Reference Card**

```bash
git status          # Check status
git add .           # Stage all changes
git commit -m "msg" # Commit with message
git push            # Push to GitHub
git pull            # Pull from GitHub
git log             # View history
git diff            # See changes
```
