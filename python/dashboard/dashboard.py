# ================================================
# dashboard.py
# Opens a simple webpage showing your object data
# NO Flask needed — uses Python's built-in server
# ================================================
# Run: python dashboard.py
# Then open: http://localhost:5000
# ================================================

import pandas as pd
import os
import http.server
from datetime import datetime

# ---- PUT YOUR ESP32-CAM IP HERE ----
ESP32_IP = "192.168.1.37"  # change to your IP
# ------------------------------------

CSV_FILE  = "events.csv"
HTML_FILE = "dashboard.html"
PORT      = 5000

def build_html():
    last_seen    = "No data yet"
    hours_idle   = "--"
    weekly_count = 0
    status_color = "#7a7a9a"
    status_text  = "No data"
    recent_rows  = ""

    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)

            if len(df) > 0:
                # Fix: add current year to timestamps
                current_year = datetime.now().year
                df['timestamp'] = pd.to_datetime(
                    df['timestamp'] + f" {current_year}",
                    format="%H:%M %d/%m %Y"
                )

                last = df.iloc[-1]
                last_seen = last['timestamp'].strftime("%H:%M on %d/%m")

                now = datetime.now()
                last_dt = last['timestamp'].to_pydatetime().replace(year=now.year)
                diff = (now - last_dt).total_seconds() / 3600
                hours_idle = f"{round(diff, 1)} hrs ago"

                if diff < 12:
                    status_color = "#40d9a0"
                    status_text  = "Recently used"
                elif diff < 36:
                    status_color = "#f0c040"
                    status_text  = "Idle for a while"
                else:
                    status_color = "#ff6b6b"
                    status_text  = "Not used in a long time!"

                weekly_count = len(df)

                # No emojis — plain text only
                for _, row in df.tail(8).iloc[::-1].iterrows():
                    icon = "PICKUP" if row['event_type'] == "PICKUP" else "PUTDOWN"
                    recent_rows += f"""
                    <tr>
                        <td>{icon}</td>
                        <td>{row['timestamp'].strftime('%H:%M %d/%m')}</td>
                        <td>{row['object_id']}</td>
                    </tr>"""

        except Exception as e:
            recent_rows = f"<tr><td colspan='3'>Error: {e}</td></tr>"

    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Objects That Remember</title>
  <meta http-equiv="refresh" content="10">
  <style>
    * {{ margin:0; padding:0; box-sizing:border-box; }}
    body {{
      background: #0c0c10;
      color: #e8e8f0;
      font-family: monospace;
      padding: 32px;
    }}
    h1 {{ color: #f0c040; font-size: 28px; margin-bottom: 4px; }}
    .sub {{ color: #7a7a9a; font-size: 12px; margin-bottom: 32px; }}
    .grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      max-width: 700px;
    }}
    .card {{
      background: #1a1a25;
      border: 1px solid #2a2a3d;
      padding: 20px;
    }}
    .card-label {{
      font-size: 10px;
      letter-spacing: .1em;
      color: #7a7a9a;
      text-transform: uppercase;
    }}
    .card-val {{
      font-size: 20px;
      margin-top: 6px;
      color: #40d9a0;
    }}
    .status {{ color: {status_color}; }}
    .stream-box {{ margin-top: 24px; max-width: 700px; }}
    .stream-box h2 {{
      font-size: 11px;
      color: #7a7a9a;
      letter-spacing: .1em;
      text-transform: uppercase;
      margin-bottom: 10px;
    }}
    img {{ width: 100%; border: 1px solid #2a2a3d; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 24px;
      max-width: 700px;
      font-size: 12px;
    }}
    th {{
      text-align: left;
      padding: 8px 12px;
      border-bottom: 1px solid #2a2a3d;
      color: #7a7a9a;
      font-size: 10px;
      letter-spacing: .1em;
      text-transform: uppercase;
    }}
    td {{ padding: 8px 12px; border-bottom: 1px solid #1a1a25; }}
  </style>
</head>
<body>
  <h1>Objects That Remember</h1>
  <p class="sub">Auto-refreshes every 10 seconds</p>

  <div class="grid">
    <div class="card">
      <div class="card-label">Last Seen</div>
      <div class="card-val">{last_seen}</div>
    </div>
    <div class="card">
      <div class="card-label">Time Idle</div>
      <div class="card-val status">{hours_idle}</div>
    </div>
    <div class="card">
      <div class="card-label">Status</div>
      <div class="card-val status">{status_text}</div>
    </div>
    <div class="card">
      <div class="card-label">Total Events</div>
      <div class="card-val">{weekly_count}</div>
    </div>
  </div>

  <div class="stream-box">
    <h2>Live Camera Feed</h2>
    <img src="http://{ESP32_IP}/stream" alt="Camera loading...">
  </div>

  <table>
    <tr><th>Event</th><th>Time</th><th>Object</th></tr>
    {recent_rows if recent_rows else '<tr><td colspan="3" style="color:#7a7a9a">No events yet - pick up your object!</td></tr>'}
  </table>
</body>
</html>"""

    # Write with UTF-8 encoding
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        build_html()
        self.path = '/' + HTML_FILE
        return super().do_GET(self)

    def log_message(self, format, *args):
        pass  # silence logs

def main():
    print("=" * 40)
    print("  Objects That Remember - Dashboard")
    print("=" * 40)
    print("Starting server...")
    print("Open this in your browser:")
    print(f"  http://localhost:{PORT}")
    print("\nPress Ctrl+C to stop.\n")

    build_html()

    with http.server.HTTPServer(("", PORT), Handler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nDashboard stopped.")

if __name__ == "__main__":
    main()
