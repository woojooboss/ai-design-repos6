"""page.html → index.html: 쓰인 글자만 남긴 Pretendard·JetBrains Mono를 HTML 안에 넣는다 (외부 폰트 요청 없음).
실행: python build.py   (page.html을 고친 뒤 다시 돌린다)"""
import base64
import io
import re
from pathlib import Path

from fontTools import subset as fts

HERE = Path(__file__).parent
FONTS = HERE.parents[1] / "Video" / "render" / "public" / "fonts"
SLOTS = {"F_MEDIUM": "Pretendard-Medium.woff2", "F_BOLD": "Pretendard-Bold.woff2", "F_EXTRABOLD": "Pretendard-ExtraBold.woff2",
         "F_BLACK": "Pretendard-Black.woff2", "F_MONO": "JetBrainsMono-Medium.woff2", "F_MONO_BOLD": "JetBrainsMono-Bold.woff2"}


def subset(path: Path, chars: str) -> bytes:
    opt = fts.Options()
    opt.flavor, opt.layout_features, opt.notdef_outline = "woff2", ["*"], True
    font = fts.load_font(str(path), opt)
    s = fts.Subsetter(options=opt)
    s.populate(text=chars)
    s.subset(font)
    buf = io.BytesIO()
    font.save(buf)
    return buf.getvalue()


html = (HERE / "page.html").read_text(encoding="utf-8")
text = re.sub(r"<style>.*?</style>|<script>.*?</script>|<[^>]+>", " ", html, flags=re.S)
chars = "".join(sorted(set(text + "복사됨Ctrl+C0123456789→·★①②"))) # 스크립트가 바꿔 넣는 글자도 포함
total = 0
for key, name in SLOTS.items():
    data = subset(FONTS / name, chars)
    total += len(data)
    html = html.replace("{{" + key + "}}", "data:font/woff2;base64," + base64.b64encode(data).decode())
(HERE / "index.html").write_text(html, encoding="utf-8")
print(f"index.html 완성 · 글자 {len(chars)}개 · 폰트 {total / 1024:.0f} KB")
