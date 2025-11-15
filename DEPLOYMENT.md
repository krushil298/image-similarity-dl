# Deployment Guide

This guide will help you deploy the Image Similarity Comparison System to various cloud platforms.

## Option 1: Render.com (Recommended - Free Tier)

Render offers free hosting with persistent deployments.

### Steps:

1. **Sign up at [render.com](https://render.com)**
   - Use your GitHub account for easy integration

2. **Create a New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `image-similarity-dl`
   - Select the repository

3. **Configure the Service**
   - **Name**: `image-similarity-dl`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`

4. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Your app will be live at: `https://image-similarity-dl.onrender.com`

### Important Notes:
- Free tier instances sleep after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- Model downloads on first run (~100MB)

---

## Option 2: Railway.app (Alternative - Free Tier)

Railway offers $5 free credit per month.

### Steps:

1. **Sign up at [railway.app](https://railway.app)**

2. **Deploy from GitHub**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `image-similarity-dl`

3. **Configure Environment**
   - Railway auto-detects Python
   - No additional configuration needed

4. **Generate Domain**
   - Go to Settings → Generate Domain
   - Your app will be live at: `https://[app-name].up.railway.app`

---

## Option 3: Heroku (Paid)

Heroku no longer offers free tier, but instructions included for reference.

### Steps:

1. **Install Heroku CLI**
   ```bash
   brew install heroku/brew/heroku  # macOS
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create image-similarity-dl
   ```

3. **Deploy**
   ```bash
   git push heroku master
   ```

4. **Open App**
   ```bash
   heroku open
   ```

---

## Local Testing Before Deployment

Test the production configuration locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run with gunicorn (production server)
gunicorn app:app

# Access at http://localhost:8000
```

---

## Environment Variables

No environment variables are required for basic deployment. All configuration is handled automatically.

---

## Troubleshooting

### Issue: Model Download Timeout
**Solution**: The first deployment may timeout while downloading ResNet50 (~100MB). The platform will retry automatically.

### Issue: Memory Limit Exceeded
**Solution**: Free tiers have memory limits. ResNet50 requires ~500MB RAM. Consider upgrading to paid tier if needed.

### Issue: Slow First Request
**Solution**: Free instances sleep after inactivity. Keep the app active or upgrade to paid tier for always-on instances.

### Issue: Upload Directory Errors
**Solution**: Ensure `uploads/` directory exists. The `.gitkeep` file maintains the directory structure.

---

## Cost Estimates

| Platform | Free Tier | Paid Tier |
|----------|-----------|-----------|
| Render   | Yes (sleeps after 15min) | $7/month |
| Railway  | $5 credit/month | Pay as you go |
| Heroku   | No | $7/month |

---

## Monitoring

### Render Dashboard
- View logs: Dashboard → Logs
- Monitor metrics: Dashboard → Metrics
- Check deployments: Dashboard → Events

### Railway Dashboard
- View logs: Project → Deployments → Logs
- Monitor usage: Project → Settings → Usage

---

## Updating the Deployment

After pushing changes to GitHub:

**Render**: Auto-deploys on every push to master
**Railway**: Auto-deploys on every push to master
**Heroku**: Manual push required (`git push heroku master`)

---

## Custom Domain (Optional)

### Render
1. Go to Settings → Custom Domain
2. Add your domain
3. Update DNS records as instructed

### Railway
1. Go to Settings → Domains
2. Add custom domain
3. Update DNS CNAME record

---

## Performance Optimization

For production deployments:

1. **Enable Caching**
   - Cache model in memory (already implemented)
   - Add Redis for response caching (optional)

2. **Use CDN**
   - Serve static files via CDN (Cloudflare, etc.)

3. **Upgrade Instance**
   - More RAM for faster processing
   - More CPU for concurrent requests

---

## Support

For deployment issues:
- Check platform status pages
- Review deployment logs
- Consult platform documentation

For application issues:
- Check GitHub Issues
- Review application logs
- Test locally first
