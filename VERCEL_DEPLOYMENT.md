# Vercel Deployment Guide for DevTrackr API

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install with `npm i -g vercel`
3. **Database**: Set up a PostgreSQL database (recommended: [Neon](https://neon.tech), [Supabase](https://supabase.com), or [Railway](https://railway.app))

## Deployment Steps

### 1. **Set up Environment Variables in Vercel**

In your Vercel dashboard, go to your project settings and add these environment variables:

```bash
# Database (REQUIRED)
DATABASE_URL=postgresql://username:password@host:port/database

# Security (REQUIRED - change this!)
SECRET_KEY=your-super-secret-key-here-change-this

# Optional Configuration
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=*
LOG_LEVEL=INFO
ENVIRONMENT=production
```

### 2. **Deploy to Vercel**

#### Option A: Using Vercel CLI
```bash
# Install Vercel CLI (if not already installed)
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# For production deployment
vercel --prod
```

#### Option B: Using Git Integration
1. Connect your GitHub repository to Vercel
2. Vercel will automatically deploy on every push to main branch

### 3. **Database Setup**

Since Vercel is serverless, you need an external database:

#### Recommended: Neon (Free PostgreSQL)
1. Go to [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string
4. Set as `DATABASE_URL` in Vercel environment variables

#### Alternative: Supabase
1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Go to Settings > Database
4. Copy the connection string
5. Set as `DATABASE_URL` in Vercel environment variables

### 4. **Run Database Migrations**

After deployment, you'll need to run database migrations. You can do this by:

1. **Using Vercel CLI**:
```bash
vercel env pull .env.local
alembic upgrade head
```

2. **Or create a migration script** (recommended for production):
   - Create a simple migration endpoint in your API
   - Call it once after deployment

## Important Notes

### ⚠️ **Database Considerations**
- Vercel functions are stateless and short-lived
- SQLite won't work reliably on Vercel (file system is read-only)
- Use PostgreSQL or another cloud database
- Consider connection pooling for production

### 🔧 **Function Limits**
- Vercel has execution time limits (10 seconds for Hobby plan)
- Consider breaking large operations into smaller functions
- Use background jobs for long-running tasks

### 🚀 **Performance Tips**
- Enable Vercel's Edge Functions for better performance
- Use Vercel's caching features
- Consider CDN for static assets

## Troubleshooting

### Common Issues:

1. **Function Timeout**: 
   - Check your database queries are optimized
   - Consider using connection pooling
   - Break down large operations

2. **Database Connection Issues**:
   - Verify `DATABASE_URL` is correctly set
   - Check database allows connections from Vercel IPs
   - Ensure database is running and accessible

3. **Import Errors**:
   - Check `vercel.json` configuration
   - Verify all dependencies are in `requirements.txt`
   - Ensure Python path is correctly set

4. **CORS Issues**:
   - Update `CORS_ORIGINS` environment variable
   - Check your frontend domain is allowed

## Testing Your Deployment

After deployment, test these endpoints:

```bash
# Health check
curl https://your-app.vercel.app/health

# API documentation
https://your-app.vercel.app/docs

# Alternative docs
https://your-app.vercel.app/redoc
```

## Production Checklist

- [ ] Database URL configured
- [ ] Secret key changed from default
- [ ] CORS origins configured for your domain
- [ ] Database migrations run
- [ ] Health check endpoint working
- [ ] API documentation accessible
- [ ] Error handling working
- [ ] Logging configured appropriately
