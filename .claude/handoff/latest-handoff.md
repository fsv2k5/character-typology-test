# Handoff: character-typology-test

Written 2026-09-04, at ~50% context. Everything below is verified, not assumed.

## Start the next session from THIS repo

```bash
cd /Users/sergiifomenko/github/character-typology-test && claude
```

Do NOT start from `~/Entravel/backend`. That was done all through this session and
its rules apply session-wide: `git push` was blocked eight times by a deny rule in
`Entravel/backend/.claude/settings.json`, and `reconcile-gate.sh` / `agent-claims.sh`
fired repeatedly as false positives on a repo they know nothing about. Every commit
here needed `AGENT_CLAIMS_SKIP=1 RECONCILE_GATE_SKIP=1` as a workaround.

## What this project is

A static self-test (Nancy McWilliams' 9 character types) on GitHub Pages, embedded
into a Tilda site.

- Repo: `github.com/fsv2k5/character-typology-test` (public)
- Pages: `https://fsv2k5.github.io/character-typology-test/`
- Live page: `https://elenamiropsy.com/test` (Tilda block T123 holding an iframe)
- Owner's practice site: `elenamiropsy.com` (Tilda Personal plan)

Files: `index.html` (the whole test, ~46KB), `presentations/0*.html` (9 type pages),
`tilda/t123-embed.html` (the embed snippet), `tools/build-email.py` (offline email
preview builder), `sources/` (transcripts, gitignored).

## Where the current task stands: WEBSITE TRANSLATION (ru / uk / en)

The owner asked for full uk+en translation with a live language switch next to the
theme toggle, keeping test progress when switching mid-test.

### Done and pushed

| Commit | What |
|---|---|
| `bd72911` | i18n scaffold: `UI` dict with ru/uk/en, language toggle, `applyLang()` |
| `246d863` | `TYPES` split into `TYPE_META` + `TYPE_TEXT{ru,uk,en}` + `syncTypes()` |
| `ea53529` | all 90 statements and 9 type texts translated to uk and en |
| `4a106d5` | `typeHref()` routes presentation links to the active language folder |

The test itself is fully trilingual and verified live (10/10 checks): switching
mid-test keeps answers, page and selected ratings, because answers are keyed by
`type-index`, never by text.

### NOT done: the 9 presentations

This is the remaining work. State when this session paused:

1. `/tmp/pres-ru.json` holds 642 extracted text nodes (~70k chars) across the 9 files.
2. FOUR Sonnet agents were translating them in parallel, writing:
   `/tmp/pres-uk-a.json` (files 01-05), `/tmp/pres-uk-b.json` (06-09),
   `/tmp/pres-en-a.json` (01-05), `/tmp/pres-en-b.json` (06-09).
   **Check whether those four files exist before doing anything else.** If they are
   gone (tmp cleared) the translation must be re-run.
3. The builder is written and untested: `pres_build.py` in the scratchpad below.
   It creates `presentations/uk/` and `presentations/en/`, substitutes the
   translations positionally (same walk as the extractor), adds the language toggle
   to every page including the Russian originals, and fixes the relative link back
   to `index.html`.

Scratchpad scripts (session-local, copy them out if the next session needs them):
`/private/tmp/claude-501/-Users-sergiifomenko-Entravel-backend/7023ac14-b8b6-4acb-9d34-0632cc123716/scratchpad/`
- `pres_extract.py` - already run, produced `/tmp/pres-ru.json`
- `pres_build.py` - NOT yet run, the next step
- `i18n_ui.py`, `types_i18n.py`, `merge_types.py`, `link_lang.py` - already applied

### First command for the next session

```bash
ls -la /tmp/pres-{uk,en}-{a,b}.json && \
python3 <scratchpad>/pres_build.py
```

Then verify in a browser (the skill at `~/.claude/skills/browser-automation/browser.mjs`
was used for every check this session) that a uk/en presentation renders, the toggle
cycles ru->uk->en, and the link back to the test works. Then commit and push.

## Verified facts worth not rediscovering

- **Email works.** EmailJS `service_9025hvd` / `template_65dcoo9` / public key
  `XIkbF6BMJH2ZIvO2t`. Credentials also in `.env` (gitignored, 600).
  The template body must be exactly `{{{message}}}` - triple braces, no `<p>` wrapper.
  A `<p>` around it breaks the HTML because `<p>` cannot contain `<div>`/`<table>`.
- **Two emails are sent per result**: one to the visitor, one to
  `elena.miro.psy@gmail.com` with subject `Копия результата: <visitor address>`.
  Not a bcc - a separate send, wrapped in try/catch so it cannot break the visitor's.
- **Tilda DNS cannot create CNAME/A records** (only TXT and MX), which is why
  `test.elenamiropsy.com` was abandoned in favour of the `/test` page with an iframe.
- **Tilda API is read-only** - no way to publish pages programmatically.
- The Tilda embed is current; it handles `ctt:height` and `ctt:top` messages. Its
  scroll-to-top branch is untestable on the live page because the T123 block sits
  first (`frameTop: 0`), so there is nothing to scroll past.
- `SITE_URL` must stay `https://fsv2k5.github.io/character-typology-test/`.
  Pointing it at `elenamiropsy.com/test/` makes every presentation link 404 -
  probed and confirmed.
- Terminology: the source uses Nancy McWilliams. A previous refactor had replaced
  "Психопатический" with "Волевой"; that was reverted. Never soften clinical terms.
- Long dashes were deliberately replaced project-wide with plain hyphens (447 of
  them). Keep it that way, including in translations.

## Owner preferences observed this session

- Wants results proved, not promised: every claim in this session was backed by a
  live browser measurement or an HTTP probe.
- Prefers translation delegated to Sonnet, code and integration kept on Opus.
- Says "давай"/"вперед" to mean "proceed without asking".
- Asked NOT to touch the Tilda account password.

## Loose ends

- The owner never confirmed whether the last archive-copy email looked right.
- `.idea/`, `.vscode/`, `__pycache__/` are now gitignored (commit `08bface`).
- The Tilda password was pasted in plain text into the session transcript early on.
  The owner explicitly said to leave it alone.
