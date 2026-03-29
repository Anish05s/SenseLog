# ================================================
# dashboard.py - Objects That Remember
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

ESP32_IP  = "192.168.1.37"   #IP Address of Module
CSV_FILE  = "events.csv"
HTML_FILE = "dashboard.html"
SNAP_DIR  = "snapshots"
PORT      = 5000


def get_snapshots():
    if not os.path.exists(SNAP_DIR):
        return []
    files = sorted(os.listdir(SNAP_DIR), reverse=True)
    return [f for f in files if f.endswith('.jpg')][:6]


def build_html():
    last_seen = "No data yet"
    hours_idle = "--"
    total_events = 0
    status_color = "#7a7a9a"
    status_text = "No data"
    recent_rows = ""
    snap_html = ""

    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)

            if {'object_id', 'event_type', 'timestamp'}.issubset(df.columns):

                if len(df) > 0:
                    current_year = datetime.now().year

                    df['timestamp'] = pd.to_datetime(
                        df['timestamp'] + f" {current_year}",
                        format="%H:%M %d/%m %Y",
                        errors='coerce'
                    )

                    df = df.dropna()

                    if len(df) > 0:
                        last = df.iloc[-1]

                        last_seen = last['timestamp'].strftime("%H:%M on %d/%m")

                        now = datetime.now()
                        last_dt = last['timestamp'].to_pydatetime()

                        diff = (now - last_dt).total_seconds() / 3600
                        hours_idle = f"{round(diff, 1)} hrs ago"

                        total_events = len(df)

                        if diff < 1:
                            status_color = "#40d9a0"
                            status_text = "Just used!"
                        elif diff < 12:
                            status_color = "#40d9a0"
                            status_text = "Recently used"
                        elif diff < 36:
                            status_color = "#f0c040"
                            status_text = "Idle"
                        else:
                            status_color = "#ff6b6b"
                            status_text = "Long time unused"

                        for _, row in df.tail(8).iloc[::-1].iterrows():
                            e = row['event_type']

                            if e == "PICKED_UP":
                                color = "#40d9a0"
                            elif e == "PERSON":
                                color = "#f0c040"
                            else:
                                color = "#7a7a9a"

                            recent_rows += f"""
                            <tr>
                                <td style="color:{color}">{e}</td>
                                <td>{row['timestamp'].strftime('%H:%M %d/%m')}</td>
                                <td>{row['object_id']}</td>
                            </tr>
                            """
            else:
                recent_rows = "<tr><td colspan='3'>Invalid CSV format</td></tr>"

        except Exception as e:
            recent_rows = f"<tr><td colspan='3'>Error: {e}</td></tr>"

    for snap in get_snapshots():
        snap_html += f'<img src="{SNAP_DIR}/{snap}" style="width:30%;margin:4px;">'

    html = f"""
    <html>
    <head>
        <meta http-equiv="refresh" content="5">
        <title>Dashboard</title>
    </head>
    <body style="background:#111;color:white;font-family:monospace">

        <h1>Objects That Remember</h1>

        <p>Last Activity: {last_seen}</p>
        <p>Time Since: {hours_idle}</p>
        <p style="color:{status_color}">Status: {status_text}</p>
        <p>Total Events: {total_events}</p>

        <h2>Live Stream</h2>
        <img src="http://{ESP32_IP}/stream" width="500">

        <h2>Events</h2>
        <table border="1">
            <tr><th>Event</th><th>Time</th><th>Object</th></tr>
            {recent_rows}
        </table>

        <h2>Snapshots</h2>
        {snap_html if snap_html else "<p>No snapshots</p>"}

    </body>
    </html>
    """

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html)


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            build_html()
            self.path = '/' + HTML_FILE
        return super().do_GET()


def main():
    print("Dashboard running at http://localhost:5000")
    build_html()

    with http.server.HTTPServer(("", PORT), Handler) as s:
        try:
            s.serve_forever()
        except KeyboardInterrupt:
            print("Stopped.")


if __name__ == "__main__":
    main()
