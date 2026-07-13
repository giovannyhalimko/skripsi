"""HTML → PDF bersih (tanpa header/footer file:///) via Chrome DevTools Protocol.
Menghormati @page & @media print di CSS (preferCSSPageSize). Usage:
  python html_to_pdf.py <file.html> [file2.html ...]
"""
import json, base64, subprocess, time, os, sys, urllib.request
from websocket import create_connection

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9411


def render(html_path, pdf_path):
    proc = subprocess.Popen(
        [CHROME, "--headless=new", f"--remote-debugging-port={PORT}", "--disable-gpu",
         "--no-first-run", "--no-default-browser-check", "--hide-scrollbars", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        ws = None
        for _ in range(60):
            try:
                d = json.load(urllib.request.urlopen(f"http://localhost:{PORT}/json"))
                pages = [t for t in d if t.get("type") == "page"]
                if pages:
                    ws = pages[0]["webSocketDebuggerUrl"]; break
            except Exception:
                pass
            time.sleep(0.2)
        if not ws:
            raise RuntimeError("DevTools tidak siap")
        conn = create_connection(ws, max_size=None, suppress_origin=True)
        n = [0]

        def cmd(method, params=None, wait_event=None):
            n[0] += 1
            conn.send(json.dumps({"id": n[0], "method": method, "params": params or {}}))
            while True:
                m = json.loads(conn.recv())
                if wait_event and m.get("method") == wait_event:
                    return m
                if m.get("id") == n[0] and not wait_event:
                    return m

        cmd("Page.enable")
        cmd("Page.navigate", {"url": "file://" + os.path.abspath(html_path)})
        cmd("Page.enable", wait_event="Page.loadEventFired")
        time.sleep(1.8)  # settle fonts/layout
        r = cmd("Page.printToPDF", {
            "displayHeaderFooter": False,
            "printBackground": True,
            "preferCSSPageSize": True,
            "paperWidth": 8.27, "paperHeight": 11.69,  # A4 fallback
        })
        open(pdf_path, "wb").write(base64.b64decode(r["result"]["data"]))
        conn.close()
        print("  ->", os.path.basename(pdf_path))
    finally:
        proc.terminate()
        try: proc.wait(timeout=5)
        except Exception: proc.kill()


if __name__ == "__main__":
    for f in sys.argv[1:]:
        out = os.path.splitext(f)[0] + ".pdf"
        print("rendering", os.path.basename(f))
        render(f, out)
