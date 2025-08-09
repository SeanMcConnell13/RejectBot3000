import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
import os
import time
import random
import sys
import requests
import re
import html

try:
    from bs4 import BeautifulSoup
    HAVE_BS4 = True
except Exception:
    HAVE_BS4 = False

def resource_path(rel_path: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
    return os.path.join(base, rel_path)

APP_DIR = os.path.dirname(__file__)
DATA_DIR = resource_path("data")
OUT_DIR = os.path.join(APP_DIR, "rejections")
TEMPLATES_PATH = resource_path(os.path.join("data", "rejections.txt"))

USER_AGENT = "RejectBot3000/1.0"
FETCH_TIMEOUT = 8
TECH_HINTS = [
    "kubernetes","k8s","docker","terraform","ansible","helm",
    "aws","azure","gcp","devops","sre","observability","prometheus",
    "grafana","splunk","kafka","rabbitmq","postgres","mysql","mssql","mongodb",
    "redis","python","golang","go","rust","c#","dotnet","node","react","typescript",
    "ci/cd","jenkins","github actions","gitlab"
]

REJECTIONS = [
    "Dear Candidate,\n\nThank you for applying to {role}. After careful review, we've decided to move forward with candidates whose experience better aligns with our current priorities. Yours did align... just in the wrong dimension.\n\nWe wish you the best in your future endeavors (preferably in a universe where we exist).\n\nSincerely,\nHuman Resources",
    "Dear Candidate,\n\nWe appreciate your interest in {role}. Unfortunately, after much deliberation, we have chosen to proceed with other applicants - mostly because our hiring committee bonded over a group text about Love Island and now only hires contestants.\n\nKind regards,\nHR Department",
    "Dear Candidate,\n\nThank you for your interest in {role}. At this time, we have decided to move forward with candidates who more closely match our strategic objectives - namely, people who can code, file their taxes, and parallel park in one try.\n\nBest,\nRecruitment Team",
    "Dear Candidate,\n\nWhile your application for {role} was impressive, we are pursuing candidates with a different set of qualifications. Specifically, the ability to survive three consecutive Zoom calls without making a sarcastic face.\n\nWe appreciate the time you invested in applying.\n\nSincerely,\nThe Hiring Committee",
    "Dear Candidate,\n\nWe reviewed your application for {role} and, after careful consideration, will be moving forward with other candidates. In unrelated news, we have a new ping pong champion in the office. Draw your own conclusions.\n\nThank you for your interest.\n\nBest,\nTalent Acquisition",
    "Dear Candidate,\n\nWe enjoyed reading your resume for {role}. It reminded us of simpler times, before we started taking this role seriously, back when 'proficient in Excel' meant you could make the cells change colors.\n\nAll the best,\nHR",
    "Dear Candidate,\n\nThank you for applying to {role}. Unfortunately, we are seeking candidates who can both meet the job requirements and remember to attach their cover letter. Bonus points for using the correct company name.\n\nRegards,\nRecruitment",
    "Dear Candidate,\n\nWe appreciate your interest in {role}. Sadly, we are prioritizing applicants who understand what 'entry level' means to us: 10 years' experience, a PhD, and the ability to work for free for 6 months.\n\nKind regards,\nHR",
    "Dear Candidate,\n\nYour enthusiasm for {role} is noted. However, we require someone who can navigate both Kubernetes clusters and our coffee machine without creating a ticket in Jira.\n\nBest,\nFacilities and HR",
    "Dear Candidate,\n\nThank you for applying to {role}. While your skills are admirable, our team decided to hire someone whose vibe check came back 'Certified Cool Guy' with bonus points for owning a slow cooker.\n\nAll the best,\nHR",
    "Subject: Regarding {role}\n\nNo.\n\nRegards,\nOperations",
    "Dear Candidate,\n\n{role} is not for the faint of heart. We need someone who reads logs like bedtime stories and answers 3am alerts with the enthusiasm of a raccoon finding an open dumpster. Your resume suggests you value sleep. We respect that. Our pager does not.\n\nOps",
    "Dear Candidate,\n\nWe appreciate your application for {role}, but we require someone who can deploy to production with one hand while extinguishing a literal fire with the other. And yes, there will be actual fire.\n\nRegards,\nOps",
    "Dear Candidate,\n\nThank you for applying to {role}. Unfortunately, you have not met our minimum requirement of 'thriving in chaos.' Our last hire built a fully operational CI/CD pipeline from a burning IKEA desk.\n\nOps",
    "Dear Candidate,\n\nWe regret to inform you that your {role} candidacy has been terminated by a kernel panic. We tried rebooting, but our feelings remain the same.\n\nBest,\nInfrastructure Team",
    "Dear Candidate,\n\nThank you for applying to {role}. We have instead decided to fill this position with a raccoon we found in the server room. It passed the background check and knows Python.\n\nBest wishes,\nHR",
    "Dear Candidate,\n\nWe appreciate your interest in {role}. However, we are looking for someone with at least 5 years' experience in technologies that do not exist yet. Bonus if they can also predict the weather.\n\nRegards,\nRecruitment",
    "Dear Candidate,\n\nThank you for applying to {role}. We have decided to promote the office plant instead. It's been here longer, drinks less coffee, and provides more oxygen.\n\nHR",
    "Dear Candidate,\n\nWe appreciate your application for {role}. Unfortunately, our astrologer advised against hiring anyone with Mercury in retrograde, Mars in Scorpio, or an email address that still uses AOL.\n\nKind regards,\nHR",
    "Dear Candidate,\n\nThank you for applying to {role}. We ran your resume through our AI filter, and it decided to become a poet instead of recommending you. It now writes sonnets about Kubernetes.\n\nSincerely,\nHR",
    "Dear Candidate,\n\nThank you for applying to {role}. We flipped a coin. It said no. Then it rolled under the fridge. We took that as a sign.\n\nRegards,\nHR",
    "Dear Candidate,\n\nYour {role} application was spirited, but our CEO's tarot deck suggested otherwise. Also, the deck is never wrong. (Except that one time, but we don't talk about it.)\n\nBest,\nHR",
    "Dear Candidate,\n\nWe appreciate your interest in {role}. Unfortunately, our last hire was too good and set unrealistic expectations for the rest of you. We're still in therapy.\n\nRegards,\nRecruitment",
    "Dear Candidate,\n\nWe read your application for {role} aloud in the break room. It was a hit. You will not be moving forward, but you may have a future in stand-up comedy.\n\nBest,\nHR",
    "Dear Candidate,\n\nWe appreciate your enthusiasm for {role}, but we must decline as we are pivoting to become a gelato stand. Our churn rate will be delicious.\n\nKind regards,\nHR",
    "Dear Candidate,\n\nWe appreciate your interest in {role}. Unfortunately, the position was filled in a dream we had last night, and we must respect dream law. We hope you understand.\n\nSincerely,\nHR",
    "Dear Candidate,\n\nYour application for {role} was impressive, but the role was given to a time traveler from the year 3022. They brought donuts.\n\nBest,\nHR",
    "Dear Candidate,\n\nThank you for your application to {role}. We are holding the role for someone prophesied to arrive during the next eclipse, wearing Crocs and carrying a USB drive.\n\nKind regards,\nHR",
    "Dear Candidate,\n\nWe appreciate your interest in {role}. Unfortunately, our HR department has transcended the need for employees. They now communicate solely through cryptic Slack emojis.\n\nSincerely,\nHR"
]

def ensure_out_dir():
    os.makedirs(OUT_DIR, exist_ok=True)

def fetch_job_text(url: str) -> str | None:
    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=FETCH_TIMEOUT)
        r.raise_for_status()
    except Exception:
        return None
    html_text = r.text
    m = re.search(r"<title[^>]*>(.*?)</title>", html_text, flags=re.IGNORECASE | re.DOTALL)
    title = html.unescape(m.group(1).strip()) if m else ""
    if HAVE_BS4:
        soup = BeautifulSoup(html_text, "html.parser")
        for tag in soup(["script","style","noscript","header","footer","nav","svg"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        content = "\n".join(lines)
    else:
        html_text_clean = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html_text, flags=re.IGNORECASE | re.DOTALL)
        content = re.sub(r"<[^>]+>", "\n", html_text_clean)
        lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
        content = html.unescape("\n".join(lines))
    if title and (not content.startswith(title)):
        content = (title + "\n\n" + content).strip()
    return content[:5000] if content else (title or None)

def infer_role_from_text(txt: str) -> str | None:
    lines = [ln.strip() for ln in txt.splitlines() if ln.strip()]
    if not lines:
        return None
    for ln in lines[:80]:
        lower = ln.lower()
        if lower.startswith("title:") or lower.startswith("job title:"):
            v = ln.split(":", 1)[1].strip()
            if 5 <= len(v) <= 120:
                return v
    first = lines[0]
    chunks = [c.strip() for c in re.split(r"[\-\|\:\u2013\u2014\u2022\u00B7]+", first) if c.strip()]
    role_words = [
        "engineer","developer","manager","architect","administrator","analyst",
        "designer","specialist","lead","principal","director","devops","sre",
        "scientist","consultant","intern","co-op","owner","qa","test","support",
        "security","ios","android","frontend","backend","full stack","platform"
    ]
    for c in chunks:
        if any(w in c.lower() for w in role_words) and 5 <= len(c) <= 120:
            return c
    if 5 <= len(first) <= 120:
        return first
    for ln in lines[1:80]:
        if any(w in ln.lower() for w in role_words) and 5 <= len(ln) <= 120:
            return ln
    return None

def extract_skills(txt: str, max_n: int = 4) -> list[str]:
    low = txt.lower()
    out, seen = [], set()
    for hint in TECH_HINTS:
        if hint in low and hint not in seen:
            out.append(hint); seen.add(hint)
        if len(out) >= max_n:
            break
    return out

def build_letter(role: str, job_txt: str | None = None) -> str:
    role_phrase = role.strip()
    inferred = None
    if not role_phrase and job_txt:
        inferred = infer_role_from_text(job_txt)
        if inferred:
            role_phrase = inferred
    if not role_phrase:
        role_phrase = "the position"
    template = random.choice(REJECTIONS)
    body = template.format(role=role_phrase)
    if job_txt:
        skills = extract_skills(job_txt)
        if skills:
            body += "\n\nP.S. We are prioritizing candidates with: " + ", ".join(skills) + "."
    return body

class Tooltip:
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tip = None
        self.after_id = None
        widget.bind("<Enter>", self._enter)
        widget.bind("<Leave>", self._leave)
    def _enter(self, _):
        self.after_id = self.widget.after(self.delay, self._show)
    def _leave(self, _):
        if self.after_id:
            self.widget.after_cancel(self.after_id)
            self.after_id = None
        self._hide()
    def _show(self):
        if self.tip: return
        x, y, cx, cy = self.widget.bbox("insert") if self.widget.winfo_class() == "Entry" else (0,0,0,0)
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + 20
        self.tip = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        lbl = ttk.Label(tw, text=self.text, style="Tooltip.TLabel", padding=(8,4))
        lbl.pack()
    def _hide(self):
        if self.tip:
            self.tip.destroy()
            self.tip = None

def show_easter_egg(root):
    if random.randint(1, 20) != 1:
        return
    top = tk.Toplevel(root)
    top.title("Congratulations")
    top.attributes("-topmost", True)
    ttk.Label(top, text="Congratulations! You got the job!", padding=12, style="H4.TLabel").pack()
    ttk.Label(top, text="...just kidding.", padding=(12,0), style="Body.TLabel").pack()
    top.after(1200, top.destroy)

def ensure_out_dir():
    os.makedirs(OUT_DIR, exist_ok=True)

def do_generate():
    all_steps = [
        "Locating HR department...",
        "Pouring lukewarm coffee...",
        "Misplacing your resume...",
        "Formatting rejection...",
        "Checking the vibe matrix...",
        "Asking the intern for advice...",
        "Opening 47 Chrome tabs...",
        "Waiting for legal to say no...",
        "Refreshing LinkedIn again...",
        "Turning it off and on again...",
        "Consulting the tarot backlog...",
        "Running AI to replace AI...",
        "Emailing someone named Bob...",
        "Counting years of 'entry level'...",
        "Rebooting the coffee machine...",
        "Blaming the staging database...",
        "Disabling production alarms...",
        "Printing your resume in Comic Sans...",
        "Auditing our meeting about meetings...",
        "Pretending this is Agile..."
    ]
    picks = random.sample(all_steps, 3)
    total_ms = 5000
    per_ms = total_ms // len(picks)
    try:
        btn_gen.state(["disabled"])
    except Exception:
        pass
    prog.place(relx=0, rely=0, relwidth=1.0, height=4)
    prog.start(8)
    def tick(i=0):
        if i < len(picks):
            status.set(picks[i])
            root.update_idletasks()
            root.after(per_ms, lambda: tick(i + 1))
        else:
            _final_generate()
            try:
                btn_gen.state(["!disabled"])
            except Exception:
                pass
            prog.stop()
            prog.place_forget()
    tick(0)

def _final_generate():
    url = url_var.get().strip()
    job_txt = fetch_job_text(url) if url else None
    if url and job_txt is None:
        status.set("Could not read job page. Using generic mode.")
    letter = build_letter("", job_txt)
    output.configure(state="normal")
    output.delete("1.0", "end")
    output.insert("1.0", letter)
    output.configure(state="normal")
    status.set("Ready")
    show_easter_egg(root)

def on_copy():
    text = output.get("1.0", "end").strip()
    if not text:
        messagebox.showinfo("Nothing to copy", "Generate a rejection first."); return
    root.clipboard_clear(); root.clipboard_append(text); root.update()
    messagebox.showinfo("Copied", "Rejection copied to clipboard.")

def on_save_txt():
    text = output.get("1.0", "end").strip()
    if not text:
        messagebox.showinfo("Nothing to save", "Generate a rejection first."); return
    ensure_out_dir()
    ts = int(time.time())
    path = os.path.join(OUT_DIR, f"rejection_{ts}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    messagebox.showinfo("Saved", "Saved to:\n" + os.path.abspath(path))
    status.set("Saved")

root = tk.Tk()
root.title("RejectBot 3000")
root.geometry("1100x720")

style = ttk.Style()
try:
    style.theme_use("clam")
except Exception:
    pass

BG = "#0f172a"
PANEL = "#111827"
CARD = "#0b1220"
TEXT = "#e5e7eb"
SUBTLE = "#94a3b8"
ACCENT = "#f97316"
ACCENT_DARK = "#c2410c"

root.configure(bg=BG)

style.configure("App.TFrame", background=BG)
style.configure("Header.TFrame", background=BG)
style.configure("Card.TFrame", background=CARD, borderwidth=0)
style.configure("TLabel", background=BG, foreground=TEXT)
style.configure("Header.TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 20, "bold"))
style.configure("SubHeader.TLabel", background=BG, foreground=SUBTLE, font=("Segoe UI", 10))
style.configure("H4.TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 12, "bold"))
style.configure("Body.TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 10))
style.configure("Card.TLabel", background=CARD, foreground=TEXT)
style.configure("CardHeader.TLabel", background=CARD, foreground=TEXT, font=("Segoe UI", 11, "bold"))

style.configure("Primary.TButton", font=("Segoe UI", 10), padding=(14, 8))
style.map("Primary.TButton",
          background=[("!disabled", ACCENT), ("active", ACCENT), ("pressed", ACCENT_DARK)],
          foreground=[("!disabled", "#111827")])

style.configure("Ghost.TButton", font=("Segoe UI", 10), padding=(12, 6), background=CARD, relief="flat")
style.map("Ghost.TButton",
          background=[("active", "#0e1526"), ("pressed", "#0c1220")],
          foreground=[("!disabled", TEXT)])

style.configure("Tooltip.TLabel", background="#111111", foreground="#f0f0f0", font=("Segoe UI", 9))

style.configure("Card.TLabelframe", background=CARD, foreground=TEXT, borderwidth=0)
style.configure("Card.TLabelframe.Label", background=CARD, foreground=SUBTLE, font=("Segoe UI", 10, "bold"))

style.configure("Accent.Horizontal.TProgressbar", troughcolor=BG, background=ACCENT, bordercolor=BG, lightcolor=ACCENT, darkcolor=ACCENT)

header = ttk.Frame(root, padding=(16, 14, 16, 8), style="Header.TFrame")
header.pack(fill="x")
ttk.Label(header, text="RejectBot 3000", style="Header.TLabel").pack(anchor="w")
ttk.Label(header, text='"Turning heartbreak into art since 2025"', style="SubHeader.TLabel").pack(anchor="w")

main = ttk.Frame(root, padding=(16, 8, 16, 16), style="App.TFrame")
main.pack(fill="both", expand=True)

pan = ttk.Panedwindow(main, orient="horizontal")
pan.pack(fill="both", expand=True)

left = ttk.Frame(pan, padding=12, style="Card.TFrame")
right = ttk.Frame(pan, padding=12, style="Card.TFrame")
pan.add(left, weight=1)
pan.add(right, weight=2)

url_var = tk.StringVar()

frm_inputs = ttk.Labelframe(left, text="Input", padding=12, style="Card.TLabelframe")
frm_inputs.pack(fill="x")

row_url = ttk.Frame(frm_inputs, style="Card.TFrame"); row_url.pack(fill="x", pady=6)
ttk.Label(row_url, text="Job URL", style="CardHeader.TLabel").pack(anchor="w")
url_entry = ttk.Entry(row_url, textvariable=url_var)
url_entry.pack(fill="x", pady=(4,0))
Tooltip(url_entry, "Paste the hopes and dreams here.")

frm_actions = ttk.Frame(left, padding=(0,12,0,0), style="Card.TFrame"); frm_actions.pack(fill="x")
btn_gen  = ttk.Button(frm_actions, text="Generate", style="Primary.TButton", command=do_generate); btn_gen.pack(side="left")
btn_copy = ttk.Button(frm_actions, text="Copy", style="Ghost.TButton", command=on_copy); btn_copy.pack(side="left", padx=8)
btn_save = ttk.Button(frm_actions, text="Save .txt", style="Ghost.TButton", command=on_save_txt); btn_save.pack(side="left")

frm_preview = ttk.Labelframe(right, text="Preview", padding=12, style="Card.TLabelframe")
frm_preview.pack(fill="both", expand=True)
output = scrolledtext.ScrolledText(frm_preview, wrap="word", height=28, font=("Segoe UI", 10), bg="#0a0f1c", fg=TEXT, insertbackground=TEXT, relief="flat")
output.pack(fill="both", expand=True)

status = tk.StringVar(value="Ready")
status_bar = ttk.Frame(root, style="Header.TFrame")
status_bar.pack(fill="x", side="bottom")
ttk.Label(status_bar, textvariable=status, style="SubHeader.TLabel", padding=(16,6)).pack(side="left")

prog = ttk.Progressbar(status_bar, mode="indeterminate", style="Accent.Horizontal.TProgressbar")
prog.place_forget()

root.mainloop()
