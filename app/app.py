from flask import Flask, jsonify, render_template_string
import os
import socket
import datetime

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 AWS ECS Deployment - DevOps Project</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        .container {
            text-align: center;
            padding: 50px 40px;
            background: rgba(255,255,255,0.05);
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            max-width: 700px;
            width: 90%;
            box-shadow: 0 25px 50px rgba(0,0,0,0.4);
            animation: fadeIn 1s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .badge {
            background: linear-gradient(135deg, #ff6b6b, #feca57);
            color: #1a1a2e;
            padding: 6px 18px;
            border-radius: 50px;
            font-size: 13px;
            font-weight: 700;
            display: inline-block;
            margin-bottom: 20px;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        h1 {
            font-size: 2.8em;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #a8edea, #fed6e3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle {
            font-size: 1.1em;
            color: rgba(255,255,255,0.6);
            margin-bottom: 40px;
        }
        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 30px 0;
            text-align: left;
        }
        .info-card {
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 15px 20px;
            transition: transform 0.2s;
        }
        .info-card:hover { transform: translateY(-3px); }
        .info-card .label {
            font-size: 11px;
            color: #a8edea;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }
        .info-card .value {
            font-size: 15px;
            font-weight: 600;
            color: white;
        }
        .status-dot {
            width: 10px; height: 10px;
            background: #2ecc71;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0%, 100% { box-shadow: 0 0 0 0 rgba(46,204,113,0.4); }
            50% { box-shadow: 0 0 0 8px rgba(46,204,113,0); }
        }
        .tech-stack {
            display: flex;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
            margin-top: 30px;
        }
        .tech-tag {
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            padding: 6px 16px;
            border-radius: 50px;
            font-size: 13px;
            font-weight: 500;
        }
        .footer {
            margin-top: 35px;
            font-size: 12px;
            color: rgba(255,255,255,0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="badge">✅ Deployment Successful</div>
        <h1>🚀 Hello from AWS ECS!</h1>
        <p class="subtitle">Your containerized application is live on Amazon ECS</p>

        <div class="info-grid">
            <div class="info-card">
                <div class="label">Status</div>
                <div class="value"><span class="status-dot"></span>Running</div>
            </div>
            <div class="info-card">
                <div class="label">Container Host</div>
                <div class="value">{{ hostname }}</div>
            </div>
            <div class="info-card">
                <div class="label">Environment</div>
                <div class="value">{{ env }}</div>
            </div>
            <div class="info-card">
                <div class="label">Server Time</div>
                <div class="value">{{ time }}</div>
            </div>
        </div>

        <div class="tech-stack">
            <span class="tech-tag">🐳 Docker</span>
            <span class="tech-tag">📦 AWS ECR</span>
            <span class="tech-tag">🎯 AWS ECS</span>
            <span class="tech-tag">⚖️ Load Balancer</span>
            <span class="tech-tag">⚙️ GitHub Actions</span>
        </div>

        <div class="footer">DevOps Internship Project — Deployed with ECS + ECR on AWS</div>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE,
        hostname=socket.gethostname(),
        env=os.environ.get("APP_ENV", "production"),
        time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

@app.route("/health")
def health():
    """Health check endpoint — used by AWS Load Balancer"""
    return jsonify({
        "status": "healthy",
        "hostname": socket.gethostname(),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
