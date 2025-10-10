# Deployment Configuration

This directory contains all deployment-related files and configurations for DevTrackr API.

## 📁 Directory Structure

```
deployment/
├── configs/                    # Vercel deployment configurations
│   ├── vercel-minimal.json    # Minimal Python function test
│   └── vercel-simple.json     # Simple FastAPI test
├── scripts/                    # Deployment automation scripts
│   └── deploy-test.py         # Deployment testing script
├── VERCEL_DEPLOYMENT.md       # Complete deployment guide
├── VERCEL_TROUBLESHOOTING.md  # Troubleshooting guide
└── README.md                  # This file
```

## 🚀 Quick Start

### Testing Different Configurations

Use the deployment script to test different configurations:

```bash
# Test minimal Python function
python deployment/scripts/deploy-test.py minimal

# Test simple FastAPI
python deployment/scripts/deploy-test.py simple

# Test full application
python deployment/scripts/deploy-test.py full
```

### Manual Configuration

```bash
# Copy minimal config
cp deployment/configs/vercel-minimal.json vercel.json

# Copy simple config
cp deployment/configs/vercel-simple.json vercel.json
```

## 📚 Documentation

- **VERCEL_DEPLOYMENT.md** - Complete deployment guide with database setup
- **VERCEL_TROUBLESHOOTING.md** - Step-by-step debugging for deployment issues

## 🔧 Configuration Files

### vercel-minimal.json
- Tests basic Python functionality on Vercel
- Uses `api/hello.py` (no FastAPI dependencies)
- Minimal configuration for debugging

### vercel-simple.json
- Tests FastAPI on Vercel
- Uses `api/simple.py` (minimal FastAPI app)
- Good for testing FastAPI compatibility

### vercel.json (main)
- Full application configuration
- Uses `api/index.py` (complete DevTrackr API)
- Requires database and environment variables

## 🐛 Troubleshooting

If deployment fails:

1. **Try minimal configuration first** - Tests if Python works on Vercel
2. **Check Vercel logs** - Look for specific error messages
3. **Verify environment variables** - Database URL and secrets
4. **Test locally** - Use `vercel dev` to test locally

## 📝 Usage Examples

```bash
# Deploy with minimal configuration
python deployment/scripts/deploy-test.py minimal
git add . && git commit -m "test: minimal deployment" && git push

# Deploy with simple FastAPI
python deployment/scripts/deploy-test.py simple
git add . && git commit -m "test: simple fastapi" && git push

# Deploy full application (requires database setup)
python deployment/scripts/deploy-test.py full
git add . && git commit -m "deploy: full application" && git push
```

## 🎯 Testing Endpoints

After deployment, test these endpoints:

- **Minimal**: `https://your-app.vercel.app/`
- **Simple**: `https://your-app.vercel.app/simple/`
- **Full**: `https://your-app.vercel.app/health`
