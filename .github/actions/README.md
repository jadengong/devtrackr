# DevTrackr CI/CD Workflows

This directory contains GitHub Actions workflows for automated testing, building, and deployment of the DevTrackr API.

## Workflows

### 1. Code Quality & Testing (`quality.yml`)
- **Triggers:** Push to main/develop, Pull requests
- **What it does:**
  - Code formatting checks (Black)
  - Linting (flake8)
  - Type checking (mypy)
  - Security scanning (bandit, safety)
  - Automated testing with coverage
  - Package building

### 2. Database Migrations (`migrations.yml`)
- **Triggers:** Changes to database models, manual dispatch
- **What it does:**
  - Migration validation
  - Schema change detection
  - Database backup creation
  - Migration status reporting

### 3. Deployment (`deploy.yml`)
- **Triggers:** Push to main, manual dispatch
- **What it does:**
  - Staging deployment (develop branch)
  - Production deployment (main branch)
  - Health checks
  - Rollback on failure
  - Deployment notifications

## How to Use

### Automatic Triggers
- **Push to develop:** Triggers staging deployment
- **Push to main:** Triggers production deployment
- **Any push:** Triggers code quality checks and testing

### Manual Triggers
1. Go to Actions tab in GitHub
2. Select the workflow you want to run
3. Click "Run workflow"
4. Choose the environment and click "Run workflow"

## Environment Setup

### Required Secrets
Set these in your GitHub repository settings:

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# Deployment (examples)
HEROKU_API_KEY=your_heroku_key
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
```

### Branch Protection
Enable branch protection rules:
- Require status checks to pass
- Require branches to be up to date
- Require pull request reviews

## Local Development

### Run Quality Checks Locally
```bash
# Install development dependencies
pip install black flake8 mypy bandit safety

# Run checks
black --check .
flake8 .
mypy .
bandit -r .
safety check
```

### Test Docker Build
```bash
# Build image
docker build -t devtrackr:test .

# Run container
docker run -p 8000:8000 devtrackr:test

# Test health endpoint
curl http://localhost:8000/health
```

## Troubleshooting

### Common Issues
1. **Tests failing:** Check test database connection
2. **Migration errors:** Verify database schema
3. **Deployment failures:** Check environment variables and secrets

### Debug Workflows
- Use `actions/upload-artifact` to save debug information
- Check workflow logs for detailed error messages
- Use `echo` statements for debugging in workflows

## Next Steps

1. **Configure deployment targets** (Heroku, AWS, etc.)
2. **Add monitoring and alerting**
3. **Implement blue-green deployments**
4. **Add performance testing**
5. **Set up automated rollbacks**
