"""
Portfolio fix script — Cloudflare email obfuscation hatalarını düzeltir.
Kullanım: index.html dosyasının yanına koy, terminalde çalıştır:
    python fix_portfolio.py
"""

import re

INPUT  = "index.html"
OUTPUT = "index.html"   # aynı dosyanın üzerine yazar
EMAIL  = "yuzun2005@gmail.com"

with open(INPUT, "r", encoding="utf-8") as f:
    html = f.read()

original = html

# 1) Tüm /cdn-cgi/l/email-protection#... href'lerini mailto: ile değiştir
html = re.sub(
    r'/cdn-cgi/l/email-protection#[a-f0-9]+',
    f'mailto:{EMAIL}',
    html
)

# 2) Cloudflare __cf_email__ span'larını gerçek email adresiyle değiştir
html = re.sub(
    r'<span class="__cf_email__"[^>]*>.*?</span>',
    EMAIL,
    html,
    flags=re.DOTALL
)

# 3) Ölü Cloudflare email-decode script tag'ini sil
html = re.sub(
    r'<script[^>]+src="/cdn-cgi/scripts/[^"]+/email-decode\.min\.js"[^>]*></script>\n?',
    '',
    html
)

if html != original:
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Düzeltmeler uygulandı → {OUTPUT}")
    print(f"   • Email href'leri: mailto:{EMAIL} olarak güncellendi")
    print(f"   • __cf_email__ span'ları: gerçek email ile değiştirildi")
    print(f"   • Cloudflare email-decode script tag'i silindi")
else:
    print("⚠️  Hiçbir şey değişmedi — zaten düzeltilmiş ya da pattern bulunamadı.")
