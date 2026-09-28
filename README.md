# cold-email-outreach

A daily, dedup-safe outreach system for finding jobs and freelance projects by email. It's built for
[Raghav Raj Sobti / BluePolaroid](https://bluepolaroid.com) (cinematographer + creative technologist), but anyone can
use it by swapping the profile and templates.

- **Five tracks**: video projects in India · creative technologist roles (anywhere) · remote tech (anywhere) ·
  remote editing (anywhere) · travel/adventure/documentary crew (anywhere)
- **Never emails anyone twice**: tracker, do-not-contact list, 60-day per-company cool-down, and a live Gmail
  sent-mail check before every send
- **Near-zero bounces**: only addresses the company published itself, an MX/DNS check, a role-address filter, and a
  bounce sweep that suppresses dead addresses automatically
- **Tracks everything** in a local spreadsheet: status, source, reply, follow-up, daily run stats
- **Runs every morning at 07:30 IST** as a Claude scheduled task: finds new leads, sends, handles follow-ups,
  updates statuses and the sheet
- **Your data stays on your computer.** This repo holds only code, templates and docs.

---

## How it works

```
             ┌──────────── 07:30 IST scheduled task (Claude) ────────────┐
             │                                                            │
 Gmail  ───► 1. statuses: bounces + replies ──► tracker.csv (LOCAL PC)   │
             │ 2. follow-ups (1 per contact, same thread, day 5)          │
 Web    ───► 3. research leads (published addresses only) → leads.json   │
             │ 4. add-leads → verify (syntax, MX, role, published)        │
             │ 5. pick (mix per track, 1 per company) → batch.json        │
 Gmail  ◄─── 6. live dedupe (in:sent to:) → send → mark-sent             │
 Gmail  ───► 7. bounce sweep → suppress → top up to target               │
             │ 8. log-run → build-xlsx → copy back to Documents\… (LOCAL) │
             └────────────────────────────────────────────────────────────┘
```

### Contact status lifecycle
`new → queued → sent → (bounced | replied | interested | rejected | follow_up_sent → no_reply)`,
plus `do_not_contact` (invalid or opted out) and `legacy_sent` (emailed before this system existed, never contacted again).

---

## Repo layout
```
scripts/outreach.py        tracker CLI (all commands below)
scripts/mxcheck.py         dependency-free MX/A lookup over UDP
templates/*.md             one email template per track + follow-up (front-matter = subject)
config/profile.example.json   your name, links, resumes, template per track
config/settings.example.json  daily target, caps, mix, pause switch
prompts/daily_run.md       the exact instructions the 07:30 scheduled task follows
skills/cold-outreach/      the same workflow as an on-demand Claude skill (/cold-outreach <N>)
docs/best-practices.md     research behind the templates and guardrails (with sources)
docs/lead-sources.md       where leads come from and what's working
```

## Local data folder (never committed)
Default: `C:\Users\<you>\Documents\cold-email-outreach-data\`, or set `OUTREACH_DATA=/path/to/folder`.

| File | What it holds |
|---|---|
| `tracker.csv` | Master list: one row per contact with every field below |
| `suppression.csv` | Do-not-contact: bounced, opted out, legacy recipients |
| `runs.csv` | One row per daily run (picked / sent / bounced / delivered / replies) |
| `Outreach_Tracker.xlsx` | The sheet: **Dashboard** (live COUNTIF formulas), **Contacts** (colour-coded by status), **Sources**, **Daily Runs**, **Do Not Contact** |
| `profile.json`, `settings.json` | Copies of the example configs with your details |
| `batch_/sent_/status_/leads_<date>.json` | Each day's audit trail |

**Tracker columns:** `id, email, contact_name, company, domain, opportunity, track, location, source_type, source_url,
source_note, date_found, mx_ok, published_on_source, verify_status, verify_note, priority, status, template, subject,
date_sent, gmail_message_id, gmail_thread_id, bounce_reason, reply_date, reply_snippet, followup_count,
next_action_date, notes`

---

## Setup (about 10 minutes)
1. **Python 3.9+** (`pip install openpyxl` for the sheet).
2. Clone: `git clone https://github.com/RaghavSobti37/cold-email-outreach && cd cold-email-outreach`
3. Make your data folder and configs:
   ```bash
   export OUTREACH_DATA=~/Documents/cold-email-outreach-data      # Windows: set OUTREACH_DATA=...
   python scripts/outreach.py init
   cp config/profile.example.json  "$OUTREACH_DATA/profile.json"   # edit: name, links, resume URLs
   cp config/settings.example.json "$OUTREACH_DATA/settings.json"  # edit: target, mix, pause
   ```
4. Edit the templates in `templates/` (keep them under ~110 words, one ask, links not attachments).
5. Import everyone you've already emailed so they're never contacted again. Export your Gmail sent recipients into
   `[{"email","date","subject","thread_id","bounced","replied"}]` and run
   `python scripts/outreach.py import-history history.json`.
6. Automate it (optional): in the Claude app, create a scheduled task for **07:30 daily** whose prompt says
   *"Follow prompts/daily_run.md in github.com/RaghavSobti37/cold-email-outreach"*. Connect Gmail and link your
   computer so it can read and write the local data folder.

## Manual use (the same steps the daily task runs)
```bash
python scripts/outreach.py add-leads leads.json     # dedupes vs tracker + do-not-contact + one per company
python scripts/outreach.py verify                   # syntax, MX, role address, published-on-source
python scripts/outreach.py pick --mix video_india=40,creative_tech=40,tech_remote=45,editing_remote=25
#   → batch_<date>.json (rendered subject + body per contact). Send each with Gmail, save ids to sent.json
python scripts/outreach.py mark-sent sent.json
python scripts/outreach.py open-threads             # list threads to check for replies / bounces
python scripts/outreach.py mark-status status.json  # bounced / replied / interested / rejected / do_not_contact
python scripts/outreach.py followups                # due follow-ups → followups_<date>.json
python scripts/outreach.py mark-followup fu.json
python scripts/outreach.py expire                   # follow-up + 7 days, no reply → no_reply
python scripts/outreach.py log-run --picked 54 --sent 54 --bounced 1 --notes "..."
python scripts/outreach.py build-xlsx && python scripts/outreach.py stats
```

### Lead file format (`leads.json`)
```json
[{"email":"jobs@studio.com","contact_name":"","company":"Studio","track":"creative_tech",
  "opportunity":"creative developer roles","location":"Paris","source_type":"company_careers_page",
  "source_url":"https://studio.com/careers","source_note":"jobs@ listed for applications",
  "published_on_source":"yes","priority":"3","notes":"HOOK: Loved your X project, ..."}]
```
Tracks: `video_india`, `creative_tech`, `tech_remote`, `editing_remote`, `adventure_video`.

---

## Guardrails (read before scaling up)
- **Gmail limit:** a regular Gmail account can send to about 500 recipients a day across *everything* it sends.
  Keep this system at 150 attempts or fewer, and don't run other bulk senders from the same inbox.
- **Bounces:** SMTP mailbox checks (e.g. [Reacher](https://github.com/reacherhq/check-if-email-exists)) need port 25,
  which is usually blocked. So the rule is published addresses only, plus the bounce sweep. The run stops itself if
  bounces pass 5%.
- **Relevance over volume:** 50 relevant emails beat 400 generic ones (see `docs/best-practices.md`). If there aren't
  enough good leads on a given day, the task sends fewer.
- **Opt-outs:** anyone who asks not to be contacted goes to `suppression.csv` for good.
- **Replies are human work:** the task flags `interested` replies at the top of its daily summary and never answers
  them itself.

## Day 1 (27 Sep 2026)
- Imported 412 people already emailed from the inbox (Sept 21–27) as do-not-contact, including 52 old bounces.
- Researched 54 new leads (Hacker News hiring threads, company sites, DesignRush, awesome-creative-technology),
  all published addresses, all passed MX.
- Run 1: sent 54, **1 bounced** (Pocket Aces `freelancers@`: published but dead, now suppressed).
- Run 2: 53 more from older HN hiring threads, India Cine Hub (Govt of India line-producer list) and city agency
  directories. **3 bounced.**
- **Day total: 107 sent, 103 delivered (3.7% bounce).** Daily goal is now 200 (see `config/settings.example.json`).

## Day 2 (28 Sep 2026): follow the replies
- Replies came from creative-dev studios (14islands, human) and adventure film (Higher Earth, interested), so round 3
  targeted those niches plus Indian travel/documentary houses.
- **188 sent, 3 bounced (1.6%), 185 delivered.** Tracker: 287 active sends, 59 bounced overall.
- The whole loop is packaged as a Claude skill: `skills/cold-outreach/SKILL.md` (run it as `/cold-outreach 200`).

## License
MIT. Use it, fork it, adapt the templates to your own work.
