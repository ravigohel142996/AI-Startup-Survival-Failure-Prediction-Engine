# Deployment Guide for AI Startup Survival Prediction Platform

## 🚀 Quick Deploy to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

### Step 1: Fork or Push Repository
```bash
# If you haven't already, push your code to GitHub
git add .
git commit -m "Complete AI Startup Survival Platform"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select:
   - **Repository**: `ravigohel142996/AI-Startup-Survival-Failure-Prediction-Engine`
   - **Branch**: `main` (or your branch name)
   - **Main file path**: `app.py`
5. Click "Deploy!"

### Step 3: Wait for Deployment
- Initial deployment takes 2-3 minutes
- You'll get a public URL like: `https://your-app-name.streamlit.app`

## 🔧 Local Development

### Setup
```bash
# Clone repository
git clone https://github.com/ravigohel142996/AI-Startup-Survival-Failure-Prediction-Engine.git
cd AI-Startup-Survival-Failure-Prediction-Engine

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

### Development Mode
```bash
# Run with auto-reload
streamlit run app.py --server.runOnSave=true

# Run on custom port
streamlit run app.py --server.port=8502
```

## 🐳 Docker Deployment (Optional)

### Create Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.headless=true"]
```

### Build and Run
```bash
# Build image
docker build -t startup-ai-platform .

# Run container
docker run -p 8501:8501 startup-ai-platform
```

## ☁️ Cloud Platform Deployments

### Heroku
1. Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.headless=true
```

2. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### AWS EC2
1. Launch EC2 instance (Ubuntu 20.04+)
2. SSH into instance
3. Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt
```
4. Run with PM2 or as service
5. Configure security group for port 8501

### Google Cloud Run
```bash
# Build and deploy
gcloud run deploy startup-ai \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 📊 Configuration

### Environment Variables (Optional)
Create `.streamlit/secrets.toml` for sensitive data:
```toml
[database]
# Add if using external database
host = "your-db-host"
user = "your-user"
password = "your-password"
```

### Custom Domain
1. In Streamlit Cloud, go to Settings
2. Add custom domain
3. Configure DNS CNAME record

## 🔒 Security Considerations

### Production Checklist
- [ ] Enable HTTPS (automatic on Streamlit Cloud)
- [ ] Add authentication if needed
- [ ] Rate limiting for API endpoints
- [ ] Input validation (already implemented)
- [ ] Error logging and monitoring
- [ ] Regular dependency updates

### Data Privacy
- Sample data is generated randomly
- No user data is stored by default
- All processing happens in-session
- Consider GDPR compliance for EU users

## 📈 Performance Optimization

### Tips for Large Scale
1. **Cache Model Training**:
```python
@st.cache_resource
def load_model():
    return StartupSurvivalModel.load('model.pkl')
```

2. **Use Pre-trained Models**:
- Train once, save model
- Load pre-trained model on startup
- Reduces cold start time

3. **Optimize Data Processing**:
- Use efficient pandas operations
- Vectorize calculations
- Limit SHAP computations for large datasets

## 🧪 Testing

### Run Tests
```bash
# Unit tests
python -c "from utils.data_processing import generate_sample_data; print('✅ Utils OK')"

# Integration test
python -c "
from model.predictor import train_model_from_data
from utils.data_processing import generate_sample_data
df = generate_sample_data(100)
model, metrics = train_model_from_data(df)
print(f'✅ Model trained: {metrics[\"accuracy\"]:.2%} accuracy')
"
```

### Load Testing
```bash
# Install locust
pip install locust

# Create locustfile.py and run
locust -f locustfile.py --host=http://localhost:8501
```

## 📞 Support & Monitoring

### Monitoring Tools
- **Streamlit Cloud**: Built-in analytics
- **Google Analytics**: Add tracking code
- **Sentry**: Error tracking
- **New Relic**: APM monitoring

### Logs
```bash
# View Streamlit logs
streamlit run app.py --logger.level=debug

# In production, logs available in platform dashboard
```

## 🔄 CI/CD Pipeline

### GitHub Actions (Optional)
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: python test_app.py
```

## 🎯 Production Checklist

Before going live:
- [x] All features implemented
- [x] UI tested and responsive
- [x] Model performance validated
- [x] Error handling in place
- [x] Documentation complete
- [ ] Custom domain configured
- [ ] Analytics setup
- [ ] Monitoring enabled
- [ ] Backup strategy defined
- [ ] User feedback mechanism

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [XGBoost Documentation](https://xgboost.readthedocs.io)
- [SHAP Documentation](https://shap.readthedocs.io)
- [Deployment Best Practices](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)

---

**Questions?** Open an issue on GitHub or contact support.
