# 🚀 Kickstarter Campaign Success Predictor

A full-stack machine learning application that predicts the success of Kickstarter campaigns using Support Vector Machine (SVM) classification. The project includes complete data analysis, model training, and an interactive web dashboard built with Flask and Plotly.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0+-orange.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📊 Overview

This data-driven web application helps creators make informed decisions before launching their Kickstarter campaigns. By analyzing historical campaign data and leveraging machine learning, the system predicts whether a project is likely to succeed or fail based on key features like funding goals, campaign duration, and project metadata.

### **Key Highlights:**
- **Machine Learning Model:** Support Vector Machine (SVM) with **70% accuracy**
- **Dataset:** Analyzed thousands of real Kickstarter campaigns
- **Interactive Dashboard:** Real-time visualizations of market trends and success patterns
- **Feature Engineering:** Automated calculation of 25+ features from raw campaign data

---

## ✨ Features

### 🎯 **Prediction Engine**
- Real-time campaign success/failure prediction
- Intelligent feature extraction from campaign details
- Considers temporal, financial, and content-based factors

### 📈 **Interactive Dashboard**
- **Category Performance Analysis:** Success rates across different project categories
- **Funding Analysis:** Goal vs. Reality scatter plots with logarithmic scaling
- **Seasonal Trends:** Time-series visualization of success rates over months/years
- **Summary Statistics:** Total projects, categories, funding ranges

### 🎨 **Modern User Interface**
- Clean, Kickstarter-inspired design
- Responsive layout for desktop and mobile
- Animated metric cards with smooth transitions
- Professional glassmorphism effects

---

## 📁 Project Structure

```
DATA_COMPUTATION_FINAL/
│
├── Dockerfile                          # Docker configuration for production
├── .dockerignore                       # Files to exclude from Docker build
├── requirements.txt                    # Project dependencies
│
├── data/
│   └── kickstarter_data_with_features.csv    # Processed dataset
│
├── EDA_Modeling/
│   ├── Data_Computation.ipynb           # Jupyter notebook for EDA
│   └── kickstarter_model.pkl            # Serialized SVM model
│
└── kickstarter_app/
    ├── app.py                           # Flask backend (updated for Docker paths)
    ├── templates/                       # HTML interfaces
    └── static/                          # CSS/JS and assets
```

---

## 🧠 Machine Learning Model

### **Algorithm: Support Vector Machine (SVM)**

The model was trained using scikit-learn's SVM classifier with the following characteristics:

- **Model Type:** Support Vector Classification (SVC)
- **Accuracy:** **70%** on test data
- **Training Dataset:** ~200,000+ Kickstarter campaigns (2009-2017)
- **Features Used:** 25+ engineered features

### **Key Features Influencing Predictions:**

| Feature Category | Examples |
|-----------------|----------|
| **Financial** | Funding goal, USD exchange rate |
| **Content** | Project name length, blurb length, cleaned text metrics |
| **Temporal** | Launch date (year/month/day/hour/weekday), deadline, campaign duration |
| **Duration** | Create-to-launch days, launch-to-deadline days |
| **Metadata** | Country, currency, staff pick status, communication settings |

### **Feature Engineering Process:**

The backend automatically extracts and calculates:
- Date/time components from timestamps (weekday, hour, month, year)
- Duration calculations in days (create-to-launch, launch-to-deadline)
- Text metrics (name length, blurb length, cleaned versions)
- Categorical encodings (country, currency, staff pick)

---
## 🛠️ Installation & Setup
 
You can run this application using either **Docker** (recommended for production) or **manual installation** (recommended for development).
 
---
 
## 🐋 Docker Setup (Recommended)
 
### **Prerequisites:**
- Docker installed on your system ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose (optional, comes with Docker Desktop)
### **Option 1: Quick Start with Docker**
 
**Step 1: Clone the Repository**
```bash
git clone https://github.com/MalakMohammedAbouElFetouh/Data_Computation_Final_Project.git
cd Data_Computation_Final_Project
```
 
**Step 2: Build the Docker Image**
```bash
docker build -t kickstarter-predictor .
```
 
**Step 3: Run the Container**
```bash
docker run -d -p 5000:5000 --name kickstarter-app kickstarter-predictor
```
 
**Step 4: Access the Application**
Open your browser and navigate to:
```
http://localhost:5000/
```
 
### **Option 2: Using Docker Compose**
 
Create a `docker-compose.yml` file in the project root:
 
```yaml
version: '3.8'
 
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./EDA_Modeling:/app/EDA_Modeling
    environment:
      - FLASK_ENV=production
    restart: unless-stopped
```
 
Then run:
```bash
docker-compose up -d
```
 
### **Docker Commands Reference**
 
```bash
# Build the image
docker build -t kickstarter-predictor .
 
# Run container (detached mode)
docker run -d -p 5000:5000 --name kickstarter-app kickstarter-predictor
 
# Run container (interactive mode with logs)
docker run -p 5000:5000 --name kickstarter-app kickstarter-predictor
 
# View logs
docker logs kickstarter-app
 
# Follow logs in real-time
docker logs -f kickstarter-app
 
# Stop the container
docker stop kickstarter-app
 
# Start the container
docker start kickstarter-app
 
# Remove the container
docker rm kickstarter-app
 
# Access container shell
docker exec -it kickstarter-app /bin/bash
 
# Rebuild after code changes
docker build -t kickstarter-predictor . --no-cache
docker stop kickstarter-app && docker rm kickstarter-app
docker run -d -p 5000:5000 --name kickstarter-app kickstarter-predictor
```
 
### **Production Deployment with Docker**
 
For production environments:
 
```bash
# Build with production tag
docker build -t kickstarter-predictor:production .
 
# Run with resource limits and restart policy
docker run -d \
  -p 80:5000 \
  --name kickstarter-prod \
  --restart=always \
  --memory="512m" \
  --cpus="1.0" \
  kickstarter-predictor:production
```
 
### **Docker Environment Variables**
 
You can customize the application using environment variables:
 
```bash
docker run -d \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e FLASK_DEBUG=0 \
  --name kickstarter-app \
  kickstarter-predictor
```
 
---

## 💻 Manual Installation (Development)

### **Prerequisites:**
- Python 3.8 or higher
- pip (Python package manager)

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/MalakMohammedAbouElFetouh/Data_Computation_Final_Project.git
cd Data_Computation_Final_Project
```

### **Step 2: Create Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install flask pandas numpy scikit-learn plotly joblib
```

**Or use requirements.txt :**
```bash
pip install -r requirements.txt
```

### **Step 4: Verify Data Files**
Ensure these files exist:
- `data/kickstarter_data_with_features.csv` (dataset)
- `EDA_Modeling/kickstarter_model.pkl` (trained model)

### **Step 5: Run the Application**
```bash
cd kickstarter_app
python app.py
```

### **Step 6: Access the Web App**
Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

---

## 🎮 Usage

### **Making Predictions**

1. Navigate to the **Home Page** (`/`)
2. Fill in the campaign details:
   - **Project Name:** Title of your campaign
   - **Blurb:** Short description (elevator pitch)
   - **Funding Goal:** Target amount in USD
   - **Country:** Project location
   - **Launch Date:** Planned campaign start date
   - **Deadline:** Campaign end date
   - **Staff Pick:** Whether featured by Kickstarter staff
   - **Currency:** Campaign currency
3. Click **"Predict"**
4. View the prediction result (SUCCESS or FAILURE) with color-coded output

### **Viewing Market Insights**

1. Navigate to the **Dashboard** (`/dashboard`)
2. Explore three interactive visualizations:
   - **Category Performance:** Bar chart showing success rates by category
   - **Funding Goal vs. Reality:** Scatter plot comparing goals to pledged amounts
   - **Seasonal Success Windows:** Line chart tracking success trends over time
3. Interact with charts (zoom, pan, hover for details)

---

## 📊 Dashboard Visualizations

### **1. Category Performance**
- Ranks project categories by success rate
- Helps identify high-performing niches
- Green bars indicate success percentage

### **2. Funding Goal vs. Reality**
- Logarithmic scatter plot (handles wide value ranges)
- Diagonal reference line shows break-even point
- Color-coded: 🟢 Successful | 🔴 Failed

### **3. Seasonal Success Trends**
- Monthly success rate over years
- Identifies optimal launch windows
- Helps with timing strategy

---

## 🔬 Model Performance

### **Evaluation Metrics:**

```
Accuracy: 70%
```

**Interpretation:**
- The model correctly predicts campaign outcomes 7 out of 10 times
- Suitable for preliminary feasibility assessment
- Best used alongside market research and expert judgment

### **Limitations:**
- Trained on historical data (2009-2017); market dynamics may have changed
- Does not account for marketing efforts post-launch
- Cannot predict viral campaigns or black swan events


---
 
## 🐛 Troubleshooting
 
### **Docker Issues**
 
**Port already in use:**
```bash
# Use a different port
docker run -d -p 8080:5000 --name kickstarter-app kickstarter-predictor
# Access at http://localhost:8080
```
 
**Container fails to start:**
```bash
# Check logs
docker logs kickstarter-app
 
# Verify files exist
docker exec -it kickstarter-app ls -la /app/data
docker exec -it kickstarter-app ls -la /app/EDA_Modeling
```
 
**Permission issues:**
```bash
# Rebuild with proper permissions
docker build -t kickstarter-predictor . --no-cache
```
 
### **Manual Installation Issues**
 
**Module not found errors:**
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```
 
**Model file not found:**
```bash
# Verify file paths match app.py configuration
# Ensure kickstarter_model.pkl is in EDA_Modeling/
```
 
---

## 🚧 Future Improvements

- [ ] Implement advanced models (Random Forest, XGBoost, Neural Networks)
- [ ] Add text analysis of project descriptions using NLP
- [ ] Integrate real-time Kickstarter API data
- [ ] Deploy to cloud platform (Heroku, AWS, Google Cloud)
- [ ] Add user authentication and campaign tracking
- [ ] Implement A/B testing suggestions
- [ ] Create mobile-responsive Progressive Web App (PWA)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### **Areas for Contribution:**
- Model improvement (hyperparameter tuning, ensemble methods)
- Additional visualizations
- UI/UX enhancements
- Documentation improvements
- Bug fixes and code optimization

---

## 🙏 Acknowledgments

- **Kickstarter** for providing publicly available campaign data
- **scikit-learn** community for excellent ML tools
- **Plotly** for interactive visualization library
- **Flask** for lightweight web framework

---

## 📚 References

- [Kickstarter Stats](https://www.kickstarter.com/help/stats)
- [scikit-learn Documentation](https://scikit-learn.org/stable/)
- [Plotly Python Documentation](https://plotly.com/python/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## 📸 Screenshots

### Prediction Interface
![Prediction Form](https://github.com/user-attachments/assets/71746e81-dd00-4595-87bf-11ade87746c4)

*Clean interface for entering campaign details and receiving instant predictions*

### Analytics Dashboard
![Dashboard](https://github.com/user-attachments/assets/0034f60e-5132-4f0c-bb86-505fd41bec2e)

*Interactive visualizations of market trends and success patterns*

---

<div align="center">

**⭐ If you found this project helpful, please consider giving it a star! ⭐**

</div>
