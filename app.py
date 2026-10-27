from flask import Flask, render_template_string
import json
import csv
import io
from flask import Response

app = Flask(__name__)


@app.route("/")
def home():
    with open("security_events.json", "r") as file:
        events = json.load(file)

    for event in events:
        attempts = event["failed_attempts"]

        if attempts >= 5:
            event["severity"] = "HIGH"
        elif attempts >= 3:
            event["severity"] = "MEDIUM"
        else:
            event["severity"] = "LOW"
    total_events = len(events)
    high_alerts = sum(1 for event in events if event["severity"] == "HIGH")
    medium_alerts = sum(1 for event in events if event["severity"] == "MEDIUM")
    low_alerts = sum(1 for event in events if event["severity"] == "LOW")
    suspicious_ips = [
    event for event in events
    if event["severity"] == "HIGH"
]
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mini SOC Dashboard</title>
        <style>
            body {
                margin: 0;
                padding: 30px;
                background: #0f172a;
                color: #e2e8f0;
                font-family: Arial, sans-serif;
            }
            .summary-container {
    display: flex;
    gap: 20px;
    margin: 20px 0;
}

.summary-card {
    flex: 1;
    background: #1e293b;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #334155;
}

.summary-card h3 {
    color: #94a3b8;
    font-size: 16px;
}

.summary-card p {
    font-size: 28px;
    font-weight: bold;
}
            .summary-container {
    display: flex;
    gap: 20px;
    margin: 20px 0;
}

.summary-card {
    flex: 1;
    background: #1e293b;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #334155;
}

.summary-card h3 {
    margin-top: 0;
    color: #94a3b8;
}

.summary-card p {
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 0;
}

            h1 {
                color: #38bdf8;
            }

            .card {
                background: #1e293b;
                padding: 20px;
                margin: 20px 0;
                border-radius: 10px;
                border: 1px solid #334155;
            }

            table {
                width: 100%;
                border-collapse: collapse;
            }

            th, td {
                padding: 14px;
                text-align: left;
                border-bottom: 1px solid #334155;
            }

            th {
                color: #38bdf8;
            }

            .HIGH {
    display: inline-block;
    background: #7f1d1d;
    color: #fecaca;
    padding: 6px 12px;
    border-radius: 20px;
    font-weight: bold;
}

.MEDIUM {
    display: inline-block;
    background: #78350f;
    color: #fde68a;
    padding: 6px 12px;
    border-radius: 20px;
    font-weight: bold;
}

.LOW {
    display: inline-block;
    background: #14532d;
    color: #bbf7d0;
    padding: 6px 12px;
    border-radius: 20px;
    font-weight: bold;
}
        </style>
        <meta http-equiv="refresh" content="10">
    </head>

    <body>
        <h1>Mini SOC Dashboard</h1>
        <p>Security Operations Center | Monitoring Dashboard</p>
        <div class="summary-container">

    <div class="summary-card">
        <h3>Total Events</h3>
        <p>{{ total_events }}</p>
    </div>

    <div class="summary-card">
        <h3>High Alerts</h3>
        <p class="HIGH">{{ high_alerts }}</p>
    </div>

    <div class="summary-card">
        <h3>Medium Alerts</h3>
        <p class="MEDIUM">{{ medium_alerts }}</p>
    </div>
<div class="summary-card">
    <h3>Suspicious IP Alerts</h3>
    <p class="HIGH">{{ high_alerts }}</p>
</div>
</div>

 </div>

        <div class="card">
            <h2>System Status</h2>
            <p class="LOW">System is Running</p>
        </div>

        <div class="card">
        <h2>🚨 Suspicious IP Addresses</h2>

<table>
    <thead>
        <tr>
            <th>IP Address</th>
            <th>Failed Attempts</th>
            <th>Severity</th>
        </tr>
    </thead>
    <tbody>
        {% for event in suspicious_ips %}
        <tr>
            <td>{{ event["ip_address"] }}</td>
            <td>{{ event["failed_attempts"] }}</td>
            <td>
                <span class="HIGH">{{ event["severity"] }}</span>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
<h2>📊 Security Analytics</h2>

<div class="summary-container">
    <div class="summary-card">
        <h3>LOW Severity</h3>
        <p>{{ low_alerts }}</p>
    </div>

    <div class="summary-card">
        <h3>MEDIUM Severity</h3>
        <p>{{ medium_alerts }}</p>
    </div>

    <div class="summary-card">
        <h3>HIGH Severity</h3>
        <p>{{ high_alerts }}</p>
    </div>
</div>

    <div class="summary-card">
    <h3>Security Alerts Chart</h3>
<canvas id="securityChart" height="100" style="max-height: 300px;"></canvas>
</div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
const ctx = document.getElementById('securityChart');

new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['LOW', 'MEDIUM', 'HIGH'],
        datasets: [{
            label: 'Number of Alerts',
            data: [
                {{ low_alerts }},
                {{ medium_alerts }},
                {{ high_alerts }}
            ],
            backgroundColor: ['#22c55e', '#f59e0b', '#ef4444']
        }]
    },
    options: {
    responsive: true,
    maintainAspectRatio: false,scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    precision: 0
                }
            }
        }
    }
});
</script>
            <h2>Security Events</h2>
            <select id="severityFilter" onchange="filterSeverity()">
    <option value="ALL">All Severities</option>
    <option value="HIGH">High</option>
    <option value="MEDIUM">Medium</option>
    <option value="LOW">Low</option>
</select>

<input
    type="text"
    id="ipSearch"
    placeholder="Search IP address..."
    onkeyup="searchIP()"
>
            <table id="eventsTable">
                <tr>
                    <th>IP Address</th>
                    <th>Failed Attempts</th>
                    <th>Severity</th>
                </tr>

                {% for event in events %}
                <tr>
                    <td>{{ event["ip_address"] }}</td>
                    <td>{{ event["failed_attempts"] }}</td>
                    <td class="{{ event['severity'] }}">
                        {{ event["severity"] }}
                    </td>
                </tr>
                {% endfor %}
            </table>
        </div>
        <script>
    function searchIP() {
        let input = document.getElementById("ipSearch").value.toLowerCase();
        let rows = document.querySelectorAll("table tr");

        for (let i = 1; i < rows.length; i++) {
            let ip = rows[i].cells[0].textContent.toLowerCase();

            if (ip.includes(input)) {
                rows[i].style.display = "";
            } else {
                rows[i].style.display = "none";
            }
        }
    }
function filterSeverity() {
    let filter = document.getElementById("severityFilter").value;
    let rows = document.querySelectorAll("table tr");

    for (let i = 1; i < rows.length; i++) {
        let severity = rows[i].cells[2].textContent.trim().toUpperCase();

        if (filter === "ALL" || severity === filter) {
            rows[i].style.display = "";
        } else {
            rows[i].style.display = "none";
        }
    }
}

async function refreshSecurityEvents() {
    try {
        const response = await fetch("/api/events");

        if (!response.ok) {
            throw new Error("Failed to fetch security events");
        }

        const data = await response.json();
        const table = document.getElementById("eventsTable");

        if (!table) return;

        // Keep the table header and replace only event rows
        table.querySelectorAll("tr:not(:first-child)").forEach(row => row.remove());

        data.events.forEach(event => {
            const attempts = Number(event.failed_attempts);

            let severity = "LOW";
            if (attempts >= 5) {
                severity = "HIGH";
            } else if (attempts >= 3) {
                severity = "MEDIUM";
            }

            const row = table.insertRow();
            row.insertCell(0).textContent = event.ip_address;
            row.insertCell(1).textContent = attempts;

            const severityCell = row.insertCell(2);
            severityCell.className = severity;
            severityCell.textContent = severity;
        });

        // Reapply the current search and severity filter
        searchIP();
        filterSeverity();

    } catch (error) {
        console.error("Unable to refresh security events:", error);
    }
}

setInterval(refreshSecurityEvents, 5000);</script>

    </body>
    </html>
        """,
        events=events,
        total_events=total_events,
        high_alerts=high_alerts,
        medium_alerts=medium_alerts,
        low_alerts=low_alerts
    )


@app.route("/export")
def export_csv():
    with open("security_events.json", "r") as file:
        events = json.load(file)

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["IP Address", "Failed Attempts", "Severity"])

    for event in events:
        writer.writerow([
            event["ip_address"],
            event["failed_attempts"],
            "HIGH" if event["failed_attempts"] >= 5
       else "MEDIUM" if event["failed_attempts"] >= 3
       else "LOW"
        ])

    response = Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=security_report.csv"
        }
    )

    return response
@app.route("/api/events")
def get_live_events():
    with open("security_events.json", "r") as file:
        events = json.load(file)

    return {"events": events}
if __name__ == "__main__":
    app.run(debug=True)
