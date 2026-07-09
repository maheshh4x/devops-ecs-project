from flask import Flask, jsonify, request, render_template_string
import os
import socket
import datetime
import platform

app = Flask(__name__)
app_start_time = datetime.datetime.now()

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 AWS ECS Live Container Console</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #070913;
            --container-bg: rgba(13, 17, 33, 0.7);
            --border-color: rgba(99, 102, 241, 0.15);
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --primary: #6366f1;
            --primary-glow: rgba(99, 102, 241, 0.35);
            --accent-cyan: #06b6d4;
            --accent-teal: #10b981;
            --accent-amber: #f59e0b;
            --accent-rose: #f43f5e;
            --card-hover-border: rgba(6, 182, 212, 0.4);
            --glass-sheen: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.01));
            --trans-speed: 0.3s;
        }

        [data-theme="light"] {
            --bg-color: #f3f4f6;
            --container-bg: rgba(255, 255, 255, 0.85);
            --border-color: rgba(99, 102, 241, 0.12);
            --text-main: #1f2937;
            --text-muted: #6b7280;
            --primary: #4f46e5;
            --primary-glow: rgba(79, 70, 229, 0.2);
            --accent-cyan: #0891b2;
            --accent-teal: #059669;
            --accent-amber: #d97706;
            --accent-rose: #e11d48;
            --card-hover-border: rgba(8, 145, 178, 0.45);
            --glass-sheen: linear-gradient(135deg, rgba(0, 0, 0, 0.02), rgba(0, 0, 0, 0.05));
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            background-image: radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.04) 0%, transparent 40%),
                              radial-gradient(circle at 90% 80%, rgba(6, 182, 212, 0.05) 0%, transparent 40%);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 30px 15px;
            transition: background-color var(--trans-speed), color var(--trans-speed);
        }

        .dashboard-container {
            width: 100%;
            max-width: 1100px;
            background: var(--container-bg);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            box-shadow: 0 20px 50px rgba(0,0,0,0.15);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        /* --- Header Section --- */
        .dash-header {
            padding: 24px 32px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
            background: var(--glass-sheen);
        }

        .header-title-sec {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .header-pulse-container {
            position: relative;
            width: 12px; height: 12px;
        }

        .pulse-dot {
            width: 12px; height: 12px;
            background-color: var(--accent-teal);
            border-radius: 50%;
            position: absolute;
            top: 0; left: 0;
            animation: pulse-ring 1.8s infinite;
        }

        @keyframes pulse-ring {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.5); }
            70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }

        h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 1.8em;
            font-weight: 700;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, var(--text-main) 30%, var(--accent-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .badges-area {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .badge {
            background: rgba(99, 102, 241, 0.12);
            color: var(--primary);
            border: 1px solid rgba(99, 102, 241, 0.2);
            padding: 6px 14px;
            border-radius: 50px;
            font-size: 11px;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        .badge.success {
            background: rgba(16, 185, 129, 0.12);
            color: var(--accent-teal);
            border-color: rgba(16, 185, 129, 0.25);
        }

        /* --- Theme Switcher Toggle --- */
        .theme-toggle {
            cursor: pointer;
            width: 44px; height: 26px;
            background: rgba(99, 102, 241, 0.2);
            border-radius: 50px;
            position: relative;
            border: 1px solid var(--border-color);
            transition: background 0.3s;
        }

        .theme-toggle-dot {
            width: 18px; height: 18px;
            background: var(--text-main);
            border-radius: 50%;
            position: absolute;
            top: 3px; left: 3px;
            transition: transform 0.3s;
        }

        [data-theme="light"] .theme-toggle-dot {
            transform: translateX(18px);
        }

        /* --- Navigation Tabs --- */
        .navigation-row {
            display: flex;
            background: rgba(13, 17, 33, 0.3);
            border-bottom: 1px solid var(--border-color);
            overflow-x: auto;
        }

        .nav-tab {
            padding: 16px 24px;
            background: none;
            border: none;
            color: var(--text-muted);
            font-family: 'Outfit', sans-serif;
            font-size: 13.5px;
            font-weight: 500;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            transition: all 0.2s;
            white-space: nowrap;
        }

        .nav-tab:hover {
            color: var(--text-main);
            background: rgba(255,255,255,0.02);
        }

        .nav-tab.active {
            color: var(--primary);
            border-bottom-color: var(--primary);
            background: rgba(99, 102, 241, 0.05);
        }

        /* --- Workspaces/Tab Panels --- */
        .tab-panel {
            padding: 32px;
            display: none;
            flex-direction: column;
            gap: 24px;
            animation: tabFadeIn 0.3s ease;
        }

        .tab-panel.active {
            display: flex;
        }

        @keyframes tabFadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* --- Grid System --- */
        .analytics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
            gap: 20px;
        }

        .card {
            background: var(--glass-sheen);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 20px;
            transition: transform 0.2s, border-color 0.2s;
        }

        .card:hover {
            transform: translateY(-3px);
            border-color: var(--card-hover-border);
        }

        .card-label {
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }

        .card-value {
            font-size: 20px;
            font-weight: 700;
            font-family: 'Outfit', sans-serif;
            color: var(--text-main);
            word-break: break-all;
        }

        /* --- Circle Gauges Area --- */
        .gauges-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
        }

        .gauge-card {
            display: flex;
            align-items: center;
            gap: 24px;
        }

        .circle-progress {
            position: relative;
            width: 100px; height: 100px;
            flex-shrink: 0;
        }

        .circle-progress svg {
            width: 100px; height: 100px;
            transform: rotate(-90deg);
        }

        .circle-progress circle {
            fill: none;
            stroke-width: 8;
        }

        .circle-bg {
            stroke: rgba(255,255,255,0.06);
        }

        [data-theme="light"] .circle-bg {
            stroke: rgba(0,0,0,0.05);
        }

        .circle-bar {
            stroke: var(--primary);
            stroke-dasharray: 251.2;
            stroke-dashoffset: 251.2;
            stroke-linecap: round;
            transition: stroke-dashoffset 0.8s ease;
        }

        .circle-bar.cyan { stroke: var(--accent-cyan); }
        .circle-bar.teal { stroke: var(--accent-teal); }
        .circle-bar.amber { stroke: var(--accent-amber); }

        .circle-value-label {
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            font-family: 'Outfit', sans-serif;
            font-size: 17px;
            font-weight: 700;
        }

        .gauge-info {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }

        .gauge-title {
            font-size: 15px;
            font-weight: 600;
            font-family: 'Outfit', sans-serif;
        }

        .gauge-subtitle {
            font-size: 12px;
            color: var(--text-muted);
        }

        /* --- Logs & CLI Viewports --- */
        .console-container {
            background-color: #030712;
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 12px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12.5px;
            line-height: 1.6;
            margin-top: 10px;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .console-header {
            background: rgba(255,255,255,0.03);
            border-bottom: 1px solid rgba(255,255,255,0.07);
            padding: 10px 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .console-header-left {
            display: flex;
            gap: 6px;
        }

        .console-dot {
            width: 8px; height: 8px;
            border-radius: 50%;
        }

        .console-title {
            font-size: 11px;
            color: rgba(255,255,255,0.4);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .console-controls {
            display: flex;
            gap: 12px;
        }

        .console-btn {
            background: none;
            border: none;
            color: rgba(255,255,255,0.5);
            cursor: pointer;
            font-size: 11px;
            transition: color 0.2s;
        }

        .console-btn:hover {
            color: #ffffff;
        }

        .console-body {
            padding: 16px;
            max-height: 240px;
            min-height: 180px;
            overflow-y: auto;
            color: #bbf7d0;
            text-align: left;
        }

        .log-line {
            margin-bottom: 6px;
            word-break: break-all;
        }

        .log-time { color: rgba(255,255,255,0.3); margin-right: 8px; }
        .log-info { color: #10b981; }
        .log-debug { color: #60a5fa; }
        .log-warn { color: #fbbf24; }

        /* --- Load Balancer Panel styles --- */
        .ping-row {
            display: flex;
            gap: 16px;
            align-items: center;
            margin-bottom: 20px;
        }

        .btn {
            background: var(--primary);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-family: 'Outfit', sans-serif;
            font-size: 13.5px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 4px 12px var(--primary-glow);
        }

        .btn:hover {
            opacity: 0.9;
            transform: translateY(-1px);
        }

        .btn.outline {
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-main);
            box-shadow: none;
        }

        .btn.outline:hover {
            background: rgba(255,255,255,0.03);
            border-color: var(--text-main);
        }

        .response-code-box {
            font-family: 'JetBrains Mono', monospace;
            background: var(--glass-sheen);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 18px;
            overflow-x: auto;
            text-align: left;
        }

        /* --- Scaling Simulator area --- */
        .slider-card {
            background: var(--glass-sheen);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
        }

        .slider-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }

        .desc-text {
            font-size: 13.5px;
            color: var(--text-muted);
            line-height: 1.6;
            max-width: 600px;
        }

        .slider-wrapper {
            display: flex;
            flex-direction: column;
            gap: 8px;
            width: 250px;
        }

        .slider-labels {
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            color: var(--text-muted);
            font-weight: 600;
        }

        .slider-element {
            width: 100%;
            height: 6px;
            border-radius: 10px;
            outline: none;
            -webkit-appearance: none;
            background: rgba(99, 102, 241, 0.2);
            cursor: pointer;
        }

        .slider-element::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 18px; height: 18px;
            border-radius: 50%;
            background: var(--primary);
            border: 2px solid var(--text-main);
            box-shadow: 0 0 8px var(--primary-glow);
        }

        .cluster-visual-box {
            border: 1px dashed var(--border-color);
            border-radius: 14px;
            padding: 30px;
            background: rgba(13, 17, 33, 0.15);
        }

        .cluster-boxes {
            display: flex;
            justify-content: center;
            gap: 24px;
            flex-wrap: wrap;
            margin-top: 15px;
        }

        .container-task-box {
            width: 180px;
            background: var(--glass-sheen);
            border: 1.5px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
            position: relative;
            transform: scale(0.95);
            opacity: 0.5;
            transition: all 0.4s ease;
        }

        .container-task-box.active {
            transform: scale(1);
            opacity: 1;
            border-color: var(--accent-teal);
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.15);
        }

        .container-task-box.scaling {
            transform: scale(1);
            opacity: 1;
            border-color: var(--accent-amber);
            border-style: dotted;
            animation: spin-glow 1.5s infinite;
        }

        @keyframes spin-glow {
            0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.2); }
            50% { box-shadow: 0 0 0 10px rgba(245, 158, 11, 0); }
            100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
        }

        .task-icon {
            font-size: 24px;
        }

        .task-title {
            font-family: 'Outfit', sans-serif;
            font-size: 13px;
            font-weight: 600;
        }

        .task-status-tag {
            font-size: 10px;
            padding: 2px 8px;
            border-radius: 4px;
            background: rgba(255,255,255,0.06);
            color: var(--text-muted);
        }

        .container-task-box.active .task-status-tag {
            background: rgba(16, 185, 129, 0.12);
            color: var(--accent-teal);
            font-weight: 600;
        }

        .container-task-box.scaling .task-status-tag {
            background: rgba(245, 158, 11, 0.12);
            color: var(--accent-amber);
            font-weight: 600;
        }

        .scaling-meta-box {
            display: flex;
            justify-content: space-around;
            gap: 20px;
            margin-top: 24px;
            border-top: 1px solid var(--border-color);
            padding-top: 20px;
            flex-wrap: wrap;
        }

        .meta-entry {
            text-align: center;
        }

        .meta-val {
            font-family: 'Outfit', sans-serif;
            font-size: 18px;
            font-weight: 700;
            color: var(--primary);
        }

        /* --- CLI Console Panel --- */
        .cli-btn-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 12px;
            margin-bottom: 8px;
        }

        .cli-btn {
            background: var(--glass-sheen);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 10px 16px;
            border-radius: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            cursor: pointer;
            text-align: left;
            transition: all 0.2s;
        }

        .cli-btn:hover {
            border-color: var(--primary);
            background: rgba(99, 102, 241, 0.04);
            transform: translateX(2px);
        }

        .cli-prompt-line {
            color: #38bdf8;
            margin-bottom: 8px;
        }

        .footer {
            padding: 20px;
            text-align: center;
            font-size: 11px;
            color: var(--text-muted);
            border-top: 1px solid var(--border-color);
            background: rgba(13, 17, 33, 0.1);
        }
    </style>
</head>
<body data-theme="dark">
    <div class="dashboard-container">
        <!-- --- HEADER --- -->
        <div class="dash-header">
            <div class="header-title-sec">
                <div class="header-pulse-container">
                    <div class="pulse-dot"></div>
                </div>
                <div>
                    <h1>AWS ECS Live Container Console</h1>
                </div>
            </div>
            <div class="badges-area">
                <span class="badge success">🟢 SERVICE RUNNING</span>
                <span class="badge">AWS REGION: us-east-1</span>
                <!-- Light/Dark Toggle -->
                <div class="theme-toggle" onclick="toggleTheme()" title="Switch Theme">
                    <div class="theme-toggle-dot"></div>
                </div>
            </div>
        </div>

        <!-- --- NAVIGATION --- -->
        <div class="navigation-row">
            <button class="nav-tab active" onclick="switchTab('container-tab')">📊 Container Hub</button>
            <button class="nav-tab" onclick="switchTab('scaling-tab')">📈 Auto-Scaling Center</button>
            <button class="nav-tab" onclick="switchTab('network-tab')">⚖️ Load Balancer</button>
            <button class="nav-tab" onclick="switchTab('cli-tab')">🐚 Infrastructure CLI</button>
        </div>

        <!-- --- TAB PANEL 1: CONTAINER HUB --- -->
        <div id="container-tab" class="tab-panel active">
            <div class="analytics-grid">
                <div class="card">
                    <div class="card-label">Container Host</div>
                    <div class="card-value">{{ hostname }}</div>
                </div>
                <div class="card">
                    <div class="card-label">Environment</div>
                    <div class="card-value">{{ env }}</div>
                </div>
                <div class="card">
                    <div class="card-label">Server Time</div>
                    <div class="card-value" id="current-server-time">{{ time }}</div>
                </div>
                <div class="card">
                    <div class="card-label">Container Uptime</div>
                    <div class="card-value" id="uptime-value">00:00:00</div>
                </div>
            </div>

            <div class="gauges-row">
                <!-- CPU Gauge -->
                <div class="card gauge-card">
                    <div class="circle-progress">
                        <svg>
                            <circle class="circle-bg" cx="50" cy="50" r="40"></circle>
                            <circle id="cpu-circle" class="circle-bar cyan" cx="50" cy="50" r="40"></circle>
                        </svg>
                        <div class="circle-value-label" id="cpu-val-lbl">24%</div>
                    </div>
                    <div class="gauge-info">
                        <div class="gauge-title">Task CPU Utilization</div>
                        <div class="gauge-subtitle">Normalized across allocated shares</div>
                    </div>
                </div>
                <!-- Memory Gauge -->
                <div class="card gauge-card">
                    <div class="circle-progress">
                        <svg>
                            <circle class="circle-bg" cx="50" cy="50" r="40"></circle>
                            <circle id="mem-circle" class="circle-bar teal" cx="50" cy="50" r="40"></circle>
                        </svg>
                        <div class="circle-value-label" id="mem-val-lbl">42%</div>
                    </div>
                    <div class="gauge-info">
                        <div class="gauge-title">Task Memory Allocation</div>
                        <div class="gauge-subtitle">Currently consuming 215MB of 512MB limit</div>
                    </div>
                </div>
                <!-- Connections Gauge -->
                <div class="card gauge-card">
                    <div class="circle-progress">
                        <svg>
                            <circle class="circle-bg" cx="50" cy="50" r="40"></circle>
                            <circle id="conn-circle" class="circle-bar amber" cx="50" cy="50" r="40"></circle>
                        </svg>
                        <div class="circle-value-label" id="conn-val-lbl">12</div>
                    </div>
                    <div class="gauge-info">
                        <div class="gauge-title">Active Target Connections</div>
                        <div class="gauge-subtitle">Simultaneous TCP connections routed via ALB</div>
                    </div>
                </div>
            </div>

            <!-- Streaming logs console -->
            <div>
                <h3 style="font-family: 'Outfit', sans-serif; font-size: 15px; margin-bottom: 8px;">☁️ Real-Time CloudWatch logs stream</h3>
                <div class="console-container">
                    <div class="console-header">
                        <div class="console-header-left">
                            <div class="console-dot" style="background:#f43f5e"></div>
                            <div class="console-dot" style="background:#eab308"></div>
                            <div class="console-dot" style="background:#10b981"></div>
                        </div>
                        <div class="console-title">ecs/my-ecs-app/log-stream</div>
                        <div class="console-controls">
                            <button class="console-btn" onclick="toggleLogs(this)">Pause</button>
                            <button class="console-btn" onclick="clearLogs()">Clear</button>
                        </div>
                    </div>
                    <div class="console-body" id="custom-logs-body">
                        <!-- Filled by JS -->
                    </div>
                </div>
            </div>
        </div>

        <!-- --- TAB PANEL 2: AUTO SCALING --- -->
        <div id="scaling-tab" class="tab-panel">
            <div class="slider-card">
                <div class="slider-row">
                    <div>
                        <h3 style="font-family: 'Outfit', sans-serif; font-size:16px; margin-bottom:6px;">Traffic Load Simulator</h3>
                        <p class="desc-text">Simulate load fluctuations on the Application Load Balancer endpoint. Increasing web traffic triggers AWS Auto-Scaling Policy Alarms causing task limits to expand.</p>
                    </div>
                    <div class="slider-wrapper">
                        <div class="slider-labels">
                            <span>LOW</span>
                            <span>NORMAL</span>
                            <span>PEAK</span>
                            <span>CRITICAL</span>
                        </div>
                        <input id="traffic-slider" type="range" min="1" max="4" value="2" class="slider-element" oninput="handleScaling(this.value)">
                    </div>
                </div>

                <div class="cluster-visual-box">
                    <h4 style="font-family: 'Outfit', sans-serif; font-size:13px; color:var(--text-muted); text-transform:uppercase; margin-bottom:15px; text-align:center;">
                        🎯 Active ECS Service Task Allocation
                    </h4>
                    <div class="cluster-boxes">
                        <!-- Task 1 -->
                        <div id="task-1" class="container-task-box active">
                            <span class="task-icon">🐳</span>
                            <span class="task-title">ecs-task-us-e1a-1</span>
                            <span class="task-status-tag">HEALTHY</span>
                        </div>
                        <!-- Task 2 -->
                        <div id="task-2" class="container-task-box active">
                            <span class="task-icon">🐳</span>
                            <span class="task-title">ecs-task-us-e1b-2</span>
                            <span class="task-status-tag">HEALTHY</span>
                        </div>
                        <!-- Task 3 -->
                        <div id="task-3" class="container-task-box">
                            <span class="task-icon">🐳</span>
                            <span class="task-title">ecs-task-us-e1a-3</span>
                            <span class="task-status-tag">SHUT DOWN</span>
                        </div>
                        <!-- Task 4 -->
                        <div id="task-4" class="container-task-box">
                            <span class="task-icon">🐳</span>
                            <span class="task-title">ecs-task-us-e1b-4</span>
                            <span class="task-status-tag">SHUT DOWN</span>
                        </div>
                    </div>
                </div>

                <div class="scaling-meta-box">
                    <div class="meta-entry">
                        <div class="card-label">Target Metric</div>
                        <div class="meta-val" id="meta-target-val">Normal Load</div>
                    </div>
                    <div class="meta-entry">
                        <div class="card-label">Simulated RPS</div>
                        <div class="meta-val" id="meta-rps-val">45 Requests / s</div>
                    </div>
                    <div class="meta-entry">
                        <div class="card-label">ECS Scaled Instances</div>
                        <div class="meta-val" id="meta-instances-val">2 Tasks</div>
                    </div>
                    <div class="meta-entry">
                        <div class="card-label">Target Group Port</div>
                        <div class="meta-val">Dynamic (Ephemeral)</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- --- TAB PANEL 3: LOAD BALANCER DIAGNOSTICS --- -->
        <div id="network-tab" class="tab-panel">
            <p class="desc-text">Test routing policies and verify reverse proxy forwarding. Click "Ping Diagnostic API" to trigger an HTTP request to the Flask server, displaying parsed HTTP headers and performance latency calculated end-to-end.</p>
            <div class="ping-row">
                <button class="btn" id="alb-ping-btn" onclick="pingDiagnostic()">Ping Diagnostic Endpoint</button>
                <div style="font-size: 13px; font-weight:600;"><span id="last-ping-status"></span> <span id="last-ping-perf" style="color:var(--accent-teal);"></span></div>
            </div>
            
            <div>
                <h3 style="font-family: 'Outfit', sans-serif; font-size:14px; margin-bottom:8px;">Root Proxy Forwarding Payload</h3>
                <div class="response-code-box">
                    <pre><code id="json-headers-out">{ "action": "Click Ping to retrieve diagnostics..." }</code></pre>
                </div>
            </div>
        </div>

        <!-- --- TAB PANEL 4: CLI CONSOLE --- -->
        <div id="cli-tab" class="tab-panel">
            <p class="desc-text">Simulate standard infrastructure commands by executing the actions below. Commands will print live output directly into the CLI console window.</p>
            <div class="cli-btn-grid">
                <button class="cli-btn" onclick="runCLICommand('aws-verify')">🧰 Verify environment tools</button>
                <button class="cli-btn" onclick="runCLICommand('ecs-cluster')">🛰️ Describe ECS Cluster</button>
                <button class="cli-btn" onclick="runCLICommand('ecr-repo')">📦 List ECR Repository Images</button>
                <button class="cli-btn" onclick="runCLICommand('tg-health')">🩺 Target Group health reports</button>
            </div>
            <div class="console-container" style="margin-top:10px;">
                <div class="console-header">
                    <div class="console-header-left">
                        <div class="console-dot" style="background:#5b21b6"></div>
                        <div class="console-dot" style="background:#4c1d95"></div>
                        <div class="console-dot" style="background:#2e1065"></div>
                    </div>
                    <div class="console-title">AWS Shell Terminal Simulator</div>
                </div>
                <div class="console-body" id="cli-output" style="color:#38bdf8; height:240px; min-height:240px; max-height:240px;">
                    <div class="cli-prompt-line">guest@aws-shell:~$ <span style="color:#ffffff;">click a command button to execute...</span></div>
                </div>
            </div>
        </div>

        <!-- --- FOOTER --- -->
        <div class="footer">
            <span>DevOps Cloud Platform Dashboard • Container: {{ hostname }} • Platform Architecture: {{ platform }} • Uptime tracked since server launch</span>
        </div>
    </div>

    <script>
        // Tab switching logic
        function switchTab(tabId) {
            document.querySelectorAll('.nav-tab').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-panel').forEach(panel => panel.classList.remove('active'));
            
            // Activate current
            const clickedBtn = Array.from(document.querySelectorAll('.nav-tab')).find(btn => btn.getAttribute('onclick').includes(tabId));
            if(clickedBtn) clickedBtn.classList.add('active');
            
            const curPanel = document.getElementById(tabId);
            if(curPanel) curPanel.classList.add('active');
        }

        // Theme Toggle logic
        function toggleTheme() {
            const body = document.body;
            const currentTheme = body.getAttribute('data-theme');
            if(currentTheme === 'light') {
                body.setAttribute('data-theme', 'dark');
            } else {
                body.setAttribute('data-theme', 'light');
            }
        }

        // Simulating telemetry gauges
        const cpuCircle = document.getElementById('cpu-circle');
        const cpuLabel = document.getElementById('cpu-val-lbl');
        const memCircle = document.getElementById('mem-circle');
        const memLabel = document.getElementById('mem-val-lbl');
        const connCircle = document.getElementById('conn-circle');
        const connLabel = document.getElementById('conn-val-lbl');

        function updateGauge(circle, label, maxVal, baseVal, suffix = '', circleDash = 251.2) {
            const val = Math.max(0, Math.min(maxVal, Math.round(baseVal + (Math.random() * 8) - 4)));
            let percentage = val;
            if(suffix === '') percentage = (val / maxVal) * 100;
            const offset = circleDash - (percentage / 100) * circleDash;
            circle.style.strokeDashoffset = offset;
            label.textContent = val + suffix;
            return val;
        }

        // Live stats interval
        let activeConnectionsNum = 12;
        setInterval(() => {
            fetch('/api/stats')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('current-server-time').textContent = data.time.split('.')[0];
                    updateGauge(cpuCircle, cpuLabel, 100, data.cpu_usage, '%');
                    updateGauge(memCircle, memLabel, 100, data.memory_usage, '%');
                    
                    // Connection gauge linked to connections
                    activeConnectionsNum = updateGauge(connCircle, connLabel, 50, activeConnectionsNum, '');
                })
                .catch(() => {
                    // Fallback
                    updateGauge(cpuCircle, cpuLabel, 100, 25, '%');
                    updateGauge(memCircle, memLabel, 100, 42, '%');
                    activeConnectionsNum = updateGauge(connCircle, connLabel, 50, activeConnectionsNum, '');
                });
        }, 2200);

        // Uptime counter
        const launchTime = new Date('{{ start_time }}');
        setInterval(() => {
            const now = new Date();
            const diffMs = now - launchTime;
            const diffHrs = Math.floor(diffMs / 3600000);
            const diffMins = Math.floor((diffMs % 3600000) / 60000);
            const diffSecs = Math.floor((diffMs % 60000) / 1000);
            
            const hoursStr = String(diffHrs).padStart(2, '0');
            const minsStr = String(diffMins).padStart(2, '0');
            const secsStr = String(diffSecs).padStart(2, '0');
            document.getElementById('uptime-value').textContent = hoursStr + ':' + minsStr + ':' + secsStr;
        }, 1000);

        // Logs Generator logic
        const logsBody = document.getElementById('custom-logs-body');
        let logsRunning = true;

        const mockLogTemplates = [
            { level: 'log-info', msg: 'HTTP/1.1 GET / healthcheck - TargetGroupHealthCheck agent: AWS-ALB/2.0' },
            { level: 'log-info', msg: 'Host headers authenticated for private subnets network interfaces' },
            { level: 'log-debug', msg: 'Local cache cleared. Gunicorn internal workers alive [PID: 24, 25]' },
            { level: 'log-info', msg: 'GET /api/stats HTTP/1.1 200 OK - execution 3ms' },
            { level: 'log-warn', msg: 'System warning - Keep-alive connection timed out for endpoint client' },
            { level: 'log-debug', msg: 'CloudWatch agents dispatched metrics packet to collector server' }
        ];

        function addLogLine() {
            if (!logsRunning) return;
            const log = mockLogTemplates[Math.floor(Math.random() * mockLogTemplates.length)];
            const timeStr = new Date().toISOString().split('T')[1].slice(0, 8);
            
            const line = document.createElement('div');
            line.className = 'log-line';
            line.innerHTML = '<span class="log-time">['+timeStr+']</span> <span class="'+log.level+'">['+log.level.replace('log-', '').toUpperCase()+']</span> ' + log.msg;
            
            logsBody.appendChild(line);
            if(logsBody.childNodes.length > 28) {
                logsBody.removeChild(logsBody.firstChild);
            }
            logsBody.scrollTop = logsBody.scrollHeight;
        }

        // Log timer
        setInterval(addLogLine, 2800);
        // Pre-fill logs
        for(let i=0; i<8; i++) addLogLine();

        function toggleLogs(btn) {
            logsRunning = !logsRunning;
            btn.textContent = logsRunning ? 'Pause' : 'Resume';
        }

        function clearLogs() {
            logsBody.innerHTML = '';
        }

        // Auto Scaling Simulator logic
        const task1 = document.getElementById('task-1');
        const task2 = document.getElementById('task-2');
        const task3 = document.getElementById('task-3');
        const task4 = document.getElementById('task-4');
        const rpsLabel = document.getElementById('meta-rps-val');
        const targetLabel = document.getElementById('meta-target-val');
        const instancesLabel = document.getElementById('meta-instances-val');

        function handleScaling(val) {
            const step = parseInt(val);
            if(step === 1) {
                // Low Load
                scaleTasks(1);
            } else if(step === 2) {
                // Normal
                scaleTasks(2);
            } else if(step === 3) {
                // Peak
                scaleTasks(3);
            } else {
                // Critical
                scaleTasks(4);
            }
        }

        function scaleTasks(activeCount) {
            if(activeCount === 1) {
                // Task 2,3,4 turned off — only task 1 stays active
                task1.className = 'container-task-box active';
                task1.querySelector('.task-status-tag').textContent = 'HEALTHY';
                task2.className = 'container-task-box';
                task2.querySelector('.task-status-tag').textContent = 'SHUT DOWN';
                task3.className = 'container-task-box';
                task3.querySelector('.task-status-tag').textContent = 'SHUT DOWN';
                task4.className = 'container-task-box';
                task4.querySelector('.task-status-tag').textContent = 'SHUT DOWN';
                
                rpsLabel.textContent = '8 Requests / s';
                targetLabel.textContent = 'Low Load';
                instancesLabel.textContent = '1 Task';
                activeConnectionsNum = 3;
            } else if(activeCount === 2) {
                task2.className = 'container-task-box active';
                task2.querySelector('.task-status-tag').textContent = 'HEALTHY';
                task3.className = 'container-task-box';
                task3.querySelector('.task-status-tag').textContent = 'SHUT DOWN';
                task4.className = 'container-task-box';
                task4.querySelector('.task-status-tag').textContent = 'SHUT DOWN';
                
                rpsLabel.textContent = '45 Requests / s';
                targetLabel.textContent = 'Normal Load';
                instancesLabel.textContent = '2 Tasks';
                activeConnectionsNum = 12;
            } else if(activeCount >= 3) {
                // Trigger scaling warning & setup task 3 active
                task2.className = 'container-task-box active';
                task2.querySelector('.task-status-tag').textContent = 'HEALTHY';
                
                task3.className = 'container-task-box scaling';
                task3.querySelector('.task-status-tag').textContent = 'PROVISIONING';
                
                if(activeCount === 4) {
                    task4.className = 'container-task-box scaling';
                    task4.querySelector('.task-status-tag').textContent = 'PROVISIONING';
                } else {
                    task4.className = 'container-task-box';
                    task4.querySelector('.task-status-tag').textContent = 'SHUT DOWN';
                }

                rpsLabel.textContent = activeCount === 3 ? '180 Requests / s' : '420 Requests / s';
                targetLabel.textContent = activeCount === 3 ? 'Peak Traffic' : 'Critical Spike';
                instancesLabel.textContent = activeCount === 3 ? '2 Tasks (+1 Scaling)' : '2 Tasks (+2 Scaling)';

                setTimeout(() => {
                    if(task3.classList.contains('scaling')) {
                        task3.className = 'container-task-box active';
                        task3.querySelector('.task-status-tag').textContent = 'HEALTHY';
                    }
                    if(activeCount === 4 && task4.classList.contains('scaling')) {
                        task4.className = 'container-task-box active';
                        task4.querySelector('.task-status-tag').textContent = 'HEALTHY';
                    }
                    instancesLabel.textContent = activeCount + ' Tasks (Dynamic)';
                }, 2200);
                activeConnectionsNum = activeCount === 3 ? 34 : 48;
            }
        }

        // ALB Pinger
        function pingDiagnostic() {
            const outBox = document.getElementById('json-headers-out');
            const perfSpan = document.getElementById('last-ping-perf');
            const statusSpan = document.getElementById('last-ping-status');
            
            statusSpan.textContent = 'Executing ping...';
            perfSpan.textContent = '';
            
            const start = performance.now();
            fetch('/api/request-headers')
                .then(res => {
                    const duration = Math.round(performance.now() - start);
                    statusSpan.textContent = '🟢 Server HTTP 200 OK';
                    perfSpan.textContent = '• Roundtrip: ' + duration + 'ms';
                    return res.text();
                })
                .then(text => {
                    try {
                        const parsed = JSON.parse(text);
                        outBox.textContent = JSON.stringify(parsed, null, 4);
                    } catch(err) {
                        outBox.textContent = text;
                    }
                })
                .catch(err => {
                    statusSpan.textContent = '🔴 Request connection failed';
                    outBox.textContent = String(err);
                });
        }

        // CLI Shell Emulator
        const cliOutput = document.getElementById('cli-output');
        const cliScripts = {
            'aws-verify': [
                'guest@aws-shell:~$ docker --version',
                'Docker version 24.0.7, build afdd53b',
                'guest@aws-shell:~$ aws --version',
                'aws-cli/2.13.26 Python/3.11.8 Windows/10 exe/AMD64 prompt/off',
                'guest@aws-shell:~$ env | grep AWS',
                'AWS_DEFAULT_REGION=us-east-1',
                'AWS_ACCESS_KEY_ID=ASIAXXXXXXXXXXXXXXXX'
            ],
            'ecs-cluster': [
                'guest@aws-shell:~$ aws ecs describe-clusters --clusters my-ecs-cluster',
                '{',
                '    "clusters": [',
                '        {',
                '            "clusterArn": "arn:aws:ecs:us-east-1:250492956933:cluster/my-ecs-cluster",',
                '            "clusterName": "my-ecs-cluster",',
                '            "status": "ACTIVE",',
                '            "registeredContainerInstancesCount": 2,',
                '            "runningTasksCount": 2,',
                '            "pendingTasksCount": 0,',
                '            "activeServicesCount": 1',
                '        }',
                '    ]',
                '}'
            ],
            'ecr-repo': [
                'guest@aws-shell:~$ aws ecr describe-repositories --repository-names my-ecs-app',
                '{',
                '    "repositories": [',
                '        {',
                '            "repositoryArn": "arn:aws:ecr:us-east-1:250492956933:repository/my-ecs-app",',
                '            "registryId": "250492956933",',
                '            "repositoryName": "my-ecs-app",',
                '            "repositoryUri": "250492956933.dkr.ecr.us-east-1.amazonaws.com/my-ecs-app",',
                '            "createdAt": "2026-07-09T09:12:00Z"',
                '        }',
                '    ]',
                '}',
                'guest@aws-shell:~$ aws ecr list-images --repository-name my-ecs-app',
                'imageDigest: sha256:78dfd4b791dc...  imageTag: latest',
                'imageDigest: sha256:90e4fbc873e2...  imageTag: 7dbfc87a'
            ],
            'tg-health': [
                'guest@aws-shell:~$ aws elbv2 describe-target-health --target-group-arn arn:aws:elasticloadbalancing:us-east-1:250492956933:targetgroup/my-app-tg/782cd9b',
                '{',
                '    "TargetHealthDescriptions": [',
                '        {',
                '            "Target": { "Id": "i-09ab7d8123bc", "Port": 32768 },',
                '            "TargetHealth": { "State": "healthy" }',
                '        },',
                '        {',
                '            "Target": { "Id": "i-02cf97b154cb", "Port": 32769 },',
                '            "TargetHealth": { "State": "healthy" }',
                '        }',
                '    ]',
                '}'
            ]
        };

        function runCLICommand(cmdKey) {
            cliOutput.innerHTML = '';
            const lines = cliScripts[cmdKey];
            let index = 0;
            
            function printNextLine() {
                if(index >= lines.length) return;
                const line = document.createElement('div');
                if (lines[index].includes('guest@aws-shell:~$')) {
                    line.className = 'cli-prompt-line';
                    line.innerHTML = 'guest@aws-shell:~$ ' + '<span style="color:#ffffff;">'+lines[index].replace('guest@aws-shell:~$ ', '')+'</span>';
                } else {
                    line.textContent = lines[index];
                    line.style.color = '#e2e8f0';
                }
                
                cliOutput.appendChild(line);
                cliOutput.scrollTop = cliOutput.scrollHeight;
                index++;
                setTimeout(printNextLine, 220);
            }
            printNextLine();
        }
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE,
        hostname=socket.gethostname(),
        env=os.environ.get("APP_ENV", "production"),
        time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        platform=f"{platform.system()} {platform.machine()}",
        start_time=app_start_time.isoformat()
    )

@app.route("/api/stats")
def stats():
    # Dynamic values simulating normal load metrics
    cpu = 15.0 + (datetime.datetime.now().second % 10) * 1.5
    mem = 40.5 + (datetime.datetime.now().minute % 5) * 0.4
    return jsonify({
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        "cpu_usage": round(cpu, 1),
        "memory_usage": round(mem, 1)
    })

@app.route("/api/request-headers")
def request_headers():
    headers_dict = dict(request.headers)
    return jsonify({
        "target_replica_host": socket.gethostname(),
        "client_remote_addr": request.remote_addr,
        "request_method": request.method,
        "protocol": request.environ.get("SERVER_PROTOCOL"),
        "user_agent": request.headers.get("User-Agent"),
        "incoming_forwarded_ips": request.headers.get("X-Forwarded-For", "None (Direct Connection)"),
        "incoming_forwarded_proto": request.headers.get("X-Forwarded-Proto", "HTTP"),
        "incoming_forwarded_port": request.headers.get("X-Forwarded-Port", "5000"),
        "raw_headers_received": headers_dict
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "hostname": socket.gethostname(),
        "timestamp": datetime.datetime.utcnow().isoformat()
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
