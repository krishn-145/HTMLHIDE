#!/usr/bin/env python3
import base64
import re
import sys
from pathlib import Path

def minify_css(css):
    css = re.sub(r"/\*(?!\!).*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,>+~])\s*", r"\1", css)
    css = re.sub(r";}", "}", css)
    return css.strip()

def minify_js(js):
    # Conservative minification; does not rename variables or alter program logic.
    js = re.sub(r"/\*[\s\S]*?\*/", "", js)
    js = re.sub(r"(^|[\s;])//[^\r\n]*", r"\1", js)
    js = re.sub(r"\s+", " ", js)
    js = re.sub(r"\s*([{}();,:=<>+\-*\/])\s*", r"\1", js)
    return js.strip()

def transform(src):
    counts = {"css": 0, "js": 0}

    def css_repl(m):
        counts["css"] += 1
        return m.group(1) + minify_css(m.group(2)) + m.group(3)

    src = re.sub(
        r"(<style\b[^>]*>)(.*?)(</style\s*>)",
        css_repl, src, flags=re.I | re.S
    )

    def js_repl(m):
        attrs, body = m.group(1), m.group(2)
        if re.search(r"\bsrc\s*=", attrs, re.I):
            return m.group(0)
        counts["js"] += 1
        return "<script" + attrs + ">" + minify_js(body) + "</script>"

    src = re.sub(
        r"<script\b([^>]*)>(.*?)</script\s*>",
        js_repl, src, flags=re.I | re.S
    )

    src = re.sub(r"<!--(?!\[if).*?-->", "", src, flags=re.S | re.I)
    parts = re.split(
        r"(<(?:pre|textarea)\b[^>]*>.*?</(?:pre|textarea)>)",
        src, flags=re.I | re.S
    )
    result = []
    for p in parts:
        if re.match(r"<(?:pre|textarea)\b", p, re.I):
            result.append(p)
        else:
            p = re.sub(r">\s+<", "><", p)
            p = re.sub(r"[ \t]{2,}", " ", p)
            result.append(p)
    return "".join(result).strip(), counts

def quote_js(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"

def build_loader(payload):
    chunks = [payload[i:i+128] for i in range(0, len(payload), 128)]
    arr = ",".join(quote_js(x) for x in chunks)
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Protected Page</title>
<script>
(function(){
"use strict";
var p=[PAYLOAD].join("");
var b=atob(p),u=new Uint8Array(b.length),i;
for(i=0;i<b.length;i++)u[i]=b.charCodeAt(i);
var h=new TextDecoder("utf-8").decode(u);
document.open();
document.write(h);
document.close();
})();
</script>
</head>
<body><noscript>JavaScript is required.</noscript></body>
</html>""".replace("PAYLOAD", arr)

def main():
    if len(sys.argv) != 3:
        print("Usage: python codehide.py INPUT OUTPUT")
        return 2
    inp, out = Path(sys.argv[1]), Path(sys.argv[2])
    if not inp.is_file():
        print("ERROR: input file not found")
        return 1
    try:
        original = inp.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print("ERROR: index.html must be UTF-8")
        return 1

    optimized, counts = transform(original)
    payload = base64.b64encode(optimized.encode("utf-8")).decode("ascii")
    final = build_loader(payload)

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(final, encoding="utf-8")

    print()
    print("╭────────────────────────────────────────────╮")
    print("│ CODEHIDEADVANCED BUILD REPORT           │")
    print("├────────────────────────────────────────────┤")
    print(f"│ Original HTML : {len(original.encode('utf-8')):,} bytes")
    print(f"│ Optimized HTML: {len(optimized.encode('utf-8')):,} bytes")
    print(f"│ Final loader  : {len(final.encode('utf-8')):,} bytes")
    print(f"│ Inline CSS    : {counts['css']} block(s)")
    print(f"│ Inline JS     : {counts['js']} block(s)")
    print("╰────────────────────────────────────────────╯")
    print(f"[+] Created: {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
