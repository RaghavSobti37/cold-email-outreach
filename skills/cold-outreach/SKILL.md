---
name: cold-outreach
description: Run Raghav's (BluePolaroid) cold-email job/freelance outreach end to end. Reads replies, targets the niches that respond, finds fresh published-address leads, dedupes against Gmail, sends N emails and updates the local tracker. Use as "/cold-outreach 200".
---

# Cold outreach run: `/cold-outreach <N>`

`<N>` is the number of emails to **send** in this run (default 100, hard cap 220 because of Gmail's ~500/day limit
across everything the inbox sends). Send fewer rather than pad with weak leads. Report the real count.

- Mailbox: raghavsobti37@gmail.com, through the Gmail connector (`mcp__Gmail__*`).
- Code: https://github.com/RaghavSobti37/cold-email-outreach. `prompts/daily_run.md` there is the detailed playbook,
  and this skill is its on-demand version.
- **Data is LOCAL ONLY**: on Raghav's PC in `C:\Users\ragha\Documents\cold-email-outreach-data\`. Never commit
  tracker/suppression/leads/batch files to GitHub.

Work straight through without asking questions. Set up a task list with these steps and tick them off.

## 1. Set up
1. Load tools in one ToolSearch call:
   `select:mcp__Gmail__search_threads,mcp__Gmail__send_message,mcp__Gmail__get_thread,SendUserMessage,TaskCreate,TaskUpdate`.
2. Code: if `/home/claude/cold-email-outreach` doesn't exist, run
   `git clone https://github.com/RaghavSobti37/cold-email-outreach /home/claude/cold-email-outreach`; otherwise `git pull`.
3. Data: load `mcp__remote-devices__device_stage_files` (and `device_commit_files`, `device_bash`) with ToolSearch.
   - Stage every file in `C:\Users\ragha\Documents\cold-email-outreach-data\` and copy them to `/home/claude/work/data`.
     Note each file's `mtimeMs`.
   - If the PC can't be reached but `/home/claude/work/data/tracker.csv` already exists in this session, use that.
   - If neither is available, rebuild a do-not-contact list from Gmail (`in:sent newer_than:180d`) and say so in the report.
4. `export OUTREACH_DATA=/home/claude/work/data` before every script call (`python3 scripts/outreach.py ...`).

## 2. Read the replies, then pick the niches
1. Bounces: search
   `(from:mailer-daemon OR from:postmaster OR subject:(undeliverable OR "delivery status notification" OR "failure notice")) newer_than:3d`.
   Pull the failed address from each notice; for a vague one (such as a Google Group notice), `get_thread` PLAIN_TEXT
   and read the `To:` line.
2. Replies: search `in:inbox newer_than:14d -from:mailer-daemon -category:promotions -category:social` and match the
   senders or thread ids against `outreach.py open-threads`. Classify each as `interested` (wants to talk, rates,
   availability, a project), `rejected`, `do_not_contact`, `auto_reply` (acknowledgement or ticket), or `replied`.
3. Write `status_<date>.json` (`[{"email","status","reason"}]`), then run `mark-status` and `expire`.
4. Niche analysis: list who replied like a human or was interested, by track, industry and region. Put about 70% of the
   research in those niches, and use the rest to keep testing others. As of 28 Sep 2026 the niches that answer are:
   - creative-dev / WebGL / immersive studios (14islands),
   - adventure / expedition / travel film (Higher Earth: Ecuador shoot).
   Indian ad agencies mostly decline.
5. Tell Raghav right away (SendUserMessage) about any `interested` reply. Never answer those on his behalf.

## 3. Find leads (the slow part, so run it in parallel)
Target about 1.25 × N verified leads (roughly 20% get dropped at dedupe or verify).
1. Write the exclusion list: every domain in tracker.csv plus suppression.csv (not free-mail domains) goes into
   `/home/claude/work/exclude_domains.txt`.
2. Start 3–5 `general-purpose` Agents in ONE message, one niche each (for example EU creative studios · Americas/APAC
   creative and immersive · adventure/travel crews and fixers worldwide · India travel/doc/line producers · remote HN
   tech). Give each agent:
   - the niche, a target count, and the exclusion file.
   - Rules: use only addresses published on the company's own site (or a government directory, or the poster's own
     hiring post). Never guess a pattern. Prefer jobs@/careers@/crew@ over hello@/info@. Skip privacy/legal/support/
     noreply/press addresses. One per company. Skip `[email protected]`-obfuscated addresses and `name[at]domain` forms
     unless the plain address is shown elsewhere.
   - Tooling: WebFetch only works without approval on URLs that came from WebSearch results, so search first
     (`"<company> contact"`, `site:<domain> contact`), then fetch that exact URL. Web search is capped at about 200 per
     session, shared across agents, so spread the queries.
   - Output: a JSON array in `/home/claude/work/leads_<date>_<niche>.json`, with fields `email, contact_name, company,
     track, opportunity, location, source_type, source_url, source_note, published_on_source:"yes", priority,
     notes:"HOOK: <one specific, true line about their work>"`.
     Tracks: `creative_tech`, `adventure_video`, `video_india`, `tech_remote`, `editing_remote`.
     Opportunity must read naturally after "Open to remote ... with X" or "work with X on ...".
     Company names: no brackets and no Ltd/Inc.
   - Each agent uses its own uniquely named scratch files (agents share the scratchpad).
3. HN "Who is hiring" (hn.algolia.com/api/v1/items/<id>) and India Cine Hub were covered in earlier runs; new monthly HN
   threads are worth a pass.

## 4. Add, verify and pick
```bash
for f in /home/claude/work/leads_<date>_*.json; do python3 scripts/outreach.py add-leads "$f"; done
python3 scripts/outreach.py verify          # syntax, MX (UDP DNS), role filter, published check
python3 scripts/outreach.py pick --mix creative_tech=..,adventure_video=..,video_india=..,tech_remote=..,editing_remote=..
```
- Size the mix to N and to the niche analysis. If fewer than N get picked, raise the per-track numbers for tracks that
  still have queued leads.
- Read every rendered subject and body in `batch_<date>.json`. Fix odd company names, broken grammar where
  `{{opportunity}}` is inserted, and doubled words. Edit the tracker's `opportunity` or `company` and re-pick rather than
  hand-editing hundreds of bodies.

## 5. Live duplicate check (never email anyone twice)
Split the batch recipients into chunks of 14 and run `mcp__Gmail__search_threads` with
`in:sent (to:a OR to:b ... )` and view `THREAD_VIEW_METADATA_ONLY`. Run up to 7 in parallel. Drop anyone who appears,
mark them `legacy_sent`, and re-pick if needed.

## 6. Send
- Split the batch into about 4 files, `send_partK.json`. Start 4 `general-purpose` Agents in ONE message. Each one:
  - loads `mcp__Gmail__send_message` and `mcp__Gmail__search_threads`;
  - sends each item exactly as written (plain text, no attachments, no markdown), up to 5 in parallel;
  - on an error, searches `in:sent to:<addr> newer_than:1d` before a single retry, so nothing is sent twice;
  - writes `sent_partK.json` (`[{id,to,ok,message_id,thread_id,date}]`) as it goes, using uniquely named helper scripts.
- Merge the parts into `data/sent_<date>.json`, then run `mark-sent`. Check that sent count == batch count and every
  recipient is unique.

## 7. Bounce sweep, top-up, log
1. Wait at least 3 minutes, then repeat the bounce search from step 2.1 (`newer_than:1d`) and `mark-status` the bounces.
   Also mark any auto-acknowledgements that came in.
2. If bounces are above 5% of this run, stop and report. If delivered < N and verified leads are still queued, send the
   remainder the same way (stay under the cap).
3. `log-run --picked X --sent X --bounced B --notes "<niches and sources>"`, then `build-xlsx`, then `stats`.

## 8. Save and publish
1. **Data to the PC:**
   - Zip `tracker.csv`, `suppression.csv`, `runs.csv`, `Outreach_Tracker.xlsx`, `profile.json`, `settings.json` and
     today's `leads_/batch_/sent_/status_` files into `/mnt/user-data/outputs/outreach_sync_<date>.zip`.
   - SendUserFile it with `display:"attach"` to get its file_uuid, then `device_commit_files` it to
     `C:\Users\ragha\Documents\cold-email-outreach-data\_sync\`.
   - With `device_bash` (a Linux shell where Documents is mounted under `/sessions/<id>/mnt/Documents`), unzip to a tmp
     folder and overwrite each file with `cat src > dest`. Deleting or replacing files isn't permitted, but overwriting
     in place is. Compare md5 hashes afterwards.
   - If the PC is offline, say so and keep the files here for next time.
2. **Code/docs to GitHub (no data):** commit template, script and doc changes plus a dated "Run N learnings" note in
   `docs/lead-sources.md`, then push. `git status` must show no data files (they're in `.gitignore`).

## 9. Report to Raghav (short)
- Flag first: interested replies (who, what they asked).
- Sent / bounced / delivered this run vs N, with the reason if short.
- Which niches got the emails and why (the reply analysis).
- New replies by type, and totals from `stats`.
- Anything blocked (PC offline, search limits).
