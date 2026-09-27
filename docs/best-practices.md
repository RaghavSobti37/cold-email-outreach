# Cold email best practices this system follows

Research summary (Sep 2026) and how each point shows up in the templates and scripts.

## What the data says
| Finding | Source | How it's applied |
|---|---|---|
| Emails under about 80–100 words with one clear ask reply best | [Woodpecker, 20M emails](https://woodpecker.co/blog/cold-email-statistics/), [Snov.io, 10M emails](https://snov.io/blog/cold-email-statistics/) | Templates are 75–107 words, with one question at the end ("Worth a quick chat?"). |
| Deeper personalization roughly doubles replies (about 17% vs 7–9%) | Woodpecker | A `HOOK:` line per lead: the specific post, page or project you saw. |
| Smaller, targeted lists beat blasts (5.8% replies under 50 contacts vs 2.1% at 1,000+) | Woodpecker | Leads are hand-qualified per track; no bought or bulk lists. |
| Follow-ups bring about 42% of all replies; 1–2 is best, 3+ hurts | Woodpecker, Snov.io | Exactly one follow-up, in the same thread, 5 days later, with an easy "not now" exit. |
| Attachments raise bounces (2.98% vs 1.86%); tracked links cut replies (0.21% vs 0.87%) | Snov.io | No attachments. Resumes are plain links on bluepolaroid.com. No open or click tracking. |
| Subject lines of 36–50 characters, personalized, do best | Woodpecker, Snov.io | "DOP + editor available for {company}", "{company} x a cinematographer who codes". |
| Best days Tue–Thu, 7–11 AM recipient time | Snov.io | Runs at 07:30 IST, which lands in the morning for India and in the first inbox check for the EU. |
| Gmail bulk-sender rules: keep spam complaints under 0.3%, keep bounces low, make opting out easy | [Google sender guidelines](https://support.google.com/a/answer/14229414?hl=en) | Published-address-only rule, MX check, bounce sweep plus auto-suppression, and the follow-up says "I won't follow up again". |

## Ideas taken from open-source outreach tools
- **[Jainprashuk/outreach](https://github.com/Jainprashuk/outreach)**: a clear per-contact status machine
  (pending, sent, bounced, replied, rejected); bounces spotted from mailer-daemon messages with the SMTP reason saved;
  replies matched by thread.
- **[1129Chengyuan/cold-email-agent](https://github.com/1129Chengyuan/cold-email-agent)**: `VERIFIED_ONLY` by default,
  a sheet as the dedupe log, and resume-grounded personalization.
- **[PaulleDemon/Email-automation](https://github.com/PaulleDemon/Email-automation)**: templating with variables and
  scheduled follow-ups.
- **[reacherhq/check-if-email-exists](https://github.com/reacherhq/check-if-email-exists)**: SMTP mailbox checks.
  Optional: it needs outbound port 25, which cloud sandboxes and most home ISPs block. That's why this system relies on
  published-only addresses plus a fast bounce sweep.

## Deliverability guardrails in code
- `verify`: syntax, typo-domain list, MX (falls back to an A record), null-MX, role-address filter,
  published-on-source requirement.
- Dedupe on four levels: tracker email, do-not-contact list, a 60-day cool-down per company domain, and a live Gmail
  `in:sent to:` check right before sending.
- Per-run caps: at most 150 attempts, and sending stops if the run's bounce rate goes over 5%.
- The Gmail consumer limit is about 500 recipients a day across **everything** sent from the account, other bots
  included.
