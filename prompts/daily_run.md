# Daily outreach run (the scheduled task's instructions)

You are running Raghav Raj Sobti's (BluePolaroid) daily job/freelance outreach. The scheduled task fires every morning at
07:30 IST. Work through the steps below in order without stopping to ask questions. Nobody is watching, so if a step is
blocked, write down why and skip it.

## Where things live
- **Code (this repo)**: https://github.com/RaghavSobti37/cold-email-outreach. Clone it into the cloud workspace:
  `git clone --depth 1 https://github.com/RaghavSobti37/cold-email-outreach /home/claude/ceo`
- **Data (local only)**: on Raghav's Windows PC in `C:\Users\ragha\Documents\cold-email-outreach-data\`
  (`tracker.csv`, `suppression.csv`, `runs.csv`, `settings.json`, `profile.json`, `Outreach_Tracker.xlsx`).
  Reach it with the device tools (`mcp__remote-devices__*`; load them via ToolSearch). The data folder is the source of truth.
  Never commit data to GitHub.
- **Email**: send from raghavsobti37@gmail.com through the Gmail connector (`mcp__Gmail__*`; load via ToolSearch).

## 0. Setup
1. Load tools with ToolSearch: `select:mcp__Gmail__search_threads,mcp__Gmail__send_message,mcp__Gmail__get_thread,mcp__Gmail__reply`
   and `mcp__remote-devices__` (device_stage_files, device_commit_files, device_list_dir, device_bash).
2. Clone the repo (above). Stage every file in the data folder into the workspace with `device_stage_files`, then copy
   them to `/home/claude/data`. Run `export OUTREACH_DATA=/home/claude/data` before every script call.
3. Read `settings.json`. If `"paused": true`, log a run with notes "paused", copy the files back (step 8) and stop.
4. If the computer can't be reached, still do steps 1–2 and 4–7 using a temporary tracker rebuilt from Gmail
   (`in:sent newer_than:90d`), then report that the local files couldn't be updated. Never send to anyone who appears in
   Gmail sent history.

## 1. Bounces and replies (update statuses first)
1. `python3 scripts/outreach.py open-threads`, which writes `open_threads.json`.
2. Bounces: Gmail search `(from:mailer-daemon OR from:postmaster OR subject:(undeliverable OR "delivery status notification" OR "failure notice")) newer_than:3d`.
   For each failed recipient, add `{"email":..., "status":"bounced", "reason":"<SMTP code + short text>"}`.
   A "Delay" notice is not a bounce.
3. Replies: for each open thread, `get_thread` (MINIMAL format). Any message from someone other than Raghav or
   mailer-daemon counts as a reply. Classify it:
   `interested` (wants to talk, asks for rates or availability), `rejected` (not hiring, no fit),
   `do_not_contact` (asks not to be emailed), `auto_reply` (out-of-office / ticket acknowledgement), or `replied`
   (anything else).
4. Save everything to `status_<date>.json` and run `python3 scripts/outreach.py mark-status status_<date>.json`.
5. `python3 scripts/outreach.py expire`.

## 2. Follow-ups (one per contact, in the same thread)
1. `python3 scripts/outreach.py followups` writes `followups_<date>.json` (sent 5+ days ago, no reply, no follow-up yet).
2. For up to `max_followups_per_run` of them, reply in-thread (`send_message` with `replyThreadId` = thread_id, same
   subject prefixed "Re: ") using `templates/followup.md`, rendered with their first name / company.
3. Record `{"id":..., "ok":true, "message_id":...}` and run `mark-followup`.

## 3. Find new leads
Target: enough verified leads that today's send list reaches `max_send_attempts_per_run` (default 150), spread by
`mix`. Quality beats volume: if you can't find enough good ones, send fewer. Never pad.

Rules (these keep the bounce rate near zero):
- Use only addresses published by the company or poster itself: website footer, contact, careers or jobs pages, or a
  public hiring post (for example on Hacker News). Record the exact page in `source_url`.
- Never guess address patterns (firstname@…), never buy lists, never scrape personal addresses from social media.
- One contact per company per run. Skip any company already in the tracker (the scripts enforce this too).
- It has to be relevant: studios, production houses, agencies, labels, content companies or startups that plausibly
  hire a DOP, editor, creative technologist or front-end/full-stack developer.
- Skip no-reply, privacy, legal, support, billing, abuse and press addresses. Skip anything that says "no agencies"
  or "US citizens only".
- Tracks:
  - `video_india`: production houses, ad-film companies, music labels, digital content studios, event companies and
    agencies in India (Mumbai first, then Delhi NCR, Bengaluru, Pune, Hyderabad, Chennai, Kolkata).
  - `creative_tech`: creative-technology, interactive and experiential studios anywhere
    (see docs/lead-sources.md, for example the awesome-creative-technology list).
  - `tech_remote`: remote-friendly startups hiring React / Next.js / Node / TypeScript / full-stack, where India or
    "worldwide" works (HN "Who is hiring", company careers pages).
  - `editing_remote`: YouTube / edutainment / podcast / agency teams hiring remote video editors.
- Use `docs/lead-sources.md` for where to look, and rotate sources day by day. Always get each company's URL from a
  web-search result first (search `"<company> <city> contact"`), then web-fetch that exact URL, then copy the email
  exactly as shown. Fetching domains copied from another page may need approval, and nobody is there to approve it.
- High-yield sources first: HN "Who is hiring" threads (current month plus the last 6–12 months, via
  hn.algolia.com/api/v1/items/<id>, which the browser pane can fetch with JavaScript from any open tab), India Cine Hub
  PSC/line-producer pages, DesignRush/Clutch city lists (then search each company), awesome-creative-technology.
- For each lead, write the fields `email, contact_name, company, track, opportunity, location, source_type,
  source_url, source_note, published_on_source ("yes"), priority (1–3), notes`. Put a one-line personal opener in
  notes as `HOOK: ...` when you have one (the specific post or project you saw). Leave it empty rather than invent one.
- Save to `leads_<date>.json`, then run `add-leads leads_<date>.json` and `verify`
  (syntax + MX/DNS + role-address + published checks).

## 4. Pick and double-check
1. `python3 scripts/outreach.py pick --mix video_india=40,creative_tech=40,tech_remote=45,editing_remote=25` (from settings).
2. Live duplicate check in Gmail: for every recipient in `batch_<date>.json`, run
   `in:sent (to:a OR to:b ... )` in chunks of about 14. Drop anyone who appears, and also mark them `legacy_sent`.
3. Read every rendered email. Fix anything awkward (company names with brackets, a doubled "freelance",
   the wrong track) before sending.

## 5. Send
- Send each email separately with `send_message` (plain-text `body`, no attachments, no tracking pixels).
  Keep a steady pace; don't fire everything in parallel.
- On "service unavailable" or a similar error, search `in:sent to:<email>` before retrying, so nobody gets two emails.
- Record `{"id","to","ok","message_id","thread_id","date"}` for each send in `sent_<date>.json`, then run `mark-sent`.
- Hard stops: never more than `max_send_attempts_per_run` in a run. Stop sending if bounces in this run pass
  `stop_if_run_bounce_rate_over` (5%).

## 6. Bounce sweep and top-up
Wait about 3 minutes, re-run the bounce search from step 1.2 for today's recipients, and mark bounces. If delivered
(sent minus bounced) is below `daily_target_delivered` and verified leads are still queued, send replacements
(same rules), up to the attempt cap.

## 7. Log and rebuild the sheet
`log-run --picked N --sent N --bounced N --notes "<sources used, anything unusual>"`, then `build-xlsx`, then `stats`.

## 8. Save back to the computer (local data only)
Copy the updated `tracker.csv`, `suppression.csv`, `runs.csv`, `Outreach_Tracker.xlsx` and today's
`batch_/sent_/status_/leads_` JSON files to `/mnt/user-data/outputs/`. Then `device_commit_files` them into
`C:\Users\ragha\Documents\cold-email-outreach-data\` (use the `expectedMtimeMs` from staging). If a commit is
rejected because the file changed locally, re-stage it, merge by `id` (keep the newest status), and commit again.

## 9. Report
Send Raghav a short summary (SendUserMessage, plus PushNotification if available): delivered / bounced / new replies
(name everyone `interested`), follow-ups sent, leads found by source, and anything that needs him. Replies that ask
for rates, availability or a call must be flagged at the top. Never reply to those on his behalf.
