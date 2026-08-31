#!/usr/bin/env python3
"""Build the HTML result email from a profile, mirroring the on-screen result.

Email clients drop CSS variables, grid and <style>, so the on-screen look is
rebuilt with tables + inline styles. Palette is the site's light theme.
"""
import json, re, sys

INK, MUTED, LINE = "#2e2c28", "#6f6d64", "#e2ddd0"
BG, CARD, CARD2 = "#f6f3ec", "#ffffff", "#f1eee6"
ACCENT_UI = "#4e6b49"
WARN_BG, WARN_LINE, WARN_INK = "#faf5e8", "#ddc9a0", "#7c6a3a"
SERIF = "Literata,'PT Serif',Georgia,serif"
SANS = "Inter,-apple-system,'Segoe UI',Roboto,Arial,sans-serif"


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def bar(name, score, color):
    """One scale row: name, track with coloured fill, value."""
    pct = max(0, min(100, int(score)))
    return f"""
<tr>
  <td style="padding:7px 0;font:400 15px {SANS};color:{INK};width:210px">{esc(name)}</td>
  <td style="padding:7px 10px">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"
           style="background:{CARD2};border:1px solid {LINE};border-radius:8px">
      <tr><td style="padding:0">
        <table role="presentation" cellpadding="0" cellspacing="0" border="0"
               width="{pct}%" style="width:{pct}%">
          <tr><td style="background:{color};height:14px;border-radius:8px;font-size:0;line-height:14px">&nbsp;</td></tr>
        </table>
      </td></tr>
    </table>
  </td>
  <td style="padding:7px 0;font:400 14px {SANS};color:{MUTED};text-align:right;width:44px">{pct}</td>
</tr>"""


def top_card(rank, name, score, color, summary, quotes):
    q = "".join(
        f'<div style="font:italic 400 14px {SANS};color:{INK};margin:8px 0;'
        f'padding-left:12px;border-left:2px solid {LINE}">'
        f'&laquo;{esc(s)}&raquo; - <b>{v}/10</b></div>'
        for s, v in quotes)
    why = (f'<div style="margin-top:12px;border-top:1px dashed {LINE};padding-top:10px">'
           f'<div style="font:400 13px {SANS};color:{MUTED};margin-bottom:4px">'
           f'Сильнее всего у вас откликнулось:</div>{q}</div>') if quotes else ""
    return f"""
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"
       style="background:{CARD};border:1px solid {LINE};border-left:4px solid {color};
              border-radius:14px;margin:16px 0">
  <tr><td style="padding:20px 22px">
    <div style="font:600 12px {SANS};letter-spacing:2px;text-transform:uppercase;color:{ACCENT_UI}">
      {rank} место - {score} из 100</div>
    <div style="font:400 19px {SERIF};color:{INK};margin:6px 0 0">{esc(name)}</div>
    <div style="font:400 15px {SANS};color:{MUTED};margin-top:8px;line-height:1.55">{esc(summary)}</div>
    {why}
  </td></tr>
</table>"""


def build(profile):
    rows = profile["rows"]
    bars = "".join(bar(r["name"], r["score"], r["color"]) for r in rows)
    cards = "".join(
        top_card(i + 1, r["name"], r["score"], r["color"], r["summary"],
                 r.get("quotes", []))
        for i, r in enumerate(rows[:3]))

    return f"""<div style="margin:0;padding:0;background:{BG}">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background:{BG}">
<tr><td align="center" style="padding:28px 12px">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="640"
       style="width:640px;max-width:100%;background:{CARD};border:1px solid {LINE};border-radius:18px">
<tr><td style="padding:32px 34px">

  <div style="font:600 12px {SANS};letter-spacing:2.5px;text-transform:uppercase;color:{ACCENT_UI}">
    Ваш результат</div>
  <h1 style="font:400 30px {SERIF};color:{INK};margin:10px 0 14px">Профиль характера</h1>

  <p style="font:400 15.5px {SANS};color:{MUTED};line-height:1.6;margin:0 0 22px">
    Каждая шкала - от 0 до 100. У большинства людей выражено сразу несколько
    типов, так что смотрите на два-три верхних: это и есть ваш почерк.</p>

  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"
         style="margin:0 0 30px">{bars}
  </table>

  <h2 style="font:400 22px {SERIF};color:{INK};margin:0 0 6px">Ваши ведущие типы - и почему</h2>
  {cards}

  <div style="background:{WARN_BG};border:1px solid {WARN_LINE};color:{WARN_INK};
              border-radius:12px;padding:14px 18px;font:400 14px {SANS};
              line-height:1.55;margin:24px 0 0">
    Высокий балл - не диагноз, а карта привычных стратегий. Если какие-то черты
    всерьёз мешают жить, лучше обсудить это со специалистом, чем воевать с собой.</div>

</td></tr></table>
</td></tr></table></div>"""


if __name__ == "__main__":
    print(build(json.load(open(sys.argv[1], encoding="utf-8"))))
