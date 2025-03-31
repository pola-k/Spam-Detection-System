# Spam Detection System

## 📌 Overview
The **Spam Detection System** is a web-based application designed to classify emails as **spam** or **not spam** using machine learning techniques. The system comprises a **React** frontend and a **Flask** backend that hosts the trained machine learning model.

## 🚀 Features
- **Real-time email classification**: Instantly determines whether an email is spam or not.
- **Modern dark-themed UI**: Provides a sleek user interface with notifications.
- **Machine learning-based text classification**: Utilizes advanced algorithms for accurate predictions.
- **Asynchronous communication**: Employs the Fetch API for seamless frontend-backend interactions.
- **Dynamic notification system**: Displays notifications with color coding (🔴 Red for spam, 🟢 Green for not spam).

## 🏗️ Tech Stack
- **Frontend**: React (Vite), JavaScript, CSS
- **Backend**: Flask (Python)
- **Machine Learning Model**: Scikit-learn (Random Forest Classifier)

## 📂 Project Structure
```
Spam-Detection-System/
├── backend/                        # Flask-based backend
│   ├── app.py                      # Main Flask application
│   ├── model.pkl                   # Serialized machine learning model
│   ├── requirements.txt            # Backend dependencies
│   ├── spam_classifier.pkl         # Additional model file
│   ├── spam_classifier_lemmatizer.pkl  # Lemmatizer model file
│   ├── spam_classifier_scaler.pkl      # Scaler model file
│   ├── spam_classifier_spell_checker.pkl  # Spell checker model file
│   └── tfidf_spam_classifier.pkl   # TF-IDF vectorizer model file
│
├── frontend/                       # React-based frontend
│   ├── src/
│   │   ├── App.js                  # Main React component
│   │   ├── App.css                 # Component-specific styles
│   │   ├── index.js                # Application entry point
│   │   └── ...                     # Other React components and assets
│   ├── public/                     # Static assets
│   │   ├── index.html              # Main HTML file
│   │   └── ...                     # Other static files
│   ├── package.json                # Frontend dependencies and scripts
│   └── ...                         # Additional configuration files
│
├── Spam and Ham Detection System.ipynb  # Jupyter Notebook for model training and evaluation
├── README.md                       # Project documentation
└── .gitignore                      # Specifies files to ignore in version control
```

## 🎯 Installation & Usage

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/pola-k/Spam-Detection-System.git
cd Spam-Detection-System
```

### 2️⃣ Backend Setup (Flask API)
Navigate to the `backend` directory:
```bash
cd backend
```
Install the dependencies individually:
```bash
pip install Flask==3.0.3
pip install joblib==1.4.2
pip install numpy==1.24.4
pip install scipy==1.10.1
pip install nltk==3.9.1
pip install scikit-learn==1.3.2
pip install pyspellchecker==0.8.2
```

Start the Flask server:
```bash
python app.py
```
The backend will be running at: `http://127.0.0.1:5000/`

### 3️⃣ Frontend Setup (React)
Navigate to the `frontend` directory:
```bash
cd ../frontend
```
Install the npm packages:
```bash
npm install
```
Start the development server:
```bash
npm run dev
```
The frontend will be available at: `http://localhost:5173/`

## 📡 API Endpoint
### 🔹 `POST /predict`
- **Description**: Predicts whether an email is spam or not.
- **Request Body**:
  ```json
  {
    "email_text": "Your email content here..."
  }
  ```
- **Response**:
  ```json
  {
    "prediction": "spam"  // or "not spam"
  }
  ```

## 🛠️ Troubleshooting
- **CORS Issues**: If you encounter Cross-Origin Resource Sharing (CORS) issues, ensure that the Flask backend allows requests from the frontend. You can use the `flask-cors` package to handle this:
  ```python
  from flask_cors import CORS
  CORS(app)
  ```
  Install the package if it's not already included:
  ```bash
  pip install flask-cors
  ```

- **Module Import Errors in VSCode**: If Visual Studio Code cannot import installed packages, ensure that:
  - The correct Python interpreter is selected (matching your virtual environment).
  - The virtual environment is activated in the terminal.
  - The `PYTHONPATH` includes the directory containing the installed packages.

- **Inconsistent Version Warnings**: If you receive warnings about version inconsistencies when unpickling the model (e.g., `InconsistentVersionWarning`), ensure that the version of `scikit-learn` used to train the model matches the version used in the backend. Consider retraining the model with the current version or downgrading `scikit-learn` to match the version used during training.

- **CORS Policy Errors in Frontend**: If the frontend encounters CORS policy errors when making requests to the backend, ensure that the backend includes the appropriate CORS headers, as shown above.

## 👤 Author
**Sameer Khawar**  
GitHub: [@pola-k](https://github.com/pola-k)
