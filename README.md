
# 🫀 Heart Disease Prediction Project

This is a machine learning-based web application that predicts the likelihood of heart disease based on user input. The goal is to assist users and healthcare professionals in quickly identifying potential heart-related health risks.

---

## 💡 Project Overview

Using a dataset of patient health metrics, this model predicts whether a person is likely to suffer from heart disease. The project combines data analysis, model training, and a Flask web interface to make predictions interactive and accessible.

---

## 🚀 Features

- 📊 Data visualization and analysis
- 🧠 Trained machine learning model (`.model` file)
- 🌐 Web interface using Flask
- 📝 User-friendly form to enter patient details
- 📁 Database to store predictions (SQLite)

---

## 🖥️ Tech Stack

- **Languages**: Python, HTML, CSS
- **Libraries**: pandas, scikit-learn, Flask, sqlite3
- **Tools**: Jupyter Notebook, VS Code, Git
- **Database**: SQLite
- **Model**: Logistic Regression *(or the actual model used)*

---

## 📂 Project Structure

```
heart-disease-prediction/
├── Heart Data/                   # Dataset and notebook
├── models/                       # Trained ML model
├── templates/                    # HTML pages
├── static/                       # Static assets (PDF reports)
├── app.py                        # Main Flask app
├── create_predictions_table.py  # Script to create SQLite table
├── data base file/              # Database folder
├── monicaheart.db               # SQLite database
└── README.md                    # Project overview
```

---

## ⚙️ How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/alipkfr/heart-disease-prediction.git

# 2. Navigate to the project directory
cd heart-disease-prediction

# 3. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # on macOS/Linux
venv\Scripts\activate     # on Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 📊 Dataset

- **Name**: `Heart_Disease_Prediction.csv`
- **Source**: *Manually added / Kaggle / UCI (choose one)*

---

## 👤 Author

**Ali Badr**  
🧑‍💻 Software Engineering Graduate  
📍 Egypt | Russia  
📫 Email: ali.abdallah.badr11@gmail.com  
🌐 Portfolio: [View Portfolio](https://port-ai-folio-builder.lovable.app/#contact)  
🔗 LinkedIn: [Ali Abdallah](https://www.linkedin.com/in/ali-abdallah-16064a319/)  
📂 GitHub: [alipkfr](https://github.com/alipkfr)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgments

Thanks to everyone who supported this project and inspired me to build real-world applications with ML and Python.
