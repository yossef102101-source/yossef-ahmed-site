from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from pathlib import Path
import json, html, os

BASE = Path(__file__).resolve().parent
DATA_FILE = BASE / 'site_settings.json'
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '')  # اضبطها في إعدادات الاستضافة ولا تستخدم كلمة مرور افتراضية
DEFAULTS = {
    'name': 'يوسف أحمد',
    'tagline': 'ملك البرمجة والأمن السيبراني 👑 شغوف بالتكنولوجيا، وبناء المواقع، وحماية الأنظمة واكتشاف الثغرات بشكل أخلاقي.',
    'photo': '',
    'tiktok': 'https://www.tiktok.com/@y.ossef__',
    'facebook': 'https://www.facebook.com/share/19aM2TwRJ2/',
    'instagram': 'https://www.instagram.com/yossef_ahmed0_1/',
    'whatsapp1': 'https://wa.me/201003086128',
    'whatsapp2': 'https://wa.me/201221483129',
    'bg': '#0b0b0b',
    'gold': '#e3bd70',
    'card': '#171717'
}

def load_settings():
    try:
        data = json.loads(DATA_FILE.read_text(encoding='utf-8'))
        return {**DEFAULTS, **data}
    except Exception:
        return DEFAULTS.copy()

def safe(v):
    return html.escape(str(v or ''), quote=True)

def page(s):
    photo = ('<img class="avatar" src="%s" alt="صورة يوسف">' % safe(s['photo'])) if s['photo'] else '<div class="avatar initials">YA</div>'
    return '''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="%s"><title>%s | الموقع الرسمي</title><style>
*{box-sizing:border-box}body{margin:0;background:%s;color:#f8f5ed;font-family:Tahoma,Arial,sans-serif;line-height:1.9}a{color:inherit;text-decoration:none}.wrap{width:90%%;max-width:1000px;margin:auto}header{padding:16px 0;border-bottom:1px solid %s55}nav{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}.brand,h1 span,h2 span,.gold{color:%s}.hero{text-align:center;min-height:70vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:35px 0}.avatar{width:130px;height:130px;border:3px solid %s;border-radius:50%%;object-fit:cover;box-shadow:0 0 25px %s44}.initials{display:grid;place-items:center;font-size:36px;color:%s;background:#222}.tag{color:%s}h1{font-size:clamp(32px,7vw,58px);margin:10px 0}.intro{max-width:700px;color:#c9c3b8}.btn{display:inline-block;border:1px solid %s;border-radius:28px;padding:8px 20px;margin:5px}.btn.primary{background:%s;color:#111;font-weight:bold}section{padding:42px 0}.title{text-align:center;font-size:28px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:15px}.tile{background:%s;border:1px solid %s44;border-radius:16px;padding:20px;text-align:center;overflow-wrap:anywhere}.tile h3{color:%s}.muted{color:#c9c3b8;font-size:14px}footer{text-align:center;padding:25px;border-top:1px solid %s44;color:#c9c3b8}.adminlink{font-size:12px;color:#aaa} @media(max-width:600px){nav{justify-content:center}}
</style></head><body><header><nav class="wrap"><strong class="brand">👑 %s</strong><div><a href="#about">نبذة عني</a> · <a href="#social">حساباتي</a> · <a href="#contact">تواصل معي</a></div></nav></header>
<main><section class="hero wrap" id="about">%s<div class="tag">💻 PROGRAMMING • CYBER SECURITY 🛡️</div><h1>أنا <span>%s</span></h1><p class="intro">%s</p><div><a class="btn primary" href="#social">حساباتي 🔗</a><a class="btn" href="#contact">تواصل معي ☎️</a></div></section>
<section id="social"><div class="wrap"><h2 class="title">حساباتي على <span class="gold">السوشيال ميديا</span></h2><div class="grid"><a class="tile" href="%s" target="_blank" rel="noopener"><h3>🎵 TikTok</h3><p class="muted">افتح الحساب ↗</p></a><a class="tile" href="%s" target="_blank" rel="noopener"><h3>📘 Facebook</h3><p class="muted">افتح الحساب ↗</p></a><a class="tile" href="%s" target="_blank" rel="noopener"><h3>📸 Instagram</h3><p class="muted">افتح الحساب ↗</p></a></div></div></section>
<section id="contact"><div class="wrap"><h2 class="title">خلّينا <span>نتواصل</span> 💬</h2><div class="grid"><a class="tile" href="%s" target="_blank" rel="noopener"><h3>💚 واتساب الأول</h3><p class="muted">راسلني مباشرة ↗</p></a><a class="tile" href="%s" target="_blank" rel="noopener"><h3>💚 واتساب الثاني</h3><p class="muted">راسلني مباشرة ↗</p></a></div></div></section></main><footer>صُنع بكل شغف بواسطة <span class="gold">%s</span> 👑<br><a class="adminlink" href="/admin">لوحة التحكم</a></footer></body></html>''' % (
        safe(s['bg']), safe(s['name']), safe(s['bg']), safe(s['gold']), safe(s['gold']), safe(s['gold']), safe(s['gold']), safe(s['gold']), safe(s['gold']), safe(s['gold']), safe(s['card']), safe(s['gold']), safe(s['gold']), safe(s['gold']), safe(s['gold']), safe(s['name']), photo, safe(s['name']), safe(s['tagline']), safe(s['tiktok']), safe(s['facebook']), safe(s['instagram']), safe(s['whatsapp1']), safe(s['whatsapp2']), safe(s['name']))

def admin_page(message=''):
    s = load_settings()
    fields = [('name','الاسم الظاهر','text'),('tagline','الوصف','textarea'),('photo','رابط الصورة (اختياري)','url'),('tiktok','رابط تيك توك','url'),('facebook','رابط فيسبوك','url'),('instagram','رابط إنستجرام','url'),('whatsapp1','رابط واتساب الأول','url'),('whatsapp2','رابط واتساب الثاني','url'),('bg','لون خلفية الموقع','color'),('gold','اللون الأساسي','color'),('card','لون البطاقات','color')]
    inputs=[]
    for key,label,typ in fields:
        value=safe(s.get(key,''))
        if typ=='textarea': control='<textarea name="%s" rows="4">%s</textarea>'%(key,value)
        else: control='<input name="%s" type="%s" value="%s" %s>'%(key,typ,value, 'required' if key in ('name','tagline') else '')
        inputs.append('<label>%s%s</label>'%(label,control))
    return '''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>لوحة تحكم يوسف</title><style>body{background:#101010;color:#f7f2e8;font-family:Tahoma,Arial;padding:18px;line-height:1.8}.panel{max-width:720px;margin:auto;background:#1b1b1b;padding:22px;border:1px solid #cba75c;border-radius:18px}h1{color:#e3bd70}label{display:block;margin:14px 0;font-weight:bold}input,textarea{display:block;width:100%%;padding:12px;margin-top:6px;border-radius:9px;border:1px solid #666;background:#090909;color:#fff;font:inherit}input[type=color]{height:52px;padding:5px}button{background:#e3bd70;color:#111;border:0;border-radius:10px;padding:13px 18px;font-weight:bold;font-size:16px;width:100%%}a{color:#e3bd70}.note{color:#c8c0b2;font-size:14px}.msg{color:#8ee6a1}</style></head><body><div class="panel"><h1>👑 لوحة تحكم يوسف أحمد</h1><p class="note">عدّل البيانات ثم اضغط حفظ. التغييرات محفوظة في ملف site_settings.json على نفس الجهاز.</p><p class="msg">%s</p><form method="post" action="/save"><label>كلمة مرور لوحة التحكم<input type="password" name="password" required autocomplete="current-password"></label>%s<button type="submit">💾 حفظ التعديلات</button></form><p><a href="/">← مشاهدة الموقع</a></p><p class="note">تنبيه: دي لوحة محلية على موبايلك. لا ترفعها للإنترنت كما هي، وغيّر كلمة المرور الافتراضية داخل الكود.</p></div></body></html>'''%(safe(message),''.join(inputs))

class Handler(BaseHTTPRequestHandler):
    def send_html(self, content, status=200):
        data=content.encode('utf-8'); self.send_response(status); self.send_header('Content-Type','text/html; charset=utf-8'); self.send_header('Content-Length',str(len(data))); self.send_header('Cache-Control','no-store'); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        if self.path.split('?')[0]=='/admin': self.send_html(admin_page())
        else: self.send_html(page(load_settings()))
    def do_POST(self):
        if self.path!='/save': self.send_html('Not found',404); return
        length=int(self.headers.get('Content-Length','0'))
        if length>20000: self.send_html(admin_page('البيانات كبيرة جدًا.'),413); return
        form=parse_qs(self.rfile.read(length).decode('utf-8'),keep_blank_values=True)
        password=form.get('password',[''])[0]
        if password != ADMIN_PASSWORD:
            self.send_html(admin_page('كلمة المرور غير صحيحة.'),403); return
        current=load_settings()
        allowed=set(DEFAULTS.keys())
        for key in allowed:
            if key in form:
                val=form[key][0].strip()
                if key in ('bg','gold','card') and not (len(val)==7 and val.startswith('#') and all(c in '0123456789abcdefABCDEF' for c in val[1:])):
                    continue
                current[key]=val[:2000]
        try:
            DATA_FILE.write_text(json.dumps(current,ensure_ascii=False,indent=2),encoding='utf-8')
            self.send_html(admin_page('تم حفظ التعديلات بنجاح ✅'))
        except Exception as e:
            self.send_html(admin_page('تعذّر الحفظ: '+str(e)))
    def log_message(self, fmt, *args): pass

if __name__=='__main__':
    print('موقع يوسف: http://127.0.0.1:8000')
    print('لوحة التحكم: http://127.0.0.1:8000/admin')
    port = int(os.environ.get('PORT', '8000'))
    if not ADMIN_PASSWORD:
        print('تنبيه: اضبط متغير البيئة ADMIN_PASSWORD في إعدادات الاستضافة قبل استخدام لوحة التحكم.')
    HTTPServer(('0.0.0.0', port),Handler).serve_forever()
