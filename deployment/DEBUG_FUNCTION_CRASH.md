# Debugging Vercel Function Crash

## 🚨 Current Issue: FUNCTION_INVOCATION_FAILED

You're getting a `500: INTERNAL_SERVER_ERROR` with `FUNCTION_INVOCATION_FAILED`. This means:
- ✅ Vercel is working
- ✅ Your connection is working  
- ✅ The deployment succeeded
- ❌ Your function is crashing when it tries to execute

## 🔧 Step-by-Step Debugging

### Step 1: Try Absolute Minimal Test

```bash
# Use the most basic possible function
python deployment/scripts/deploy-test.py test-minimal

# Commit and deploy
git add .
git commit -m "debug: test absolute minimal function"
git push
```

**Test:** `https://your-app.vercel.app/`
**Expected:** Simple "OK" response
**If this fails:** There's a fundamental Vercel/Python issue

### Step 2: Check Vercel Function Logs

1. Go to your Vercel dashboard
2. Click on your project
3. Go to "Functions" tab
4. Click on the failed function
5. Check the "Logs" section for specific error messages

**Look for:**
- Import errors
- Syntax errors
- Missing dependencies
- Python version issues

### Step 3: Try Enhanced Minimal Test

```bash
# Use the enhanced minimal function with error handling
python deployment/scripts/deploy-test.py minimal

git add .
git commit -m "debug: test enhanced minimal with error handling"
git push
```

**Test:** `https://your-app.vercel.app/`
**Expected:** JSON response with success or error details

### Step 4: Check Common Issues

#### Python Version
Vercel uses Python 3.9 by default. Check if you're using any Python 3.10+ features.

#### Import Issues
The function might be trying to import modules that don't exist in the Vercel environment.

#### Dependencies
Check if all required packages are in `api/requirements.txt`.

### Step 5: Test Locally

```bash
# Install Vercel CLI
npm i -g vercel

# Test locally
vercel dev
```

This will run your function locally and show any errors.

## 🎯 Most Likely Causes

1. **Missing dependencies** - Packages not in `api/requirements.txt`
2. **Import errors** - Trying to import modules that don't exist
3. **Python version mismatch** - Using features not available in Python 3.9
4. **Handler signature** - Wrong function signature for Vercel
5. **Path issues** - Relative imports not working in serverless environment

## 🔍 Debugging Commands

```bash
# Test absolute minimal
python deployment/scripts/deploy-test.py test-minimal

# Test enhanced minimal  
python deployment/scripts/deploy-test.py minimal

# Test simple FastAPI
python deployment/scripts/deploy-test.py simple

# Test full application
python deployment/scripts/deploy-test.py full
```

## 📝 What to Share

If you're still stuck, please share:
1. **Vercel function logs** (from the Functions tab)
2. **Which test level failed** (test-minimal, minimal, simple, full)
3. **Exact error message** from the logs
4. **Your current `vercel.json`** configuration

## 🚀 Quick Fixes to Try

1. **Check the logs first** - This will tell us exactly what's wrong
2. **Try test-minimal** - This is the simplest possible function
3. **Verify Python syntax** - Run `python -m py_compile api/test_minimal.py`
4. **Check requirements** - Make sure `api/requirements.txt` exists and has minimal deps

The logs will give us the exact error message we need to fix this!
