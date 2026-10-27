# 🔐 Mini SOC – Security Monitoring Dashboard

A Flask-based Mini Security Operations Center (SOC) dashboard designed to monitor security events, identify suspicious IP addresses, classify alert severity, and generate security reports.

## 📌 Project Overview

The Mini SOC project provides a dashboard for analyzing sample security events based on failed login attempts. It helps users identify potentially suspicious activity through severity classification and visual analytics.

## ✨ Features

* **Security Dashboard:** Displays security event summaries.
* **Severity Detection:** Classifies events as LOW, MEDIUM, or HIGH.
* **Security Analytics:** Visualizes alert counts using a bar chart.
* **IP Address Search:** Searches events by IP address.
* **Severity Filter:** Filters events by alert severity.
* **CSV Export:** Downloads security event reports.
* **JSON Data Storage:** Reads sample security events from a JSON file.
* **Automatic Page Refresh:** Refreshes the dashboard periodically.

## 🛠️ Technologies Used

* Python
* Flask
* HTML
* CSS
* JavaScript
* Chart.js
* JSON
* CSV

## 📂 Project Structure

```text
Mini-SOC-Security-Monitor/
├── app.py
└── security_events.json
```

## ⚙️ How to Run

1. Install Python.

2. Install Flask:

   ```bash
   pip install flask
   ```

3. Clone or download this repository.

4. Open a terminal in the project folder.

5. Run the application:

   ```bash
   python app.py
   ```

6. Open this address in your browser:

   ```text
   http://127.0.0.1:5000
   ```

## 📊 Severity Classification

| Failed Login Attempts | Severity |
| --------------------- | -------- |
| Fewer than 3          | LOW      |
| 3–4                   | MEDIUM   |
| 5 or more             | HIGH     |

## 🧪 Testing

The dashboard can be tested using the sample events stored in `security_events.json`. Search, severity filtering, alert visualization, and CSV export can be checked using these sample records.

## 🚀 Future Improvements

* Integration with real security logs.
* Live event ingestion and monitoring.
* User authentication and access control.
* Additional security analytics and alert notifications.

## ⚠️ Disclaimer

This project is intended for educational purposes and uses sample security event data. It does not currently provide comprehensive real-world network monitoring or intrusion detection.

## 👩‍💻 Author

**Dhriti Singh**

B.Tech – Cybersecurity
