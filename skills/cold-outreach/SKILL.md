---
name: cold-outreach
description: Run Raghav's BluePolaroid cold-email outreach end to end across video, creative-tech and coding (freelance/remote dev) tracks, with link-rich HTML emails. Use as /cold-outreach 200 or /cold-outreach 100 coding.
---

# Cold outreach run: `/cold-outreach <N> [focus]`

- `<N>` = number of emails to **send** this run (default 100). Hard cap: 220 per run and ~450 per day across
  everything the inbox sends (Gmail limit is ~500 recipients/day). Check today's total first with
  `in:sent after:<today>` if another run already happened today. Send fewer rather than pad with weak leads.
- `[focus]` (optional) = a track or niche to weight toward, e.g. `coding`, `video`, `creative`, `adventure`.
  Without it, weight by the reply analysis in step 2.

Fixed facts:
- Mailbox: raghavsobti37@gmail.com, via the Gmail connector (`mcp__Gmail__*`).
- Code: https://github.com/RaghavSobti37/cold-email-outreach (`scripts/outreach.py`, `templates/`, `prompts/daily_run.md`).
- **Data is LOCAL ONLY**: `C:\Users\ragha\Documents\cold-email-outreach-data\` on Raghav's PC
  (`tracker.csv`, `suppression.csv`, `runs.csv`, `Outreach_Tracker.xlsx`, `profile.json`, `settings.json`).
  Never commit data to GitHub.
- Raghav's links (all in `profile.json`; every email carries them):
  - Creative portfolio https://bluepolaroid.com/ · film projects https://bluepolaroid.com/projects
  - **Coding portfolio https://bluepolaroid.com/coding** · GitHub https://github.com/RaghavSobti37
  - LinkedIn https://www.linkedin.com/in/raghav-raj-sobti/ · Instagram https://www.instagram.com/bluepolaroid05/
  - Resumes: video `…/resumes/raghav-videographer-resume.pdf`, tech `…/resumes/raghav-creative-technologist-resume.pdf`
  - Live builds: The Shakti Collective https://theshakticollective.in/ · CoreKnot https://tsccoreknot.com/ ·
    Shrim Exports https://www.shrimexport.com/ · EKORS ERP repo https://github.com/RaghavSobti37/Ekors-ERP

Work straight through without asking questions. Make a task list from the steps below and tick them off.

## 1. Set up
1. One ToolSearch call:
   `select:mcp__Gmail__search_threads,mcp__Gmail__send_message,mcp__Gmail__get_thread,SendUserMessage,TaskCreate,TaskUpdate`.
2. Code: `git clone https://github.com/RaghavSobti37/cold-email-outreach /home/claude/cold-email-outreach` (or `git pull`).
3. Data: load `mcp__remote-devices__device_stage_files`, `device_commit_files`, `device_bash` with ToolSearch.
   - Stage every file in the data folder and copy to `/home/claude/work/data`.
   - PC offline but `/home/claude/work/data/tracker.csv` exists this session → use it. Neither → rebuild a
     do-not-contact list from Gmail (`in:sent newer_than:180d`) and say so in the report.
   - Make sure `profile.json` has `coding_url`, `tsc_url`, `coreknot_url`, `shrim_url`, `ekors_repo` and the
     `coding_freelance` track (copy missing keys from `config/profile.example.json`).
4. `export OUTREACH_DATA=/home/claude/work/data` before every `python3 scripts/outreach.py …` call.

## 2. Read replies → pick niches
1. Bounces: `(from:mailer-daemon OR from:postmaster OR subject:(undeliverable OR "delivery status notification" OR "failure notice")) newer_than:3d`.
   Vague notices (Google Groups): `get_thread` PLAIN_TEXT and read the `To:` line.
2. Replies: `in:inbox newer_than:14d -from:mailer-daemon -category:promotions -category:social`, match against
   `outreach.py open-threads`. Classify: `interested` (wants to talk / rates / availability / project), `replied`,
   `rejected`, `do_not_contact`, `auto_reply` (acknowledgement; stays "sent" so the follow-up still goes).
3. `status_<date>.json` = `[{"email","status","date","snippet"}]` (snippet = one line: who + what they said) →
   `mark-status`, then `expire`.
4. Niche analysis by track / industry / region → ~70% of research into what replies, ~30% testing. As of 28 Sep 2026:
   creative-dev / WebGL studios (14islands: human reply), adventure/expedition film (Higher Earth: interested, Ecuador),
   remote dev posts on HN (Prophet Town replied with a form). Indian ad agencies mostly decline.
5. Tell Raghav immediately (SendUserMessage) about any `interested` reply. Never answer those on his behalf.

## 3. Follow-ups (before new sends)
`followups` → `followups_<date>.json` (already rendered with `subject`, `body`, `html`). Send each in-thread:
`send_message` with `replyThreadId`=thread_id, `to`, `subject`, `body`, `htmlBody`=html. Then `mark-followup`.
They count toward N.

## 4. Find leads (parallel)
Target ≈ 1.25 × N verified leads.
1. Exclusion list: all domains in tracker.csv + suppression.csv (minus free-mail) → `/home/claude/work/exclude_domains.txt`.
2. Start 3–5 `general-purpose` Agents in ONE message, one niche each. Tracks and what to look for:
   | track | who | good sources |
   |---|---|---|
   | `creative_tech` | creative-dev / WebGL / immersive / motion studios worldwide | awesome-creative-technology, Awwwards studio pages, "best WebGL agencies" posts |
   | `coding_freelance` | web design / branding agencies, Webflow / Framer / Shopify / headless studios that use freelance devs (UK, EU, AU/NZ, US, CA, SG, UAE) | "Webflow agency <city>", Framer Experts, goodspeed.studio agency lists, "work with us" pages |
   | `tech_remote` | remote-first startups (media, video, creator, edtech, AI apps), Indian startups hiring React/Next.js, dev shops hiring contractors | careers pages; HN "Who is hiring" + "Freelancer? Seeking freelancer?" threads (Jun–Sep 2026 HN posts are already all emailed) |
   | `video_india` | Indian production / travel / documentary / line-production houses | India Cine Hub, company sites |
   | `adventure_video` | travel / adventure / expedition film cos + fixers worldwide | "film fixer <country>" |
   | `editing_remote` | YouTube / podcast / agency teams hiring remote editors | job posts, company sites |
   Tell every agent:
   - Only addresses published on the company's own site or the poster's own job post. Never guess. Prefer
     jobs@/careers@/work@/freelance@ over hello@/info@. Skip privacy/legal/support/noreply/press. One per company.
     Skip `[email protected]` and `name[at]domain` obfuscations unless the plain address appears elsewhere.
   - Skip "US-only / EU-only / citizens only / 7+ years" roles.
   - WebFetch works without approval only on URLs from WebSearch results → search first, then fetch that exact URL.
     Web search ≈200/session shared across agents.
   - **If WebFetch says "session limit"**, don't stop: read pages in the built-in browser pane instead
     (`mcp__remote-devices__Claude_Browser__*`, load them with ToolSearch query `mcp__remote-devices__Claude_Browser__`;
     `navigate` + `get_page_text`; each new site may need a one-time approval from Raghav via `request_access`),
     or pull HN threads with `javascript_tool` fetches to `https://hn.algolia.com/api/v1/items/<id>` from any open tab.
     Find thread ids with `https://hn.algolia.com/api/v1/search_by_date?tags=story&query=Who%20is%20hiring`
     (and `…query=Seeking%20freelancer`). If neither works, schedule a `send_later` to this session for when the
     limit resets and continue then.
   - Output `/home/claude/work/leads_<date>_<niche>.json`: `email, contact_name, company, track, opportunity, location,
     source_type, source_url, source_note, published_on_source:"yes", priority, notes:"HOOK: <one specific true line>"`.
     `opportunity` must read naturally in the template sentence (e.g. "remote front-end / full-stack work",
     "freelance front-end / Next.js builds", "creative-dev and film projects"). No brackets or Ltd/Inc in names.
   - Unique scratch-file names per agent (shared scratchpad).

## 5. Add, verify, pick, review
```bash
for f in /home/claude/work/leads_<date>_*.json; do python3 scripts/outreach.py add-leads "$f"; done
python3 scripts/outreach.py verify
python3 scripts/outreach.py pick --mix creative_tech=..,coding_freelance=..,tech_remote=..,video_india=..,adventure_video=..,editing_remote=..
```
- Size the mix to N and the niche analysis; if fewer than N get picked, raise the numbers for tracks that still have
  queued leads.
- `pick` writes `batch_<date>.json` with `subject`, `body` (plain text) and **`html`** for each email.
- Templates use `[label](url)` links. Plain text shows them as `label (url)` and the signature row as one
  `label: url` per line. HTML shows labelled links. Every template ends with a link row:
  - video tracks: Portfolio · Projects · LinkedIn · Instagram · Resume
  - creative_tech: Portfolio · Coding portfolio · GitHub · LinkedIn · Resume
  - tech_remote / coding_freelance: Coding portfolio · GitHub · LinkedIn · Resume (+ Creative portfolio)
- Read a sample from every track (subject, body, html). Fix odd company names or `{{opportunity}}` grammar in the
  tracker and re-pick; never hand-edit hundreds of bodies.

## 6. Live duplicate check
Chunks of 14 recipients → `mcp__Gmail__search_threads` `in:sent (to:a OR to:b …)`, view `THREAD_VIEW_METADATA_ONLY`,
≤7 in parallel. Drop anyone found, mark `legacy_sent`, re-pick if needed.

## 7. Send (HTML + plain text)
- Split the batch into ~4 `send_partK.json` files; start 4 `general-purpose` Agents in ONE message. Each:
  - loads `mcp__Gmail__send_message` + `mcp__Gmail__search_threads`;
  - sends every item exactly as given: `to=[to]`, `subject`, `body` = item.body, **`htmlBody` = item.html**;
    no attachments, ≤5 in parallel;
  - on error: `in:sent to:<addr> newer_than:1d` before ONE retry (never send twice);
  - writes `sent_partK.json` `[{id,to,ok,message_id,thread_id,date}]` progressively, unique helper-script names.
- Merge into `data/sent_<date>.json` → `mark-sent`. Check count == batch count and all recipients unique.

## 8. Bounce sweep, log, sheet
1. Wait ≥3 min, repeat the bounce search, `mark-status` bounces and any new auto-replies (with snippets).
2. Bounces >5% of the run → stop and report. Delivered < N with verified leads still queued → send the rest (under cap).
3. `log-run --picked X --sent X --bounced B --notes "<niches, sources>"` → `build-xlsx` → `stats`.

## 9. Save to the PC + publish code
1. Zip `tracker.csv suppression.csv runs.csv Outreach_Tracker.xlsx profile.json settings.json` + today's
   `leads_/batch_/sent_/status_` files → `/mnt/user-data/outputs/outreach_sync_<date>.zip`; SendUserFile
   (`display:"attach"`) for its file_uuid; `device_commit_files` → `C:\Users\ragha\Documents\cold-email-outreach-data\_sync\`.
2. `device_bash` (Linux shell; Documents is under `/sessions/<id>/mnt/Documents`, find it with
   `find / -maxdepth 5 -type d -name cold-email-outreach-data`): unzip to a tmp dir, overwrite each file with
   `cat src > dest` (delete/replace isn't permitted; in-place overwrite is), then compare md5s.
3. Code/doc changes → commit + push (no data; `.gitignore` covers it). Add a dated "Run learnings" note to
   `docs/lead-sources.md`.

## 10. Report (short)
- Interested replies first (who, what they asked).
- Sent / bounced / delivered vs N (and why if short), split by track.
- Niches targeted and why.
- The sheet path: `C:\Users\ragha\Documents\cold-email-outreach-data\Outreach_Tracker.xlsx`.
- Anything blocked (PC offline, fetch/search limits).
