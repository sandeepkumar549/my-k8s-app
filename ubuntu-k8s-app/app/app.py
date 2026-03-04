from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import socket
import datetime

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Get info about the pod/container
        hostname = socket.gethostname()
        app_env = os.environ.get("APP_ENV", "unknown")
        app_name = os.environ.get("APP_NAME", "Ubuntu App")
        version = os.environ.get("APP_VERSION", "v1")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{app_name}</title>
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --bg: #0f1117;
      --card: #1a1d27;
      --border: #2a2d3a;
      --accent: #e95420;
      --accent2: #77216f;
      --green: #3ab54a;
      --text: #e8e8f0;
      --muted: #7a7a96;
    }}
    body {{
      background: var(--bg);
      color: var(--text);
      font-family: 'DM Mono', monospace;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }}
    body::before {{
      content: '';
      position: fixed; inset: 0;
      background-image:
        linear-gradient(rgba(233,84,32,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(233,84,32,0.03) 1px, transparent 1px);
      background-size: 30px 30px;
      pointer-events: none;
    }}
    .container {{
      position: relative; z-index: 1;
      max-width: 750px; width: 100%;
    }}
    .ubuntu-badge {{
      display: inline-flex; align-items: center; gap: 0.6rem;
      background: rgba(233,84,32,0.1);
      border: 1px solid rgba(233,84,32,0.3);
      color: var(--accent); font-size: 0.85rem;
      padding: 0.5rem 1.2rem; border-radius: 100px;
      margin-bottom: 2rem;
    }}
    .ubuntu-circle {{
      width: 10px; height: 10px; border-radius: 50%;
      background: var(--accent);
      animation: pulse 2s ease-in-out infinite;
    }}
    @keyframes pulse {{
      0%,100% {{ opacity:1; transform:scale(1); }}
      50% {{ opacity:0.5; transform:scale(0.8); }}
    }}
    h1 {{
      font-family: 'Syne', sans-serif;
      font-size: clamp(2rem, 5vw, 3.5rem);
      font-weight: 800; line-height: 1.1;
      margin-bottom: 0.5rem;
    }}
    h1 span {{ color: var(--accent); }}
    .subtitle {{
      color: var(--muted); font-size: 0.9rem;
      margin-bottom: 2.5rem; line-height: 1.6;
    }}
    .terminal {{
      background: #0a0c10;
      border: 1px solid var(--border);
      border-radius: 12px; overflow: hidden;
      margin-bottom: 1.5rem;
      box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }}
    .terminal-bar {{
      background: #1a1d27;
      padding: 0.8rem 1rem;
      display: flex; align-items: center; gap: 0.5rem;
      border-bottom: 1px solid var(--border);
    }}
    .tb-dot {{
      width: 12px; height: 12px; border-radius: 50%;
    }}
    .tb-red {{ background: #ff5f57; }}
    .tb-yellow {{ background: #febc2e; }}
    .tb-green {{ background: #28c840; }}
    .tb-title {{
      margin-left: 0.5rem; font-size: 0.8rem;
      color: var(--muted);
    }}
    .terminal-body {{ padding: 1.5rem; font-size: 0.85rem; line-height: 2; }}
    .line {{ display: flex; gap: 0.5rem; flex-wrap: wrap; }}
    .prompt {{ color: var(--accent); }}
    .cmd {{ color: #7ec8e3; }}
    .output {{ color: var(--green); }}
    .output-white {{ color: var(--text); }}
    .output-muted {{ color: var(--muted); }}
    .cards {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem; margin-top: 1.5rem;
    }}
    .info-card {{
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: 12px; padding: 1.2rem;
      transition: border-color 0.3s;
    }}
    .info-card:hover {{ border-color: var(--accent); }}
    .info-label {{
      font-size: 0.7rem; color: var(--muted);
      text-transform: uppercase; letter-spacing: 0.1em;
      margin-bottom: 0.4rem;
    }}
    .info-value {{
      font-size: 1rem; font-weight: 500;
      color: var(--text);
    }}
    .info-value.green {{ color: var(--green); }}
    .info-value.orange {{ color: var(--accent); }}
    .footer {{
      text-align: center; margin-top: 2rem;
      color: var(--muted); font-size: 0.78rem;
    }}
    .footer span {{ color: var(--accent); }}
  </style>
</head>
<body>
  <div class="container">

    <div class="ubuntu-badge">
      <div class="ubuntu-circle"></div>
      🐧 Running on Ubuntu · Kubernetes Pod
    </div>

    <h1>Hello from<br/><span>Ubuntu</span> + K8s!</h1>
    <p class="subtitle">
      This page is served by a Python HTTP server running inside an
      Ubuntu Docker container, deployed on Kubernetes with 3 replicas.
    </p>

    <!-- Terminal Window -->
    <div class="terminal">
      <div class="terminal-bar">
        <div class="tb-dot tb-red"></div>
        <div class="tb-dot tb-yellow"></div>
        <div class="tb-dot tb-green"></div>
        <span class="tb-title">ubuntu@{hostname}:~$</span>
      </div>
      <div class="terminal-body">
        <div class="line">
          <span class="prompt">ubuntu@{hostname}:~$</span>
          <span class="cmd">kubectl get pods -n my-ubuntu-app</span>
        </div>
        <div class="line">
          <span class="output">NAME &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; READY &nbsp; STATUS &nbsp;&nbsp; REPLICAS</span>
        </div>
        <div class="line">
          <span class="output-white">ubuntu-app-xxx-pod1 &nbsp;&nbsp; 1/1 &nbsp;&nbsp;&nbsp; Running &nbsp; 3</span>
        </div>
        <br/>
        <div class="line">
          <span class="prompt">ubuntu@{hostname}:~$</span>
          <span class="cmd">cat /etc/os-release | grep PRETTY</span>
        </div>
        <div class="line">
          <span class="output">PRETTY_NAME="Ubuntu 22.04.3 LTS"</span>
        </div>
        <br/>
        <div class="line">
          <span class="prompt">ubuntu@{hostname}:~$</span>
          <span class="cmd">echo $APP_ENV</span>
        </div>
        <div class="line">
          <span class="output">{app_env}</span>
        </div>
        <br/>
        <div class="line">
          <span class="prompt">ubuntu@{hostname}:~$</span>
          <span class="cmd">date</span>
        </div>
        <div class="line">
          <span class="output">{current_time}</span>
        </div>
      </div>
    </div>

    <!-- Info Cards -->
    <div class="cards">
      <div class="info-card">
        <div class="info-label">🖥️ Pod Hostname</div>
        <div class="info-value orange">{hostname}</div>
      </div>
      <div class="info-card">
        <div class="info-label">📦 App Name</div>
        <div class="info-value">{app_name}</div>
      </div>
      <div class="info-card">
        <div class="info-label">🏷️ Version</div>
        <div class="info-value green">{version}</div>
      </div>
      <div class="info-card">
        <div class="info-label">🌍 Environment</div>
        <div class="info-value">{app_env}</div>
      </div>
      <div class="info-card">
        <div class="info-label">🐧 Base Image</div>
        <div class="info-value orange">Ubuntu 22.04</div>
      </div>
      <div class="info-card">
        <div class="info-label">✅ Status</div>
        <div class="info-value green">Running</div>
      </div>
    </div>

    <div class="footer">
      <p>Deployed on <span>Kubernetes</span> · Base image: <span>ubuntu:22.04</span> · Namespace: <span>my-ubuntu-app</span></p>
    </div>

  </div>
</body>
</html>"""

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def log_message(self, format, *args):
        pass

print("🐧 Ubuntu + Kubernetes server starting on port 8080...")
HTTPServer(("", 8080), Handler).serve_forever()
