# 🚀 Quick Start Guide

Get the AI Startup Survival Prediction Platform running in 3 minutes!

## ⚡ Super Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py

# 3. Open browser at http://localhost:8501
```

That's it! The app is now running. 🎉

## 📝 First Prediction in 30 Seconds

1. **Train Model** (on the main page)
   - ✅ Check "Use Sample Dataset (for demo)"
   - Click "🎯 Generate & Train with Sample Data"
   - Wait 5-10 seconds for training

2. **Make Prediction**
   - Scroll down to "Step 2: Predict Startup Survival"
   - Default values are already filled in
   - Click "🎯 Predict Survival"

3. **View Results**
   - See failure probability
   - Check health scores
   - Review AI recommendations
   - Get 30-60-90 day action plan

## 🎯 What You Get

### Instant Analysis
- **Failure Probability**: 0-100% risk score
- **Survival Timeline**: Estimated months to failure/success
- **Risk Level**: Low/Medium/High/Critical classification

### AI Insights
- **Health Scores**: Financial, Growth, Team, Market (0-100)
- **Feature Importance**: What drives the prediction
- **SHAP Analysis**: Transparent AI decision-making

### Actionable Recommendations
- **Priority Ranked**: Critical → Warning → Optimization
- **Specific Actions**: What to do immediately
- **Impact Clarity**: Expected outcomes
- **30-60-90 Day Plans**: Strategic roadmap

## 📊 Input Your Own Data

### Manual Entry
Fill in these 11 metrics:
- Monthly Burn Rate ($)
- Monthly Revenue ($)
- Total Funding Raised ($)
- Team Size
- Months Since Founding
- Monthly Growth Rate (%)
- Total Customers
- Market Competition (1-10)
- Team Experience (years)
- Number of Pivots
- Number of Investors

### CSV Upload
Create CSV with columns:
```
burn_rate,revenue,funding_raised,team_size,months_since_founding,
monthly_growth_rate,customer_count,market_competition,
team_experience,pivots_count,investor_count
```

See `data/sample_data.csv` for example.

## 🌐 Deploy to Cloud (Optional)

### Streamlit Cloud (Free)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Click "Deploy"
5. Get public URL in 2-3 minutes

### Local Development
```bash
# Run with auto-reload
streamlit run app.py --server.runOnSave=true

# Run on different port
streamlit run app.py --server.port=8502
```

## 🔧 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt --upgrade
```

### Port already in use
```bash
streamlit run app.py --server.port=8502
```

### SHAP warnings
These are normal and don't affect functionality. The app still works perfectly.

## 📚 Need More Help?

- **README.md**: Complete user guide
- **DEPLOYMENT.md**: Detailed deployment instructions
- **PROJECT_SUMMARY.md**: Technical architecture

## 💡 Pro Tips

1. **Use Sample Data First**: Get familiar with the platform
2. **Try Different Models**: XGBoost vs Random Forest
3. **Experiment with Inputs**: See how metrics affect predictions
4. **Export Results**: Download CSV for batch predictions
5. **Review Action Plans**: Implement the recommendations

## 🎉 You're Ready!

Your AI-powered startup survival prediction platform is now operational.

**Like Tesla Autopilot for Startups - Predict failures, prevent disasters!** 🚀💎

---

*For detailed documentation, see README.md*  
*For deployment help, see DEPLOYMENT.md*
