"""Extract the readable text of a Dominion careers (SuccessFactors RMK) job page.

Usage: python -I r_parse_job_page.py <job.html> [...]
Prints title, date, location, req id and the job description as plain text.
Reads files only; executes nothing from them.
"""
import html
import re
import sys


def clean(fragment):
    fragment = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", fragment, flags=re.S | re.I)
    fragment = re.sub(r"<br\s*/?>|</p>|</li>|</div>|</h\d>", "\n", fragment, flags=re.I)
    fragment = re.sub(r"<li[^>]*>", "\n- ", fragment, flags=re.I)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    fragment = html.unescape(fragment)
    fragment = re.sub(r"[ \t\xa0]+", " ", fragment)
    fragment = re.sub(r"\n\s*\n+", "\n", fragment)
    return fragment.strip()


def first(pattern, text):
    m = re.search(pattern, text, flags=re.S | re.I)
    return clean(m.group(1)) if m else ""


def main():
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        title = first(r'<h1[^>]*>(.*?)</h1>', text) or first(r"<title>(.*?)</title>", text)
        date = first(r'itemprop="datePosted"[^>]*content="([^"]+)"', text) or first(r'data-careersite-propertyid="date"[^>]*>(.*?)</', text)
        loc = first(r'data-careersite-propertyid="city"[^>]*>(.*?)</', text)
        req = first(r'data-careersite-propertyid="customfield\d"[^>]*>(.*?)</', text)
        desc = first(r'<span class="jobdescription">(.*)</span>\s*</div>', text)
        if not desc:
            desc = first(r'class="jobdescription"[^>]*>(.*?)<div class="(?:applylink|job-share|social)', text)
        expired = "no longer available" in text.lower() or "job has expired" in text.lower() or "not available" in text.lower()
        print("=" * 100)
        print(f"FILE: {path}")
        print(f"TITLE: {title}\nDATE: {date}\nCITY: {loc}\nREQ/CUSTOM: {req}\nEXPIRED-HINT: {expired}")
        print("DESCRIPTION:\n" + (desc[:12000] if desc else "(no description block found)"))


if __name__ == "__main__":
    main()
